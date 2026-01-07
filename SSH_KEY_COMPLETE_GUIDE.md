# Complete SSH Key Setup Guide - Everything You Need

## Overview

This guide covers everything about SSH keys for your EC2 deployment:
- What SSH keys are
- How to download them
- Where to save them
- How to set permissions
- How to use them
- Troubleshooting

---

## What is an SSH Key?

### Simple Explanation

An SSH key is like a special password that's more secure:
- **Public key** - Like your email address (you share it)
- **Private key** (.pem file) - Like your password (you keep it secret)

When you connect to EC2:
1. Your computer sends the public key
2. EC2 checks if it matches
3. If it matches, you're allowed in

### Why Use SSH Keys?

✅ More secure than passwords
✅ Can't be guessed
✅ Can't be brute-forced
✅ Industry standard

---

## Part 1: Download SSH Key from AWS

### Step 1: Go to AWS Console

1. Open browser
2. Go to https://console.aws.amazon.com
3. Sign in with your email and password

### Step 2: Navigate to EC2

1. In search bar at top, type "EC2"
2. Click "EC2" from dropdown
3. You're in EC2 Dashboard

### Step 3: Launch Instance

1. Click orange "Launch Instance" button
2. Follow the instance setup steps

### Step 4: Create Key Pair

When you see "Key pair (login)" section:

1. Click dropdown: "Create new key pair"
2. Dialog appears with options:
   - **Key pair name:** Type `nitro-swim-key`
   - **Key pair type:** Keep "RSA" selected
   - **Private key file format:** Keep ".pem" selected

3. Click "Create key pair"

### Step 5: File Downloads

**What happens:**
- File `nitro-swim-key.pem` downloads automatically
- Usually goes to `~/Downloads/`
- This is your private key

**Important:** This is the ONLY time you can download this key!
- If you lose it, you'll need to create a new one
- Save it safely!

### Step 6: Verify Download

1. Open Finder
2. Go to Downloads folder
3. Look for `nitro-swim-key.pem`
4. You should see it there

---

## Part 2: Save SSH Key to Correct Location

### Why Location Matters

SSH looks for keys in specific locations:
- `~/.ssh/` is the standard location
- SSH won't find keys in Downloads
- You need to move it to `~/.ssh/`

### Step 1: Open Terminal

**On macOS:**
1. Press `Cmd + Space`
2. Type "Terminal"
3. Press Enter

**You should see:**
```
Last login: Fri Jan 03 20:00:00 on ttys000
yourname@yourcomputer ~ %
```

### Step 2: Create .ssh Folder

Type this command:
```bash
mkdir -p ~/.ssh
```

**What this does:**
- Creates a hidden folder named `.ssh` in your home directory
- The `-p` flag means "create if it doesn't exist"

**Press Enter**

### Step 3: Navigate to Downloads

Type:
```bash
cd ~/Downloads
```

**You should see:**
```
yourname@yourcomputer Downloads %
```

### Step 4: Verify Key File Exists

Type:
```bash
ls -la nitro-swim-key.pem
```

**You should see:**
```
-rw-r--r--  1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem
```

If you see "No such file or directory":
- Check Downloads folder in Finder
- Make sure file name is exactly `nitro-swim-key.pem`

### Step 5: Move File to .ssh

Type:
```bash
mv nitro-swim-key.pem ~/.ssh/
```

**What this does:**
- Moves the file from Downloads to .ssh folder
- `mv` = move command
- `nitro-swim-key.pem` = source file
- `~/.ssh/` = destination folder

**Press Enter**

### Step 6: Verify File Moved

Type:
```bash
ls -la ~/.ssh/
```

**You should see:**
```
total 8
drwx------   3 yourname  staff    96 Jan  3 20:00 .
drwxr-xr-x  27 yourname  staff   864 Jan  3 20:00 ..
-rw-r--r--   1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem
```

**Look for:** `nitro-swim-key.pem` in the list

The file is now in the right place! ✅

---

## Part 3: Set Proper Permissions

### Why Permissions Matter

SSH requires specific permissions for security:
- Only you can read the file
- Nobody else can access it
- SSH will refuse to use it if permissions are wrong

### Step 1: Set Permissions

Type:
```bash
chmod 400 ~/.ssh/nitro-swim-key.pem
```

**What this does:**
- `chmod` = change permissions
- `400` = read-only for owner, no access for others
- `~/.ssh/nitro-swim-key.pem` = the file

**Press Enter**

### Step 2: Verify Permissions

Type:
```bash
ls -la ~/.ssh/nitro-swim-key.pem
```

**You should see:**
```
-r--------  1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem
```

**Important:** Look for `-r--------` at the beginning

**Breakdown:**
- `-` = it's a file
- `r` = owner can read
- `--------` = nobody else can do anything

This is correct! ✅

---

## Part 4: Test SSH Connection

### Step 1: Get Your EC2 IP Address

From AWS Console:
1. Go to EC2 Dashboard
2. Click "Instances"
3. Find your instance
4. Look at "Public IPv4 address" column
5. Copy the IP (e.g., `54.123.45.67`)

### Step 2: Test Connection

Type:
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67
```

**Replace `54.123.45.67` with your actual IP**

**What this does:**
- `ssh` = secure shell command
- `-i` = use this identity (key) file
- `~/.ssh/nitro-swim-key.pem` = path to your key
- `ec2-user@54.123.45.67` = username and IP

**Press Enter**

### Step 3: First Connection

**You'll see:**
```
The authenticity of host '54.123.45.67 (54.123.45.67)' can't be established.
ECDSA key fingerprint is SHA256:xxxxx...
Are you sure you want to continue connecting (yes/no)?
```

**Type:** `yes`
**Press Enter**

### Step 4: Connected!

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

**You're now connected to your EC2 instance!** ✅

### Step 5: Exit Connection

Type:
```bash
exit
```

**You should see:**
```
logout
Connection to 54.123.45.67 closed.
yourname@yourcomputer Downloads %
```

You're back on your local machine! ✅

---

## Part 5: Understanding Permissions

### Permission Codes Explained

```
-r--------
││││││││
││││││└─ Others: execute (no)
│││││└── Others: write (no)
││││└─── Others: read (no)
│││└──── Group: execute (no)
││└───── Group: write (no)
│└────── Group: read (no)
└─────── Owner: execute (no)
```

Wait, owner can't execute? That's fine for a key file!

### What 400 Means

- `4` = read permission for owner only
- `0` = no permissions for group
- `0` = no permissions for others

**Result:** Only you can read the file, nobody else can access it

### Other Common Permissions

| Code | Meaning | Use Case |
|------|---------|----------|
| 400 | Read-only for owner | SSH keys (most secure) |
| 600 | Read/write for owner | SSH keys (alternative) |
| 644 | Read for all, write for owner | Regular files |
| 755 | Execute for all, write for owner | Scripts |

**For SSH keys, always use 400 or 600!**

---

## Part 6: Troubleshooting

### Problem 1: "No such file or directory"

**What you see:**
```
ls: nitro-swim-key.pem: No such file or directory
```

**Cause:** File not in Downloads folder

**Solution:**
1. Check Downloads folder in Finder
2. Make sure file name is exactly `nitro-swim-key.pem`
3. Try: `ls -la ~/Downloads/` to see all files

### Problem 2: "Permission denied (publickey)"

**What you see:**
```
Permission denied (publickey).
```

**Cause:** SSH key permissions are wrong

**Solution:**
```bash
# Check permissions
ls -la ~/.ssh/nitro-swim-key.pem

# Should show: -r--------
# If not, fix it:
chmod 400 ~/.ssh/nitro-swim-key.pem
```

### Problem 3: "Connection refused"

**What you see:**
```
ssh: connect to host 54.123.45.67 port 22: Connection refused
```

**Cause:** EC2 instance not running or not ready

**Solution:**
1. Check EC2 instance is running in AWS Console
2. Wait 2-3 minutes for instance to fully start
3. Verify IP address is correct

### Problem 4: "Connection timed out"

**What you see:**
```
ssh: connect to host 54.123.45.67 port 22: Operation timed out
```

**Cause:** Security group doesn't allow SSH

**Solution:**
1. Go to AWS Console
2. EC2 → Security Groups
3. Edit inbound rules
4. Allow SSH (port 22) from your IP

### Problem 5: "No such file or directory" (after moving)

**What you see:**
```
ssh: /Users/yourname/.ssh/nitro-swim-key.pem: No such file or directory
```

**Cause:** File not moved to .ssh folder

**Solution:**
```bash
# Check if file is in .ssh
ls -la ~/.ssh/

# If not there, move it:
mv ~/Downloads/nitro-swim-key.pem ~/.ssh/
```

---

## Part 7: Security Best Practices

### ✅ DO

- Keep .pem file in `~/.ssh/`
- Set permissions to 400
- Never share the .pem file
- Never commit to Git
- Backup the file safely
- Use different keys for different purposes
- Rotate keys periodically

### ❌ DON'T

- Share the .pem file with anyone
- Upload to GitHub or public places
- Change permissions to 644 or 777
- Leave it in Downloads folder
- Use the same key for multiple purposes
- Commit to version control
- Store in cloud storage without encryption

---

## Part 8: Quick Reference

### All Commands in One Place

```bash
# Create .ssh folder
mkdir -p ~/.ssh

# Navigate to Downloads
cd ~/Downloads

# Verify key file exists
ls -la nitro-swim-key.pem

# Move key to .ssh
mv nitro-swim-key.pem ~/.ssh/

# Verify file moved
ls -la ~/.ssh/nitro-swim-key.pem

# Set permissions
chmod 400 ~/.ssh/nitro-swim-key.pem

# Verify permissions
ls -la ~/.ssh/nitro-swim-key.pem

# Test connection (replace IP)
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67

# Exit connection
exit
```

---

## Part 9: File Locations

### Where Everything Goes

```
Your Computer
│
├── Home Directory (~)
│   │   (e.g., /Users/yourname/)
│   │
│   ├── Downloads/
│   │   └── nitro-swim-key.pem  ← Downloaded here
│   │
│   └── .ssh/
│       └── nitro-swim-key.pem  ← Final location
│
└── (Other folders)
```

### Path Examples

| Item | Path |
|------|------|
| Home directory | `~` or `/Users/yourname/` |
| Downloads folder | `~/Downloads/` or `/Users/yourname/Downloads/` |
| .ssh folder | `~/.ssh/` or `/Users/yourname/.ssh/` |
| Key file | `~/.ssh/nitro-swim-key.pem` |

---

## Part 10: Common Questions

### Q: Where is my home directory?
**A:** Type `echo ~` in Terminal to see the full path

### Q: Can I use a different folder?
**A:** Yes, but `~/.ssh/` is the standard location. SSH looks there by default.

### Q: What if I lose the .pem file?
**A:** You'll need to create a new key pair and relaunch the EC2 instance.

### Q: Can I use the same key for multiple instances?
**A:** Yes, you can reuse the same key for multiple EC2 instances.

### Q: Is 400 permission the only option?
**A:** 400 and 600 both work. 400 is more secure (read-only).

### Q: How do I know if permissions are correct?
**A:** Run `ls -la ~/.ssh/nitro-swim-key.pem` and look for `-r--------`

### Q: Can I change the key name?
**A:** Yes, but remember to use the new name in SSH commands.

### Q: What if I accidentally deleted the key?
**A:** You'll need to create a new key pair in AWS and relaunch the instance.

### Q: Is it safe to backup the key?
**A:** Yes, backup it safely. Store backups securely (encrypted).

### Q: Can I use the key on multiple computers?
**A:** Yes, copy the key to `~/.ssh/` on each computer.

---

## Part 11: Complete Example Session

Here's what a complete session looks like from start to finish:

```bash
# 1. Create .ssh folder
yourname@yourcomputer ~ % mkdir -p ~/.ssh

# 2. Go to Downloads
yourname@yourcomputer ~ % cd ~/Downloads

# 3. Verify key file
yourname@yourcomputer Downloads % ls -la nitro-swim-key.pem
-rw-r--r--  1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem

# 4. Move file
yourname@yourcomputer Downloads % mv nitro-swim-key.pem ~/.ssh/

# 5. Verify moved
yourname@yourcomputer Downloads % ls -la ~/.ssh/nitro-swim-key.pem
-rw-r--r--  1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem

# 6. Set permissions
yourname@yourcomputer Downloads % chmod 400 ~/.ssh/nitro-swim-key.pem

# 7. Verify permissions
yourname@yourcomputer Downloads % ls -la ~/.ssh/nitro-swim-key.pem
-r--------  1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem

# 8. Test connection
yourname@yourcomputer Downloads % ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67
The authenticity of host '54.123.45.67 (54.123.45.67)' can't be established.
ECDSA key fingerprint is SHA256:abcdef1234567890...
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '54.123.45.67' (ECDSA) to the list of known hosts.
Welcome to Ubuntu 20.04.X LTS (GNU/Linux 5.10.0-1234-aws x86_64)
...
ec2-user@ip-172-31-xx-xx:~$

# 9. Exit
ec2-user@ip-172-31-xx-xx:~$ exit
logout
Connection to 54.123.45.67 closed.
yourname@yourcomputer Downloads %
```

---

## Success Checklist

- [ ] SSH key downloaded from AWS
- [ ] .ssh folder created
- [ ] SSH key moved to ~/.ssh/
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

## Additional Resources

### Related Documentation
- `SSH_KEY_SETUP.md` - Detailed setup guide
- `SSH_KEY_VISUAL_GUIDE.md` - Visual terminal walkthrough
- `DETAILED_STEPS.md` - Complete deployment guide
- `COMMAND_REFERENCE.md` - All commands

### External Resources
- [AWS EC2 Key Pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)
- [SSH Documentation](https://man.openbsd.org/ssh)
- [Linux File Permissions](https://www.linux.com/training-tutorials/understanding-linux-file-permissions/)

---

## You're All Set! ✅

Your SSH key is now:
- ✅ Downloaded from AWS
- ✅ Saved in the correct location
- ✅ Has correct permissions
- ✅ Tested and working
- ✅ Ready for EC2 deployment

**Ready to deploy? Go to `DETAILED_STEPS.md` - Step 7!**
