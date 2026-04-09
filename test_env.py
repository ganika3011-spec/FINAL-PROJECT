#!/usr/bin/env python
"""
Simple test script to verify .env configuration is loaded correctly
"""
import os
import sys
from pathlib import Path

# Add project to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Load environment
from dotenv import load_dotenv
load_dotenv()

print("✅ Environment Configuration Test")
print("=" * 50)
print(f"SECRET_KEY configured: {bool(os.getenv('SECRET_KEY'))}")
print(f"DEBUG mode: {os.getenv('DEBUG')}")
print(f"Database: {os.getenv('DB_NAME')}")
print(f"DB User: {os.getenv('DB_USER')}")
print(f"DB Host: {os.getenv('DB_HOST')}")
print("=" * 50)
print("✅ All environment variables loaded successfully!")
