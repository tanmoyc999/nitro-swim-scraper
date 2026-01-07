# EC2 Deployment Guide - Step by Step

## Prerequisites
- AWS account with EC2 access
- EC2 instance running (t2.micro free tier recommended)
- Ubuntu 20.04 LTS or Amazon Linux 2
- SSH key pair (.pem file)
- Your local machine with SSH access

---

## Step 1: Launch EC2 Instance

### 1.1 Go to AWS Console
- Navigate to EC2 Dashboard
- Click "Launch Instances"

### 1.2 Configure Instance
- **AMI**: Ubuntu Server 20.04 LTS (free tier eligible)
- **Instance Type**: t2.micro (free tier)
- **Storage**: 20 GB (default is fine)
- **Security Group**: Allow SSH (port 22) from your IP

### 1.3 Create/Select Key Pair
- Create new key pair or use existing
- Download .pem file (save it safely)
- Set permissions: `chmod 400 your-key.pem`

### 1.4 Launch
- Click "Launch Instance"
- Wait for instance to be "running"
- Note the **Public IPv4 address** (e.g., 54.123.45.67)

---

## Step 2: Copy Project to EC2

### 2.1 From Your Local Machine
Open terminal and run:

```bash
# Replace with your actual IP and key path
scp -r nitro_swim_scraper/ ec2-user@54.123.45.67:/home/ec2-user/

# Or if using ubuntu user:
scp -r nitro_swim_scraper/ ubuntu@54.123.45.67:/home/ubuntu/
```

**What this does:**
- Copies entire `nitro_swim_scraper` folder to EC2
- Creates `/home/ec2-user/nitro_swim_scraper/` on the instance

### 2.2 Verify Copy
```bash
ssh -i your-key.pem ec2-user@54.123.45.67 "ls -la nitro_swim_scraper/"
```

Expected output:
```
config.py
nitro-swim.service
README.md
requirements.txt
scheduler.py
scraper.py
setup_ec2.sh
setup_local.sh
```

---

## Step 3: SSH into EC2 Instance

```bash
ssh -i your-key.pem ec2-user@54.123.45.67
```

You should see:
```
Welcome to Ubuntu 20.04.X LTS
...
ec2-user@ip-172-31-xx-xx:~$
```

---

## Step 4: Run Setup Script

### 4.1 Navigate to Project
```bash
cd nitro_swim_scraper
```

### 4.2 Make Script Executable
```bash
chmod +x setup_ec2.sh
```

### 4.3 Run Setup
```bash
./setup_ec2.sh
```

**What this script does:**
1. Updates system packages (`apt-get update`)
2. Installs Python3 and pip
3. Installs Python dependencies from requirements.txt
4. Creates log directory at `/var/log/nitro_swim`
5. Copies systemd service file
6. Enables the service (auto-start on reboot)
7. Starts the service

### 4.4 Expected Output
```
==========================================
Nitro Swim Scraper - EC2 Setup
==========================================
Updating system packages...
Installing Python3 and pip...
Installing Python dependencies...
Creating log directory...
Setting up systemd service...
Enabling service...
Starting service...

==========================================
Setup Complete!
==========================================

Service Status:
● nitro-swim.service - Nitro Swim Class Scraper
   Loaded: loaded (/etc/systemd/system/nitro-swim.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2026-01-03 20:15:00 UTC; 2s ago
   ...
```

---

## Step 5: Verify Service is Running

### 5.1 Check Service Status
```bash
sudo systemctl status nitro-swim.service
```

Expected output:
```
● nitro-swim.service - Nitro Swim Class Scraper
   Loaded: loaded (/etc/systemd/system/nitro-swim.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2026-01-03 20:15:00 UTC; 2s ago
   Main PID: 1234 (python3)
   Tasks: 5 (limit: 1024)
   Memory: 45.2M
   CGroup: /system.slice/nitro-swim.service
           └─1234 /usr/bin/python3 /home/ec2-user/nitro_swim_scraper/scheduler.py
```

### 5.2 View Logs
```bash
tail -f /var/log/nitro_swim_scraper.log
```

Expected output:
```
2026-01-03 20:15:00,123 - INFO - Starting scheduler - running every 60 minutes
2026-01-03 20:15:05,456 - INFO - ============================================================
2026-01-03 20:15:05,456 - INFO - Starting scheduled scraper job
2026-01-03 20:15:05,456 - INFO - ============================================================
2026-01-03 20:15:10,789 - INFO - Fetching page with Playwright: https://nitroswim.captyn.com/...
2026-01-03 20:15:15,012 - INFO - Page fetched successfully, HTML length: 62834
2026-01-03 20:15:15,012 - INFO - Found 'spot' in HTML content
2026-01-03 20:15:15,012 - INFO - Found 'TF' in HTML content
2026-01-03 20:15:15,014 - INFO - Found 3 'spots open' occurrences
2026-01-03 20:15:15,014 - INFO - Processing spot match 1: 2 spots at position 18870
2026-01-03 20:15:15,014 - INFO -   Found TF 1
2026-01-03 20:15:15,014 - INFO -   Successfully extracted class info
...
2026-01-03 20:15:20,345 - INFO - Email sent successfully
```

Press `Ctrl+C` to exit log view.

---

## Step 6: Verify Email Notifications

### 6.1 Check Email
- Check your email (tanmoyc999@gmail.com)
- Look for subject: "Nitro Swim - Available Classes"
- Should contain class details with times and available spots

### 6.2 If Email Not Received
Check logs for errors:
```bash
sudo journalctl -u nitro-swim.service -n 50
```

Common issues:
- Gmail app password incorrect
- 2FA not enabled on Gmail
- Firewall blocking SMTP (port 587)

---

## Step 7: Manage the Service

### 7.1 Stop Service
```bash
sudo systemctl stop nitro-swim.service
```

### 7.2 Start Service
```bash
sudo systemctl start nitro-swim.service
```

### 7.3 Restart Service
```bash
sudo systemctl restart nitro-swim.service
```

### 7.4 View Service Logs
```bash
sudo journalctl -u nitro-swim.service -f
```

### 7.5 Disable Auto-Start (if needed)
```bash
sudo systemctl disable nitro-swim.service
```

---

## Step 8: Monitor Continuous Operation

### 8.1 Check if Running Every Hour
The service runs every 60 minutes. To verify:

```bash
# View last 20 log entries
tail -20 /var/log/nitro_swim_scraper.log

# Watch logs in real-time
tail -f /var/log/nitro_swim_scraper.log
```

### 8.2 Expected Behavior
- Service starts automatically on EC2 reboot
- Runs scraper every 60 minutes
- Sends email only when classes are available
- Logs all activity to `/var/log/nitro_swim_scraper.log`

---

## Step 9: Troubleshooting

### Issue: Service Not Running
```bash
sudo systemctl status nitro-swim.service
sudo journalctl -u nitro-swim.service -n 50
```

### Issue: No Emails Received
```bash
# Check logs for email errors
grep -i "email\|smtp\|error" /var/log/nitro_swim_scraper.log

# Verify Gmail credentials in config.py
cat nitro_swim_scraper/config.py | grep -A 5 "EMAIL_CONFIG"
```

### Issue: High Memory Usage
- Playwright browser uses ~100-150MB
- Normal for this type of scraper
- t2.micro has 1GB RAM, should be fine

### Issue: Slow Performance
- First run takes longer (browser startup)
- Subsequent runs are faster
- Network latency to Nitro Swim website affects speed

---

## Step 10: Optional - Modify Configuration

### 10.1 Change Interval (e.g., every 30 minutes)
```bash
sudo nano nitro_swim_scraper/config.py
```

Find and change:
```python
SCHEDULER_CONFIG = {
    'interval_minutes': 30,  # Changed from 60
    ...
}
```

Save (Ctrl+X, Y, Enter) and restart:
```bash
sudo systemctl restart nitro-swim.service
```

### 10.2 Change Email Recipients
```bash
sudo nano nitro_swim_scraper/config.py
```

Find and change:
```python
EMAIL_CONFIG = {
    'recipient_email': 'your-new-email@gmail.com',
    ...
}
```

Restart service:
```bash
sudo systemctl restart nitro-swim.service
```

---

## Summary

Your EC2 instance is now:
✅ Running the Nitro Swim scraper continuously
✅ Checking for available classes every 60 minutes
✅ Sending email notifications when spots are available
✅ Auto-starting on instance reboot
✅ Logging all activity for monitoring

The service will run 24/7 on your free tier EC2 instance!

---

## Cost Estimate (Free Tier)
- EC2 t2.micro: FREE (750 hours/month)
- Data transfer: FREE (1GB/month outbound)
- Total monthly cost: $0 (within free tier limits)

---

## Need Help?

Check logs:
```bash
tail -f /var/log/nitro_swim_scraper.log
```

View service status:
```bash
sudo systemctl status nitro-swim.service
```

Restart service:
```bash
sudo systemctl restart nitro-swim.service
```
