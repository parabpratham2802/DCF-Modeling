import yfinance as yf

ticker_symbol = input("Enter ticker symbol: ")
ticker = yf.Ticker(ticker_symbol)
info = ticker.info

company_name = info.get("longName")
beta = info.get("beta")
Equity = info.get("marketCap")
debt = info.get("totalDebt")
cash = info.get("totalCash")

print(f"Company: {company_name}")
print(f"Beta: {beta}")
print(f"Market Cap (Equity): {Equity}")
print(f"Total Debt: {debt}")
print(f"Total Cash: {cash}")
cashflow = ticker.cashflow
print(cashflow)

free_cash_flow = cashflow.loc["Free Cash Flow"].iloc[0]
print(f"Free Cash Flow: {free_cash_flow}")

# --- Manual assumptions ---
growth_rate = float(input("Growth Rate (%): ")) / 100
risk_free_rate = float(input("Risk Free Rate (%): ")) / 100
market_return = float(input("Market Retuen (%): ")) /100
tax_rate = float(input("Tax Rate (%): ")) / 100
cost_of_debt_rate = float(input("Cost of Debt (%): "))/100

cost_of_equity = risk_free_rate + (market_return-risk_free_rate) * beta
After_cost_of_debt = cost_of_debt_rate * ( 1 - tax_rate)
total_capital = Equity + debt


wacc = (
    ( Equity / (total_capital)) * cost_of_equity
    + (debt / (total_capital)) * After_cost_of_debt
)

print(f"{company_name} has a wacc of {wacc * 100:.2f}%")
if growth_rate > wacc :
    print("Error: Growth rate must be less than WACC")
    exit()

years = int(input("How many years do you want to forecast? "))

cash_flows = []
discounted_cash_flows = []

for i in range(years):
    fcf = free_cash_flow * (1 + growth_rate) ** (i + 1)
    discounted_cf = fcf / (1 + wacc) ** (i + 1)
    cash_flows.append(fcf)
    discounted_cash_flows.append(discounted_cf)


terminal_value = cash_flows[-1] * (1 + growth_rate) / (wacc - growth_rate)
discounted_terminal_value = terminal_value / (1 + wacc) ** years

enterprise_value = sum(discounted_cash_flows) + discounted_terminal_value

print(f"Enterprise Value = {enterprise_value:,.2f}")

equity_value = enterprise_value - debt + cash

print(f"Equity Value = {equity_value:,.2f}")

shares_outstanding = info.get("sharesOutstanding")
price_per_share = equity_value / shares_outstanding

print(f"Implied Share Price = {price_per_share:,.2f}")
