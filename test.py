
from datetime import datetime

date_raw = datetime.now()

date, time = date_raw.split(" ")
time = time.split(".")[0]


