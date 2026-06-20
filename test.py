from datetime import datetime
from zoneinfo import ZoneInfo

print(datetime.now(ZoneInfo("Asia/Dhaka")))
print(datetime.now(ZoneInfo("Asia/Rajshahi")))
