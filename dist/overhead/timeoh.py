from datetime import datetime


def timestamp_convert(time_stamp, get_date=1, get_time=1, date_str="dmy"):
	t = datetime.fromtimestamp(time_stamp / 1e3)
	a, b = "", ""
	if get_date:
		d, m, y = "", "", ""
		if "d" in date_str:
			d = "%d."
		if "m" in date_str:
			m += "%m."
		if "y" in date_str:
			y += "%Y"
		a = t.strftime(f'{d}{m}{y}')
	if get_time:
		b = t.strftime('%H:%M:%S')
	return f'{a} {b}'.strip()
