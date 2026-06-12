from datetime import datetime
from zoneinfo import ZoneInfo

dhaka = datetime.now(ZoneInfo("Asia/Dhaka"))
tokyo = datetime.now(ZoneInfo("Asia/Tokyo"))
seoul = datetime.now(ZoneInfo("Asia/Seoul"))

# Busan uses the same timezone as Seoul
busan = datetime.now(ZoneInfo("Asia/Seoul"))

# Shenzhen uses the same timezone as Shanghai
shenzhen = datetime.now(ZoneInfo("Asia/Shanghai"))

print("Dhaka:", dhaka.strftime("%Y-%m-%d \n Time: %H:%M:%S"))
print("Busan:", busan.strftime("%Y-%m-%d \n Time: %H:%M:%S"))
print("Tokyo:", tokyo.strftime("%Y-%m-%d \n Time: %H:%M:%S"))
print("Seoul:", seoul.strftime("%Y-%m-%d \n Time: %H:%M:%S"))
print("Shenzhen:", shenzhen.strftime("%Y-%m-%d \n Time: %H:%M:%S"))