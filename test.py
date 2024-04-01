import datetime
import pytz
import sys
import time
import concurrent.futures # as per docs best method for allowcate all threds without any efforts
# import resource # not working for me, please check your end
import psutil #need for memory usage cal
from yahoo_fin import stock_info
from companies import watchout_list # importing as list from file, to do as much as faster
import warnings


IST = pytz.timezone('Asia/Kolkata')
now_date_time = datetime.datetime.now(tz=IST)

log_path = "lessthan100.txt"
sys.stdout = open(log_path, "a+")

def get_price(name):
        price = stock_info.get_live_price(name)
        if price <= 100:print({name:price})


start_time = time.time()
# start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # Get initial memory usage
start_memory = psutil.Process().memory_info().rss

warnings.simplefilter(action='ignore', category=FutureWarning)


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(get_price, watchout_list)



end_time = time.time()
# end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss  # Get final memory usage
end_memory = psutil.Process().memory_info().rss



timetook = end_time - start_time
memory_used = (end_memory - start_memory) / (1024 * 1024)  #1024*1024 for show in MB
print(f"Total Time: {timetook} seconds")
print(f"Total Memory Used: {memory_used:.2f} MB")
