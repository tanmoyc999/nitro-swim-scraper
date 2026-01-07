# Quick Start - EC2 Deployment

## TL;DR - 5 Steps

### Step 1: Launch EC2
- Go to AWS Console → EC2 → Launch Instance
- Choose: Ubuntu 20.04 LTS, t2.micro
- Create/download SSH key (.pem file)
- Note the Public IP address

### Step 2: Copy Project
```bash
scp -r nitro_swim_scraper/ ec2-user@YOUR_IP:/home/ec2-user/
```

### Step 3: SSH In
```bash
ssh -i your-key.pem ec2-user@YOUR_IP
```

### Step 4: Run Setup
```bash
cd nitro_swim_scraper
chmod +x setup_ec2.sh
./setup_ec2.sh
```

### Step 5: Done!
Service is running. Check status:
```bash
sudo systemctl status nitro-swim.service
```

---

## Verify It's Working

### Check Logs
```bash
tail -f /var/log/nitro_swim_scraper.log
```

### Check Email
Look for "Nitro Swim - Available Classes" in tanmoyc999@gmail.com

### Check Service
```bash
sudo systemctl status nitro-swim.service
```

---

## Common Commands

| Command | Purpose |
|---------|---------|
| `sudo systemctl status nitro-swim.service` | Check if running |
| `sudo systemctl restart nitro-swim.service` | Restart service |
| `sudo systemctl stop nitro-swim.service` | Stop service |
| `tail -f /var/log/nitro_swim_scraper.log` | View live logs |
| `sudo journalctl -u nitro-swim.service -f` | View systemd logs |

---

## What Happens Next

✅ Service starts automatically
✅ Runs every 60 minutes
✅ Checks for available classes
✅ Sends email if spots found
✅ Logs everything
✅ Continues 24/7

---

## Troubleshooting

**Service not running?**
```bash
sudo systemctl status nitro-swim.service
sudo journalctl -u nitro-swim.service -n 50
```

**No emails?**
```bash
grep -i "email\|error" /var/log/nitro_swim_scraper.log
```

**Want to change interval?**
```bash
sudo nano nitro_swim_scraper/config.py
# Change interval_minutes
sudo systemctl restart nitro-swim.service
```

---

## Cost
FREE! (within AWS free tier limits)
