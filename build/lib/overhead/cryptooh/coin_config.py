#
# @dataclass
# class CoinsCandles:
# 	COINS_BTC: tuple = ("BTCBUSD",)
# 	COINS_TOP: tuple = ("BTCBUSD", "ETHBUSD", "BNBBUSD")
# 	COINS_DOGS: tuple = ("DOGEBUSD", "SHIBBUSD")
# 	COINS_POS: tuple = ("ALGOBUSD", "IOTABUSD")
# 	COINS_NEW: tuple = ("GMTBUSD", "APEBUSD", "RAREBUSD")
# 	CANDLES_4: tuple = ("3m", "15m", "1h", "4h")
# 	CANDLES_5: tuple = ("5m", "30m", "1h", "4h", "1d")
# 	CANDLES_9: tuple = ("5m", "15m", "1h", "4h", "12h", "1d", "3d", "1w", "1M")
# 	CANDLES_10: tuple = ("3m", "5m", "15m", "1h", "4h", "12h", "1d", "3d", "1w", "1M")
# 	CANDLES_ALL: tuple = ("1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M")
#
# @dataclass
# class ConfigParameters:
# 	_BINANCE_PATH: Path = Path("D:/PycharmProjects/Binance")
# 	BINANCE_API_KEY: str = "rWpEV2x1Kj2AwzPVgXQBMyWzsTCPIjnMoXMeCvfd9f1iZFWSOSRRHHI6CVQbGk4T"
# 	BINANCE_API_SECRET: str = "i9K42DnBQVeCOwcwF2P93QBi2ziEnMLu0TeVaUb4VRgl3soFG4cKj0Cr6LkHXrHP"
# 	PORTFOLIO_BINANCE: Path = Path(_BINANCE_PATH).joinpath("portfolio_binance.json")
# 	PORTFOLIO_CRYPTO: str = Path(_BINANCE_PATH).joinpath("portfolio_crypto.json")
# 	BINANCE_HISTORY_START_TIMESTAMP: int = 1621433867000
#
# 	@property
# 	def get_binance(self):
# 		json = JSON()
# 		print(Path("."))
# 		return json.load_file(self.PORTFOLIO_BINANCE)
#
# 	@property
# 	def get_crypto(self):
# 		json = JSON()
# 		return json.load_file(self.PORTFOLIO_CRYPTO)
#
# 	def get_coins(self, portfolio, wallet):
# 		return [item['asset']+"BUSD" for item in portfolio['wallet'][wallet]['assets']]
#
# 	def get_net_assets(self, portfolio, wallet):
# 		return [float(item['netAsset']) for item in portfolio['wallet'][wallet]['assets']]
#
# 	def get_coins_assets(self, portfolio, wallet):
# 		return {item['asset'] + "BUSD": float(item['netAsset']) for item in portfolio['wallet'][wallet]['assets']}
