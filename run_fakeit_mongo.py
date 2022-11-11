import subprocess
from threading import Thread
import sys

_items = None
_threads = None
_global_offset = 0
_mongo_url = ''
workdir = "../fakeit"

p = subprocess.Popen('make build', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                     cwd=workdir)
retval = p.wait()


def run(batch_size, total_batches, group, g, m_url):
    for i in range(0, int(total_batches)):
        command = "./bin/fakeit -m customers.yaml,orders.yaml -n {} -d mongodb --offset {} --mongodb_url '{}'"\
            .format(batch_size, int(batch_size * group * total_batches + i * batch_size + g), m_url)
        p = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             cwd=workdir)
        for line in p.stdout.readlines():
            print(line)
        retval = p.wait()


def run_fakeit(i, t, g, m_url):
    batch_size = 10000
    total_batches = i / (batch_size * t)
    for i in range(0, t):
        new_thread = Thread(target=run, args=(batch_size, total_batches, i, g, m_url))
        new_thread.start()


for i, item in enumerate(sys.argv):
    if item == "-i":
        _items = int(sys.argv[i + 1])
    elif item == "-t":
        _threads = int(sys.argv[i + 1])
    elif item == "-m_url":
        _mongo_url = sys.argv[i + 1]
    elif item == "-g":
        _global_offset = int(sys.argv[i + 1])

if _items and _threads:
    run_fakeit(i=_items, t=_threads, g=_global_offset, m_url=_mongo_url)
else:
    print("Usage run_fakeit.py -i <items>  -t <thereads>")
