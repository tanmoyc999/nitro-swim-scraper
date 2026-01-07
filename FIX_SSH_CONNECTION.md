# Fix SSH Connection - Nuclear Option

## The Problem

Instance 3.15.186.224 shows `nitro-swim-key` as the key pair, but SSH still fails with "Permission denied (publickey)".

This usually means:
1. Instance wasn't actually created with this key
2. Instance is still initializing
3. Key mismatch in AWS

## The Solution: Terminate and Recreate

### Step 1: Terminate Current Instance

1. Go to AWS Console: https://console.aws.amazon.com
2. EC2 → Instances
3. Select instance `3.15.186.224`
4. Click "Instance State" (top right)
5. Click "Terminate instance"
6. Click "Terminate" to confirm
7. Wait for it to terminate (30 seconds)

### Step 2: Launch New Instance

1. Click "Launch Instance" button
2. Fill in:
   - **Name:** `nitro-swim-scraper`
   - **AMI:** Ubuntu Server 20.04 LTS (free tier eligible)
   - **Instance Type:** t2.micro (free tier eligible)

3. **Key pair:** Click dropdown
   - Select: `nitro-swim-key`
   - **IMPORTANT:** Make sure it says `nitro-swim-key`

4. **Network settings:**
   - VPC: default
   - Subnet: default
   - Auto-assign public IP: Enable

5. **Firewall (security group):**
   - Select: Create security group
   - Name: `nitro-swim-sg`
   - Description: `Security group for Nitro Swim scraper`
   - Inbound rules:
     - Type: SSH
     - Port: 22
     - Source: 0.0.0.0/0 (or your IP)

6. **Storage:**
   - Keep default (20 GB)

7. Click "Launch Instance"

### Step 3: Wait for Instance to Start

1. Go to EC2 → Instances
2. Find your new instance
3. Wait for:
   - Instance State: "running"
   - Status checks: "2/2 checks passed"
4. This takes 2-3 minutes

### Step 4: Get New IP Address

1. Select your instance
2. Copy "Public IPv4 address"
3. Example: `54.123.45.67`

### Step 5: Connect

```bash
ssh -i ~/.ssh/nitro-swim-key.pem ec2-user@NEW_IP
```

Replace `NEW_IP` with your actual IP

### Step 6: Verify Connection

You should see:
```
Welcome to Ubuntu 20.04.X LTS (GNU/Linux 5.10.0-1234-aws x86_64)
...
ec2-user@ip-172-31-xx-xx:~$
```

### Step 7: Exit

```bash
exit
```

---

## If Still Not Working

Try this diagnostic:

```bash
# Check key file
ls -la ~/.ssh/nitro-swim-key.pem

# Should show: -r--------

# Try with verbose output
ssh -vvv -i ~/.ssh/nitro-swim-key.pem ec2-user@NEW_IP

# Look for "Offering public key" in output
```

---

## Alternative: Use EC2 Instance Connect

If SSH still doesn't work:

1. Go to AWS Console
2. EC2 → Instances
3. Select your instance
4. Click "Connect" button (top right)
5. Click "EC2 Instance Connect" tab
6. Click "Connect"
7. Browser opens terminal to your instance

This bypasses SSH entirely!

---

## Once Connected

After you successfully connect, run:

```bash
cd nitro_swim_scraper
chmod +x setup_ec2.sh
./setup_ec2.sh
```

---

## Quick Checklist

- [ ] Old instance terminated
- [ ] New instance launched with `nitro-swim-key`
- [ ] Instance is "running"
- [ ] Status checks show "2/2 checks passed"
- [ ] Public IPv4 address copied
- [ ] SSH connection successful
- [ ] See Ubuntu welcome message
- [ ] Exited with `exit` command

---

## You're Almost There!

Once you get SSH working, the deployment is just a few commands away!
