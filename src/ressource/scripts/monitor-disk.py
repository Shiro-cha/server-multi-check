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

            # Calculate block sizes
            block_size = stat.f_frsize  # Filesystem block size
            total_blocks = stat.f_blocks  # Total number of blocks
            free_blocks = stat.f_bfree  # Number of free blocks
            available_blocks = stat.f_bavail  # Number of blocks available to non-root users

            # Calculate space in bytes
            total_space = total_blocks * block_size
            free_space = free_blocks * block_size
            used_space = total_space - free_space

            # Convert bytes to gigabytes
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
            # Skip filesystems that cannot be accessed (e.g., network mounts)
            return None


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
            available_gb = 0  # Avoid KeyError if missing
        
        return (
            "Mount Point: %s\n"
            "Total: %.2f GB\n"
            "Used: %.2f GB\n"
            "Free: %.2f GB\n"
            "Available: %.2f GB" % (
                usage['mount_point'],
                usage['total_gb'],
                usage['used_gb'],
                usage['free_gb'],
                available_gb
            )
        )


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
        for mount_point in mounted_points:
            calculator = self.calculator(mount_point)
            usage = calculator.get_usage()
            print(self.formatter.format(usage))
            print('')


# Main execution
if __name__ == "__main__":
    reader = MountedFilesystemReader()
    calculator = FilesystemUsageCalculator
    formatter = FilesystemUsageFormatter()

    reporter = FilesystemReporter(reader, calculator, formatter)
    reporter.generate_report()