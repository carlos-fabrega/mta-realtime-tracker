# MTA Real-Time Subway Tracker

Real-time subway arrival display for NYC's Fulton Station, built with Raspberry Pi, Python/Flask, and the MTA GTFS-realtime API.

## Features

- **Live MTA Data Integration** - Fetches real-time A/C and 4/5 train arrivals via MTA GTFS-realtime API
- **Web-Based Display** - Clean, professional HTML/CSS interface showing destinations and arrival times
- **Automated Scheduling** - Display automatically turns on/off during work hours via cron jobs
- **Headless Deployment** - Runs on Raspberry Pi Zero 2 W with auto-starting Firefox kiosk mode
- **Production-Ready** - Systemd service auto-restarts on reboot, runs 24/7 without intervention

## Hardware

- Raspberry Pi Zero 2 W (512MB RAM)
- Mini HDMI to HDMI cable
- 5V Micro USB power supply
- WiFi connectivity

## Tech Stack

- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **Data:** MTA GTFS-realtime API (protobuf)
- **Deployment:** Raspberry Pi OS, Systemd, Cron scheduling
- **Browser:** Firefox in kiosk mode

## Installation

### Prerequisites
```bash
pip install requests gtfs-realtime-bindings protobuf flask
```

### Quick Start
```bash
python3 mta_server.py
```
Access at `http://localhost:5000`

### Full Deployment
1. Flash Raspberry Pi OS to SD card
2. Configure SSH and WiFi via Raspberry Pi Imager
3. Install dependencies
4. Copy project files to `/home/pi/mta-tracker/`
5. Set up systemd service for auto-start:
```bash
   sudo cp mta-tracker.service /etc/systemd/system/
   sudo systemctl enable mta-tracker.service
   sudo systemctl start mta-tracker.service
```
6. Configure display scheduling with crontab

## Project Structure
mta-realtime-tracker/
├── mta_server.py              # Flask backend + MTA API integration
├── templates/
│   └── index.html             # Web interface with real-time updates
├── display-control.sh         # Script for display on/off control
├── README.md
└── .gitignore

## How It Works

### Backend (`mta_server.py`)
- Fetches GTFS-realtime data from MTA endpoints (ACE and 1-7 lines)
- Parses arrival times for Fulton Station uptown trains (A38N, 635N)
- Provides REST API endpoint `/api/trains` with JSON response
- Runs as systemd service on Raspberry Pi

### Frontend (`index.html`)
- Auto-refreshing web interface (updates every 30 seconds)
- Displays top 7 upcoming trains with colored indicators
- Shows destination and arrival time for each train
- Responsive design optimized for 20"+ displays

### Display Scheduling (`display-control.sh`)
- Controls HDMI display power via `vcgencmd`
- Scheduled via cron jobs:
  - OFF at 10 AM on weekdays
  - ON at 6 PM on weekdays
  - Always ON on weekends

## Key Technologies

**GTFS-Realtime Integration**
- Parses protobuf binary data from MTA API
- Extracts trip updates for specific stations
- Calculates minutes until arrival

**Raspberry Pi Deployment**
- Headless setup via SSH (no keyboard/monitor needed)
- Auto-login and auto-start via systemd and bash profile
- Scheduled display control with cron
- 24/7 operation with minimal power consumption

**Web Interface**
- Real-time data fetching via JavaScript fetch API
- Smooth animations and hover effects
- MTA-style color coding for train lines

## Future Enhancements

- RGB LED Matrix display (64x32) for authentic MTA aesthetic
- Support for additional stations and train lines
- Mobile app integration
- Real-time delay/alert notifications
- Historical data analytics

## Lessons Learned

- GTFS-realtime protobuf parsing and API integration
- Raspberry Pi headless deployment and system administration
- Full-stack web development with Flask
- System-level scheduling and process management
- IoT project development and automation

## Author

**Carlos Fabrega**
- GitHub: [@carlos-fabrega](https://github.com/carlos-fabrega)
- LinkedIn: [Carlos Fabrega](https://linkedin.com/in/carlosfabrega0)

## License

MIT License - feel free to use this project for your own stations!
