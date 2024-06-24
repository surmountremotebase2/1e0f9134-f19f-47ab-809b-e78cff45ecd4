from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define a list of tickers within the oil industry. 
        # These can be adjusted based on market performance, sector analysis, etc.
        self.tickers = ["XOM", "CVX", "COP", "SLB", "PSX"]
        # Adding more data sources or technical indicators could 
        # provide a more nuanced strategy.
    
    @property
    def interval(self):
        # The data interval for analysis; this can be adjusted based on strategy needs.
        return "1day"  
    
    @property
    def assets(self):
        # The assets this strategy is concerned with.
        return self.tickers

    @property
    def data(self):
        # This strategy primarily uses RSI, but more data sources can be added for a comprehensive analysis.
        return [Asset(ticker) for ticker in self.tickers]

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            rsi_data = RSI(ticker, data["ohlcv"], length=14)  # Using a 14-day period for RSI calculation

            if rsi_data is None or len(rsi_data) == 0:
                continue  # Skip if no data available
            
            current_rsi = rsi_data[-1]
            
            # Allocation strategy based on RSI values. This simplistic approach can be refined with more nuances.
            if current_rsi < 30:
                # The security is considered oversold, indicating a potential buying opportunity. 
                # Allocating a higher percentage to these stocks.
                allocation_dict[ticker] = 1.0 / len(self.tickers)
            elif current_rsi > 70:
                # The security is considered overbought, indicating a potential selling point or to be avoided for purchase.
                # No allocation to these stocks.
                allocation_dict[ticker] = 0
            else:
                # For securities not in the overbought or oversold zone, allocate evenly.
                # This division can also be adjusted based on additional analysis or to weight certain stocks more heavily.
                allocation_dict[ticker] = 0.5 / len(self.tickers)
                
        if not allocation_dict:
            # In case all tickers are overbought, this could leave the dict empty,
            # hence it's prudent to have a fallback strategy.
            allocation_dict = {ticker: 1.0 / len(self.tickers) for ticker in self.tickers}
        
        return TargetAllocation(allocation_dict)