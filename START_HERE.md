# START HERE - Complete Deployment Guide

Welcome! This guide will walk you through deploying the Nitro Swim scraper to AWS EC2.

---

## What This Project Does

✅ Automatically checks Nitro Swim website for available classes
✅ Runs every 60 minutes (24/7)
✅ Sends email notifications when spots are available
✅ Runs on free AWS EC2 tier (costs $0)
✅ Auto-starts on reboot
✅ Logs all activity

---

## What You Need

1. **AWS Account** (free tier)
2. **SSH Key** (downloaded from AWS)
3. **This Project** (already have it)
4. **Terminal/Command Line** (Mac/Linux/Windows)
5. **Email** (tanmoyc999@gmail.com - receives notifications)

---

## Documentation Files

Choose your learning style:

### 📋 Quick Start (5 minutes)
**File:** `QUICK_START.md`
- TL;DR version
- 5 main steps
- For experienced users

### 📖 Detailed Steps (30 minutes)
**File:** `DETAILED_STEPS.md`
- Step-by-step with explanations
- What to expect at each step
- Screenshots descriptions
- For beginners

### 🔧 Command Reference
**File:** `COMMAND_REFERENCE.md`
- Copy & paste ready commands
- Organized by category
- For quick lookups

### ✅ Checklist
**File:** `CHECKLIST.md`
- Checkbox format
- Track your progress
- Troubleshooting section

### 📚 Full Deployment Guide
**File:** `DEPLOYMENT_GUIDE.md`
- Comprehensive reference
- All details
- For deep understanding

---

## Quick Navigation

### I'm a Beginner
1. Read: `DETAILED_STEPS.md` (Part 1-5)
2. Follow: Step by step
3. Use: `CHECKLIST.md` to track progress
4. Reference: `COMMAND_REFERENCE.md` if stuck

### I'm Experienced
1. Read: `QUICK_START.md`
2. Use: `COMMAND_REFERENCE.md` for commands
3. Reference: `DETAILED_STEPS.md` if needed

### I Need Help
1. Check: `CHECKLIST.md` - Troubleshooting section
2. Review: `COMMAND_REFERENCE.md` - Common Issues
3. Read: `DETAILED_STEPS.md` - Step 17 Troubleshooting

---

## The 5-Minute Overview

### Step 1: Launch EC2 Instance
- Go to AWS Console
- Launch Ubuntu 20.04 LTS, t2.micro
- Download SSH key

### Step 2: Copy Project
```bash
scp -r nitro_swim_scraper/ ec2-user@YOUR_IP:/home/ec2-user/
```

### Step 3: SSH In
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP
```

### Step 4: Run Setup
```bash
cd nitro_swim_scraper
chmod +x setup_ec2.sh
./setup_ec2.sh
```

### Step 5: Done!
- Service running
- Emails being sent
- 24/7 monitoring active

---

## File Structure

```
nitro_swim_scraper/
├── START_HERE.md                 ← You are here
├── QUICK_START.md                ← 5-minute version
├── DETAILED_STEPS.md             ← Complete walkthrough
├── COMMAND_REFERENCE.md          ← Copy & paste commands
├── CHECKLIST.md                  ← Track progress
├── DEPLOYMENT_GUIDE.md           ← Full reference
│
├── scraper.py                    ← Main scraper code
├── scheduler.py                  ← Runs every 60 minutes
├── config.py                     ← Configuration
├── requirements.txt              ← Python dependencies
│
├── setup_ec2.sh                  ← Automated setup script
├── setup_local.sh                ← Local setup script
├── nitro-swim.service            ← Systemd service file
│
└── README.md                     ← Project overview
```

---

## What Happens After Setup

### Minute 0
- Service starts
- Begins waiting for next scheduled run

### Minute 1-5
- First scraper job runs
- Fetches Nitro Swim website
- Finds available classes
- Sends email notification

### Minute 5-60
- Service waits
- Logs are written
- Everything runs in background

### Minute 60
- Second scraper job runs
- Repeats every 60 minutes
- Continues 24/7

---

## Expected Results

### In Your Email (tanmoyc999@gmail.com)

**Subject:** Nitro Swim - Available Classes (2026-01-03)

**Content:**
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
```

### In EC2 Logs

```
2026-01-03 20:25:00,123 - INFO - Starting scheduler - running every 60 minutes
2026-01-03 20:25:05,456 - INFO - Starting scheduled scraper job
2026-01-03 20:25:10,789 - INFO - Fetching page with Playwright
2026-01-03 20:25:15,012 - INFO - Page fetched successfully
2026-01-03 20:25:15,014 - INFO - Found 3 'spots open' occurrences
2026-01-03 20:25:15,014 - INFO - Processing spot match 1: 2 spots
2026-01-03 20:25:15,014 - INFO - Found TF 1
2026-01-03 20:25:15,014 - INFO - Successfully extracted class info
2026-01-03 20:25:20,345 - INFO - Email sent successfully
```

---

## Common Questions

### Q: Will this cost money?
**A:** No! AWS free tier covers:
- 750 hours/month of t2.micro (more than 24/7)
- 1GB outbound data transfer
- Total: $0/month

### Q: What if I stop using it?
**A:** Just terminate the EC2 instance in AWS Console. No charges after that.

### Q: Can I change the check interval?
**A:** Yes! Edit `config.py` and change `interval_minutes` from 60 to whatever you want.

### Q: Can I change the email recipient?
**A:** Yes! Edit `config.py` and change `recipient_email`.

### Q: What if the service stops?
**A:** It auto-restarts on reboot. You can also manually restart:
```bash
sudo systemctl restart nitro-swim.service
```

### Q: How do I monitor it?
**A:** Check logs anytime:
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP "tail -f /var/log/nitro_swim_scraper.log"
```

### Q: What if something breaks?
**A:** See `CHECKLIST.md` - Troubleshooting section

---

## Next Steps

### Choose Your Path:

**Path 1: I want to start NOW**
→ Go to `QUICK_START.md`

**Path 2: I want detailed instructions**
→ Go to `DETAILED_STEPS.md`

**Path 3: I want to understand everything**
→ Read `DEPLOYMENT_GUIDE.md`

**Path 4: I want to track my progress**
→ Use `CHECKLIST.md`

---

## Key Commands to Remember

```bash
# Connect to EC2
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP

# Check if running
sudo systemctl status nitro-swim.service

# View logs
tail -f /var/log/nitro_swim_scraper.log

# Restart service
sudo systemctl restart nitro-swim.service

# Exit EC2
exit
```

---

## Support Resources

| Issue | Solution |
|-------|----------|
| Don't know where to start | Read `DETAILED_STEPS.md` |
| Need quick commands | Use `COMMAND_REFERENCE.md` |
| Want to track progress | Use `CHECKLIST.md` |
| Service not working | See `CHECKLIST.md` - Troubleshooting |
| Need full reference | Read `DEPLOYMENT_GUIDE.md` |

---

## Timeline

| Time | Action |
|------|--------|
| 5 min | Read this file |
| 10 min | Create AWS account & EC2 instance |
| 5 min | Download SSH key & set permissions |
| 5 min | Copy project to EC2 |
| 10 min | Run setup script |
| 5 min | Verify everything works |
| **Total: ~40 minutes** | **Deployment complete!** |

---

## Success Indicators

✅ You'll know it's working when:
1. Setup script completes without errors
2. Service shows "active (running)"
3. Logs show successful scraper runs
4. Email received in tanmoyc999@gmail.com inbox
5. New emails arrive every 60 minutes

---

## What's Included

✅ Automated scraper (finds available classes)
✅ Email notifications (sends updates)
✅ Scheduler (runs every 60 minutes)
✅ Logging (tracks everything)
✅ Auto-start (survives reboots)
✅ Configuration (easy to customize)
✅ Documentation (this!)

---

## Ready to Deploy?

### Option 1: Quick Start (Experienced Users)
→ Open `QUICK_START.md`

### Option 2: Detailed Steps (Beginners)
→ Open `DETAILED_STEPS.md`

### Option 3: Full Reference (Deep Dive)
→ Open `DEPLOYMENT_GUIDE.md`

---

## Questions?

1. **How do I...?** → Check `COMMAND_REFERENCE.md`
2. **What if...?** → Check `CHECKLIST.md` - Troubleshooting
3. **I'm stuck on step X** → Check `DETAILED_STEPS.md` - Step X
4. **I need to do X** → Check `DEPLOYMENT_GUIDE.md`

---

## Let's Go! 🚀

Pick a guide above and start deploying!

**Estimated time to full deployment: 40 minutes**

Good luck! 🎉
