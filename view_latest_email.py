#!/usr/bin/env python
"""
Helper script to view the latest verification email
Usage: python view_latest_email.py
"""
import os
import glob
from pathlib import Path

SENT_EMAILS_DIR = Path('sent_emails')

if not SENT_EMAILS_DIR.exists():
    print("❌ No sent_emails directory found!")
    exit(1)

# Get all email files
email_files = sorted(glob.glob(str(SENT_EMAILS_DIR / '*.log')), key=os.path.getctime, reverse=True)

if not email_files:
    print("❌ No email files found in sent_emails directory!")
    exit(1)

# Read the latest email
latest_email = email_files[0]
print(f"📧 Latest Email: {Path(latest_email).name}\n")
print("=" * 80)

with open(latest_email, 'r') as f:
    content = f.read()
    # Extract the activation link from the email
    if '/accounts/activate/' in content:
        # Find the activation link
        start = content.find('http://localhost:8000/accounts/activate/')
        if start != -1:
            end = content.find('"', start)
            if end != -1:
                activation_link = content[start:end]
                print("\n✅ ACTIVATION LINK:\n")
                print(activation_link)
                print("\n" + "=" * 80)
    
    print("\n📝 Full Email Content:\n")
    print(content)
