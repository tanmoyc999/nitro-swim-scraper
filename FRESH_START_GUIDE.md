# Fresh Start - Complete EC2 Deployment Guide

## Overview

You'll deploy the Nitro Swim scraper to AWS EC2 free tier in 6 main steps.

**Total Time:** ~45 minutes
**Cost:** $0 (free tier)

---

## STEP 1: Create AWS Account (If You Don't Have One)

### 1.1 Go to AWS
- Open browser: https://aws.amazon.com
- Click "Create an AWS Account"
- Enter email, password, account name
- Add payment method (won't be charged for free tier)
- Verify phone number
- Choose "Basic Support" (free)

### 1.2 Verify Email
- Check your email for AWS verification link
- Click the link to activate

### 1.3 Sign In
- Go to https://console.aws.amazon.com
- Sign in with your email and password

---

## STEP 2: Create SSH Key Pair

### 2.1 Go to EC2 Dashboard
1. In search bar at top, type "EC2"
2. Click "EC2" from dropdown
3. You're in EC2 Dashboard

### 2.2 Create Key Pair
1. In left menu, click "Key Pairs"
2. Click "Create key pair" button
3. Fill in:
   - **Name:** `nitro-swim-key`
   - **Key pair type:** RSA
   - **Private key file format:** .pem
4. Click "Create key pair"

### 2.3 Save Key File
- File `nitro-swim-key.pem` downloads automatically
- Usually goes to `~/Downloads/`
- **IMPORTANT:** Save this safely!

### 2.4 Move Key to .ssh Folder

Open Terminal and run:

```bash
# Create .ssh folder
mkdir -p ~/.ssh

# Move key file
mv ~/Downloads/nitro-swim-key.pem ~/.ssh/

# Set permissions
chmod 400 ~/.ssh/nitro-swim-key.pem

# Verify
ls -la ~/.ssh/nitro-swim-key.pem
```

You should see:
```
-r--------  1 yourname  staff  1678 Jan  3 20:00 /Users/yourname/.ssh/nitro-swim-key.pem
```

---

## STEP 3: Create Security Group

### 3.1 Go to Security Groups
1. EC2 Dashboard → left menu
2. Click "Security Groups"
3. Click "Create security group"

### 3.2 Configure Security Group
Fill in:
- **Security group name:** `nitro-swim-sg`
- **Description:** `Security group for Nitro Swim scraper`
- **VPC:** default

### 3.3 Add Inbound Rule
1. Under "Inbound rules", click "Add rule"
2. Fill in:
   - **Type:** SSH
   - **Port range:** 22
   - **Source:** 0.0.0.0/0 (or your IP for more security)
3. Click "Create security group"

---

## STEP 4: Launch EC2 Instance

### 4.1 Go to Instances
1. EC2 Dashboard → left menu
2. Click "Instances"
3. Click "Launch instances" button

### 4.2 Configure Instance

**Name and tags:**
- Name: `nitro-swim-scraper`

**Application and OS Images:**
- Search: "Ubuntu"
- Select: "Ubuntu Server 20.04 LTS"
- Verify: "Free tier eligible"

**Instance type:**
- Select: `t2.micro`
- Verify: "Free tier eligible"

**Key pair (login):**
- Select: `nitro-swim-key`

**Network settings:**
- VPC: default
- Subnet: default
- Auto-assign public IP: Enable
- Security group: Select `nitro-swim-sg`

**Storage:**
- Keep default (20 GB)

### 4.3 Launch
1. Click "Launch instance"
2. Wait for confirmation
3. Click "View all instances"

### 4.4 Wait for Instance to Start
1. Find your instance: `nitro-swim-scraper`
2. Wait for:
   - **Instance State:** "running"
   - **Status checks:** "2/2 checks passed"
3. This takes 2-3 minutes

### 4.5 Get Public IP Address
1. Select your instance
2. Look at "Public IPv4 address" column
3. Copy the IP (e.g., `54.123.45.67`)
4. **Save this IP - you'll need it!**

---

## STEP 5: Connect to EC2 and Copy Project

### 5.1 Test SSH Connection

Open Terminal and run:

```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP
```

Replace `YOUR_IP` with your actual IP address.

**First time, you'll see:**
```
The authenticity of host 'YOUR_IP (YOUR_IP)' can't be established.
ECDSA key fingerprint is SHA256:xxxxx...
Are you sure you want to continue connecting (yes/no)?
```

Type: `yes`
Press Enter

**You should see:**
```
Welcome to Ubuntu 20.04.X LTS (GNU/Linux 5.10.0-1234-aws x86_64)
...
ec2-user@ip-172-31-xx-xx:~$
```

### 5.2 Exit Connection

Type:
```bash
exit
```

### 5.3 Copy Project to EC2

From your local machine, run:

```bash
scp -r nitro_swim_scraper/ ec2-user@YOUR_IP:/home/ec2-user/
```

Replace `YOUR_IP` with your actual IP.

**Wait for copy to complete** (takes 30 seconds)

### 5.4 Verify Copy

Run:
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP "ls -la nitro_swim_scraper/"
```

You should see all your files listed.

---

## STEP 6: Run Setup and Deploy

### 6.1 SSH Into EC2

```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP
```

You should see:
```
ec2-user@ip-172-31-xx-xx:~$
```

### 6.2 Navigate to Project

```bash
cd nitro_swim_scraper
```

### 6.3 Make Setup Script Executable

```bash
chmod +x setup_ec2.sh
```

### 6.4 Run Setup Script

```bash
./setup_ec2.sh
```

**What happens:**
- Updates system packages (30 seconds)
- Installs Python3 and pip (20 seconds)
- Installs dependencies (2-3 minutes)
- Creates log directory
- Sets up systemd service
- Starts the service

**Wait for "Setup Complete!" message**

### 6.5 Verify Service is Running

```bash
sudo systemctl status nitro-swim.service
```

You should see:
```
● nitro-swim.service - Nitro Swim Class Scraper
   Loaded: loaded (/etc/systemd/system/nitro-swim.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2026-01-03 20:25:00 UTC; 2s ago
```

### 6.6 View Logs

```bash
tail -f /var/log/nitro_swim_scraper.log
```

You should see:
```
2026-01-03 20:25:00,123 - INFO - Starting scheduler - running every 60 minutes
2026-01-03 20:25:05,456 - INFO - Starting scheduled scraper job
2026-01-03 20:25:10,789 - INFO - Fetching page with Playwright
2026-01-03 20:25:15,012 - INFO - Page fetched successfully
2026-01-03 20:25:15,014 - INFO - Found 3 'spots open' occurrences
...
2026-01-03 20:25:20,345 - INFO - Email sent successfully
```

Press `Ctrl+C` to exit logs.

### 6.7 Exit EC2

```bash
exit
```

---

## STEP 7: Verify Email Notification

### 7.1 Check Email

1. Go to Gmail: https://mail.google.com
2. Sign in with: tanmoyc999@gmail.com
3. Check Inbox

### 7.2 Look for Email

**Subject:** `Nitro Swim - Available Classes (2026-01-03)`

**Content should show:**
```
Available Classes Summary
Total Classes with Availability: 3

1. TF 1 - Technique and Fitness (TF)
   Day: M, W
   Time: 4:05 pm-4:50 pm
   Available Spots: 2
   Location: Nitro Swimming Cedar Park

2. TF 4 - Technique and Fitness (TF)
   Day: Tu, Th
   Time: 4:05 pm-4:50 pm
   Available Spots: 2
   Location: Nitro Swimming Cedar Park

3. TF 5 - Technique and Fitness (TF)
   Day: Tu, Th
   Time: 4:20 pm-5:05 pm
   Available Spots: 1
   Location: Nitro Swimming Cedar Park
```

**If you see this, everything is working!** ✅

---

## STEP 8: Monitor Service (Ongoing)

### 8.1 Check Status Anytime

```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP "sudo systemctl status nitro-swim.service"
```

### 8.2 View Recent Logs

```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP "tail -20 /var/log/nitro_swim_scraper.log"
```

### 8.3 Check Email

- Check tanmoyc999@gmail.com inbox
- Should receive email every 60 minutes (if classes available)

---

## Quick Reference Commands

### Local Machine (Your Computer)

```bash
# Copy project to EC2
scp -r nitro_swim_scraper/ ec2-user@YOUR_IP:/home/ec2-user/

# Connect to EC2
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP

# Check status remotely
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP "sudo systemctl status nitro-swim.service"

# View logs remotely
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP "tail -f /var/log/nitro_swim_scraper.log"
```

### On EC2 (After SSH Connection)

```bash
# Navigate to project
cd nitro_swim_scraper

# Make setup executable
chmod +x setup_ec2.sh

# Run setup
./setup_ec2.sh

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

# Exit EC2
exit
```

---

## Troubleshooting

### Problem: "Permission denied (publickey)"

**Solution:**
```bash
# Check key permissions
ls -la ~/.ssh/nitro-swim-key.pem

# Should show: -r--------

# If not, fix it:
chmod 400 ~/.ssh/nitro-swim-key.pem
```

### Problem: "Connection refused"

**Solution:**
- Wait 2-3 minutes for instance to fully start
- Check instance state is "running"
- Check status checks show "2/2 checks passed"

### Problem: "Connection timed out"

**Solution:**
- Check security group allows SSH (port 22)
- Check your firewall isn't blocking SSH

### Problem: Service not running

**Solution:**
```bash
# Check status
sudo systemctl status nitro-swim.service

# Restart
sudo systemctl restart nitro-swim.service

# View logs
tail -20 /var/log/nitro_swim_scraper.log
```

### Problem: No emails received

**Solution:**
```bash
# Check logs for errors
grep -i "error\|email" /var/log/nitro_swim_scraper.log

# Verify Gmail credentials in config.py
cat config.py | grep -A 5 "EMAIL_CONFIG"

# Check if 2FA enabled on Gmail
# Check if app password is correct
```

---

## Success Checklist

- [ ] AWS account created
- [ ] SSH key pair created and saved
- [ ] Security group created
- [ ] EC2 instance launched
- [ ] Instance is "running"
- [ ] Status checks show "2/2 checks passed"
- [ ] Public IP address copied
- [ ] SSH connection tested
- [ ] Project copied to EC2
- [ ] Setup script executed
- [ ] Service shows "active (running)"
- [ ] Logs show successful scraper runs
- [ ] Email received in inbox
- [ ] New emails arrive every 60 minutes

**All checked? Deployment complete!** ✅

---

## What Happens Now

✅ Service runs automatically
✅ Checks Nitro Swim every 60 minutes
✅ Sends email when classes available
✅ Continues 24/7
✅ Auto-starts on reboot
✅ Costs $0/month

---

## Cost Breakdown

**AWS Free Tier Includes:**
- 750 hours/month of t2.micro (more than 24/7)
- 1GB outbound data transfer
- Total: $0/month

---

## Next Steps

1. Follow steps 1-8 above
2. Verify email received
3. Monitor logs daily
4. Service runs automatically!

---

## Need Help?

- **SSH issues:** See "Troubleshooting" section
- **Service issues:** Check logs with `tail -f /var/log/nitro_swim_scraper.log`
- **Email issues:** Verify Gmail credentials in `config.py`
- **General help:** Check `COMMAND_REFERENCE.md`

---

## You're Ready!

Everything is set up and tested. Follow the 8 steps above and you'll have a working 24/7 scraper on EC2!

Good luck! 🚀
