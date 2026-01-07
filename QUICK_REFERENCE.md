# Quick Reference - EC2 Deployment

## TL;DR - 5 Steps to Deploy

### Step 1: Create EC2 Instance
- AWS Console → EC2 → Launch instances
- Ubuntu 20.04 LTS, t2.micro, free tier
- Key pair: `nitro-swim-key`
- Security group: Allow SSH

### Step 2: Copy Project
```bash
scp -r nitro_swim_scraper/ ubuntu@YOUR_IP:/home/ubuntu/
```

### Step 3: SSH Into EC2
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ubuntu@YOUR_IP
```

### Step 4: Run Setup
```bash
cd nitro_swim_scraper
chmod +x setup_ec2.sh
./setup_ec2.sh
```

### Step 5: Verify
```bash
sudo systemctl status nitro-swim.service
tail -f /var/log/nitro_swim/nitro_swim_scraper.log
```

---

## Scheduled Run Times (UTC)

| UTC Time | CST Time |
|----------|----------|
| 02:00    | 8 PM     |
| 04:00    | 10 PM    |
| 05:00    | 11 PM    |
| 06:00    | 12 AM    |
| 20:00    | 2 PM     |
| 21:00    | 3 PM     |
| 23:00    | 5 PM     |

---

## Common Commands

```bash
# Check service status
sudo systemctl status nitro-swim.service

# View logs (last 50 lines)
tail -50 /var/log/nitro_swim/nitro_swim_scraper.log

# View logs (real-time)
tail -f /var/log/nitro_swim/nitro_swim_scraper.log

# Restart service
sudo systemctl restart nitro-swim.service

# Stop service
sudo systemctl stop nitro-swim.service

# Start service
sudo systemctl start nitro-swim.service
```

---

## Remote Commands (From Your Mac)

```bash
# Check status
ssh -i ~/.ssh/nitro-swim-key.pem ubuntu@18.117.154.7 "sudo systemctl status nitro-swim.service"

# View logs
ssh -i ~/.ssh/nitro-swim-key.pem ubuntu@18.117.154.7 "tail -20 /var/log/nitro_swim/nitro_swim_scraper.log"

# Restart service
ssh -i ~/.ssh/nitro-swim-key.pem ubuntu@18.117.154.7 "sudo systemctl restart nitro-swim.service"
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Service not running | `./setup_ec2.sh` then `sudo systemctl restart nitro-swim.service` |
| Permission denied SSH | `chmod 400 ~/.ssh/nitro-swim-key.pem` |
| No emails | Check `config.py` Gmail credentials |
| Playwright error | `sudo apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2t64` |

---

## Key Files

- `setup_ec2.sh` - Automated setup script
- `scheduler.py` - Runs scraper at scheduled times
- `scraper.py` - Fetches and parses classes
- `config.py` - Email and scheduler settings
- `nitro-swim.service` - Systemd service file

---

## Important Notes

✅ Service runs 24/7 on EC2
✅ Auto-restarts if it crashes
✅ Auto-starts on EC2 reboot
✅ You can turn off your Mac
✅ Costs $0/month (free tier)
✅ Emails sent to tanmoyc999@gmail.com

---

## Need Help?

1. Check logs: `tail -f /var/log/nitro_swim/nitro_swim_scraper.log`
2. Read `DEPLOYMENT_FIXED.md` for detailed troubleshooting
3. Verify service: `sudo systemctl status nitro-swim.service`
