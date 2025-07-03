#!/usr/bin/env python3
"""Simple test to verify the lister works"""

from lister import AutoLister

print("🧪 Testing Auto Lister...")

# Test item loading
lister = AutoLister()
items = lister.load_items()

print(f"✅ Successfully loaded {len(items)} items:")
for item in items:
    print(f"  - {item.get('title', 'Unknown')} (${item.get('price', 'N/A')})")
    print(f"    Folder: {item['folder']}")

print("\n✅ Item loading test passed!")
print("🔧 Note: Browser automation would start when running 'python lister.py'")
