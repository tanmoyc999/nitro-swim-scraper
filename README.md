# Nitro Swim Class Scraper

Automated scraper to check available swimming classes at Nitro Cedar Park and send email notifications.

## Features

- Scrapes available classes from Nitro Swim website
- Identifies open spots for each class (TF1-TF2)
- Sends email notifications with class availability
- EC2-compatible with systemd scheduler
- Logging for monitoring and debugging

## Project Structure

```
nitro_swim_scraper/
├── scraper.py          # Main scraper logic
├── scheduler.py        # EC2 scheduler
├── config.py           # Configuration
├── requirements.txt    # Python dependencies
├── setup_ec2.sh        # EC2 setup script
└── nitro-swim.service  # Systemd service file
```

## Local Setup

### Prerequisites
- Python 3.7+
- pip

### Installation

1. Clone/navigate to the project directory
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the scraper once:
```bash
python scraper.py
```

## EC2 Setup

### Prerequisites
- EC2 instance (t2.micro free tier eligible)
- Ubuntu 20.04 LTS or similar
- SSH access to instance

### Automated Setup

1. Copy all files to your EC2 instance:
```bash
scp -r nitro_swim_scraper/ ec2-user@your-instance-ip:/home/ec2-user/
```

2. SSH into your instance:
```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

3. Run the setup script:
```bash
cd nitro_swim_scraper
chmod +x setup_ec2.sh
./setup_ec2.sh
```

### Manual Setup

1. Update system:
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

2. Install Python and pip:
```bash
sudo apt-get install -y python3 python3-pip
```

3. Install dependencies:
```bash
cd ~/nitro_swim_scraper
pip3 install -r requirements.txt
```

4. Create log directory:
```bash
sudo mkdir -p /var/log/nitro_swim
sudo chown $USER:$USER /var/log/nitro_swim
```

5. Copy systemd service file:
```bash
sudo cp nitro-swim.service /etc/systemd/system/
sudo systemctl daemon-reload
```

6. Enable and start the service:
```bash
sudo systemctl enable nitro-swim.service
sudo systemctl start nitro-swim.service
```

### Monitoring

Check service status:
```bash
sudo systemctl status nitro-swim.service
```

View logs:
```bash
tail -f /var/log/nitro_swim_scraper.log
```

View systemd logs:
```bash
sudo journalctl -u nitro-swim.service -f
```

## Configuration

Edit `config.py` to customize:
- Email addresses
- Scraper interval (default: 60 minutes)
- Log file location
- Website URL

## Troubleshooting

### Email not sending
- Verify Gmail app password is correct
- Ensure 2FA is enabled on Gmail account
- Check firewall allows SMTP (port 587)

### Script not running on EC2
- Check service status: `sudo systemctl status nitro-swim.service`
- Check logs: `sudo journalctl -u nitro-swim.service -n 50`
- Verify Python path: `which python3`

### No classes found
- Verify website URL is accessible
- Check if page structure has changed
- Review HTML parsing logic in `scraper.py`

## Notes

- The scraper uses generic regex patterns for flexibility
- Adjust parsing logic if website structure changes
- Email notifications only sent when classes are available
- Logs are stored in `/var/log/nitro_swim_scraper.log`
