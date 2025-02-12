import json
import os

class MountedFilesystemReader:
    """
    Reads mounted filesystems from /proc/mounts.
    """
    def get_mounted_filesystems(self):
        """
        Get a list of mounted filesystems by reading /proc/mounts.
        Returns a list of mount points.
        """
        mount_points = []
        with open('/proc/mounts', 'r') as f:
            for line in f:
                parts = line.split()
                if len(parts) > 1:
                    mount_points.append(parts[1])  # Second column is the mount point
        
        # Remove duplicates while preserving order (Python 2.6 workaround)
        seen = set()
        unique_mounts = []
        for mount in mount_points:
            if mount not in seen:
                seen.add(mount)
                unique_mounts.append(mount)

        return unique_mounts


class FilesystemUsageCalculator:
    """
    Calculates filesystem usage for a given mount point.
    """
    def __init__(self, path):
        self.path = path

    def get_usage(self):
        """
        Get filesystem usage information for the mount point.
        Returns a dictionary with total, used, and free space in GB.
        """
        try:
            stat = os.statvfs(self.path)

            block_size = stat.f_frsize  
            total_blocks = stat.f_blocks  
            free_blocks = stat.f_bfree 
            available_blocks = stat.f_bavail  

            total_space = total_blocks * block_size
            free_space = free_blocks * block_size
            used_space = total_space - free_space

            def bytes_to_gb(bytes_value):
                if bytes_value is None:
                    return 0
                return bytes_value / (1024.0 ** 3)

            def usage_percent(used_space, total_space):
                if total_space == 0:
                    return 0
                return (used_space / float(total_space)) * 100

            return {
                'mount_point': self.path,
                'total_gb': bytes_to_gb(total_space),
                'used_gb': bytes_to_gb(used_space),
                'free_gb': bytes_to_gb(free_space),
                'available_gb': bytes_to_gb(available_blocks * block_size),
                'usage_percent': usage_percent(used_space, total_space)
            }
        except OSError:
            print("Unable to access filesystem.")
            return OSError


class FilesystemUsageFormatter:
    """
    Formats filesystem usage information into a human-readable string.
    """
    def format(self, usage):
        """
        Format filesystem usage information.
        """
        if usage is None:
            return "Unable to access filesystem."
        
        try:
            available_gb = usage['available_gb']
        except KeyError:
            available_gb = 0
            
        # JSON-like formatting
        json_format = {
            "MountPoint": usage["mount_point"],
            "Total": usage["total_gb"],
            "Used": usage["used_gb"],
            "Free": usage["free_gb"],
            "Available": available_gb
        }
        
        return json_format


class FilesystemReporter:
    """
    Reports filesystem usage for all mounted filesystems.
    """
    def __init__(self, reader, calculator, formatter):
        self.reader = reader
        self.calculator = calculator
        self.formatter = formatter

    def generate_report(self):
        """
        Generate a report for all mounted filesystems.
        """
        mounted_points = self.reader.get_mounted_filesystems()
        disk_usage = []
        for mount_point in mounted_points:
            calculator = self.calculator(mount_point)
            usage = calculator.get_usage()
            formatted = self.formatter.format(usage)
            disk_usage.append(formatted)

        print(json.dumps(disk_usage))
# Main execution
if __name__ == "__main__":
    reader = MountedFilesystemReader()
    calculator = FilesystemUsageCalculator
    formatter = FilesystemUsageFormatter()

    reporter = FilesystemReporter(reader, calculator, formatter)
    reporter.generate_report()