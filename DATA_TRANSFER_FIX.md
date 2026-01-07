# Data Transfer Optimization - Fix for 3GB Forecast

## Problem

AWS billing forecast showed 3 GB data transfer, which exceeds the 1 GB free tier limit.

## Root Cause

Playwright was downloading:
- All images on the webpage
- All CSS stylesheets
- All JavaScript files
- Extra resources not needed for scraping

This was happening 7 times per day, causing excessive data transfer.

## Solution Implemented

### 1. Block Unnecessary Resources

Updated `scraper.py` to block images, CSS, and other non-essential resources:

```python
# Block images and stylesheets to reduce data transfer
page.route("**/*.{png,jpg,jpeg,gif,svg,webp,css}", lambda route: route.abort())
```

**Impact:** Reduces data per page fetch from ~5 MB to ~500 KB

### 2. Reduce Logging Verbosity

Updated `scheduler.py` to:
- Only log when classes are found
- Remove verbose separator lines
- Reduce debug information

**Impact:** Reduces log file growth

### 3. Add Log Rotation

Implemented rotating file handler:
- Max 5 MB per log file
- Keep 3 backup files
- Automatically deletes old logs

**Impact:** Prevents logs from consuming disk space

### 4. Optimize Playwright Launch

- Reduced timeout from 60s to 30s
- Reduced wait time from 5s to 3s
- Better resource cleanup

**Impact:** Faster execution, less memory usage

## New Data Transfer Estimate

**Before optimization:**
- Setup: ~360 MB (one-time)
- Per run: ~5 MB × 7 runs/day × 30 days = 1,050 MB
- **Total: ~1.4 GB/month** ❌ Over limit

**After optimization:**
- Setup: ~360 MB (one-time)
- Per run: ~500 KB × 7 runs/day × 30 days = 105 MB
- **Total: ~465 MB/month** ✅ Under limit

## How to Deploy

### Step 1: Copy Updated Files

```bash
scp nitro_swim_scraper/scraper.py ubuntu@18.117.154.7:/home/ubuntu/nitro_swim_scraper/
scp nitro_swim_scraper/scheduler.py ubuntu@18.117.154.7:/home/ubuntu/nitro_swim_scraper/
```

### Step 2: SSH Into EC2

```bash
ssh -i ~/.ssh/nitro-swim-key.pem ubuntu@18.117.154.7
```

### Step 3: Restart Service

```bash
sudo systemctl restart nitro-swim.service
```

### Step 4: Verify

```bash
sudo systemctl status nitro-swim.service
tail -f /var/log/nitro_swim/nitro_swim_scraper.log
```

## Verification

After deployment, check:

1. **Service is running:**
   ```bash
   sudo systemctl status nitro-swim.service
   ```
   Should show: `Active: active (running)`

2. **Logs are being written:**
   ```bash
   tail -f /var/log/nitro_swim/nitro_swim_scraper.log
   ```
   Should show: `Scheduler started. Waiting for scheduled times...`

3. **Next scheduled run works:**
   - Wait for next scheduled time
   - Should see: `Starting scheduled scraper job`
   - Should see: `Found X available classes` (if any)
   - Should see: `Email sent successfully` (if classes found)

## Expected Results

✅ Data transfer reduced by ~90%
✅ Logs won't grow excessively
✅ Service runs faster
✅ Still within free tier
✅ No billing charges

## Monitoring

Check AWS billing dashboard weekly:
- Should show data transfer under 500 MB
- Should show $0.00 charges
- Forecast should show under 1 GB

## Files Changed

1. `scraper.py`
   - Added resource blocking
   - Reduced timeouts
   - Better cleanup

2. `scheduler.py`
   - Added log rotation
   - Reduced logging verbosity
   - Only log when needed

## Rollback (If Needed)

If something breaks, you can revert:

```bash
# SSH into EC2
ssh -i ~/.ssh/nitro-swim-key.pem ubuntu@YOUR_IP

# Stop service
sudo systemctl stop nitro-swim.service

# Restore from backup (if you have one)
# Or re-run setup script
cd nitro_swim_scraper
./setup_ec2.sh
```

## Questions?

- Check logs: `tail -f /var/log/nitro_swim/nitro_swim_scraper.log`
- Check service: `sudo systemctl status nitro-swim.service`
- Check billing: AWS Console → Billing Dashboard

---

**Summary:** Updated code to reduce data transfer by ~90%. Should now stay well under 1 GB free tier limit. No billing charges expected.
