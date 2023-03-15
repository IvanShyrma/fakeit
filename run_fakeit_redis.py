import subprocess
from threading import Thread
import sys

# Example to run
# python3 run_fakeit_redis.py -i 10000 -t 2 -r_url 'redis://USER:PASS@HOST:PORT'

_items = None
_threads = None
_global_offset = 0
_redis_url = ''
workdir = "../fakeit"

p = subprocess.Popen('make build', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                     cwd=workdir)
retval = p.wait()


def run(batch_size, total_batches, group, g, r_url):
    for i in range(0, int(total_batches)):
        command = "./bin/fakeit -m customers.yaml,orders.yaml --exclude Orders -n {} -d redis --offset {} --redis_url '{}'"\
            .format(batch_size, int(batch_size * group * total_batches + i * batch_size + g), r_url)    # --exclude Orders or Customers if you need. It's optional
        p = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             cwd=workdir)
        for line in p.stdout.readlines():
            print(line)
        retval = p.wait()


def run_fakeit(i, t, g, r_url):
    batch_size = 5000
    total_batches = i / (batch_size * t)
    for i in range(0, t):
        new_thread = Thread(target=run, args=(batch_size, total_batches, i, g, r_url))
        new_thread.start()


for i, item in enumerate(sys.argv):
    if item == "-i":
        _items = int(sys.argv[i + 1])
    elif item == "-t":
        _threads = int(sys.argv[i + 1])
    elif item == "-r_url":
        _redis_url = sys.argv[i + 1]
    elif item == "-g":
        _global_offset = int(sys.argv[i + 1])

if _items and _threads:
    run_fakeit(i=_items, t=_threads, g=_global_offset, r_url=_redis_url)
else:
    print("Usage run_fakeit.py -i <items>  -t <threads> -r_url <'redis://user@pass:host:port'>")
