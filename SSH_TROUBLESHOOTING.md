# SSH Permission Denied - Troubleshooting Guide

## Error: "Permission denied (publickey)"

This error means SSH can't authenticate with your key. Here are the solutions:

---

## Problem 1: Wrong Key Pair for Instance

### Symptom
```
ec2-user@3.15.186.224: Permission denied (publickey).
```

### Cause
You're using a different EC2 instance than the one you created the key for.

### Solution

**Step 1: Check Your EC2 Instances**

1. Go to AWS Console
2. EC2 → Instances
3. Look at all your instances
4. Note which key pair each one uses

**Step 2: Use Correct Instance**

If you have the original instance (13.59.168.106):
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@13.59.168.106
```

**Step 3: If You Created a New Instance**

If the new instance (3.15.186.224) was created with a DIFFERENT key:
- You need that key file
- Or terminate this instance and create a new one with `nitro-swim-key`

---

## Problem 2: Instance Created Without Correct Key

### Symptom
New instance won't accept your key

### Cause
You selected a different key pair when launching the instance

### Solution

**Option A: Terminate and Relaunch (Recommended)**

1. Go to AWS Console
2. EC2 → Instances
3. Select the instance (3.15.186.224)
4. Click "Instance State" → "Terminate instance"
5. Confirm termination
6. Launch a NEW instance
7. When asked for key pair, select: `nitro-swim-key`
8. Launch and use the new IP

**Option B: Use the Correct Key**

If you created the instance with a different key:
1. Find that key file (check Downloads)
2. Move it to ~/.ssh/
3. Set permissions: `chmod 400 ~/.ssh/other-key.pem`
4. Connect with: `ssh -i ~/.ssh/other-key.pem ec2-user@3.15.186.224`

---

## Problem 3: Key File Permissions Wrong

### Symptom
```
Permission denied (publickey).
```

### Cause
SSH key file has wrong permissions

### Solution

**Step 1: Check Permissions**
```bash
ls -la ~/.ssh/nitro-swim-key.pem
```

**You should see:**
```
-r--------@ 1 tanmoychakraborty  staff  1678 Jan  3 18:20 /Users/tanmoychakraborty/.ssh/nitro-swim-key.pem
```

**Important:** Look for `-r--------` at the beginning

**Step 2: If Permissions Are Wrong**

Fix them:
```bash
chmod 400 ~/.ssh/nitro-swim-key.pem
```

**Step 3: Verify Again**
```bash
ls -la ~/.ssh/nitro-swim-key.pem
```

Should show: `-r--------`

---

## Problem 4: Instance Not Ready

### Symptom
```
Permission denied (publickey).
```

### Cause
Instance is still starting up

### Solution

**Step 1: Wait**
- Wait 2-3 minutes after launching instance
- Instance needs time to fully boot

**Step 2: Check Status**
1. Go to AWS Console
2. EC2 → Instances
3. Look at "Instance State" column
4. Should show "running"
5. Look at "Status checks" column
6. Should show "2/2 checks passed"

**Step 3: Try Again**
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@3.15.186.224
```

---

## Problem 5: Security Group Doesn't Allow SSH

### Symptom
```
Connection timed out
```
(Different from "Permission denied")

### Cause
Security group doesn't allow SSH (port 22)

### Solution

**Step 1: Go to AWS Console**
1. EC2 → Instances
2. Select your instance
3. Click "Security" tab
4. Click security group name

**Step 2: Edit Inbound Rules**
1. Click "Edit inbound rules"
2. Look for SSH rule (port 22)
3. If not there, click "Add rule"
4. Type: SSH
5. Port: 22
6. Source: 0.0.0.0/0 (or your IP)
7. Click "Save rules"

**Step 3: Try Again**
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@3.15.186.224
```

---

## Quick Diagnosis

Run this to check everything:

```bash
# 1. Check key file exists
ls -la ~/.ssh/nitro-swim-key.pem

# 2. Check permissions
ls -la ~/.ssh/nitro-swim-key.pem | grep "^-r"

# 3. Try connection with verbose output
ssh -vvv -i ~/.ssh/nitro-swim-key.pem ec2-user@3.15.186.224
```

The verbose output (`-vvv`) will show exactly where it's failing.

---

## Most Common Solution

**99% of the time, the issue is:**

You created a new EC2 instance and selected a DIFFERENT key pair.

**Fix:**
1. Terminate the new instance
2. Launch a new instance
3. Select the SAME key pair: `nitro-swim-key`
4. Use the new IP

---

## Step-by-Step Fix

### Step 1: Check Your Instances

Go to AWS Console:
1. EC2 → Instances
2. Look at all instances
3. Note the key pair for each

### Step 2: Identify the Problem

**If you see:**
- Instance 1 (13.59.168.106) - Key: nitro-swim-key ✅
- Instance 2 (3.15.186.224) - Key: something-else ❌

**Then:** Terminate Instance 2 and create a new one with nitro-swim-key

### Step 3: Terminate Wrong Instance

1. Select Instance 2 (3.15.186.224)
2. Click "Instance State" → "Terminate instance"
3. Confirm

### Step 4: Launch New Instance

1. Click "Launch Instance"
2. Choose Ubuntu 20.04 LTS, t2.micro
3. When asked for key pair, select: `nitro-swim-key`
4. Launch

### Step 5: Get New IP

1. Wait for instance to start
2. Copy the new "Public IPv4 address"
3. Use it to connect

### Step 6: Connect

```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@NEW_IP
```

---

## Verification Checklist

- [ ] Instance is running (not pending)
- [ ] Status checks show "2/2 checks passed"
- [ ] Instance uses key pair: `nitro-swim-key`
- [ ] SSH key file exists: `~/.ssh/nitro-swim-key.pem`
- [ ] SSH key permissions: `-r--------`
- [ ] Security group allows SSH (port 22)
- [ ] Using correct IP address
- [ ] Waited 2-3 minutes after launch

---

## If Still Not Working

Run verbose SSH to see exactly what's happening:

```bash
ssh -vvv -i ~/.ssh/nitro-swim-key.pem ec2-user@3.15.186.224
```

Look for:
- "Trying private key" - Key file found ✅
- "Permission denied" - Key doesn't match ❌
- "Connection timed out" - Security group issue ❌
- "Connection refused" - Instance not ready ❌

---

## Next Steps

1. Identify which instance to use
2. Terminate the wrong one (if needed)
3. Launch new instance with correct key
4. Connect with correct IP
5. Continue with deployment

---

## Quick Reference

| Error | Cause | Fix |
|-------|-------|-----|
| Permission denied | Wrong key pair | Use correct instance or relaunch with correct key |
| Connection timed out | Security group | Allow SSH in security group |
| Connection refused | Instance not ready | Wait 2-3 minutes |
| No such file | Key not found | Check key location |
| Bad permissions | Wrong chmod | Run `chmod 400 ~/.ssh/nitro-swim-key.pem` |

---

## You're Almost There!

Once you fix the key pair issue, you'll be able to connect and deploy!
