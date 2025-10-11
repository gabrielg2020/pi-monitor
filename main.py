#!/usr/bin/env python3

import os
import time
from datetime import datetime

import psutil
import requests
from dotenv import load_dotenv


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

    now = datetime.now()
    timestamp_str = now.strftime('%Y-%m-%d %H:%M:%S')

    # Create record for JSON
    record = {
        'host_id': int(os.getenv('HOSTNAME')),
        "timestamp": int(now.timestamp()),
        "cpu_usage": round(cpu, 1),
        "memory_usage_percent": round(memory['percent'], 1),
        "memory_total_bytes": int(memory['total_gb'] * 1024 ** 3),
        "memory_used_bytes": int(memory['used_gb'] * 1024 ** 3),
        "memory_available_bytes": int(memory['available_gb'] * 1024 ** 3),
        "disk_usage_percent": round(disk['percent'], 1),
        "disk_total_bytes": int(disk['total_gb'] * 1024 ** 3),
        "disk_used_bytes": int(disk['used_gb'] * 1024 **3),
        "disk_available_bytes": int(disk['free_gb'] * 1024 **3)
    }

    print(f"\n{'=' * 60}")
    print(f"System Monitor - {timestamp_str}")
    print(f"{'=' * 60}")

    print(f"\n🔧 CPU Usage: {cpu:.1f}%")

    print(f"\n💾 Memory Usage: {memory['percent']:.1f}%")
    print(f"   Used: {memory['used_gb']:.2f} GB / {memory['total_gb']:.2f} GB")
    print(f"   Available: {memory['available_gb']:.2f} GB")

    print(f"\n📁 Disk Usage: {disk['percent']:.1f}%")
    print(f"   Used: {disk['used_gb']:.2f} GB")
    print(f"   Free: {disk['free_gb']:.2f} GB / {disk['total_gb']:.2f} GB")

    print(f"\n{'='*60}")

    return record


def send_push_request(records, address):
    """Push data to remote API"""
    url = f"{address}/api/push"
    print(f"Pushing data to {url} ...")
    try:
        response = requests.post(url, json={'record': records})
        if response.status_code == 200:
            print("Data successfully pushed to remote API.")
        else:
            print(f"Failed to push data. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.RequestException as e:
        print(f"Error pushing data to API: {e}")



def main():
    """Main monitoring loop"""
    load_dotenv()
    api_address = os.getenv('API_ADDRESS', 'http://localhost:8000')
    port = os.getenv('PORT', 8080)
    address = f"{api_address}:{port}"
    print(f"API Address: {address}")
    print("Raspberry Pi System Monitor")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            record = display_stats()
            send_push_request(record, address)
            time.sleep(5)  # Update every 5 seconds
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")


if __name__ == "__main__":
    main()
