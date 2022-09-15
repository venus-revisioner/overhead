from pprint import pprint
import time

from overhead.cryptooh import BinanceStream
from overhead.jsonoh import JSON


def save_real_time_prices_to_json(price_file_json, COINS):
	simple_stream = BinanceStream(COINS, verbose=False)
	simple_stream.start()
	price_dict = {0: {}}
	json = JSON()

	try:
		json.load_file(price_file_json)
	except Exception:
		json.json_dict = price_dict

	while simple_stream.is_alive():
		time.sleep(1)
		timestamp = int(time.time())
		print("-"*30)
		print(time.ctime(timestamp))
		print("TIMESTAMP:", timestamp)
		json.json_dict[timestamp] = simple_stream.real_time_prices
		pprint(json.json_dict[timestamp])
		json.save_file(price_file_json, json.json_dict, "+w")


def save_candles_to_json(price_file_json, COINS, CANDLES):
	simple_stream = BinanceStream(COINS, CANDLES, verbose=False, simple=False)
	simple_stream.start()
	price_dict = {}
	json = JSON()

	json.load_file(price_file_json)

	if json.json_dict is None:
		price_dict = {}

	while simple_stream.is_alive():
		time.sleep(20)
		timestamp = int(time.time())
		print("-"*30)
		print(time.ctime(timestamp))
		print("TIMESTAMP:", timestamp)
		print("SAVING", COINS, ":", len(CANDLES), "candles")
		pprint(simple_stream.coin_dict)
		price_dict[int(timestamp)] = simple_stream.coin_dict
		json.save_file(price_file_json, price_dict, "w+")


def stream_real_time_prices(COINS):
	simple_stream = BinanceStream(COINS, verbose=True, simple=True)
	simple_stream.POLL_TIME = 0.5
	simple_stream.start()
