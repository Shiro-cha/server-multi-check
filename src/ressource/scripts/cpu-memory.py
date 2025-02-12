import json
import time

class CpuUsageReader(object):
    """
    Single Responsibility Principle (SRP):
      - This class is solely responsible for measuring CPU usage.
    """
    def __init__(self):
        pass

    def _read_cpu_times(self):
        """
        Reads the first line of /proc/stat which contains overall CPU times.
        Returns a tuple (idle, total) representing idle time and total time.
        """
        try:
            f = open('/proc/stat', 'r')
            line = f.readline()
            f.close()
        except IOError:
            return None, None
        parts = line.split()
        if parts[0] != 'cpu':
            return None, None
       
        try:
            times = [int(x) for x in parts[1:]]
        except ValueError:
            return None, None
        idle = times[3] 
        total = sum(times)
        return idle, total

    def get_cpu_usage_percentage(self):
        """
        Measures the CPU usage percentage over a 1-second interval.
        This method takes two readings separated by 1 second and calculates the difference.
        """
        idle1, total1 = self._read_cpu_times()
    
        time.sleep(1)
        idle2, total2 = self._read_cpu_times()
        if idle1 is None or total1 is None or idle2 is None or total2 is None:
            return 0.0
        idle_delta = idle2 - idle1
        total_delta = total2 - total1
        if total_delta == 0:
            return 0.0
        cpu_usage = (1.0 - float(idle_delta) / total_delta) * 100
        return cpu_usage


class MemoryUsageReader(object):
    """
    Single Responsibility Principle (SRP):
      - This class is solely responsible for reading memory usage data.
    """
    def __init__(self):
        pass

    def get_memory_usage(self):
        """
        Reads /proc/meminfo and parses total, free, and used memory values.
        The values are converted from kilobytes to megabytes.
        Returns a tuple: (total_memory, used_memory, free_memory).
        For free memory, it prefers 'MemAvailable' if available; otherwise, 'MemFree'.
        """
        mem_info = {}
        try:
            f = open('/proc/meminfo', 'r')
            for line in f:
                parts = line.split(':')
                if len(parts) < 2:
                    continue
                key = parts[0]
                
                try:
                    value = int(parts[1].strip().split()[0])
                except (ValueError, IndexError):
                    continue
                mem_info[key] = value
            f.close()
        except IOError:
            return None, None, None

        total = mem_info.get('MemTotal', 0) / 1024
        
        if 'MemAvailable' in mem_info:
            free = mem_info['MemAvailable'] / 1024
        else:
            free = mem_info.get('MemFree', 0) / 1024
        used = total - free
        return total, used, free


class SystemMonitor(object):
    """
    Dependency Inversion Principle (DIP):
      - This high-level module depends on the abstractions provided by CpuUsageReader and MemoryUsageReader.
      - It doesn't depend on their concrete implementations.
    """
    def __init__(self, cpu_reader=None, mem_reader=None):
        self.cpu_reader = cpu_reader or CpuUsageReader()
        self.mem_reader = mem_reader or MemoryUsageReader()

    def get_system_usage(self):
        """
        Retrieves system metrics:
          - CPU usage percentage
          - Memory metrics: total, used, and free (in MB)
        Returns a tuple: (cpu_usage, total_memory, used_memory, free_memory)
        """
        cpu_usage = self.cpu_reader.get_cpu_usage_percentage()
        total_mem, used_mem, free_mem = self.mem_reader.get_memory_usage()
        free_mem_percent = self.calculate_free_percent(total_mem, free_mem)
        used_mem_percent = self.calculate_used_percent(total_mem, used_mem)
        return cpu_usage, total_mem, used_mem, free_mem, used_mem_percent, free_mem_percent
    def calculate_used_percent(self, total, used):
        return (used / total) * 100
    def calculate_free_percent(self, total, free):
        return (free / total) * 100

class JSONFormatter(object):
    """
    Single Responsibility Principle (SRP):
      - This class is solely responsible for formatting data as JSON.
    """
    def __init__(self):
        pass

    def format(self, data):
        """
        Formats the given data as JSON.
        """
        return json.dumps(data)

if __name__ == '__main__':
    monitor = SystemMonitor()
    json_formatter = JSONFormatter()
    cpu_usage, total_mem, used_mem, free_mem,used_mem_percent, free_mem_percent = monitor.get_system_usage()
    data = {
        'cpu_usage': cpu_usage,
        'total_memory': total_mem,
        'used_memory': used_mem,
        'free_memory': free_mem,
        'used_memory_percent': used_mem_percent,
        'free_memory_percent': free_mem_percent
    }
    print(json_formatter.format(data))
