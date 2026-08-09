# 🛡️ Intelligent Network Traffic Anomaly Detector

Behavioral and statistical network anomaly detection designed for resource efficiency. 

This Python-based monitoring system detects unknown threats and zero-day spikes in real-time. By utilizing a signature-free approach relying heavily on probability and statistical Z-score deviation, it effectively identifies anomalous traffic patterns without needing predefined threat definitions. The detector features flexible ingestion, allowing you to analyze raw live packet streams or static `.pcap` files, alongside a live Streamlit dashboard for visualizing metrics and security alerts.

## 📋 Features

* **Signature-Free Detection** - Detects unknown threats and zero-day spikes via Z-score deviation.
* **Flexible Ingestion** - Analyzes raw live network traffic or offline PCAP files.
* **Intelligent Baseline Learning** - Adaptive baseline that learns normal traffic patterns with a configurable warmup period.
* **Live Traffic Metrics** - Rolling window analysis of packets-per-second, protocol distribution, and source IPs.
* **Security Dashboard** - Real-time Streamlit dashboard with visual alerts, packet trends, and protocol distribution.
* **Modular Architecture** - Independent modules for packet capture, feature extraction, baseline management, and alerting.
* **CSV Logging** - Detailed traffic logs for forensic analysis and compliance.

## 🚀 Quick Start

### Prerequisites

* Python 3.8+
* `pip` package manager
* Linux/macOS for live packet capture (requires libpcap)
* Administrative privileges for live network interface capture

### Installation

1. Clone the repository:
```bash
git clone [https://github.com/milandoes/Intelligent-Network-Traffic-Anomaly-Detector-.git](https://github.com/milandoes/Intelligent-Network-Traffic-Anomaly-Detector-.git)
cd Intelligent-Network-Traffic-Anomaly-Detector-

```

2. Install dependencies:

```bash
pip install scapy streamlit pandas numpy

```

### Running in PCAP Mode (No Root Required)

The easiest way to get started is using the included demo traffic file:

```bash
# Run the anomaly detector on the demo traffic
python anomaly_detector.py --mode pcap --pcap-file demo_traffic.pcap --threshold 3.0 --warmup 50

# In another terminal, launch the live dashboard
streamlit run dashboard.py

```

Visit `http://localhost:8501` to see the dashboard.

### Running in Live Mode (Requires Root/Admin)

```bash
sudo python anomaly_detector.py --mode live --interface eth0 --threshold 3.0 --warmup 50

```

*Note: Adjust `eth0` to your network interface (use `ifconfig` or `ip addr` to find it).*

## 📊 Command-Line Options

```text
--mode {live,pcap}       Capture mode: live interface or offline PCAP file (default: pcap)
--interface INTERFACE    Network interface for live mode (e.g., eth0, wlan0)
--pcap-file PATH         Path to PCAP file for offline mode (default: demo_traffic.pcap)
--threshold SCORE        Z-score anomaly threshold (default: 3.0)
--warmup PACKETS         Number of packets to learn baseline before detecting (default: 50)
--window SECONDS         Rolling window size in seconds for traffic metrics (default: 5)
--log PATH               Output log file path (CSV) (default: traffic_log.csv)

```

**Example with Custom Settings:**

```bash
python anomaly_detector.py \
  --mode pcap \
  --pcap-file demo_traffic.pcap \
  --threshold 2.5 \
  --warmup 100 \
  --window 10 \
  --log my_results.csv

```

## 📁 Project Structure

```text
NetworkAnomalyDetector/
├── anomaly_detector.py      # Main detector engine
├── dashboard.py             # Streamlit real-time visualization
├── traffic_gen.py           # Synthetic PCAP generator
├── demo_traffic.pcap        # Pre-generated demo traffic file
├── traffic_log.csv          # Output CSV log (generated during execution)
└── README.md                # This file

```

## 🏗️ Architecture

**Core Modules**

* **Packet Capture:** Live network interface sniffing using Scapy, and offline PCAP file reading.
* **Feature Extraction:** Parses IP, TCP/UDP/ICMP protocols, extracting packet size, IPs, and timestamps.
* **Baseline Management:** Maintains a rolling window of normal packet sizes, computing mean and standard deviation for statistical analysis.
* **Traffic Metrics:** Real-time rolling window analysis tracking packets-per-second (PPS) and protocol distribution.
* **Anomaly Detection:** Z-score calculation with a configurable threshold to flag deviations.
* **Alerting & Logging:** CSV output and real-time console alerts with visual warnings.

**Dashboard Features**

* **Live Metrics:** Total packets analyzed, anomaly count, threat level.
* **Packet Size Trend:** Line chart of the last 50 packets.
* **Protocol Distribution:** Bar chart breakdown (TCP, UDP, ICMP).
* **Security Alerts Table:** Highlighted view of detected anomalies.

## 📈 Output Log Format

The `traffic_log.csv` contains:

| Timestamp | Source_IP | Dest_IP | Protocol | Payload_Size | Z_Score | Is_Anomaly |
| --- | --- | --- | --- | --- | --- | --- |
| 10:45:23 | 192.168.1.5 | 192.168.1.1 | TCP | 156 | -0.42 | NO |
| 10:45:24 | 10.0.0.99 | 192.168.1.1 | TCP | 4521 | 5.87 | YES |

## 🔧 Generating Demo Traffic

To create your own synthetic traffic with anomalies:

```bash
python traffic_gen.py

```

This generates `demo_traffic.pcap` containing normal baseline packets and injected anomalous volumetric spikes.

## 🎯 Use Cases

* **Network Intrusion Detection:** Identify unusual traffic patterns indicating attacks.
* **DDoS Detection:** Spot volumetric anomalies in packet sizes.
* **Compliance Monitoring:** Log all traffic for audit trails.
* **Network Health Monitoring:** Baseline-aware alerts for operational anomalies.

## ⚙️ Tuning Guide

**Adjusting Sensitivity**

* Lower threshold (e.g., 2.0) → More sensitive, higher false positive rate.
* Higher threshold (e.g., 4.0) → Less sensitive, may miss subtle anomalies.
* *Recommended: Start at 3.0 and adjust based on your traffic profile.*

**Warmup Period**

* Shorter warmup (e.g., 20) → Faster detection, less robust baseline.
* Longer warmup (e.g., 200) → More stable baseline, slower to start alerting.
* *Recommended: 50–100 packets depending on traffic volume.*

## 🐛 Troubleshooting

* **"Scapy is required" Error:** Run `pip install scapy`.
* **No packets captured in live mode:** Ensure you are running with `sudo`, verify the interface name, and check firewall rules.
* **Dashboard shows "Waiting for data":** Ensure `anomaly_detector.py` is running and that `traffic_log.csv` exists in the same directory.
* **High false positive rate:** Increase `--threshold` or extend `--warmup` to capture more baseline variation.

## 📝 Output Example

**Console Output:**

```text
=== Intelligent Network Traffic Anomaly Detector ===
Mode: pcap | Threshold: Z > 3.0 | Warmup: 50 packets
Logging to: traffic_log.csv

Learning baseline... 1/50
Learning baseline... 2/50
...
OK  | 192.168.1.15 | TCP | 142B | Z=-0.31
🚨 ANOMALY | 10.0.0.99 -> 192.168.1.1 | TCP | 4521B | Z=5.87
[METRICS] PPS: 14.2 | Unique Src IPs: 8 | Protocol dist: {'TCP': '85.0%', 'UDP': '15.0%'}

```

## 🔐 Security Considerations

* **Root/Admin Access:** Live capture requires elevated privileges; verify you are on a trusted network.
* **PCAP File Validation:** Only load PCAP files from trusted sources.
* **CSV Logging:** Ensure log file permissions are restricted in production environments.

## 📄 License

This project is open source. See the repository for license details.

## 👤 Author

**milandoes** - [GitHub Profile](https://www.google.com/search?q=https://github.com/milandoes)

## 🤝 Contributing

Contributions to improve the statistical models or resource efficiency are highly welcome! Feel free to submit issues, fork the repository, and open pull requests.

```

```
