# coding=utf-8
from dataclasses import dataclass
from pprint import pprint
import sys
import threading
import time

import websocket

from overhead.jsonoh import JSONhelper
from overhead.cryptooh import BinanceStream, BinanceStreamThread, BinanceFunctions, candle_data_parsing
from overhead.cryptooh import CoinsCandles as COCA

jsono = JSONhelper()


def save_real_time_prices_to_json(price_file_json, COINS):
	simple_stream = BinanceStream(COINS, verbose=False)
	simple_stream.start()
	price_dict = {0: {}}

	try:
		json.load_file(price_file_json)
	except Exception:
		jsono.json_dict = price_dict

	while simple_stream.is_alive():
		time.sleep(1)
		timestamp = int(time.time())
		print("-"*30)
		print(time.ctime(timestamp))
		print("TIMESTAMP:", timestamp)
		json.json_dict[timestamp] = simple_stream.real_time_prices
		pprint(json.json_dict[timestamp])
		json.save_file(price_file_json, jsono.json_dict, "+w")


def save_candles_to_json(price_file_json, COINS, CANDLES):
	simple_stream = BinanceStream(COINS, CANDLES, verbose=False, simple=False)
	simple_stream.start()
	json = JSONhelper()

	json.load_file(price_file_json)

	price_dict = {}
	while simple_stream.is_alive():
		time.sleep(20)
		timestamp = int(time.time())
		print("-"*30)
		print(time.ctime(timestamp))
		print("TIMESTAMP:", timestamp)
		print("SAVING", COINS, ":", len(CANDLES), "candles")
		pprint(simple_stream.coin_dict)
		price_dict[timestamp] = simple_stream.coin_dict
		jsono.save_file(price_file_json, price_dict, "w+")


def stream_real_time_prices(COINS):
	simple_stream = BinanceStream(COINS, verbose=True, simple=False)
	simple_stream.POLL_TIME = 1.
	simple_stream.start()
	

@dataclass
class MiniLoop:
	stream_thread: BinanceStreamThread
	coin_dict: dict
	poll_time: (int, float) = 1
	parsed_dict: dict = None
	verbose: bool = False
	
	def __post_init__(self):
		print('\nStarting streaming coin candles...')
		while True:
			try:
				stream = self.stream_thread.get_stream_json_decoded()
				
				if stream and 'stream' in stream.keys():
					# populate coin dict
					co = f'{stream["data"]["s"]}'.lower()
					ca = f'{stream["data"]["k"]["i"]}'
					self.coin_dict[co][ca] = candle_data_parsing(stream['data']['k'])
					self.parsed_dict = self.coin_dict[co][ca]
					if self.verbose:
						print(self.coin_dict[co][ca])
			
			except KeyboardInterrupt as e:
				print(e)
				self.stream_thread.quit()
				break
		
			time.sleep(self.poll_time)
	
	@property
	def real_time_candles_raw(self):
		return self.coin_dict

	@property
	def real_time_candles_parse(self):
		return self.parsed_dict
	
	@property
	def get_raw_stream(self):
		return self.stream_thread


def small_standalone_stream(cryptos="BTCUSDT"):
	"""
	Use:
	
	small_standalone_stream("BTCUSDT")
	
	:param cryptos:
	:type cryptos:
	:property: dict of candles
	:property: dict of candles parsed data
	:property: thread of the websocket running in
	:rtype:
	"""
	import json
	BinanceFunctions()
	# coins, candles = COCA.COINS_TOP + COCA.COINS_DOGS + COCA.COINS_POS, COCA.CANDLES_9
	coins, candles = f'{cryptos}', COCA.CANDLES_9
	
	coins = [f'{i}'.lower() for i in coins]
	
	candle_group_dict = {}
	coin_dict = {a: {b: {} for b in candles} for a in coins}
	coin_str_dict = {a: {b: "" for b in candles} for a in coins}
	
	columns = [[]] * 4
	columns[0] = ["high", "low", "volume", "volatility"]
	columns[2] = ["open", "close", "", "norm"]
	
	# address = f'wss://dex.binance.org/api'
	address = 'wss://stream.binance.com:9443'
	
	coin_get_str = "stream?streams="
	for coin in coins:
		for candle in candles:
			coin_get_str += f'{coin}@kline_{candle}/'
	
	coin_get_str = coin_get_str[:-1]
	
	socket = websocket.WebSocket()
	address_sub = f'{address}/{coin_get_str}'
	socket.connect(address_sub)
	socket.send(json.dumps({"method": "SUBSCRIBE", "params": coins, "id": 1}))
	poll_time = 1
	stream_thread = BinanceStreamThread(socket, poll_time=poll_time)
	stream_thread.start()
	
	MiniLoop(stream_thread, coin_dict, poll_time)
	
	socket.send(json.dumps({"method": "UNSUBSCRIBE", "params": coins, "id": 312}))
	stream_thread.quit()
	sys.exit(0)
