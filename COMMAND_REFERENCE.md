# Command Reference - Copy & Paste Ready

## Prerequisites
- AWS account created
- EC2 instance launched (Ubuntu 20.04 LTS, t2.micro)
- SSH key downloaded and saved to `~/.ssh/nitro-swim-key.pem`
- Project copied to EC2

---

## Replace These Values

```
YOUR_IP = Your EC2 Public IPv4 address (e.g., 54.123.45.67)
YOUR_KEY = Path to your .pem file (e.g., ~/.ssh/nitro-swim-key.pem)
```

---

## SETUP COMMANDS (Run Once)

### 1. Set Key Permissions (Local Machine)
```bash
chmod 400 ~/.ssh/nitro-swim-key.pem
```

### 2. Copy Project to EC2 (Local Machine)
```bash
scp -r nitro_swim_scraper/ ec2-user@YOUR_IP:/home/ec2-user/
```

### 3. SSH into EC2 (Local Machine)
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP
```

### 4. Navigate to Project (On EC2)
```bash
cd nitro_swim_scraper
```

### 5. Make Setup Script Executable (On EC2)
```bash
chmod +x setup_ec2.sh
```

### 6. Run Setup Script (On EC2)
```bash
./setup_ec2.sh
```

### 7. Wait for Setup to Complete
- Takes about 5-10 minutes
- Watch for "Setup Complete!" message

---

## VERIFICATION COMMANDS (Run After Setup)

### Check Service Status
```bash
sudo systemctl status nitro-swim.service
```

### View Live Logs
```bash
tail -f /var/log/nitro_swim_scraper.log
```

### View Last 20 Log Lines
```bash
tail -20 /var/log/nitro_swim_scraper.log
```

### Search Logs for Errors
```bash
grep -i error /var/log/nitro_swim_scraper.log
```

### Check if Service is Running
```bash
sudo systemctl is-active nitro-swim.service
```

### View Service Details
```bash
sudo systemctl show nitro-swim.service
```

---

## MANAGEMENT COMMANDS (Ongoing)

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

### Enable Auto-Start (if disabled)
```bash
sudo systemctl enable nitro-swim.service
```

### Disable Auto-Start
```bash
sudo systemctl disable nitro-swim.service
```

### View Systemd Logs
```bash
sudo journalctl -u nitro-swim.service -f
```

### View Last 50 Systemd Logs
```bash
sudo journalctl -u nitro-swim.service -n 50
```

---

## CONFIGURATION COMMANDS

### Edit Configuration
```bash
cd nitro_swim_scraper
sudo nano config.py
```

**To save in nano:**
- Press `Ctrl+X`
- Press `Y`
- Press `Enter`

### View Configuration
```bash
cat config.py
```

### View Email Configuration
```bash
grep -A 5 "EMAIL_CONFIG" config.py
```

### View Scheduler Configuration
```bash
grep -A 5 "SCHEDULER_CONFIG" config.py
```

---

## REMOTE COMMANDS (From Local Machine)

### Check Status Remotely
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP "sudo systemctl status nitro-swim.service"
```

### View Logs Remotely
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP "tail -20 /var/log/nitro_swim_scraper.log"
```

### Restart Service Remotely
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP "sudo systemctl restart nitro-swim.service"
```

### Stop Service Remotely
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP "sudo systemctl stop nitro-swim.service"
```

### Start Service Remotely
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP "sudo systemctl start nitro-swim.service"
```

### Copy Logs to Local Machine
```bash
scp -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP:/var/log/nitro_swim_scraper.log ./nitro_swim_scraper.log
```

---

## TROUBLESHOOTING COMMANDS

### Check if Python is Installed
```bash
python3 --version
```

### Check if Dependencies are Installed
```bash
pip3 list | grep -E "requests|beautifulsoup4|playwright|schedule"
```

### Check Disk Space
```bash
df -h
```

### Check Memory Usage
```bash
free -h
```

### Check CPU Usage
```bash
top
```

### Check Network Connectivity
```bash
ping nitroswim.captyn.com
```

### Check if Port 587 (SMTP) is Accessible
```bash
telnet smtp.gmail.com 587
```

### View All Running Processes
```bash
ps aux | grep python
```

### Kill Process (if needed)
```bash
kill -9 PROCESS_ID
```

---

## LOG ANALYSIS COMMANDS

### Count Total Log Entries
```bash
wc -l /var/log/nitro_swim_scraper.log
```

### View Logs from Last Hour
```bash
tail -f /var/log/nitro_swim_scraper.log
```

### View Logs from Specific Date
```bash
grep "2026-01-03" /var/log/nitro_swim_scraper.log
```

### View Only Error Logs
```bash
grep -i "error\|failed\|exception" /var/log/nitro_swim_scraper.log
```

### View Only Success Logs
```bash
grep -i "success\|completed\|sent" /var/log/nitro_swim_scraper.log
```

### View Logs with Line Numbers
```bash
grep -n "email sent" /var/log/nitro_swim_scraper.log
```

### Count Successful Runs
```bash
grep -c "Email sent successfully" /var/log/nitro_swim_scraper.log
```

### Count Failed Runs
```bash
grep -c "Error\|Failed" /var/log/nitro_swim_scraper.log
```

---

## FILE MANAGEMENT COMMANDS

### List Project Files
```bash
ls -la nitro_swim_scraper/
```

### View File Sizes
```bash
du -sh nitro_swim_scraper/*
```

### View Log File Size
```bash
du -sh /var/log/nitro_swim_scraper.log
```

### Backup Log File
```bash
cp /var/log/nitro_swim_scraper.log /var/log/nitro_swim_scraper.log.backup
```

### Clear Log File (if too large)
```bash
sudo truncate -s 0 /var/log/nitro_swim_scraper.log
```

### View Project Directory Structure
```bash
tree nitro_swim_scraper/
```

---

## SYSTEM COMMANDS

### Reboot EC2 Instance
```bash
sudo reboot
```

### Shutdown EC2 Instance
```bash
sudo shutdown -h now
```

### Check System Uptime
```bash
uptime
```

### Check System Load
```bash
cat /proc/loadavg
```

### View System Information
```bash
uname -a
```

### Check Ubuntu Version
```bash
lsb_release -a
```

---

## EXIT AND DISCONNECT

### Exit SSH Session
```bash
exit
```

### Disconnect from EC2
```bash
logout
```

---

## QUICK TROUBLESHOOTING FLOW

### 1. Service Not Running?
```bash
sudo systemctl status nitro-swim.service
sudo systemctl restart nitro-swim.service
```

### 2. Check Logs for Errors
```bash
tail -50 /var/log/nitro_swim_scraper.log
grep -i error /var/log/nitro_swim_scraper.log
```

### 3. Check Email Configuration
```bash
grep -A 5 "EMAIL_CONFIG" config.py
```

### 4. Restart Service
```bash
sudo systemctl restart nitro-swim.service
```

### 5. Monitor Logs
```bash
tail -f /var/log/nitro_swim_scraper.log
```

---

## COMMON ISSUES & FIXES

### Issue: "Permission denied" when connecting
**Fix:**
```bash
chmod 400 ~/.ssh/nitro-swim-key.pem
```

### Issue: "Connection refused"
**Fix:**
```bash
# Check if instance is running in AWS Console
# Wait 2-3 minutes for instance to fully start
# Verify IP address is correct
```

### Issue: Service not starting
**Fix:**
```bash
sudo systemctl restart nitro-swim.service
sudo journalctl -u nitro-swim.service -n 50
```

### Issue: No emails received
**Fix:**
```bash
# Check logs
grep -i "email\|smtp" /var/log/nitro_swim_scraper.log

# Verify Gmail credentials in config.py
cat config.py | grep -A 5 "EMAIL_CONFIG"

# Check if 2FA is enabled on Gmail
# Check if app password is correct
```

### Issue: High memory usage
**Fix:**
```bash
# This is normal for Playwright
# Monitor with:
free -h
top
```

### Issue: Slow performance
**Fix:**
```bash
# First run is slower (browser startup)
# Subsequent runs are faster
# Monitor with:
tail -f /var/log/nitro_swim_scraper.log
```

---

## USEFUL ALIASES (Optional)

Add to your local `~/.bashrc` or `~/.zshrc`:

```bash
# EC2 Connection
alias ec2-connect="ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP"
alias ec2-logs="ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP 'tail -f /var/log/nitro_swim_scraper.log'"
alias ec2-status="ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP 'sudo systemctl status nitro-swim.service'"
alias ec2-restart="ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP 'sudo systemctl restart nitro-swim.service'"
```

Then use:
```bash
ec2-connect          # Connect to EC2
ec2-logs             # View logs
ec2-status           # Check status
ec2-restart          # Restart service
```

---

## Notes

- Replace `YOUR_IP` with your actual EC2 Public IPv4 address
- All commands assume you're using the default `ec2-user` (Ubuntu AMI)
- For Amazon Linux, use `ec2-user`; for Ubuntu, use `ubuntu`
- Commands with `sudo` require elevated privileges
- Log file location: `/var/log/nitro_swim_scraper.log`
- Service name: `nitro-swim.service`
- Config file: `~/nitro_swim_scraper/config.py`
