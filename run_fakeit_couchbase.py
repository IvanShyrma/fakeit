import subprocess
from threading import Thread
import sys

# Example to run
# python3 run_fakeit_couchbase.py -i 2000 -d couchbase -s $HOST -b $BUCKET_NAME -u $USER_NAME -p $PASS -t 2


_items = None
_threads = None
_global_offset = 0
_mongo_url = ''
_server_host = ''
_user = ''
_password = ''
_bucket = ''
workdir = "../fakeit"

p = subprocess.Popen('make build', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                     cwd=workdir)
retval = p.wait()


def run(batch_size, total_batches, group, g, host, bucket, user, password):
    for i in range(0, int(total_batches)):
        command = "./bin/fakeit -m customers.yaml,orders.yaml -n {} -d couchbase -s {} -b {} -u {} -p {} --offset {}"\
            .format(batch_size,
                    host,
                    bucket,
                    user,
                    password,
                    int(batch_size * group * total_batches + i * batch_size + g))
        print(command)
        p = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             cwd=workdir)
        for line in p.stdout.readlines():
            print(line)
        retval = p.wait()


def run_fakeit(i, t, g, host, bucket, user, password):
    batch_size = 1000
    total_batches = i / (batch_size * t)
    for i in range(0, t):
        new_thread = Thread(target=run, args=(batch_size, total_batches, i, g, host, bucket, user, password))
        new_thread.start()


for i, item in enumerate(sys.argv):
    if item == "-i":
        _items = int(sys.argv[i + 1])
    elif item == "-t":
        _threads = int(sys.argv[i + 1])
    elif item == "-s":
        _server_host = sys.argv[i + 1]
    elif item == "-b":
        _bucket = sys.argv[i + 1]
    elif item == "-u":
        _user = sys.argv[i + 1]
    elif item == "-p":
        _password = sys.argv[i + 1]
    elif item == "-g":
        _global_offset = int(sys.argv[i + 1])

if _items and _threads:
    run_fakeit(i=_items, t=_threads, g=_global_offset, host=_server_host, bucket=_bucket, user=_user, password=_password)
else:
    print("Usage run_fakeit.py -i <items>  -t <threads> -m_url <'mongodb+srv://user@pass:host'>")
