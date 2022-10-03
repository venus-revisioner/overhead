# coding=utf-8

import threading
import websocket
import json
import time
import numpy as np
import sys

from overhead.toolboxoh import KeyHandler, ColorizeText
from overhead.toolboxoh import timestamp_convert, human_readable_big_number
from overhead.terminaloh import Terminal
from overhead.cryptooh import BinanceFunctions
from overhead.cryptooh import CoinsCandles as COCA


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
        # print_boxed(self.__str__())
        # time.sleep(1)

        while True:
            self.result = self.socket.recv()
            time.sleep(self.poll_time)

            if self.quit_flag:
                break

        self.result = self.socket.recv()

    def get_stream_json_decoded(self):
        if self.result is not None:
            self.stream_data = self.stream_decoder.decode(self.result)
            return self.stream_data

    def quit(self):
        self.quit_flag = True


def coin_change(new, old):
    c = (float(new)/float(old))*100-100
    return c


def volatility(high, low):
    v_sorted = [float(high), float(low)]
    v_sorted.sort()
    return ((v_sorted[1] / v_sorted[0] - 1.) * 100.)


def candle_normalize(low, high, close):
    range = float(high) - float(low)
    if range > 0.:
        return (float(close)-float(low)) / range
    else:
        return 0.5


def longest_nested_list(x):
    b = lambda x: len(x)
    return max(list(map(b, x)))


# def shortest_nested_list(x):
#     b = lambda x: len(x)
#     return max(list(map(b, x)))


def print_info_text():
    s = 'Listening data stream...'
    print(s + " " * (terminal_dim[0]-len(s)))
    s = 'Type "q" and hit Enter to exit program.'
    print(s + " " * (terminal_dim[0]-len(s)))


def num_form(s):
    rounded = '{:.8f}'.format(round(float(s), 8))
    r_int = rounded.split('.')[0]
    r_decimal = rounded.split('.')[1]

    if 10. >= float(s) >= 0.01:
        rounded = '{:.4f}'.format(round(float(s), 4))
        if float(r_decimal) < 0.:
            rounded = r_int

    elif float(r_int) > 10.:
        rounded = '{:.2f}'.format(round(float(s), 2))
        if float(r_decimal) < 0.:
            rounded = r_int
    else:
        rounded = f'0.{r_decimal}'
    return rounded


def column_formatter(x):
    b = lambda y: f'{y:<11}'
    c = list(map(b, x))
    s = "".join(c)
    s = s.strip("\t")
    return s + "\n"


def create_candle_group():
    for c in candles:
        candle_group_dict[c] = {k: v[c].splitlines() for k, v in coin_str_dict.items()}


def create_parallel_view():
    candle_group_str = ""

    temp = [list(c.values()) for c in candle_group_dict.values()]

    for item in temp:
        for substring in list(zip(*item)):
            a = f'\t  '.join(substring)
            candle_group_str += f'{a}\n'

    print(candle_group_str)


def format_kline(data, width):
    vol = data['v']
    vol = human_readable_big_number(float(vol))
    vol = f'{vol:11}'
    # color.fore = 'cyan'
    # vol = color.colorize(vol)

    volatility_percent = volatility(data["h"], data["l"])
    normalized = candle_normalize(data['l'],data['h'],data['c'])

    status = data["x"]

    if volatility_percent < 0.5:
        color.fore = 'light black'
    elif 0.5 <= volatility_percent < 2.5:
        color.fore = 'green'
    elif 2.5 <= volatility_percent < 5.:
        color.fore = 'light yellow'
    elif 5. <= volatility_percent < 10.:
        color.fore = 'light blue'
    elif 10. <= volatility_percent < 20.:
        color.fore = 'light magenta'
    else:
        color.fore = 'red'

    volatility_str = f'{ volatility_percent:.3f} %'
    volatility_str = f'{volatility_str:11}'
    volatility_str = color.colorize(volatility_str)

    high_str = f'{num_form(data["h"]):11}'
    color.style = 'bright'
    color.fore = 'green'
    high_str = color.colorize(high_str)

    low_str = f'{num_form(data["l"]):11}'
    color.style = 'bright'
    color.fore = 'light red'
    low_str = color.colorize(low_str)

    columns[1] = [high_str, low_str, vol, volatility_str]

    change = float(coin_change(data['c'], data['o']))

    close = num_form(data['c'])

    if change >= 0.:
        change = f'+{change:.3f} %'
        color.style = 'bright'
        # color.back = 'blue'
        # color.fore = 'white'
        # color.fore = 'blue'
        # color.fore = 'green'
        color.fore = 'light blue'
        change = color.colorize(change)
        color.style = 'bright'
        # color.style = 'dim'
        # color.back = 'blue'
        # color.back = 'magenta'
        # color.back = 'light black'
        # color.fore = 'green'
        color.fore = 'light blue'
            # color.fore = 'light blue'
            # columns[2][1] = f'{color.colorize(columns[2][1])}'
    else:
        change = f'{change:.3f} %'
        # color.style = 'dim'
        # color.style = 'bright'
        # color.back = 'red'
        # color.fore = 'red'
        # color.fore = 'white'
        color.fore = 'light red'
        change = color.colorize(change)
        # color.style = 'dim'
        # color.back = 'red'
        # color.fore = 'white'
        color.fore = 'light red'
            # color.fore = 'light red'
            # columns[2][1] = f'{color.colorize(columns[2][1])}'

    close = color.colorize(close)
    # normalized_str = f'{normalized:.4f}'
    normalized_str = f'{normalized:.6f}'
    normalized_str = f'{normalized_str:7}'
    if normalized < 0.05:
        color.back = 'red'
        color.fore = 'light white'
    elif 0.3333 < normalized <= 0.05:
        color.fore = 'light black'
    elif 0.6666 < normalized <= 0.3333:
        color.fore = 'white'
    elif 0.95 > normalized >= 0.6666:
        color.fore = 'light white'
    elif normalized >= 0.95:
        color.back = 'blue'
        color.fore = 'light white'
    normalized_str = color.colorize(normalized_str)

    columns[3] = [num_form(data['o']), close, change, normalized_str]

    coin = data['s']
    color.fore = 'light yellow'
    coin = color.colorize(coin)

    rows = np.array(columns).swapaxes(0, 1).tolist()
    lines = [column_formatter(rows[i]) for i in range(longest_nested_list(columns))]
    lines_string = "".join(lines)

    interval = f'interval={data["i"]}'
    color.fore = 'light white'
    interval = color.colorize(interval)

    header = f'{coin}{interval:>{width-len(data["s"])+4}}'.replace(" ", "-")

    time_str = f'{timestamp_convert(data["t"])} --- {timestamp_convert(data["T"])}'
    time_str = f'{time_str:^{width-5}s}'

    if not status:
        color.fore = 'light black'
    else:
        color.fore = 'black'
        color.back = 'white'
    time_str = color.colorize(time_str).strip(" ")
    separator = f'{"-" * (width-5)}'
    separator = f'{separator:^{width-5}s}'

    return f'{header}\n{time_str}\n{separator}\n{lines_string}\n'


def data_parsing(data):
    data_dict =  {
    "vol": data['v'],
    "high": data['h'],
    "low": data['l'],
    "open": data['o'],
    "close": data['c'],
    "symbol": data['s'],
    "status": data['x'],
    "interval": data['i'],
    "start": data['t'],
    "end": data['T']
    }
    return data_dict


def data_simple_print(data_dict, candle):
    for k in data_dict.keys():
        if len(data_dict[k][candle]) > 0:
            data_str = f'{k.upper():12}{data_dict[k][candle]["close"]}'
            print(f'{data_str}' + " " * (terminal_dim[0]-len(data_str)))


def stream_loop(sock):
    terminal.clear()

    while True:
        try:
            stream = stream_thread.get_stream_json_decoded()

            if stream and 'stream' in stream.keys():
                # populate coin dict
                co = f'{stream["data"]["s"]}'.lower()
                ca = f'{stream["data"]["k"]["i"]}'

                if LITE_MODE:
                    coin_dict[co][ca] = data_parsing(stream['data']['k'])
                    terminal.jump(terminal_dim[1])
                    terminal.cursor.hide()
                    topic = f'\n** LITE MODE **'
                    print(f'{topic}' + " " * (terminal_dim[0]-len(topic)-1) + "\n")
                    data_simple_print(coin_dict, ca)
                    print(" " * terminal_dim[0])
                else:
                    coin_str_dict[co][ca] = format_kline(stream['data']['k'], width=WIDTH)
                    terminal.jump(terminal_dim[1])
                    terminal.cursor.hide()
                    create_candle_group()
                    create_parallel_view()


                print_info_text()

            if key_handler.quit_flag:
                stream_thread.quit()
                break

        except Exception as e:
            print(e)
            stream_thread.quit()
            break

        time.sleep(POLL_TIME)


WIDTH = 48
LITE_MODE = False

POLL_TIME = 1/6 if LITE_MODE else 1/20
terminal = Terminal()
terminal.clear()

key_handler = KeyHandler(verbose=1)
key_handler.start()

color = ColorizeText()
color.reset_all()

BINANCE_FUNC = BinanceFunctions()
# coins, candles = COCA.COINS_TOP + COCA.COINS_DOGS + COCA.COINS_POS, COCA.CANDLES_9
coins, candles = ("BTCBUSD", "ALGOBUSD"), COCA.CANDLES_9

coins = [f'{i}'.lower() for i in coins]

candle_group_dict = {}
coin_dict = {a: {b: {} for b in candles} for a in coins}
coin_str_dict = {a: {b: "" for b in candles} for a in coins}

columns = [[]] * 4
columns[0] = ["high", "low", "volume", "volatility"]
columns[2] = ["open", "close", "", "norm"]

print(f'Python {sys.version} on {sys.platform}\n')
time.sleep(1)

if LITE_MODE:
    terminal_dim = WIDTH, len(coins) + 9
else:
    terminal_dim = 49 * len(coins), int(8.5 * len(candles)) + 5

terminal.resize(*terminal_dim)
terminal.cursor.hide()
terminal.clear()

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

stream_thread = BinanceStreamThread(socket, poll_time=POLL_TIME)
stream_thread.start()

stream_loop(socket)

socket.send(json.dumps({"method": "UNSUBSCRIBE", "params": coins, "id": 312}))

stream_thread.quit()
terminal.cursor.show()
terminal.resize(80, 24)
sys.exit(0)
