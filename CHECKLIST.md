# EC2 Deployment Checklist

## Pre-Deployment Checklist

### AWS Account Setup
- [ ] AWS account created
- [ ] Payment method added
- [ ] Email verified

### Local Machine Preparation
- [ ] Project folder exists: `nitro_swim_scraper/`
- [ ] All files present:
  - [ ] `scraper.py`
  - [ ] `scheduler.py`
  - [ ] `config.py`
  - [ ] `requirements.txt`
  - [ ] `setup_ec2.sh`
  - [ ] `nitro-swim.service`
  - [ ] `README.md`
- [ ] SSH key downloaded: `nitro-swim-key.pem`
- [ ] SSH key saved to: `~/.ssh/nitro-swim-key.pem`
- [ ] SSH key permissions set: `chmod 400 ~/.ssh/nitro-swim-key.pem`

---

## EC2 Instance Setup Checklist

### Launch Instance
- [ ] Go to AWS EC2 Dashboard
- [ ] Click "Launch Instance"
- [ ] Name: `nitro-swim-scraper`
- [ ] AMI: Ubuntu Server 20.04 LTS
- [ ] Instance Type: t2.micro
- [ ] Key Pair: `nitro-swim-key`
- [ ] Security Group: Allow SSH (port 22)
- [ ] Storage: 20 GB
- [ ] Click "Launch Instance"

### Wait for Instance
- [ ] Instance State: "running" ✅
- [ ] Status Checks: "2/2 checks passed" ✅
- [ ] Public IPv4 Address: Visible ✅
- [ ] Note the IP address: `_________________`

---

## File Transfer Checklist

### Copy Project to EC2
- [ ] Open Terminal on local machine
- [ ] Run: `scp -r nitro_swim_scraper/ ec2-user@YOUR_IP:/home/ec2-user/`
- [ ] Wait for copy to complete
- [ ] Verify: `ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP "ls -la nitro_swim_scraper/"`
- [ ] All files visible ✅

---

## SSH Connection Checklist

### Connect to EC2
- [ ] Open Terminal
- [ ] Run: `ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP`
- [ ] Accept fingerprint: Type "yes"
- [ ] Connected to EC2 ✅
- [ ] Prompt shows: `ec2-user@ip-xxx:~$`

### Navigate to Project
- [ ] Run: `cd nitro_swim_scraper`
- [ ] Run: `ls -la`
- [ ] All files visible ✅

---

## Setup Script Execution Checklist

### Prepare Setup
- [ ] Run: `chmod +x setup_ec2.sh`
- [ ] Verify: `ls -la setup_ec2.sh` shows `x` permission ✅

### Run Setup
- [ ] Run: `./setup_ec2.sh`
- [ ] Watch for progress messages:
  - [ ] "Updating system packages..."
  - [ ] "Installing Python3 and pip..."
  - [ ] "Installing Python dependencies..."
  - [ ] "Creating log directory..."
  - [ ] "Setting up systemd service..."
  - [ ] "Enabling service..."
  - [ ] "Starting service..."
- [ ] Wait for "Setup Complete!" message ✅
- [ ] Setup took approximately: 5-10 minutes

---

## Verification Checklist

### Check Service Status
- [ ] Run: `sudo systemctl status nitro-swim.service`
- [ ] Status shows: "active (running)" ✅
- [ ] Loaded shows: "enabled" ✅
- [ ] No errors visible ✅

### Check Logs
- [ ] Run: `tail -f /var/log/nitro_swim_scraper.log`
- [ ] Logs show:
  - [ ] "Starting scheduler - running every 60 minutes"
  - [ ] "Starting scheduled scraper job"
  - [ ] "Fetching page with Playwright"
  - [ ] "Page fetched successfully"
  - [ ] "Found X 'spots open' occurrences"
  - [ ] "Processing spot match"
  - [ ] "Found TF X"
  - [ ] "Successfully extracted class info"
  - [ ] "Sending email to tanmoyc999@gmail.com"
  - [ ] "Email sent successfully"
- [ ] No error messages ✅
- [ ] Exit logs: Press `Ctrl+C`

### Check Email
- [ ] Open Gmail: https://mail.google.com
- [ ] Sign in: tanmoyc999@gmail.com
- [ ] Check Inbox
- [ ] Email received with subject: "Nitro Swim - Available Classes" ✅
- [ ] Email contains:
  - [ ] Class numbers (TF 1, TF 4, TF 5, etc.)
  - [ ] Days (M, W, Tu, Th, etc.)
  - [ ] Times (4:05 pm-4:50 pm, etc.)
  - [ ] Available spots (1, 2, etc.)
  - [ ] Location (Nitro Swimming Cedar Park)

---

## Post-Deployment Checklist

### Verify Auto-Start
- [ ] Run: `sudo systemctl is-enabled nitro-swim.service`
- [ ] Output: "enabled" ✅

### Verify Continuous Operation
- [ ] Wait 5 minutes
- [ ] Run: `tail -20 /var/log/nitro_swim_scraper.log`
- [ ] New log entries visible ✅

### Disconnect from EC2
- [ ] Run: `exit`
- [ ] Back on local machine ✅

---

## Ongoing Monitoring Checklist (Daily)

### Daily Check
- [ ] Check email for new notifications
- [ ] Run: `ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP "sudo systemctl status nitro-swim.service"`
- [ ] Status: "active (running)" ✅
- [ ] Run: `ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP "tail -20 /var/log/nitro_swim_scraper.log"`
- [ ] Recent logs show successful runs ✅

### Weekly Check
- [ ] Verify service still running
- [ ] Check for any error messages in logs
- [ ] Verify emails still being received
- [ ] Check EC2 instance health in AWS Console

### Monthly Check
- [ ] Review logs for patterns
- [ ] Check if any configuration changes needed
- [ ] Verify email recipient still correct
- [ ] Check if interval needs adjustment

---

## Troubleshooting Checklist

### If Service Not Running
- [ ] SSH into EC2
- [ ] Run: `sudo systemctl status nitro-swim.service`
- [ ] Check error message
- [ ] Run: `sudo systemctl restart nitro-swim.service`
- [ ] Wait 30 seconds
- [ ] Run: `sudo systemctl status nitro-swim.service` again
- [ ] Status: "active (running)" ✅

### If No Emails Received
- [ ] Check logs: `grep -i "email\|error" /var/log/nitro_swim_scraper.log`
- [ ] Verify Gmail credentials in config.py
- [ ] Check if 2FA enabled on Gmail
- [ ] Verify app password is correct
- [ ] Check if SMTP port 587 accessible
- [ ] Restart service: `sudo systemctl restart nitro-swim.service`

### If High Memory Usage
- [ ] This is normal (Playwright uses 100-150MB)
- [ ] Monitor with: `free -h`
- [ ] t2.micro has 1GB RAM (sufficient)
- [ ] No action needed

### If Slow Performance
- [ ] First run is slower (browser startup)
- [ ] Subsequent runs are faster
- [ ] Check network connectivity: `ping nitroswim.captyn.com`
- [ ] Monitor logs: `tail -f /var/log/nitro_swim_scraper.log`

---

## Configuration Changes Checklist

### Change Check Interval
- [ ] SSH into EC2
- [ ] Run: `cd nitro_swim_scraper`
- [ ] Run: `sudo nano config.py`
- [ ] Find: `'interval_minutes': 60,`
- [ ] Change to desired interval (e.g., 30)
- [ ] Save: `Ctrl+X`, `Y`, `Enter`
- [ ] Restart: `sudo systemctl restart nitro-swim.service`
- [ ] Verify: `sudo systemctl status nitro-swim.service`

### Change Email Recipient
- [ ] SSH into EC2
- [ ] Run: `cd nitro_swim_scraper`
- [ ] Run: `sudo nano config.py`
- [ ] Find: `'recipient_email': 'tanmoyc999@gmail.com',`
- [ ] Change to new email
- [ ] Save: `Ctrl+X`, `Y`, `Enter`
- [ ] Restart: `sudo systemctl restart nitro-swim.service`
- [ ] Verify: `sudo systemctl status nitro-swim.service`

---

## Maintenance Checklist

### Monthly Maintenance
- [ ] Check log file size: `du -sh /var/log/nitro_swim_scraper.log`
- [ ] If > 100MB, backup and clear:
  - [ ] `cp /var/log/nitro_swim_scraper.log /var/log/nitro_swim_scraper.log.backup`
  - [ ] `sudo truncate -s 0 /var/log/nitro_swim_scraper.log`
- [ ] Check disk space: `df -h`
- [ ] Verify service still enabled: `sudo systemctl is-enabled nitro-swim.service`

### Quarterly Maintenance
- [ ] Review logs for patterns
- [ ] Check if any updates needed
- [ ] Verify email notifications still working
- [ ] Test manual run: `python3 scraper.py`

---

## Decommissioning Checklist (if needed)

### Stop Service
- [ ] SSH into EC2
- [ ] Run: `sudo systemctl stop nitro-swim.service`
- [ ] Run: `sudo systemctl disable nitro-swim.service`
- [ ] Verify: `sudo systemctl status nitro-swim.service` shows "inactive"

### Backup Data
- [ ] Copy logs to local machine:
  - [ ] `scp -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP:/var/log/nitro_swim_scraper.log ./backup/`
- [ ] Copy config:
  - [ ] `scp -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP:/home/ec2-user/nitro_swim_scraper/config.py ./backup/`

### Terminate Instance
- [ ] Go to AWS EC2 Console
- [ ] Select instance
- [ ] Click "Instance State" → "Terminate instance"
- [ ] Confirm termination
- [ ] Instance deleted ✅

---

## Success Criteria

✅ All items checked = Successful Deployment!

Your EC2 instance is now:
- Running 24/7
- Checking for available classes every 60 minutes
- Sending email notifications when spots available
- Auto-starting on reboot
- Logging all activity
- Costing $0 (free tier)

---

## Quick Reference

| Item | Value |
|------|-------|
| Instance Type | t2.micro |
| OS | Ubuntu 20.04 LTS |
| Service Name | nitro-swim.service |
| Log Location | /var/log/nitro_swim_scraper.log |
| Check Interval | 60 minutes |
| Email Recipient | tanmoyc999@gmail.com |
| Cost | FREE (free tier) |
| Uptime | 24/7 |

---

## Support

If something goes wrong:
1. Check logs: `tail -f /var/log/nitro_swim_scraper.log`
2. Check service: `sudo systemctl status nitro-swim.service`
3. Restart: `sudo systemctl restart nitro-swim.service`
4. Review DETAILED_STEPS.md for troubleshooting
5. Review COMMAND_REFERENCE.md for commands
