import itertools
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
import sys
import threading
import time

# Importing all the modules in the __all__ list.

import os

# import importlib
# importlib.importmodule(("apps", "coin_config", "grid_calculator"))
import websocket

from ..jsonoh import JSONhelper
from ..decooh import terminal_rolling
from ..toolboxoh import KeyHandler
from ..decooh import terminal_rolling



@dataclass
class CoinsCandles:
	COINS_BTC: tuple = ("BTCBUSD",)
	COINS_TOP: tuple = ("BTCBUSD", "ETHBUSD", "BNBBUSD")
	COINS_DOGS: tuple = ("DOGEBUSD", "SHIBBUSD")
	COINS_POS: tuple = ("ALGOBUSD", "IOTABUSD")
	COINS_NEW: tuple = ("GMTBUSD", "APEBUSD", "RAREBUSD")
	CANDLES_4: tuple = ("3m", "15m", "1h", "4h")
	CANDLES_5: tuple = ("5m", "30m", "1h", "4h", "1d")
	CANDLES_9: tuple = ("5m", "15m", "1h", "4h", "12h", "1d", "3d", "1w", "1M")
	CANDLES_10: tuple = ("3m", "5m", "15m", "1h", "4h", "12h", "1d", "3d", "1w", "1M")
	CANDLES_ALL: tuple = ("1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M")
	CANDLES_7_TODAY: tuple = ("5m", "15m", "1h", "4h", "12h", "1d", "3d")

@dataclass
class ConfigParameters:
	_BINANCE_PATH: Path = Path("D:/PycharmProjects/Binance")
	BINANCE_API_KEY: str = "rWpEV2x1Kj2AwzPVgXQBMyWzsTCPIjnMoXMeCvfd9f1iZFWSOSRRHHI6CVQbGk4T"
	BINANCE_API_SECRET: str = "i9K42DnBQVeCOwcwF2P93QBi2ziEnMLu0TeVaUb4VRgl3soFG4cKj0Cr6LkHXrHP"
	PORTFOLIO_BINANCE: Path = Path(_BINANCE_PATH).joinpath("portfolio_binance.json")
	PORTFOLIO_CRYPTO: str = Path(_BINANCE_PATH).joinpath("portfolio_crypto.json")
	BINANCE_HISTORY_START_TIMESTAMP: int = 1621433867000

	@property
	def get_binance(self):
		json = JSONhelper()
		print(Path("."))
		return json.load_file(self.PORTFOLIO_BINANCE)

	@property
	def get_crypto(self):

		json = JSON()
		return json.load_file(self.PORTFOLIO_CRYPTO)

	def get_coins(self, portfolio, wallet):
		return [item['asset']+"BUSD" for item in portfolio['wallet'][wallet]['assets']]

	def get_net_assets(self, portfolio, wallet):
		return [float(item['netAsset']) for item in portfolio['wallet'][wallet]['assets']]

	def get_coins_assets(self, portfolio, wallet):
		return {item['asset'] + "BUSD": float(item['netAsset']) for item in portfolio['wallet'][wallet]['assets']}

class BinanceStreamThread(threading.Thread):
	def __init__(self, socket, poll_time=1.):
		threading.Thread.__init__(self)
		self.socket = socket
		self.poll_time = poll_time
		self.result = None
		self.stream_decoder = json.decoder.JSONDecoder()
		self.quit_flag = False
		self.stream_data = None

	def run(self):
		while True:
			try:
				self.result = self.socket.recv()
				time.sleep(self.poll_time)

				if self.quit_flag:
					break

				self.result = self.socket.recv()

			except Exception as e:
				time.sleep(5)
				print(e)
				self.quit()
				break

	def get_stream_json_decoded(self):
		if self.result is not None:
			self.stream_data = self.stream_decoder.decode(self.result)
			return self.stream_data

	def quit(self):
		self.quit_flag = True


class BinanceStream(threading.Thread):
	def __init__(self, coins, candles=("1m",), verbose=True, simple=False):

		threading.Thread.__init__(self)
		self.VERBOSE = verbose
		self.SIMPLE = simple
		self.POLL_TIME = 1 / 6
		self.WIDTH = 30

		self.key_handler = KeyHandler(verbose=1)

		self.socket = websocket.WebSocket()
		self.stream_thread = BinanceStreamThread(self.socket, poll_time=self.POLL_TIME)

		self.coins = coins
		self.candles = candles

		self.init_coins()

	def run(self):
		print("INITIALIZING STREAM...")
		if self.VERBOSE or self.SIMPLE:
			self.terminal = Terminal()
			self.terminal.clear()
			terminal_dim = self.WIDTH, len(self.coins) + 4
			self.terminal.resize(*terminal_dim)
		coin_get_str = "stream?streams="
		for coin, candle in itertools.product(self.coins, self.candles):
			coin_get_str += f'{coin}@kline_{candle}/'
		coin_get_str = coin_get_str[:-1]
		address = 'wss://stream.binance.com:9443'
		address_sub = f'{address}/{coin_get_str}'
		self.socket.connect(address_sub)
		self.socket.send(json.dumps({"method": "SUBSCRIBE", "params": self.coins, "id": 1}))

		self.key_handler.start()
		self.stream_thread.start()
		self.stream_loop()
		self.socket.send(json.dumps({"method": "UNSUBSCRIBE", "params": self.coins, "id": 312}))

		self.stream_thread.quit()
		if self.VERBOSE:
			self.terminal.resize(80, 20)
		print("\nEXIT COMPLETED\n")
		time.sleep(1)
		sys.exit(0)

	def init_coins(self):
		if isinstance(self.coins, str):
			self.coins = self.coins,
		if isinstance(self.candles, str):
			self.candles = self.candles,

		self.coins = [f'{i}'.lower() for i in self.coins]

		self.coin_dict = {a: {b: {'close': '0.'} for b in self.candles} for a in self.coins}
		self.real_time_prices = {a: '0.' for a in self.coins}

	def get_real_time_prices(self, coin=None, candle=None):
		if coin is None:
			coin = list(self.coin_dict.keys())[0]
		if candle is None:
			candle = self.candles[0]
		self.real_time_prices[coin] = self.coin_dict[coin][candle]["close"]
		return self.real_time_prices[coin]

	def print_real_time_prices(self, candle=None):
		if candle is None:
			candle = self.candles[0]
		self.terminal.clear()
		print(f'{"BINANCE STREAM":^{self.WIDTH}}')
		print("-" * (self.WIDTH))
		for k in self.coin_dict.keys():
			if len(self.coin_dict[k][candle]) > 0 and float(self.real_time_prices[k]) > 0.:
				data_str = f'{k.upper():12}{self.real_time_prices[k]}'
				print(data_str)
		print("-" * (self.WIDTH))

	@terminal_rolling
	def wrap_real_time_prices(self, price_dict, *args, **kwargs):
		for k, v in price_dict.items():
			if isinstance(v, (float, int)):
				v = (v, )
			price_str = "".join(f'{str(item).rstrip("0").rstrip("."):15}' for item in v)
			data_str = f'{k.upper():15}{price_str}'
			print(data_str)

	def stream_loop(self):
		listen_str = "LISTENING STREAM..."
		print(f'{listen_str}' + " " * (self.WIDTH - len(listen_str)))
		while True:
			try:
				stream = self.stream_thread.get_stream_json_decoded()
				if stream and 'stream' in stream.keys():
					co = f'{stream["data_tools"]["s"]}'.lower()
					ca = f'{stream["data_tools"]["k"]["i"]}'
					if self.SIMPLE and float(stream['data_tools']['k']['c']) != float(self.coin_dict[co][ca]['close']):
						self.get_real_time_prices(co)
						if self.VERBOSE:
							self.print_real_time_prices()
					self.coin_dict[co][ca] = candle_data_parsing(stream['data_tools']['k'])
				if self.key_handler.quit_flag:
					self.stream_thread.quit()
					break
				time.sleep(self.POLL_TIME)
			except Exception as e:
				time.sleep(5)
				print(e)
				self.stream_thread.quit()
				break


class BinanceFunctions:
	def __init__(self):
		from binance import Client
		#-----------------------------------------------------
		self._json = JSON()
		self.CONFIG = ConfigParameters()
		_API_KEY = self.CONFIG.BINANCE_API_KEY
		_API_SECRET = self.CONFIG.BINANCE_API_SECRET
		self._PORTFOLIO_CRYPTO = self.CONFIG.PORTFOLIO_CRYPTO
		self._PORTFOLIO_BINANCE = self.CONFIG.PORTFOLIO_BINANCE
		self._BINANCE_HISTORY_START_TIMESTAMP = self.CONFIG.BINANCE_HISTORY_START_TIMESTAMP
		#-----------------------------------------------------
		self.portfolio_crypto = self._json.load_file(self._PORTFOLIO_CRYPTO)
		self.portfolio_binance = self._json.load_file(self._PORTFOLIO_BINANCE)
		#-----------------------------------------------------
		self._client = Client(_API_KEY, _API_SECRET)

		self.ASSET_VALUES = {}

	def print_portfolio_binance(self):
		pprint(self.portfolio_binance)

	def print_portfolio_crypto(self):
		pprint(self.portfolio_crypto)

	def fiat_deposit_history(self, days=None, update=False, from_date=(2022,1,1), save=False):
		end = int(time.time() * 1000)
		fiat_deposits = {}

		if days is None:
			start = self._BINANCE_HISTORY_START_TIMESTAMP
			fiat_deposits = {"total_sum": 0.}
		else:
			start = int(time.time() - 60 * 60 * 24 * days * 1000)

		if update:
			last_update = self.portfolio_crypto['binance_deposits']['query_end']
			last_update = last_update.split(".")
			y, m, d = int(last_update[2]), int(last_update[1].strip()), int(last_update[0].strip())
			start = int(time.mktime((y, m, d, 0, 0, 0, 0, 0, 0)) * 1000)

		if from_date:
			y,m,d = from_date
			start = int(time.mktime((y, m, d, 0, 0, 0, 0, 0, 0)) * 1000)

		# print(f'Start date:\t{timestamp_convert(start)}')
		# print(f'End date:\t{timestamp_convert(end)}')
		# print()
		params = {"transactionType": 0, "beginTime": start, "endTime": end}
		query = self._client.get_fiat_deposit_withdraw_history(**params)
		data = query['data_tools']
		fiat_deposits['currency'] = data[0]["fiatCurrency"]
		fiat_deposits['total_deposits'] = len(data)
		fiat_deposits['query_start'] = timestamp_convert(start, get_time=0)
		fiat_deposits['query_end'] = timestamp_convert(end, get_time=0)
		for e, transaction in enumerate(data[::-1]):
			amt = float(transaction['amount'])
			deposit_time = timestamp_convert(transaction['createTime'],get_time=0)
			currency = transaction["fiatCurrency"]
			fiat_deposits[e] = {"date": deposit_time, "amount": amt, "currency": currency}
			fiat_deposits['total_sum'] += amt
		fiat_deposits['total_sum'] = round(fiat_deposits['total_sum'],3)
		pprint(fiat_deposits)
		self.portfolio_crypto['binance_deposits'] = fiat_deposits
		# pprint(self.portfolio_crypto)
		if save:
			self._json.save_file(self._PORTFOLIO_CRYPTO, self.portfolio_crypto, mode='+w')
		else:
			print(f'\nDATA NOT SAVED TO file: "{self._PORTFOLIO_CRYPTO}"')


	def account_update_json(self, wallet="SPOT"):
		my_balances = self.portfolio_binance
		asset_list = []
		if wallet not in my_balances['wallet'].keys():
			my_balances['wallet'][wallet] = {}
		if wallet == "SPOT":
			print(f'UPDATING {self._PORTFOLIO_BINANCE}: {wallet}')
			account_balance = self._client.get_account(timestamp=time.time())
			asset_list.extend({'asset': asset['asset'], 'free': asset['free']} for asset in account_balance['balances'] if float(asset['free']) != 0.0)

			my_balances['wallet'][wallet] = {'assets': asset_list}
		if wallet == "MARGIN":
			print(f'UPDATING {self._PORTFOLIO_BINANCE}: {wallet}')
			account_balance = self._client.get_margin_account(timestamp=time.time())
			for k, v in account_balance.items():
				if 'total' in k:
					my_balances['wallet'][wallet][k] = v
			asset_list.extend(asset for asset in account_balance['userAssets'] if float(asset['netAsset']) != 0.0)

			my_balances['wallet'][wallet]['assets'] = asset_list
		if wallet == "FUTURES":
			print(f'UPDATING {self._PORTFOLIO_BINANCE}: {wallet}')
			account_balance = self._client.futures_account(timestamp=time.time())
			for k, v in account_balance.items():
				if k in ('total', 'Balance'):
					my_balances['wallet'][wallet][k] = v
			asset_list.extend(asset for asset in account_balance['assets'] if float(asset['unrealizedProfit']) != 0.0)

			my_balances['wallet'][wallet]['assets'] = asset_list
		self.portfolio_binance = my_balances
		self._json.save_file(self._PORTFOLIO_BINANCE, my_balances, mode='+w')

	def make_assets_dict(self, wallet):
		return self.CONFIG.get_coins_assets(self.portfolio_binance, wallet)

	def multiply_assets(self, a, b):
		f = lambda x,y: x*y if y >= 0. and x >= 0. else x
		return {z: round(f(float(x), float(y)), 2) for x, y, z in zip(a.values(), b.values(), a.keys())}

	def sum_assets(self):
		return round(float(sum(i for i in self.ASSET_VALUES.values() if i > 0.0)), 2)

	def borrowed(self, a):
		# return sum([float(i['borrowed']) for i in self.portfolio_binance['wallet']['MARGIN']['assets']])
		return round(min(a.values()), 2)

	def equity(self, a):
		return round(self.ASSET_VALUES['MARGIN_EQUITY'] + self.ASSET_VALUES['BORROWED'], 2)

	def free_busd(self):
		assets = self.portfolio_binance['wallet']['MARGIN']['assets']
		free = [item['free'] for item in assets if item['asset'] == "BUSD"]
		return round(float(free[0]), 2)

	def interest(self, b):
		interest_bnb = sum(float(i['interest']) for i in self.portfolio_binance['wallet']['MARGIN']['assets'])

		return round(interest_bnb * float(b['bnbbusd']), 4)

	def risk_ratio(self):
		risk_ratio = self.ASSET_VALUES['MARGIN_EQUITY'] / ((self.ASSET_VALUES['BORROWED'] * -1. + self.ASSET_VALUES['INTEREST']))
		return round(risk_ratio, 3)

	def total_asset_values(self, a, b):
		self.ASSET_VALUES = self.multiply_assets(a, b)
		self.ASSET_VALUES['MARGIN_EQUITY'] = self.sum_assets()
		self.ASSET_VALUES['BORROWED'] = self.borrowed(a)
		self.ASSET_VALUES['TRUE_EQUITY'] = self.equity(a)
		self.ASSET_VALUES['FREE_BUSD'] = self.free_busd()
		self.ASSET_VALUES['INTEREST'] = self.interest(b)
		self.ASSET_VALUES['RISK_RATIO'] = self.risk_ratio()
		return self.ASSET_VALUES


from typing import Any


def coin_change(new, old):
	return (float(new) / float(old)) * 100 - 100


def volatility(high, low):
	v_sorted = [float(high), float(low) ]
	v_sorted.sort()
	return ((v_sorted[ 1 ] / v_sorted[ 0 ] - 1.) * 100.)


def candle_normalize(low, high, close):
	range = float(high) - float(low)
	return (float(close) - float(low)) / range if range > 0.0 else 0.0


def candle_normalize_invert(low, high, normalized):
	return (high - low) * normalized + low


def candle_data_parsing(data):
	data_dict: Any = {
			"vol":      data[ 'v' ],
			"high":     data[ 'h' ],
			"low":      data[ 'l' ],
			"open":     data[ 'o' ],
			"close":    data[ 'c' ],
			"symbol":   data[ 's' ],
			"status":   data[ 'x' ],
			"interval": data[ 'i' ],
			"start":    data[ 't' ],
			"end":      data[ 'T' ]}
	return data_dict
