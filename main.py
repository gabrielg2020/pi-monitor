#!/usr/bin/env python3

import psutil
import time
import json
from datetime import datetime
from collections import deque


def get_cpu_usage():
    """Get current CPU usage percentage"""
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    """Get memory usage details"""
    mem = psutil.virtual_memory()
    return {
        'percent': mem.percent,
        'used_gb': mem.used / (1024**3),
        'total_gb': mem.total / (1024**3),
        'available_gb': mem.available / (1024**3)
    }


def get_disk_usage(path='/'):
    """Get disk usage for specified path"""
    disk = psutil.disk_usage(path)
    return {
        'percent': disk.percent,
        'used_gb': disk.used / (1024**3),
        'free_gb': disk.free / (1024**3),
        'total_gb': disk.total / (1024**3)
    }


def display_stats():
    """Display system statistics"""
    cpu = get_cpu_usage()
    memory = get_memory_usage()
    disk = get_disk_usage()

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create record for JSON
    record = {
        'timestamp': timestamp,
        'cpu_percent': round(cpu, 1),
        'memory': {
            'percent': round(memory['percent'], 1),
            'used_gb': round(memory['used_gb'], 2),
            'total_gb': round(memory['total_gb'], 2),
            'available_gb': round(memory['available_gb'], 2)
        },
        'disk': {
            'percent': round(disk['percent'], 1),
            'used_gb': round(disk['used_gb'], 2),
            'free_gb': round(disk['free_gb'], 2),
            'total_gb': round(disk['total_gb'], 2)
        }
    }

    print(f"\n{'='*60}")
    print(f"System Monitor - {timestamp}")
    print(f"{'='*60}")

    print(f"\n🔧 CPU Usage: {cpu:.1f}%")

    print(f"\n💾 Memory Usage: {memory['percent']:.1f}%")
    print(f"   Used: {memory['used_gb']:.2f} GB / {memory['total_gb']:.2f} GB")
    print(f"   Available: {memory['available_gb']:.2f} GB")

    print(f"\n📁 Disk Usage: {disk['percent']:.1f}%")
    print(f"   Used: {disk['used_gb']:.2f} GB")
    print(f"   Free: {disk['free_gb']:.2f} GB / {disk['total_gb']:.2f} GB")

    print(f"\n{'='*60}")

    return record


def save_to_json(records, filename='system_stats.json'):
    """Save records to JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(list(records), f, indent=2)
    except Exception as e:
        print(f"Error saving to JSON: {e}")


def main():
    """Main monitoring loop"""
    print("Raspberry Pi System Monitor")
    print("Press Ctrl+C to stop\n")

    # Use deque to automatically maintain last 100 records
    records = deque(maxlen=100)

    try:
        while True:
            record = display_stats()
            records.append(record)
            save_to_json(records)
            time.sleep(5)  # Update every 5 seconds
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
        print(f"Final data saved to system_stats.json ({len(records)} records)")


if __name__ == "__main__":
    main()
