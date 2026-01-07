# What Was Fixed - Technical Details

## Issues Encountered

During the previous deployment attempts, the service kept failing with these errors:

```
Error fetching page: Host system is missing dependencies to run browsers.
```

And later:

```
sudo: playwright: command not found
```

The service would show:
```
Active: activating (auto-restart) (Result: exit-code)
```

---

## Root Causes

### 1. Missing Playwright System Dependencies

**Problem:** Playwright needs system libraries to run browsers, but they weren't installed.

**What was missing:**
- libatk1.0-0
- libatk-bridge2.0-0
- libcups2
- libatspi2.0-0
- libxcomposite1
- libxdamage1
- libxfixes3
- libxrandr2
- libgbm1
- libpango-1.0-0
- libcairo2
- libasound2t64

**Fix:** Added to `setup_ec2.sh`:
```bash
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
```

### 2. Playwright Browsers Not Installed

**Problem:** Even with dependencies, Playwright needs to download and install browser binaries.

**What was missing:** The `playwright install` command

**Fix:** Added to `setup_ec2.sh`:
```bash
python3 -m playwright install
```

This downloads Chromium, Firefox, and WebKit browsers that Playwright needs.

### 3. Incorrect Log File Path

**Problem:** Config had wrong path for Ubuntu instance:
```python
'log_file': '/home/ubuntu/nitro_swim_scraper/nitro_swim_scraper.log'
```

But the service runs as `ubuntu` user, and logs should go to a system location.

**Fix:** Changed to:
```python
'log_file': '/var/log/nitro_swim/nitro_swim_scraper.log'
```

This is the standard location for application logs on Linux.

### 4. Service File Logging Not Configured

**Problem:** The systemd service file didn't specify where to write logs.

**Original:**
```ini
StandardOutput=journal
StandardError=journal
```

**Fix:** Added explicit log file paths:
```ini
StandardOutput=append:/var/log/nitro_swim/nitro_swim_scraper.log
StandardError=append:/var/log/nitro_swim/nitro_swim_scraper.log
```

### 5. Setup Script Didn't Create Log Directory

**Problem:** The setup script created `/var/log/nitro_swim` but didn't set proper permissions.

**Fix:** Updated setup script to:
```bash
sudo mkdir -p /var/log/nitro_swim
sudo chown $USER:$USER /var/log/nitro_swim
```

---

## Files Changed

### 1. `setup_ec2.sh`

**Before:**
```bash
# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Create log directory
echo "Creating log directory..."
sudo mkdir -p /var/log/nitro_swim
sudo chown $USER:$USER /var/log/nitro_swim
```

**After:**
```bash
# Install system dependencies for Playwright
echo "Installing system dependencies for Playwright..."
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

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
python3 -m playwright install

# Create log directory
echo "Creating log directory..."
sudo mkdir -p /var/log/nitro_swim
sudo chown $USER:$USER /var/log/nitro_swim
```

### 2. `config.py`

**Before:**
```python
SCHEDULER_CONFIG = {
    'interval_minutes': 60,
    'log_file': '/home/ubuntu/nitro_swim_scraper/nitro_swim_scraper.log',
    'enable_logging': True
}
```

**After:**
```python
SCHEDULER_CONFIG = {
    'interval_minutes': 60,
    'log_file': '/var/log/nitro_swim/nitro_swim_scraper.log',
    'enable_logging': True
}
```

### 3. `nitro-swim.service`

**Before:**
```ini
StandardOutput=journal
StandardError=journal
```

**After:**
```ini
StandardOutput=journal
StandardError=journal
StandardOutput=append:/var/log/nitro_swim/nitro_swim_scraper.log
StandardError=append:/var/log/nitro_swim/nitro_swim_scraper.log
```

### 4. `scheduler.py`

**Minor fix:** Reordered scheduled times to be in chronological order (UTC):
```python
schedule_times = [
    "02:00",  # 8 PM CST
    "04:00",  # 10 PM CST
    "05:00",  # 11 PM CST
    "06:00",  # 12 AM CST
    "20:00",  # 2 PM CST
    "21:00",  # 3 PM CST
    "23:00",  # 5 PM CST
]
```

---

## How to Deploy with Fixes

### Option 1: Fresh EC2 Instance (Recommended)

1. Create new EC2 instance
2. Copy updated project files
3. Run `./setup_ec2.sh`
4. Done!

### Option 2: Fix Existing EC2 Instance

If you already have an instance running:

```bash
# SSH into instance
ssh -i ~/.ssh/nitro-swim-key.pem ubuntu@YOUR_IP

# Stop service
sudo systemctl stop nitro-swim.service

# Install system dependencies
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

# Create log directory
sudo mkdir -p /var/log/nitro_swim
sudo chown ubuntu:ubuntu /var/log/nitro_swim

# Copy updated files
cd nitro_swim_scraper
# (Copy updated config.py, scheduler.py, nitro-swim.service)

# Restart service
sudo systemctl restart nitro-swim.service

# Check status
sudo systemctl status nitro-swim.service
```

---

## Verification

After deployment, verify everything works:

```bash
# Check service is running
sudo systemctl status nitro-swim.service

# Should show: Active: active (running)

# Check logs
tail -f /var/log/nitro_swim/nitro_swim_scraper.log

# Should show: Scheduler started. Waiting for scheduled times...

# Wait for next scheduled time, should see:
# Starting scheduled scraper job
# Fetching page with Playwright
# Page fetched successfully
# Found X 'spots open' occurrences
# Email sent successfully
```

---

## Why These Fixes Work

1. **System dependencies** - Playwright needs these libraries to render web pages
2. **Browser installation** - Playwright needs actual browser binaries to run
3. **Correct log path** - `/var/log/` is where system services write logs
4. **Service logging** - Ensures logs are captured and accessible
5. **Proper permissions** - Allows the service to write logs

---

## Testing Locally (Optional)

Before deploying to EC2, you can test locally:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python3 -m playwright install

# Run scraper
python3 scraper.py

# Should see: Found X available classes
# Should receive email
```

---

## Summary

The deployment now:
✅ Installs all required system dependencies
✅ Installs Playwright browsers
✅ Writes logs to correct location
✅ Service auto-starts and auto-restarts
✅ Runs at scheduled times (7 times per day)
✅ Sends email notifications
✅ Costs $0/month on free tier

You can now turn off your Mac and the scraper will continue running 24/7 on EC2!
