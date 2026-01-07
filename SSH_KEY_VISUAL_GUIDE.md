# SSH Key Setup - Visual Step-by-Step Guide

## Complete Terminal Walkthrough

This guide shows exactly what you'll see in Terminal at each step.

---

## Step 1: Open Terminal

### Action
Press `Cmd + Space`, type "Terminal", press Enter

### What You See
```
Last login: Fri Jan 03 20:00:00 on ttys000
yourname@yourcomputer ~ %
```

**Explanation:**
- `Last login:` - When you last opened Terminal
- `yourname@yourcomputer` - Your username and computer name
- `~` - You're in home directory
- `%` - Ready for commands

---

## Step 2: Create .ssh Folder

### Command
```bash
mkdir -p ~/.ssh
```

### What You Type
```
yourname@yourcomputer ~ % mkdir -p ~/.ssh
```

### What You See After Pressing Enter
```
yourname@yourcomputer ~ %
```

**Explanation:**
- No output = success!
- The folder is created silently

---

## Step 3: Verify Folder Created

### Command
```bash
ls -la ~/
```

### What You Type
```
yourname@yourcomputer ~ % ls -la ~/
```

### What You See
```
total 56
drwxr-xr-x  27 yourname  staff   864 Jan  3 20:00 .
drwxr-xr-x   5 root      wheel   160 Jan  2 10:00 ..
-rw-r--r--   1 yourname  staff  3456 Jan  3 19:00 .bash_profile
-rw-r--r--   1 yourname  staff  2345 Jan  3 19:00 .bashrc
drwx------   5 yourname  staff   160 Jan  3 20:00 .ssh          ← HERE!
drwxr-xr-x   3 yourname  staff    96 Jan  3 19:00 Desktop
drwxr-xr-x   3 yourname  staff    96 Jan  3 19:00 Documents
drwxr-xr-x   3 yourname  staff    96 Jan  3 19:00 Downloads
...
```

**Look for:** `drwx------   5 yourname  staff   160 Jan  3 20:00 .ssh`

This means the `.ssh` folder exists! ✅

---

## Step 4: Navigate to Downloads

### Command
```bash
cd ~/Downloads
```

### What You Type
```
yourname@yourcomputer ~ % cd ~/Downloads
```

### What You See
```
yourname@yourcomputer Downloads %
```

**Explanation:**
- Prompt changed from `~` to `Downloads`
- You're now in the Downloads folder

---

## Step 5: Verify SSH Key File

### Command
```bash
ls -la nitro-swim-key.pem
```

### What You Type
```
yourname@yourcomputer Downloads % ls -la nitro-swim-key.pem
```

### What You See
```
-rw-r--r--  1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem
```

**Explanation:**
- `-rw-r--r--` - File permissions (will change later)
- `1704` - File size in bytes
- `Jan  3 20:00` - When downloaded
- `nitro-swim-key.pem` - The file name

**If you see this, the file exists!** ✅

**If you see "No such file or directory":**
- Check Downloads folder in Finder
- Make sure file name is exactly `nitro-swim-key.pem`

---

## Step 6: Move File to .ssh

### Command
```bash
mv nitro-swim-key.pem ~/.ssh/
```

### What You Type
```
yourname@yourcomputer Downloads % mv nitro-swim-key.pem ~/.ssh/
```

### What You See
```
yourname@yourcomputer Downloads %
```

**Explanation:**
- No output = success!
- File moved silently

---

## Step 7: Verify File Moved

### Command
```bash
ls -la ~/.ssh/
```

### What You Type
```
yourname@yourcomputer Downloads % ls -la ~/.ssh/
```

### What You See
```
total 8
drwx------   3 yourname  staff    96 Jan  3 20:00 .
drwxr-xr-x  27 yourname  staff   864 Jan  3 20:00 ..
-rw-r--r--   1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem
```

**Look for:** `nitro-swim-key.pem` in the list

**This means the file is in the right place!** ✅

---

## Step 8: Set Permissions

### Command
```bash
chmod 400 ~/.ssh/nitro-swim-key.pem
```

### What You Type
```
yourname@yourcomputer Downloads % chmod 400 ~/.ssh/nitro-swim-key.pem
```

### What You See
```
yourname@yourcomputer Downloads %
```

**Explanation:**
- No output = success!
- Permissions changed silently

---

## Step 9: Verify Permissions Changed

### Command
```bash
ls -la ~/.ssh/nitro-swim-key.pem
```

### What You Type
```
yourname@yourcomputer Downloads % ls -la ~/.ssh/nitro-swim-key.pem
```

### What You See (BEFORE)
```
-rw-r--r--  1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem
```

### What You See (AFTER)
```
-r--------  1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem
```

**Compare:**
- BEFORE: `-rw-r--r--` (readable by everyone)
- AFTER: `-r--------` (readable by owner only)

**This is correct!** ✅

---

## Step 10: Test SSH Connection

### Get Your EC2 IP Address

From AWS Console:
1. Go to EC2 Dashboard
2. Click "Instances"
3. Find your instance
4. Copy "Public IPv4 address"

Example: `54.123.45.67`

### Command
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67
```

### What You Type
```
yourname@yourcomputer Downloads % ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67
```

### What You See (First Time)
```
The authenticity of host '54.123.45.67 (54.123.45.67)' can't be established.
ECDSA key fingerprint is SHA256:abcdef1234567890...
Are you sure you want to continue connecting (yes/no)?
```

### What You Type
```
yes
```

### What You See (After yes)
```
Warning: Permanently added '54.123.45.67' (ECDSA) to the list of known hosts.
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

**You're now connected to EC2!** ✅

---

## Step 11: Exit Connection

### Command
```bash
exit
```

### What You Type
```
ec2-user@ip-172-31-xx-xx:~$ exit
```

### What You See
```
logout
Connection to 54.123.45.67 closed.
yourname@yourcomputer Downloads %
```

**You're back on your local machine!** ✅

---

## Complete Terminal Session Example

Here's what a complete session looks like:

```bash
# Step 1: Create .ssh folder
yourname@yourcomputer ~ % mkdir -p ~/.ssh

# Step 2: Verify folder
yourname@yourcomputer ~ % ls -la ~/ | grep ssh
drwx------   5 yourname  staff   160 Jan  3 20:00 .ssh

# Step 3: Go to Downloads
yourname@yourcomputer ~ % cd ~/Downloads

# Step 4: Verify key file
yourname@yourcomputer Downloads % ls -la nitro-swim-key.pem
-rw-r--r--  1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem

# Step 5: Move file
yourname@yourcomputer Downloads % mv nitro-swim-key.pem ~/.ssh/

# Step 6: Verify moved
yourname@yourcomputer Downloads % ls -la ~/.ssh/nitro-swim-key.pem
-rw-r--r--  1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem

# Step 7: Set permissions
yourname@yourcomputer Downloads % chmod 400 ~/.ssh/nitro-swim-key.pem

# Step 8: Verify permissions
yourname@yourcomputer Downloads % ls -la ~/.ssh/nitro-swim-key.pem
-r--------  1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem

# Step 9: Test connection
yourname@yourcomputer Downloads % ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67
The authenticity of host '54.123.45.67 (54.123.45.67)' can't be established.
ECDSA key fingerprint is SHA256:abcdef1234567890...
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '54.123.45.67' (ECDSA) to the list of known hosts.
Welcome to Ubuntu 20.04.X LTS (GNU/Linux 5.10.0-1234-aws x86_64)
...
ec2-user@ip-172-31-xx-xx:~$

# Step 10: Exit
ec2-user@ip-172-31-xx-xx:~$ exit
logout
Connection to 54.123.45.67 closed.
yourname@yourcomputer Downloads %
```

---

## Quick Copy-Paste Commands

If you want to just copy and paste all commands:

```bash
# Create .ssh folder
mkdir -p ~/.ssh

# Move key file (from Downloads)
mv ~/Downloads/nitro-swim-key.pem ~/.ssh/

# Set permissions
chmod 400 ~/.ssh/nitro-swim-key.pem

# Verify permissions
ls -la ~/.ssh/nitro-swim-key.pem

# Test connection (replace IP with your actual IP)
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67

# Exit connection
exit
```

---

## Troubleshooting with Examples

### Problem: "No such file or directory"

**What you see:**
```
yourname@yourcomputer Downloads % ls -la nitro-swim-key.pem
ls: nitro-swim-key.pem: No such file or directory
```

**Solution:**
1. Check Downloads folder in Finder
2. Make sure file name is exactly `nitro-swim-key.pem`
3. Try: `ls -la ~/Downloads/` to see all files

### Problem: "Permission denied (publickey)"

**What you see:**
```
Permission denied (publickey).
```

**Solution:**
```bash
# Check permissions
ls -la ~/.ssh/nitro-swim-key.pem

# Should show: -r--------
# If not, fix it:
chmod 400 ~/.ssh/nitro-swim-key.pem
```

### Problem: "Connection refused"

**What you see:**
```
ssh: connect to host 54.123.45.67 port 22: Connection refused
```

**Solution:**
1. Check EC2 instance is running in AWS Console
2. Wait 2-3 minutes for instance to fully start
3. Verify IP address is correct

### Problem: "Connection timed out"

**What you see:**
```
ssh: connect to host 54.123.45.67 port 22: Operation timed out
```

**Solution:**
1. Check security group allows SSH (port 22)
2. Check your firewall isn't blocking SSH
3. Try again in a few minutes

---

## File Locations Visualization

```
Your Computer
│
├── Home Directory (~)
│   │
│   ├── Downloads/
│   │   └── nitro-swim-key.pem  ← Downloaded here
│   │
│   └── .ssh/
│       └── nitro-swim-key.pem  ← Moved here (final location)
│
└── (Other folders)
```

---

## Permissions Visualization

### Before (Wrong)
```
-rw-r--r--  1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem
 ││││││││
 ││││││└─ Others: no execute
 │││││└── Others: no write
 ││││└─── Others: CAN READ ❌ (WRONG!)
 │││└──── Group: no execute
 ││└───── Group: no write
 │└────── Group: CAN READ ❌ (WRONG!)
 └─────── Owner: CAN READ ✅
```

### After (Correct)
```
-r--------  1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem
 ││││││││
 ││││││└─ Others: no execute
 │││││└── Others: no write
 ││││└─── Others: no read ✅ (CORRECT!)
 │││└──── Group: no execute
 ││└───── Group: no write
 │└────── Group: no read ✅ (CORRECT!)
 └─────── Owner: CAN READ ✅ (CORRECT!)
```

---

## Success Checklist

- [ ] Terminal opened
- [ ] .ssh folder created
- [ ] SSH key file moved to ~/.ssh/
- [ ] Permissions set to 400
- [ ] Permissions verified (shows `-r--------`)
- [ ] SSH connection tested successfully
- [ ] Can see EC2 welcome message
- [ ] Exited connection successfully

**All checked? You're ready to deploy!** ✅

---

## Next Steps

1. ✅ SSH key setup complete
2. → Go to `DETAILED_STEPS.md` - Step 7: Copy Project to EC2

---

## Quick Reference

| Task | Command |
|------|---------|
| Create .ssh | `mkdir -p ~/.ssh` |
| Move key | `mv ~/Downloads/nitro-swim-key.pem ~/.ssh/` |
| Set permissions | `chmod 400 ~/.ssh/nitro-swim-key.pem` |
| Verify permissions | `ls -la ~/.ssh/nitro-swim-key.pem` |
| Test connection | `ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP` |
| Exit connection | `exit` |

---

## You're All Set! ✅

Your SSH key is now properly configured and ready to use!
