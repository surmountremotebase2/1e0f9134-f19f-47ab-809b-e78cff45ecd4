from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Example tickers, replace with Spanish companies' tickers if known
        self.tickers = ["BBVA", "SAN"]  # Assuming BBVA (Banco Bilbao Vizcaya Argentaria) and SAN (Banco Santander) as examples
        
        # In a real scenario, ensure the tickers belong to the Spanish companies you're interested in
        self.data_list = []  # Data required. Add data sources here if needed, such as InstitutionalOwnership("BBVA")

    @property
    def interval(self):
        return "1day"  # Define the time interval for the dataset

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        
        # Simple logic: Allocate based on EMA crossovers as an example. Adjust the logic to fit criteria for Spanish stocks
        for ticker in self.tickers:
            close_prices = [x[ticker]["close"] for x in data["ohlcv"] if ticker in x]  # Fetch closing prices
            if len(close_prices) > 50:  # Ensure there's enough data to calculate
                short_ema = EMA(ticker, data["ohlcv"], length=10)[-1]  # Short-term EMA
                long_ema = EMA(ticker, data["ohlcv"], length=50)[-1]  # Long-term EMA
                
                if short_ema > long_ema:
                    log(f"Going long on {ticker}, short EMA is above long EMA")
                    allocation_dict[tollower] = 1 / len(self.tickers)  # Simple equal-weighted allocation
                else:
                    log(f"No position on {ticker}, short EMA is below long EMA")
                    allocation_dict[ticker] = 0  # Not investing
            else:
                allocation_dict[ticker] = 0  # Not enough data to make a decision
                
        return TargetAllocation(allocation_dict)