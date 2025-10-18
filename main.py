#!/usr/bin/env python3

import os
import socket
import time

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
        "percent": mem.percent,
        "used_gb": mem.used / (1024**3),
        "total_gb": mem.total / (1024**3),
        "available_gb": mem.available / (1024**3),
    }


def get_disk_usage(path="/"):
    """Get disk usage for specified path"""
    disk = psutil.disk_usage(path)
    return {
        "percent": disk.percent,
        "used_gb": disk.used / (1024**3),
        "free_gb": disk.free / (1024**3),
        "total_gb": disk.total / (1024**3),
    }


def display_stats(host_id):
    """Display system statistics"""
    cpu = get_cpu_usage()
    memory = get_memory_usage()
    disk = get_disk_usage()
    timestamp = time.time()

    # Create record for JSON
    record = {
        "host_id": int(host_id),
        "timestamp": int(timestamp),
        "cpu_usage": round(cpu, 1),
        "memory_usage_percent": round(memory["percent"], 1),
        "memory_total_bytes": int(memory["total_gb"] * 1024**3),
        "memory_used_bytes": int(memory["used_gb"] * 1024**3),
        "memory_available_bytes": int(memory["available_gb"] * 1024**3),
        "disk_usage_percent": round(disk["percent"], 1),
        "disk_total_bytes": int(disk["total_gb"] * 1024**3),
        "disk_used_bytes": int(disk["used_gb"] * 1024**3),
        "disk_available_bytes": int(disk["free_gb"] * 1024**3),
    }

    print(f"\n{'=' * 60}")
    print(f"System Monitor - {timestamp}")
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


def post_metrics(records, address):
    """Push data to remote API"""
    address += "/metrics"
    print(f"Pushing data to {address} ...")
    try:
        response = requests.post(address, json={"record": records})
        if response.status_code == 201:
            print("Data successfully pushed to remote API.")
        else:
            print(f"Failed to push data. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.RequestException as e:
        print(f"Error pushing data to API: {e}")

def post_host(address):
    """Register host with remote API"""
    address += "/hosts"
    print(os.getenv("HOST_IP"))
    host_data = {
        "hostname": socket.gethostname(),
        "ip_address": os.getenv("HOST_IP"),
        "role": os.getenv("HOST_ROLE"),
    }

    payload = {"host": host_data}
    
    print(f"Registering host at {address} ...")
    try:
        response = requests.post(address, json=payload)
        if response.status_code == 201:
            host_id = response.json().get("id")
            print(f"Host registered with ID: {host_id}")
            return host_id
        else:
            print(f"Failed to register host. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.RequestException as e:
        print(f"Error registering host to API: {e}")
    return None

def main():
    """Main monitoring loop"""
    load_dotenv()
    port = os.getenv("PORT", 8080)
    version = os.getenv("API_VERSION", "v1")
    print(f"Starting monitoring on port {port} and version {version}")
    api_address = os.getenv("API_ADDRESS", "https://localhost:{PORT}").format(
        PORT=port, API_VERSION=version
    )
    print(f"API Address: {api_address}")
    print("Raspberry Pi System Monitor")
    print("Press Ctrl+C to stop\n")

    host_id = post_host(api_address)
    if host_id is None:
        print("Exiting due to host registration failure.")
        return

    try:
        while True:
            record = display_stats(host_id)
            post_metrics(record, api_address)
            time.sleep(5)  # Update every 5 seconds
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")


if __name__ == "__main__":
    main()
