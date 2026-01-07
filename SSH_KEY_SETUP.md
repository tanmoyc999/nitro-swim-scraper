# SSH Key Setup - Step by Step

## What is an SSH Key?

An SSH key is like a password, but more secure. It has two parts:
- **Public key** - You give this to AWS
- **Private key** (.pem file) - You keep this secret on your computer

The .pem file is what you download from AWS. You need to save it safely and set proper permissions.

---

## Step 1: Download SSH Key from AWS

### 1.1 During EC2 Instance Launch

When you launch an EC2 instance, AWS asks you to create or select a key pair.

**What you see:**
```
Key pair (login)
[Create new key pair ▼]
```

### 1.2 Create New Key Pair

1. Click "Create new key pair"
2. A dialog appears with options:
   - **Key pair name:** `nitro-swim-key`
   - **Key pair type:** RSA (keep selected)
   - **Private key file format:** .pem (keep selected)

3. Click "Create key pair"

### 1.3 File Downloads

**What happens:**
- File `nitro-swim-key.pem` automatically downloads to your computer
- Usually goes to: `~/Downloads/`
- This is your private key - keep it safe!

### 1.4 Verify Download

Open Finder:
1. Press `Cmd + Space`
2. Type "Finder"
3. Press Enter
4. Go to Downloads folder
5. Look for `nitro-swim-key.pem`

You should see it there.

---

## Step 2: Create .ssh Directory

### 2.1 Open Terminal

**On macOS:**
1. Press `Cmd + Space`
2. Type "Terminal"
3. Press Enter

**You should see:**
```
Last login: Fri Jan 03 20:00:00 on ttys000
yourname@yourcomputer ~ %
```

### 2.2 Create .ssh Folder

Type this command:
```bash
mkdir -p ~/.ssh
```

**What this does:**
- `mkdir` = make directory
- `-p` = create parent directories if needed
- `~/.ssh` = creates folder named `.ssh` in your home directory

**Press Enter**

### 2.3 Verify Folder Created

Type:
```bash
ls -la ~/
```

**You should see:**
```
drwx------   5 yourname  staff   160 Jan  3 20:00 .ssh
```

The `.ssh` folder is now created!

---

## Step 3: Move SSH Key to .ssh Folder

### 3.1 Navigate to Downloads

Type:
```bash
cd ~/Downloads
```

**You should see:**
```
yourname@yourcomputer Downloads %
```

### 3.2 Verify Key File Exists

Type:
```bash
ls -la nitro-swim-key.pem
```

**You should see:**
```
-rw-r--r--  1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem
```

### 3.3 Move File to .ssh

Type:
```bash
mv nitro-swim-key.pem ~/.ssh/
```

**What this does:**
- `mv` = move file
- `nitro-swim-key.pem` = source file
- `~/.ssh/` = destination folder

**Press Enter**

### 3.4 Verify File Moved

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

The file is now in `~/.ssh/`!

---

## Step 4: Set Proper Permissions

### 4.1 Why Permissions Matter

SSH requires the key file to have specific permissions for security:
- Only you can read it
- Nobody else can access it
- SSH will refuse to use it if permissions are wrong

### 4.2 Set Permissions

Type:
```bash
chmod 400 ~/.ssh/nitro-swim-key.pem
```

**What this does:**
- `chmod` = change mode (permissions)
- `400` = read-only for owner, no access for others
- `~/.ssh/nitro-swim-key.pem` = the file

**Press Enter**

### 4.3 Verify Permissions

Type:
```bash
ls -la ~/.ssh/nitro-swim-key.pem
```

**You should see:**
```
-r--------  1 yourname  staff  1704 Jan  3 20:00 nitro-swim-key.pem
```

**Important:** Look for `-r--------` at the beginning
- First `-` = it's a file
- `r` = read permission for owner only
- `--------` = no permissions for group or others

This is correct! ✅

---

## Step 5: Test SSH Key

### 5.1 Get Your EC2 IP Address

From AWS Console:
- Go to EC2 Dashboard
- Click "Instances"
- Find your instance
- Copy "Public IPv4 address" (e.g., `54.123.45.67`)

### 5.2 Test Connection

Type:
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@54.123.45.67
```

**Replace `54.123.45.67` with your actual IP**

### 5.3 First Connection

**You'll see:**
```
The authenticity of host '54.123.45.67 (54.123.45.67)' can't be established.
ECDSA key fingerprint is SHA256:xxxxx...
Are you sure you want to continue connecting (yes/no)?
```

Type: `yes`
Press Enter

### 5.4 Connected!

**You should see:**
```
Welcome to Ubuntu 20.04.X LTS (GNU/Linux 5.10.0-1234-aws x86_64)

ec2-user@ip-172-31-xx-xx:~$
```

You're now connected to your EC2 instance! ✅

### 5.5 Exit Connection

Type:
```bash
exit
```

You're back on your local machine.

---

## Troubleshooting

### Issue: "Permission denied (publickey)"

**Cause:** SSH key permissions are wrong

**Fix:**
```bash
chmod 400 ~/.ssh/nitro-swim-key.pem
```

### Issue: "No such file or directory"

**Cause:** File not in correct location

**Fix:**
1. Check file location:
```bash
ls -la ~/.ssh/nitro-swim-key.pem
```

2. If not found, move it:
```bash
mv ~/Downloads/nitro-swim-key.pem ~/.ssh/
```

### Issue: "Connection refused"

**Cause:** EC2 instance not running or wrong IP

**Fix:**
1. Check instance is running in AWS Console
2. Verify IP address is correct
3. Wait 2-3 minutes for instance to fully start

### Issue: "Connection timed out"

**Cause:** Security group doesn't allow SSH

**Fix:**
1. Go to AWS Console
2. EC2 → Security Groups
3. Edit inbound rules
4. Allow SSH (port 22) from your IP

---

## File Locations Summary

| Item | Location |
|------|----------|
| Downloaded file | `~/Downloads/nitro-swim-key.pem` |
| Final location | `~/.ssh/nitro-swim-key.pem` |
| Home directory | `~` (e.g., `/Users/yourname/`) |
| SSH folder | `~/.ssh/` (e.g., `/Users/yourname/.ssh/`) |

---

## Permissions Explained

### What Each Permission Means

```
-r--------
│││││││││
││││││││└─ Others: execute (no)
│││││││└── Others: write (no)
││││││└─── Others: read (no)
│││││└──── Group: execute (no)
││││└───── Group: write (no)
│││└────── Group: read (no)
││└─────── Owner: execute (no)
│└──────── Owner: write (no)
└───────── Owner: read (yes)
```

**400 means:**
- Owner: read only (r)
- Group: no access (-)
- Others: no access (-)

This is the correct permission for SSH keys!

---

## Security Best Practices

✅ **DO:**
- Keep .pem file in `~/.ssh/`
- Set permissions to 400
- Never share the .pem file
- Never commit to Git
- Backup the file safely

❌ **DON'T:**
- Share the .pem file with anyone
- Upload to GitHub or public places
- Change permissions to 644 or 777
- Leave it in Downloads folder
- Use the same key for multiple purposes

---

## Quick Reference

### Create .ssh folder
```bash
mkdir -p ~/.ssh
```

### Move key file
```bash
mv ~/Downloads/nitro-swim-key.pem ~/.ssh/
```

### Set permissions
```bash
chmod 400 ~/.ssh/nitro-swim-key.pem
```

### Verify permissions
```bash
ls -la ~/.ssh/nitro-swim-key.pem
```

### Test connection
```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@YOUR_IP
```

### Exit connection
```bash
exit
```

---

## Next Steps

Once your SSH key is set up:

1. ✅ SSH key saved to `~/.ssh/nitro-swim-key.pem`
2. ✅ Permissions set to 400
3. ✅ Connection tested successfully
4. → Go to `DETAILED_STEPS.md` - Step 7: Copy Project to EC2

---

## Common Questions

### Q: Where is my home directory?
**A:** Type `echo ~` in Terminal to see the full path

### Q: Can I use a different folder?
**A:** Yes, but `~/.ssh/` is the standard location

### Q: What if I lose the .pem file?
**A:** You'll need to create a new key pair and relaunch the instance

### Q: Can I use the same key for multiple instances?
**A:** Yes, you can reuse the same key for multiple EC2 instances

### Q: Is 400 permission the only option?
**A:** Yes, SSH requires exactly 400 (or 600 with write permission, but 400 is safer)

### Q: How do I know if permissions are correct?
**A:** Run `ls -la ~/.ssh/nitro-swim-key.pem` and look for `-r--------`

---

## You're All Set! ✅

Your SSH key is now:
- ✅ Saved in the correct location
- ✅ Has correct permissions
- ✅ Ready to use for EC2 connection

**Next:** Go to `DETAILED_STEPS.md` - Step 7 to copy your project to EC2!
