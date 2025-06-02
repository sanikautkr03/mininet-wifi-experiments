# Mininet-WiFi Experiments

This repository contains a collection of wireless networking experiments using [Mininet-WiFi](https://github.com/intrig-unicamp/mininet-wifi). These experiments simulate mobile stations, handover mechanisms, and web server performance in wireless topologies.

---

## 📁 Contents

| File          | Description |
|---------------|-------------|
| `exp1.py` - `exp6.py` | Basic topologies, mobility, range, and propagation scenarios |
| `exp7.py` | Roaming with multiple access points |
| `exp8.py` | Mobility scenario with handover demonstration |
| `exp9.py` | Signal-strength-based handover using RSSI |
| `exp10.py` | Performance evaluation of a web server with mobile clients |
| `*.pcap` | Packet captures from various nodes |
| `webserver.log` | Access log from web server (h1) |
| `*.log` | Optional experiment logs |

---

## ✅ Requirements

- Ubuntu 20.04+ (or any Debian-based distro)
- [Mininet-WiFi](https://github.com/intrig-unicamp/mininet-wifi)
- `apache2-utils` (for ApacheBench):
  ```bash
  sudo apt install apache2-utils
