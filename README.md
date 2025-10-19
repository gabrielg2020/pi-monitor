# monitor-agent

A lightweight Python agent that collects system metrics from devices and reports them to the monitoring API. Designed to run as a background service with minimal resource usage.

## Features

- **Lightweight**: Minimal CPU and memory footprint
- **Real-time Monitoring**: Collects metrics every 5 seconds
- **Comprehensive Metrics**: CPU, memory, and disk usage
- **Automatic Registration**: Self-registers with the API on first run
- **Systemd Integration**: Runs as a system service
- **Error Handling**: Graceful error handling and retry logic

## Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Running as Service](#running-as-service)

## Architecture

![Architecture Preview](docs/images/architecture.png)

## Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **systemd** (for running as service)
- Access to the monitoring API

## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/gabrielg2020/monitor-agent.git
    cd monitor-agent
    ```

2. **Create virtual environment**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create configuration file**

    ```bash
    cp .env.example .env
    vim .env
    ```

5. **Make executable**

    ```bash
    chmod +x main.py
    ```
## Configuration

### Environment Variables

Create a `.env` file:
```bash
API_ADDRESS=http://localhost
API_VERSION=v1
API_PORT=8191
HOST_ROLE=server
```

### Configuration Options

| Variable      | Description                             | Default | Required |
|---------------|-----------------------------------------|---------|----------|
| `API_URL`     | Monitor API base URL                    | -       | Yes      |
| `API_VERSION` | API version                             | v1      | No       |
| `API_PORT`    | API port                                | 8191    | No       |
| `HOST_ROLE`   | Role of the host (e.g., server, client) | server  | No       |

## Usage

### Run Manually
```bash
# Activate virtual environment
source .venv/bin/activate

# Run agent
./main.py

# Or with Python
python main.py
```

### Run in Background (tmux)
```bash
# Start tmux session
tmux new -s monitor-agent

# Activate venv and run
source .venv/bin/activate
./main.py

# Detach: Ctrl+B, then D
# Reattach: tmux attach -t monitor-agent
```

## Running as Service

### Create Systemd Service

1. **Create service file**
    ```bash
    sudo nano /etc/systemd/system/monitor-agent.service
    ```

2. **Add configuration**
    ```ini
    [Unit]
    Description=Monitor Agent
    After=network.target docker.service
    Wants=network-online.target
    
    [Service]
    Type=simple
    User=pi
    WorkingDirectory=/home/pi/scripts/monitor-agent
    ExecStart=/home/pi/scripts/monitor-agent/.venv/bin/python /home/pi/scripts/monitor-agent/main.py
    Restart=always
    RestartSec=10
    
    [Install]
    WantedBy=multi-user.target
    ```

3. **Enable and start service**
    ```bash
    # Reload systemd
    sudo systemctl daemon-reload
    
    # Enable service (start on boot)
    sudo systemctl enable monitor-agent
    
    # Start service
    sudo systemctl start monitor-agent
    
    # Check status
    sudo systemctl status monitor-agent
    ```

### Service Management

```bash
# View logs
sudo journalctl -u monitor-agent -f

# Restart service
sudo systemctl restart monitor-agent

# Stop service
sudo systemctl stop monitor-agent

# Disable auto-start
sudo systemctl disable monitor-agent

# View recent logs
sudo journalctl -u monitor-agent -n 50
```

## API Integration

### Host Registration

On first run, the agent automatically registers with the API:
```python
POST /api/v1/hosts
{
  "hostname": "pi-01",
  "ip_address": "192.168.0.24",
  "role": "server"
}
```

### Metric Submission

Every 5 seconds:
```python
POST /api/v1/metrics
{
  "hostname": "pi-01",
  "cpu_usage": 45.2,
  "memory_usage_percent": 67.8,
  # ... other metrics
}
```

## Related Projects

- [Monitor API](https://github.com/gabrielg2020/monitor-api) - Backend API server
- [Monitor Frontend](https://github.com/gabrielg2020/monitor-frontend) - Web dashboard
- [Monitor db](https://github.com/gabrielg2020/monitor-db) - Database schema


## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Built with 💻 by Gabriel Guimaraes

