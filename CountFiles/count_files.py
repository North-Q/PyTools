import os

def count_files_with_suffixes(directory, suffixes):
    counts = {suffix: 0 for suffix in suffixes}
    for root, dirs, files in os.walk(directory):
        for file in files:
            for suffix in suffixes:
                if file.endswith(suffix):
                    counts[suffix] += 1
    return counts

# Example usage
directory = 'E:\\摄影\\待处理\\2024.6.2-11毕业旅行\\丽江\\未选中'
suffixes = ['.ARW']  # Replace with the suffixes you need
file_counts = count_files_with_suffixes(directory, suffixes)
for suffix, count in file_counts.items():
    print(f"Total number of files with suffix '{suffix}': {count}")

# Total number of files with suffix '.ARW': 1508
# Total number of files with suffix '.JPG': 0
# Total number of files with suffix '.DNG': 0

# Total number of files with suffix '.ARW': 1734
# Total number of files with suffix '.JPG': 1734
# Total number of files with suffix '.DNG': 0

# 阳
# Total number of files with suffix '.ARW': 221
# Total number of files with suffix '.JPG': 221
# Total number of files with suffix '.DNG': 0

