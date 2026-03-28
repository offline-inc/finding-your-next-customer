# Plexus - Ideal Customer Profile

**One-liner:** HardwareOps: observability platform for physical systems

**Stage:** Early. One named customer (Scout Space, satellite monitoring). Actively hiring GTM. Legal name: Plexus Aerospace, Inc.

## Who buys

**Starting vertical (workshop recommendation): Autonomous vehicle companies.** This is a question for the founding team to confirm, but the product fits any company shipping software-defined hardware.

- **Autonomous vehicle companies** - self-driving cars, mining trucks, agricultural equipment, autonomous delivery robots. Mission-critical systems generating massive telemetry that needs real-time observability
- **Aerospace and satellite companies** - building/operating satellites, launch vehicles, drones. Scout Space (their one customer) is in this category. Post-deployment hardware they can't physically access
- **Robotics companies** - warehouse automation, manufacturing robots. Software-defined machines scaling from prototype to fleet
- **IoT device fleet operators** - companies shipping connected hardware (ESP32, Raspberry Pi, STM32-based devices) at scale

## What the product actually does

- Python SDK (Linux devices) and C SDK (embedded, ~1.5 KB RAM)
- Supports 15+ telemetry protocols
- Auto-generated dashboards from device sensor data
- GPU-accelerated visualization (100K+ data points at 60fps)
- Threshold alerts + anomaly detection
- Remote device commands
- Runbook automation
- AI root-cause analysis (Pro tier+)
- Pricing starts at $500/mo. Free tier: 5 devices, live-only data

## Key pains

- The "standard stack" requires 5+ separate tools (MQTT, Telegraf, InfluxDB, Grafana, Docker), each needing independent configuration
- Silent failures: one team had 3,872 failure warnings before realizing no data was flowing
- Days to get from sensor data to dashboards. Most hardware projects fail before reaching production observability
- Debugging is primitive: printf over UART during development, then blindness once devices ship
- Enterprise platforms are bloated and expensive (LabVIEW at $4,000/seat)
- "Software teams have DevOps. Hardware teams have spreadsheets."

## Where to find them

- LinkedIn Sales Navigator: filter by "autonomous vehicles," "robotics," "aerospace" + engineering/ops titles
- Crunchbase: companies tagged robotics, aerospace, autonomous vehicles with Series A+ funding
- GitHub/open-source: teams contributing to ROS, PX4, ArduPilot, Autoware
- Trade shows: AUVSI XPONENTIAL, Space Symposium, Automate, CES (automotive)
- Job boards: companies posting roles mentioning "telemetry," "fleet monitoring," "hardware observability"

## Qualifying signals

- Shipping or testing autonomous/semi-autonomous hardware in the field
- Engineering team of 10+ (enough complexity to need observability tooling)
- Currently cobbling together MQTT + Grafana + custom Python scripts
- Scaling from single prototype to multi-device fleet
- Job postings mentioning "telemetry," "anomaly detection," or "embedded systems"

## Key ICP question to resolve

Which vertical first? Autonomous vehicles, aerospace, or robotics? (Recommendation: pick one)
