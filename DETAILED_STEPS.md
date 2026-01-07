# Detailed Step-by-Step EC2 Deployment Guide

## PART 1: AWS SETUP

---

## Step 1: Create AWS Account (if you don't have one)

### 1.1 Go to AWS
- Open browser: https://aws.amazon.com
- Click "Create an AWS Account"
- Enter email, password, account name
- Add payment method (won't be charged for free tier)
- Verify phone number
- Choose "Basic Support" (free)

### 1.2 Verify Email
- Check your email for AWS verification link
- Click the link to activate account

---

## Step 2: Access EC2 Dashboard

### 2.1 Sign In
- Go to https://console.aws.amazon.com
- Sign in with your email and password

### 2.2 Navigate to EC2
- In the search bar at top, type "EC2"
- Click "EC2" from dropdown
- You're now in EC2 Dashboard

### 2.3 Check Region
- Look at top-right corner
- Select a region close to you (e.g., us-east-1, us-west-2)
- All free tier instances work the same

---

## Step 3: Launch EC2 Instance

### 3.1 Click "Launch Instance"
- In EC2 Dashboard, click orange "Launch Instance" button
- You'll see "Launch an instance" page

### 3.2 Name Your Instance
- Under "Name and tags" section
- Type: `nitro-swim-scraper`
- This helps you identify it later

### 3.3 Choose Operating System (AMI)

**What you see:**
- List of operating systems
- Ubuntu, Amazon Linux, Windows, etc.

**What to do:**
- Look for "Ubuntu Server 20.04 LTS"
- Click on it
- You should see "Free tier eligible" label

**Why Ubuntu 20.04?**
- Free tier eligible
- Widely supported
- Easy to use
- All our scripts work on it

### 3.4 Choose Instance Type

**What you see:**
- List of instance types: t2.micro, t2.small, t3.micro, etc.

**What to do:**
- Select "t2.micro"
- You should see "Free tier eligible" label

**Why t2.micro?**
- 1 GB RAM (enough for our scraper)
- 1 vCPU (enough for our needs)
- FREE for 750 hours/month
- Perfect for this project

### 3.5 Create Key Pair

**What you see:**
- "Key pair (login)" section
- Dropdown showing "Create new key pair"

**What to do:**
1. Click "Create new key pair"
2. A dialog appears
3. Enter name: `nitro-swim-key`
4. Keep "RSA" selected
5. Keep ".pem" format selected
6. Click "Create key pair"

**What happens:**
- File `nitro-swim-key.pem` downloads to your computer
- **IMPORTANT**: Save this file safely! You need it to access EC2.
- Don't share this file with anyone

**Where to save:**
- Create folder: `~/.ssh/` (in your home directory)
- Move the .pem file there
- Run: `chmod 400 ~/.ssh/nitro-swim-key.pem`

### 3.6 Configure Security Group (Firewall)

**What you see:**
- "Network settings" section
- "Firewall (security group)" options

**What to do:**
1. Click "Create security group"
2. Name: `nitro-swim-sg`
3. Description: `Security group for Nitro Swim scraper`
4. Under "Inbound rules", you should see:
   - Type: SSH
   - Port: 22
   - Source: 0.0.0.0/0 (or your IP for more security)

**Why SSH?**
- Allows you to connect to the instance
- Port 22 is standard for SSH

**Security note:**
- For production, restrict source to your IP only
- For now, 0.0.0.0/0 is fine (free tier)

### 3.7 Storage Configuration

**What you see:**
- "Configure storage" section
- Default: 20 GB

**What to do:**
- Keep default (20 GB)
- This is enough for our scraper

### 3.8 Review and Launch

**What you see:**
- Summary of your configuration
- t2.micro, Ubuntu 20.04, 20GB storage, etc.

**What to do:**
1. Review everything
2. Click orange "Launch instance" button
3. Wait for confirmation

**What happens:**
- Instance starts launching
- You see "Launch Status" page
- Click "View all instances" or "Instances" in left menu

---

## Step 4: Wait for Instance to Start

### 4.1 View Instances
- Go to EC2 Dashboard → Instances
- You should see your instance: `nitro-swim-scraper`

### 4.2 Check Status
- Look at "Instance State" column
- Wait for it to change from "pending" to "running"
- This takes 30-60 seconds

### 4.3 Get Public IP Address
- Once "running", look at "Public IPv4 address" column
- Copy this IP (e.g., `54.123.45.67`)
- **You'll need this IP to connect**

### 4.4 Wait for System Status
- Look at "Status checks" column
- Wait for it to show "2/2 checks passed"
- This means the instance is fully ready
- Takes about 2-3 minutes

---

## PART 2: PREPARE YOUR LOCAL MACHINE

---

## Step 5: Set Up SSH Key on Your Computer

### 5.1 Open Terminal

**On macOS:**
- Press Cmd + Space
- Type "Terminal"
- Press Enter

**On Windows:**
- Use PowerShell or Git Bash
- Or use PuTTY (download separately)

### 5.2 Set Key Permissions

```bash
chmod 400 ~/.ssh/nitro-swim-key.pem
```

**What this does:**
- Makes the key file readable only by you
- Required for SSH security

**Verify:**
```bash
ls -la ~/.ssh/nitro-swim-key.pem
```

You should see:
```
-r--------  1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem
```

---

## Step 6: Prepare Project Files

### 6.1 Verify Project Structure

On your local machine, check you have:
```
nitro_swim_scraper/
├── scraper.py
├── scheduler.py
├── config.py
├── requirements.txt
├── setup_ec2.sh
├── nitro-swim.service
├── README.md
├── DEPLOYMENT_GUIDE.md
└── QUICK_START.md
```

### 6.2 Verify Files Exist

```bash
ls -la nitro_swim_scraper/
```

You should see all files listed above.

---

## PART 3: COPY PROJECT TO EC2

---

## Step 7: Copy Files to EC2

### 7.1 Get Your EC2 IP Address
- From AWS Console, copy the "Public IPv4 address"
- Example: `54.123.45.67`

### 7.2 Copy Project

**Open Terminal on your local machine:**

```bash
scp -r nitro_swim_scraper/ ec2-user@54.123.45.67:/home/ec2-user/
```

**Replace `54.123.45.67` with your actual IP address**

**What this command does:**
- `scp` = secure copy
- `-r` = recursive (copy entire folder)
- `nitro_swim_scraper/` = source folder on your computer
- `ec2-user@54.123.45.67` = destination user and IP
- `:/home/ec2-user/` = destination path on EC2

### 7.3 Enter Key Passphrase (if prompted)
- If you set a passphrase when creating the key, enter it
- Otherwise, it connects directly

### 7.4 Wait for Copy to Complete

**Expected output:**
```
scraper.py                                    100%  5.2KB   2.1MB/s   00:00
scheduler.py                                  100%  2.1KB   1.5MB/s   00:00
config.py                                     100%  1.2KB   1.0MB/s   00:00
requirements.txt                              100%  0.2KB   0.2MB/s   00:00
setup_ec2.sh                                  100%  1.8KB   1.2MB/s   00:00
nitro-swim.service                            100%  0.3KB   0.3MB/s   00:00
README.md                                     100%  4.5KB   2.0MB/s   00:00
DEPLOYMENT_GUIDE.md                           100%  8.2KB   3.0MB/s   00:00
QUICK_START.md                                100%  2.1KB   1.5MB/s   00:00
```

### 7.5 Verify Copy Was Successful

```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67 "ls -la nitro_swim_scraper/"
```

**Expected output:**
```
total 48
drwxr-xr-x  9 ec2-user ec2-user  288 Jan  3 20:15 .
drwxr-xr-x  3 ec2-user ec2-user   96 Jan  3 20:14 ..
-rw-r--r--  1 ec2-user ec2-user 5234 Jan  3 20:15 scraper.py
-rw-r--r--  1 ec2-user ec2-user 2145 Jan  3 20:15 scheduler.py
-rw-r--r--  1 ec2-user ec2-user 1234 Jan  3 20:15 config.py
-rw-r--r--  1 ec2-user ec2-user  234 Jan  3 20:15 requirements.txt
-rwxr-xr-x  1 ec2-user ec2-user 1823 Jan  3 20:15 setup_ec2.sh
-rw-r--r--  1 ec2-user ec2-user  345 Jan  3 20:15 nitro-swim.service
-rw-r--r--  1 ec2-user ec2-user 4567 Jan  3 20:15 README.md
```

---

## PART 4: CONNECT TO EC2 AND RUN SETUP

---

## Step 8: SSH into EC2 Instance

### 8.1 Open Terminal

```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67
```

**Replace `54.123.45.67` with your actual IP**

### 8.2 First Connection Warning

**You'll see:**
```
The authenticity of host '54.123.45.67 (54.123.45.67)' can't be established.
ECDSA key fingerprint is SHA256:xxxxx...
Are you sure you want to continue connecting (yes/no)?
```

**What to do:**
- Type: `yes`
- Press Enter

### 8.3 Connected!

**You should see:**
```
Welcome to Ubuntu 20.04.X LTS (GNU/Linux 5.10.0-1234-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Fri Jan 03 20:20:00 UTC 2026

  System load:  0.00              Processes:             95
  Usage of /:   2.1% of 19.21GB   Users logged in:       0
  Memory usage: 5%                IP address for eth0:   172.31.xx.xx
  Swap usage:   0%

ec2-user@ip-172-31-xx-xx:~$
```

**You're now connected to your EC2 instance!**

---

## Step 9: Navigate to Project

### 9.1 Go to Project Directory

```bash
cd nitro_swim_scraper
```

### 9.2 Verify Files

```bash
ls -la
```

**You should see:**
```
total 48
-rw-r--r--  1 ec2-user ec2-user 5234 Jan  3 20:15 scraper.py
-rw-r--r--  1 ec2-user ec2-user 2145 Jan  3 20:15 scheduler.py
-rw-r--r--  1 ec2-user ec2-user 1234 Jan  3 20:15 config.py
-rw-r--r--  1 ec2-user ec2-user  234 Jan  3 20:15 requirements.txt
-rwxr-xr-x  1 ec2-user ec2-user 1823 Jan  3 20:15 setup_ec2.sh
-rw-r--r--  1 ec2-user ec2-user  345 Jan  3 20:15 nitro-swim.service
```

---

## Step 10: Make Setup Script Executable

### 10.1 Add Execute Permission

```bash
chmod +x setup_ec2.sh
```

### 10.2 Verify

```bash
ls -la setup_ec2.sh
```

**You should see:**
```
-rwxr-xr-x  1 ec2-user ec2-user 1823 Jan  3 20:15 setup_ec2.sh
```

**The `x` means it's executable**

---

## Step 11: Run Setup Script

### 11.1 Execute Setup

```bash
./setup_ec2.sh
```

### 11.2 What Happens (Step by Step)

**1. System Update (takes 30-60 seconds)**
```
Updating system packages...
Hit:1 http://archive.ubuntu.com/ubuntu focal InRelease
Get:2 http://archive.ubuntu.com/ubuntu focal-updates InRelease
...
```

**2. Install Python (takes 20-30 seconds)**
```
Installing Python3 and pip...
Reading package lists... Done
Building dependency tree
...
Setting up python3-pip (20.0.2-5ubuntu1.9) ...
```

**3. Install Dependencies (takes 2-3 minutes)**
```
Installing Python dependencies...
Collecting requests==2.31.0
  Downloading requests-2.31.0-py3-none-any.whl (62 kB)
Collecting beautifulsoup4==4.12.2
  Downloading beautifulsoup4-4.12.2-py3-none-any.whl (142 kB)
Collecting playwright==1.40.0
  Downloading playwright-1.40.0-py3-none-macosx_11_0_arm64.whl (32.5 MB)
...
Successfully installed requests beautifulsoup4 lxml schedule playwright
```

**4. Create Log Directory**
```
Creating log directory...
```

**5. Setup Systemd Service**
```
Setting up systemd service...
```

**6. Enable Service**
```
Enabling service...
Created symlink /etc/systemd/system/multi-user.target.wants/nitro-swim.service → /etc/systemd/system/nitro-swim.service.
```

**7. Start Service**
```
Starting service...
```

### 11.3 Setup Complete!

**You should see:**
```
==========================================
Setup Complete!
==========================================

Service Status:
● nitro-swim.service - Nitro Swim Class Scraper
   Loaded: loaded (/etc/systemd/system/nitro-swim.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2026-01-03 20:25:00 UTC; 2s ago
   Main PID: 1234 (python3)
   Tasks: 5 (limit: 1024)
   Memory: 45.2M
   CGroup: /system.slice/nitro-swim.service
           └─1234 /usr/bin/python3 /home/ec2-user/nitro_swim_scraper/scheduler.py

To view logs:
  tail -f /var/log/nitro_swim_scraper.log

To check service status:
  sudo systemctl status nitro-swim.service

To stop the service:
  sudo systemctl stop nitro-swim.service
```

---

## PART 5: VERIFY EVERYTHING IS WORKING

---

## Step 12: Check Service Status

### 12.1 View Service Status

```bash
sudo systemctl status nitro-swim.service
```

**Expected output:**
```
● nitro-swim.service - Nitro Swim Class Scraper
   Loaded: loaded (/etc/systemd/system/nitro-swim.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2026-01-03 20:25:00 UTC; 2m 30s ago
   Main PID: 1234 (python3)
   Tasks: 5 (limit: 1024)
   Memory: 45.2M
   CGroup: /system.slice/nitro-swim.service
           └─1234 /usr/bin/python3 /home/ec2-user/nitro_swim_scraper/scheduler.py
```

**What to look for:**
- `Active: active (running)` ✅ Good
- `Loaded: loaded ... enabled` ✅ Will auto-start on reboot

### 12.2 Exit Status View

Press `q` to exit

---

## Step 13: View Live Logs

### 13.1 Watch Logs in Real-Time

```bash
tail -f /var/log/nitro_swim_scraper.log
```

**Expected output:**
```
2026-01-03 20:25:00,123 - INFO - Starting scheduler - running every 60 minutes
2026-01-03 20:25:05,456 - INFO - ============================================================
2026-01-03 20:25:05,456 - INFO - Starting scheduled scraper job
2026-01-03 20:25:05,456 - INFO - ============================================================
2026-01-03 20:25:10,789 - INFO - Fetching page with Playwright: https://nitroswim.captyn.com/...
2026-01-03 20:25:15,012 - INFO - Page fetched successfully, HTML length: 62834
2026-01-03 20:25:15,012 - INFO - Found 'spot' in HTML content
2026-01-03 20:25:15,012 - INFO - Found 'TF' in HTML content
2026-01-03 20:25:15,014 - INFO - Found 3 'spots open' occurrences
2026-01-03 20:25:15,014 - INFO - Processing spot match 1: 2 spots at position 18870
2026-01-03 20:25:15,014 - INFO -   Found TF 1
2026-01-03 20:25:15,014 - INFO -   Successfully extracted class info
2026-01-03 20:25:15,014 - INFO - Processing spot match 2: 2 spots at position 20911
2026-01-03 20:25:15,014 - INFO -   Found TF 4
2026-01-03 20:25:15,014 - INFO -   Successfully extracted class info
2026-01-03 20:25:15,014 - INFO - Processing spot match 3: 1 spots at position 22952
2026-01-03 20:25:15,014 - INFO -   Found TF 5
2026-01-03 20:25:15,014 - INFO -   Successfully extracted class info
2026-01-03 20:25:15,014 - INFO - Extracted 3 available classes
2026-01-03 20:25:20,345 - INFO - Sending email to tanmoyc999@gmail.com
2026-01-03 20:25:25,678 - INFO - Email sent successfully
2026-01-03 20:25:25,678 - INFO - Notification process completed successfully
```

**What this means:**
- ✅ Scraper is running
- ✅ Found 3 classes with available spots
- ✅ Email sent successfully

### 13.2 Exit Log View

Press `Ctrl+C` to stop watching logs

---

## Step 14: Check Email

### 14.1 Open Email

- Go to Gmail: https://mail.google.com
- Sign in with: tanmoyc999@gmail.com
- Check Inbox

### 14.2 Look for Email

**Subject:** `Nitro Swim - Available Classes (2026-01-03)`

**Email content should show:**
```
Available Classes Summary (2026-01-03 20:25:20)
Total Classes with Availability: 3
============================================================

1. TF 1 - Technique and Fitness (TF)
   Day: M, W
   Time: 4:05 pm-4:50 pm
   Available Spots: 2
   Location: Nitro Swimming Cedar Park
------------------------------------------------------------
2. TF 4 - Technique and Fitness (TF)
   Day: Tu, Th
   Time: 4:05 pm-4:50 pm
   Available Spots: 2
   Location: Nitro Swimming Cedar Park
------------------------------------------------------------
3. TF 5 - Technique and Fitness (TF)
   Day: Tu, Th
   Time: 4:20 pm-5:05 pm
   Available Spots: 1
   Location: Nitro Swimming Cedar Park
------------------------------------------------------------
```

**If you see this, everything is working! ✅**

---

## Step 15: Disconnect from EC2 (Optional)

### 15.1 Exit SSH Session

```bash
exit
```

**You're back on your local machine**

### 15.2 Verify

You should see your local prompt again:
```
yourname@yourcomputer ~ %
```

---

## PART 6: ONGOING MANAGEMENT

---

## Step 16: Monitor Service (Daily)

### 16.1 Check Status Anytime

```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67 "sudo systemctl status nitro-swim.service"
```

### 16.2 View Recent Logs

```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67 "tail -20 /var/log/nitro_swim_scraper.log"
```

### 16.3 Check Email

- Check tanmoyc999@gmail.com inbox
- Should receive email every 60 minutes (if classes available)

---

## Step 17: Troubleshooting

### Issue 1: Service Not Running

**Check status:**
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67 "sudo systemctl status nitro-swim.service"
```

**Restart service:**
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67 "sudo systemctl restart nitro-swim.service"
```

### Issue 2: No Emails Received

**Check logs for errors:**
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67 "grep -i error /var/log/nitro_swim_scraper.log"
```

**Common causes:**
- Gmail app password incorrect
- 2FA not enabled on Gmail account
- Firewall blocking SMTP

### Issue 3: High Memory Usage

**This is normal!**
- Playwright browser uses 100-150MB
- t2.micro has 1GB RAM
- Should be fine

### Issue 4: Slow Performance

**First run is slower (browser startup)**
- Subsequent runs are faster
- Network latency affects speed

---

## Step 18: Modify Configuration (Optional)

### 18.1 Change Check Interval

**SSH into EC2:**
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67
```

**Edit config:**
```bash
cd nitro_swim_scraper
sudo nano config.py
```

**Find this line:**
```python
'interval_minutes': 60,  # Run every hour
```

**Change to (e.g., 30 minutes):**
```python
'interval_minutes': 30,  # Run every 30 minutes
```

**Save:**
- Press `Ctrl+X`
- Press `Y`
- Press `Enter`

**Restart service:**
```bash
sudo systemctl restart nitro-swim.service
```

### 18.2 Change Email Recipient

**Edit config:**
```bash
sudo nano config.py
```

**Find:**
```python
'recipient_email': 'tanmoyc999@gmail.com',
```

**Change to your email:**
```python
'recipient_email': 'your-email@gmail.com',
```

**Save and restart:**
```bash
sudo systemctl restart nitro-swim.service
```

---

## Step 19: Stop Service (if needed)

### 19.1 Stop Service

```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67 "sudo systemctl stop nitro-swim.service"
```

### 19.2 Disable Auto-Start

```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67 "sudo systemctl disable nitro-swim.service"
```

### 19.3 Start Again

```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67 "sudo systemctl start nitro-swim.service"
```

---

## Step 20: Terminate Instance (if done)

### 20.1 Go to AWS Console

- EC2 Dashboard → Instances
- Select your instance
- Click "Instance State" → "Terminate instance"

**Warning:** This deletes everything on the instance!

---

## Summary

You now have:
✅ EC2 instance running 24/7
✅ Scraper checking every 60 minutes
✅ Email notifications when spots available
✅ Auto-start on reboot
✅ All logs saved
✅ Zero cost (free tier)

**The service will continue running automatically!**

---

## Quick Reference Commands

```bash
# Connect to EC2
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP

# Check service status
sudo systemctl status nitro-swim.service

# View logs
tail -f /var/log/nitro_swim_scraper.log

# Restart service
sudo systemctl restart nitro-swim.service

# Stop service
sudo systemctl stop nitro-swim.service

# Start service
sudo systemctl start nitro-swim.service

# View recent logs
tail -20 /var/log/nitro_swim_scraper.log

# Search logs for errors
grep -i error /var/log/nitro_swim_scraper.log

# Exit SSH
exit
```

---

## Need Help?

1. Check logs: `tail -f /var/log/nitro_swim_scraper.log`
2. Check service: `sudo systemctl status nitro-swim.service`
3. Restart: `sudo systemctl restart nitro-swim.service`
4. Check email: Look in tanmoyc999@gmail.com inbox
