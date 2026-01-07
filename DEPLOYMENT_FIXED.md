# EC2 Deployment Guide - Fixed Version

## What Was Fixed

The previous deployment had several issues that prevented the service from running:

1. **Playwright browser dependencies missing** - Added system package installation
2. **Playwright browsers not installed** - Added `playwright install` step
3. **Incorrect log file path** - Updated to `/var/log/nitro_swim/`
4. **Service file logging configuration** - Fixed to write to correct log location
5. **Scheduler timezone handling** - Clarified UTC conversion for CST times

---

## Quick Start (If You Already Have an EC2 Instance)

If you already have an Ubuntu instance running, SSH into it and run:

```bash
cd nitro_swim_scraper
chmod +x setup_ec2.sh
./setup_ec2.sh
```

The script will now:
- Install all system dependencies for Playwright
- Install Python packages
- Install Playwright browsers
- Set up the systemd service
- Start the service automatically

---

## Complete Fresh Deployment (From Scratch)

### Step 1: Create EC2 Instance

1. Go to AWS Console → EC2 Dashboard
2. Click "Launch instances"
3. Select: **Ubuntu Server 20.04 LTS** (Free tier eligible)
4. Instance type: **t2.micro** (Free tier eligible)
5. Create/select key pair: `nitro-swim-key`
6. Create/select security group: Allow SSH (port 22)
7. Storage: 20 GB (default)
8. Launch instance

### Step 2: Wait for Instance to Start

- Wait for "Instance State" = "running"
- Wait for "Status checks" = "2/2 checks passed"
- Copy the "Public IPv4 address"

### Step 3: Connect to EC2

```bash
ssh -i ~/.ssh/nitro-swim-key.pem ubuntu@18.117.154.7
```

### Step 4: Copy Project to EC2

From your local machine (in a new terminal):

```bash
scp -r nitro_swim_scraper/ ubuntu@18.117.154.7:/home/ubuntu/
```

### Step 5: Run Setup Script

Back in your SSH session:

```bash
cd nitro_swim_scraper
chmod +x setup_ec2.sh
./setup_ec2.sh
```

**This will take 5-10 minutes.** Wait for "Setup Complete!" message.

### Step 6: Verify Service is Running

```bash
sudo systemctl status nitro-swim.service
```

You should see:
```
● nitro-swim.service - Nitro Swim Class Scraper
   Loaded: loaded (/etc/systemd/system/nitro-swim.service; enabled; vendor preset: enabled)
   Active: active (running) since ...
```

### Step 7: Check Logs

```bash
tail -f /var/log/nitro_swim/nitro_swim_scraper.log
```

You should see:
```
2026-01-04 03:40:00,123 - INFO - Starting scheduler with specific times (UTC):
2026-01-04 03:40:00,124 - INFO -   - 02:00 UTC
2026-01-04 03:40:00,125 - INFO -   - 04:00 UTC
...
2026-01-04 03:40:00,131 - INFO - Scheduler started. Waiting for scheduled times...
```

Press `Ctrl+C` to exit logs.

### Step 8: Wait for First Scheduled Run

The service will run at these times (UTC):
- 02:00 UTC (8 PM CST)
- 04:00 UTC (10 PM CST)
- 05:00 UTC (11 PM CST)
- 06:00 UTC (12 AM CST)
- 20:00 UTC (2 PM CST)
- 21:00 UTC (3 PM CST)
- 23:00 UTC (5 PM CST)

When a scheduled time arrives, you'll see in logs:
```
2026-01-04 06:00:00,123 - INFO - ============================================================
2026-01-04 06:00:00,124 - INFO - Starting scheduled scraper job
2026-01-04 06:00:00,125 - INFO - ============================================================
2026-01-04 06:00:05,456 - INFO - Fetching page with Playwright: https://nitroswim.captyn.com/...
2026-01-04 06:00:10,789 - INFO - Page fetched successfully, HTML length: 45678
2026-01-04 06:00:10,790 - INFO - Found 3 'spots open' occurrences
2026-01-04 06:00:10,791 - INFO - Extracted 3 available classes
2026-01-04 06:00:10,792 - INFO - Sending email to tanmoyc999@gmail.com
2026-01-04 06:00:12,345 - INFO - Email sent successfully
2026-01-04 06:00:12,346 - INFO - Job completed successfully with email notification
```

### Step 9: Check Email

Go to Gmail: https://mail.gmail.com
Sign in with: tanmoyc999@gmail.com

You should receive an email with subject: `Nitro Swim - Available Classes (2026-01-04 06:00)`

---

## Troubleshooting

### Problem: Service shows "activating (auto-restart)"

**Cause:** Service is crashing. Check logs:

```bash
tail -50 /var/log/nitro_swim/nitro_swim_scraper.log
```

**Common issues:**
- Playwright dependencies still missing
- Python packages not installed
- Virtual environment not created

**Solution:** Run setup script again:

```bash
./setup_ec2.sh
```

### Problem: "No such file or directory" for log file

**Cause:** Log directory doesn't exist.

**Solution:**

```bash
sudo mkdir -p /var/log/nitro_swim
sudo chown ubuntu:ubuntu /var/log/nitro_swim
sudo systemctl restart nitro-swim.service
```

### Problem: "Permission denied" when SSH

**Cause:** Key permissions wrong or wrong key.

**Solution:**

```bash
# Check key permissions (should be -r-------)
ls -la ~/.ssh/nitro-swim-key.pem

# Fix if needed
chmod 400 ~/.ssh/nitro-swim-key.pem

# Try SSH again
ssh -i ~/.ssh/nitro-swim-key.pem ubuntu@YOUR_IP
```

### Problem: Playwright still failing

**Cause:** Browser dependencies not installed.

**Solution:**

```bash
# Install dependencies manually
sudo apt-get install -y \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2t64

# Install Playwright browsers
python3 -m playwright install

# Restart service
sudo systemctl restart nitro-swim.service
```

### Problem: No emails received

**Cause:** Gmail credentials wrong or 2FA enabled.

**Solution:**

1. Check credentials in config.py:
   ```bash
   cat config.py | grep -A 5 "EMAIL_CONFIG"
   ```

2. Verify Gmail app password is correct:
   - Go to https://myaccount.google.com/apppasswords
   - Generate new app password if needed
   - Update in config.py

3. Restart service:
   ```bash
   sudo systemctl restart nitro-swim.service
   ```

---

## Useful Commands

### Check Service Status

```bash
sudo systemctl status nitro-swim.service
```

### View Logs (Last 50 lines)

```bash
tail -50 /var/log/nitro_swim/nitro_swim_scraper.log
```

### View Logs (Real-time)

```bash
tail -f /var/log/nitro_swim/nitro_swim_scraper.log
```

### Restart Service

```bash
sudo systemctl restart nitro-swim.service
```

### Stop Service

```bash
sudo systemctl stop nitro-swim.service
```

### Start Service

```bash
sudo systemctl start nitro-swim.service
```

### View Service Logs (systemd)

```bash
sudo journalctl -u nitro-swim.service -f
```

### Check if Service Auto-starts on Reboot

```bash
sudo systemctl is-enabled nitro-swim.service
```

Should show: `enabled`

---

## Verification Checklist

- [ ] EC2 instance created and running
- [ ] SSH connection works
- [ ] Project copied to EC2
- [ ] Setup script executed successfully
- [ ] Service shows "active (running)"
- [ ] Logs show "Scheduler started"
- [ ] First scheduled run completes
- [ ] Email received in inbox
- [ ] Service auto-starts on reboot

---

## What Happens Now

✅ Service runs automatically 24/7
✅ Checks Nitro Swim at scheduled times
✅ Sends email when classes available
✅ Auto-restarts if it crashes
✅ Auto-starts on EC2 reboot
✅ Costs $0/month (free tier)

---

## Can You Turn Off Your Mac?

**YES!** The service runs on EC2, not your Mac. You can:
- Close your laptop
- Shut down your Mac
- Unplug your Mac
- Go on vacation

The scraper will continue running 24/7 on AWS EC2.

---

## Monitoring from Your Mac

You can check the service anytime from your Mac:

```bash
# Check status
ssh -i ~/.ssh/nitro-swim-key.pem ubuntu@18.117.154.7 "sudo systemctl status nitro-swim.service"

# View recent logs
ssh -i ~/.ssh/nitro-swim-key.pem ubuntu@18.117.154.7 "tail -20 /var/log/nitro_swim/nitro_swim_scraper.log"

# View real-time logs
ssh -i ~/.ssh/nitro-swim-key.pem ubuntu@18.117.154.7 "tail -f /var/log/nitro_swim/nitro_swim_scraper.log"
```

---

## Next Steps

1. Follow the "Complete Fresh Deployment" steps above
2. Wait for first scheduled run
3. Check email for notification
4. Monitor logs for a few days
5. Enjoy automatic class notifications!

Good luck! 🚀
