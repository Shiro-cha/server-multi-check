# it python 2.7.5

import os
import sys

def get_cpu_usage():
    return os.popen("top -b -n1 | grep 'Cpu(s)' | awk '{print $2 + $4}'").readline().strip()

def get_memory_usage():
    return os.popen("free | grep Mem | awk '{print $3/$2 * 100.0}'").readline().strip()

# get disk usage using python native library
def get_disk_usage():
    import psutil
    return psutil.disk_usage('/').percent