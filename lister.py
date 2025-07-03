#!/usr/bin/env python3
"""
Auto Lister - Automated listing management for second-hand items
Manages listings across Facebook Marketplace, Kijiji, and eBay using Playwright
"""

import json
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
import time
import random

class AutoLister:
    def __init__(self, items_dir="items", browser_data_dir="browser_data"):
        self.items_dir = Path(items_dir)
        self.browser_data_dir = Path(browser_data_dir)
        self.browser_data_dir.mkdir(exist_ok=True)
        
        self.platforms = {
            'facebook': {
                'url': 'https://www.facebook.com/marketplace',
                'name': 'Facebook Marketplace'
            },
            'kijiji': {
                'url': 'https://www.kijiji.ca',
                'name': 'Kijiji'
            },
            'ebay': {
                'url': 'https://www.ebay.com',
                'name': 'eBay'
            }
        }
        
        self.playwright = None
        self.browser = None
        self.context = None

    def start_browser(self):
        """Start browser with persistent context"""
        try:
            self.playwright = sync_playwright().start()
            
            # Use persistent context to maintain login sessions
            context_dir = self.browser_data_dir / "context"
            context_dir.mkdir(exist_ok=True)
            
            self.context = self.playwright.chromium.launch_persistent_context(
                user_data_dir=str(context_dir),
                headless=False,
                args=['--no-sandbox', '--disable-dev-shm-usage'],
                viewport={'width': 1280, 'height': 720}
            )
            
            # For persistent context, browser is None since we use context directly
            self.browser = None
            
            print("✓ Browser started with persistent session")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start browser: {e}")
            print("\nTry running: python setup.py")
            return False

    def stop_browser(self):
        """Clean up browser resources"""
        if self.context:
            self.context.close()
        # No need to close browser separately when using persistent context
        if self.playwright:
            self.playwright.stop()

    def ask_platform_preferences(self):
        """Ask user which platforms they want to use"""
        print("🔧 Platform Setup")
        print("=" * 30)
        
        selected_platforms = []
        
        for platform_key, platform_info in self.platforms.items():
            while True:
                response = input(f"Do you want to use {platform_info['name']}? (y/n): ").strip().lower()
                if response in ['y', 'yes']:
                    selected_platforms.append(platform_key)
                    print(f"✅ {platform_info['name']} added")
                    break
                elif response in ['n', 'no']:
                    print(f"⏭️  {platform_info['name']} skipped")
                    break
                else:
                    print("Please enter 'y' for yes or 'n' for no")
        
        if not selected_platforms:
            print("\n❌ No platforms selected. Exiting...")
            return None
        
        print(f"\n✅ Selected platforms: {', '.join([self.platforms[p]['name'] for p in selected_platforms])}")
        return selected_platforms

    def login_check_and_wait(self, platform_key, platform_info):
        """Open platform main page and wait for user login"""
        print(f"\n🔐 Login Check: {platform_info['name']}")
        print("-" * 40)
        
        page = self.context.new_page()
        
        # Navigate to main platform URL
        main_url = platform_info['url']
        print(f"📂 Opening {platform_info['name']}...")
        page.goto(main_url)
        self.human_delay(2, 4)
        
        print(f"🔍 Please check if you're logged into {platform_info['name']}")
        print("   - If not logged in, please log in now")
        print("   - If already logged in, you're ready to continue")
        
        input(f"   Press Enter when you're logged into {platform_info['name']}...")
        
        print(f"✅ Ready to proceed with {platform_info['name']}")
        return page

    def load_items(self):
        """Load all items from the items directory"""
        items = []
        
        if not self.items_dir.exists():
            print(f"❌ Items directory '{self.items_dir}' not found")
            return items
            
        for item_dir in self.items_dir.iterdir():
            if item_dir.is_dir():
                info_file = item_dir / "info.json"
                if info_file.exists():
                    try:
                        with open(info_file, 'r') as f:
                            item_data = json.load(f)
                            item_data['folder'] = item_dir.name
                            item_data['path'] = item_dir
                            items.append(item_data)
                    except Exception as e:
                        print(f"⚠️  Failed to load {info_file}: {e}")
                else:
                    print(f"⚠️  No info.json found in {item_dir}")
        
        return items

    def human_delay(self, min_seconds=1, max_seconds=3):
        """Add human-like delay between actions"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

    def check_facebook_listing(self, page, item):
        """Check if item exists on Facebook Marketplace and compare data"""
        try:
            print(f"   📋 Checking Facebook for: {item.get('title', 'Unknown')}")
            page.goto("https://www.facebook.com/marketplace/you/selling")
            self.human_delay(2, 4)
            
            # Look for the item title in listings
            title = item.get('title', '')
            if title:
                # Check if any listing contains the title
                page_content = page.content().lower()
                if title.lower() in page_content:
                    print(f"   ✅ Found existing listing on Facebook")
                    # Could add price/description comparison here
                    return True
            
            print(f"   📝 No existing listing found on Facebook")
            return False
            
        except Exception as e:
            print(f"   ⚠️  Error checking Facebook listing: {e}")
            return None

    def check_kijiji_listing(self, page, item):
        """Check if item exists on Kijiji and compare data"""
        try:
            print(f"   📋 Checking Kijiji for: {item.get('title', 'Unknown')}")
            page.goto("https://www.kijiji.ca/m-my-ads.html")
            self.human_delay(2, 4)
            
            title = item.get('title', '')
            if title:
                # Check if any listing contains the title
                page_content = page.content().lower()
                if title.lower() in page_content:
                    print(f"   ✅ Found existing listing on Kijiji")
                    return True
            
            print(f"   📝 No existing listing found on Kijiji")
            return False
            
        except Exception as e:
            print(f"   ⚠️  Error checking Kijiji listing: {e}")
            return None

    def check_ebay_listing(self, page, item):
        """Check if item exists on eBay and compare data"""
        try:
            print(f"   📋 Checking eBay for: {item.get('title', 'Unknown')}")
            page.goto("https://www.ebay.com/mys/active")
            self.human_delay(2, 4)
            
            title = item.get('title', '')
            if title:
                # Check if any listing contains the title
                page_content = page.content().lower()
                if title.lower() in page_content:
                    print(f"   ✅ Found existing listing on eBay")
                    return True
            
            print(f"   📝 No existing listing found on eBay")
            return False
            
        except Exception as e:
            print(f"   ⚠️  Error checking eBay listing: {e}")
            return None

    def post_to_facebook(self, page, item):
        """Post item to Facebook Marketplace"""
        try:
            page.goto("https://www.facebook.com/marketplace/create/item")
            self.human_delay(3, 5)
            
            # Fill in basic information
            title_input = page.wait_for_selector('input[placeholder*="title" i], input[aria-label*="title" i]', timeout=10000)
            if title_input:
                title_input.fill(item.get('title', ''))
                self.human_delay(1, 2)
            
            # Price
            price_input = page.query_selector('input[placeholder*="price" i], input[aria-label*="price" i]')
            if price_input:
                price_input.fill(str(item.get('price', '')))
                self.human_delay(1, 2)
            
            # Description
            desc_input = page.query_selector('textarea[placeholder*="description" i], textarea[aria-label*="description" i]')
            if desc_input:
                desc_input.fill(item.get('description', ''))
                self.human_delay(1, 2)
            
            print(f"✓ Facebook form filled for '{item.get('title', 'Unknown')}'")
            print("  Please complete the posting manually (add photos, select category, etc.)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error posting to Facebook: {e}")
            return False

    def post_to_kijiji(self, page, item):
        """Post item to Kijiji"""
        try:
            page.goto("https://www.kijiji.ca/p-post-ad.html")
            self.human_delay(3, 5)
            
            # Fill in basic information
            title_input = page.wait_for_selector('input[id*="title"], input[name*="title"]', timeout=10000)
            if title_input:
                title_input.fill(item.get('title', ''))
                self.human_delay(1, 2)
            
            # Description
            desc_input = page.query_selector('textarea[id*="description"], textarea[name*="description"]')
            if desc_input:
                desc_input.fill(item.get('description', ''))
                self.human_delay(1, 2)
            
            # Price
            price_input = page.query_selector('input[id*="price"], input[name*="price"]')
            if price_input:
                price_input.fill(str(item.get('price', '')))
                self.human_delay(1, 2)
            
            print(f"✓ Kijiji form filled for '{item.get('title', 'Unknown')}'")
            print("  Please complete the posting manually (add photos, select category, etc.)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error posting to Kijiji: {e}")
            return False

    def post_to_ebay(self, page, item):
        """Post item to eBay"""
        try:
            page.goto("https://www.ebay.com/sl/sell")
            self.human_delay(3, 5)
            
            # Fill in basic information
            title_input = page.wait_for_selector('input[id*="title"], input[name*="title"]', timeout=10000)
            if title_input:
                title_input.fill(item.get('title', ''))
                self.human_delay(1, 2)
            
            # Description
            desc_input = page.query_selector('textarea, iframe[title*="description"]')
            if desc_input:
                if desc_input.tag_name.lower() == 'iframe':
                    # Handle iframe editor
                    frame = page.frame(url=desc_input.get_attribute('src'))
                    if frame:
                        body = frame.query_selector('body')
                        if body:
                            body.fill(item.get('description', ''))
                else:
                    desc_input.fill(item.get('description', ''))
                self.human_delay(1, 2)
            
            # Price
            price_input = page.query_selector('input[id*="price"], input[name*="price"]')
            if price_input:
                price_input.fill(str(item.get('price', '')))
                self.human_delay(1, 2)
            
            print(f"✓ eBay form filled for '{item.get('title', 'Unknown')}'")
            print("  Please complete the posting manually (add photos, select category, etc.)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error posting to eBay: {e}")
            return False

    def run(self):
        """Main execution method with improved workflow"""
        print("🚀 Auto Lister Starting...")
        print("=" * 50)
        
        # Step 1: Ask platform preferences
        selected_platforms = self.ask_platform_preferences()
        if not selected_platforms:
            return
        
        # Step 2: Load items
        items = self.load_items()
        if not items:
            print("\n❌ No items found in items/ directory")
            print("Create item folders in items/ with info.json files")
            print("Example: items/my_item/info.json")
            return
        
        print(f"\n📋 Found {len(items)} items to process")
        
        # Step 3: Start browser
        if not self.start_browser():
            return
        
        # Step 4: Login check for each selected platform
        print(f"\n🔐 Platform Login Phase")
        print("=" * 30)
        
        platform_pages = {}
        
        try:
            for platform_key in selected_platforms:
                platform_info = self.platforms[platform_key]
                page = self.login_check_and_wait(platform_key, platform_info)
                platform_pages[platform_key] = page
            
            # Step 5: Process items for each platform
            print(f"\n📦 Item Processing Phase")
            print("=" * 30)
            
            for item in items:
                print(f"\n📦 Processing: {item.get('title', 'Unknown Item')}")
                print(f"   Folder: {item['folder']}")
                print(f"   Price: ${item.get('price', 'N/A')}")
                
                for platform_key in selected_platforms:
                    platform_info = self.platforms[platform_key]
                    page = platform_pages[platform_key]
                    
                    print(f"\n🔍 Checking {platform_info['name']}...")
                    
                    # Check if listing exists
                    exists = None
                    if platform_key == 'facebook':
                        exists = self.check_facebook_listing(page, item)
                    elif platform_key == 'kijiji':
                        exists = self.check_kijiji_listing(page, item)
                    elif platform_key == 'ebay':
                        exists = self.check_ebay_listing(page, item)
                    
                    if exists is None:
                        print(f"   ⚠️  Could not check {platform_info['name']} properly")
                        continue
                    elif exists:
                        print(f"   ✅ Item already listed on {platform_info['name']}")
                        continue
                    else:
                        # Ask user if they want to post
                        response = input(f"   📝 Post '{item.get('title', 'Unknown')}' to {platform_info['name']}? (y/n): ").strip().lower()
                        if response in ['y', 'yes']:
                            print(f"   🚀 Opening posting form for {platform_info['name']}...")
                            
                            success = False
                            if platform_key == 'facebook':
                                success = self.post_to_facebook(page, item)
                            elif platform_key == 'kijiji':
                                success = self.post_to_kijiji(page, item)
                            elif platform_key == 'ebay':
                                success = self.post_to_ebay(page, item)
                            
                            if success:
                                input(f"   ⏸️  Press Enter when you've finished posting to {platform_info['name']}...")
                            
                            self.human_delay(2, 4)
                        else:
                            print(f"   ⏭️  Skipped posting to {platform_info['name']}")
            
            print("\n🎉 Processing complete!")
            print("Browser will remain open for any final actions...")
            input("Press Enter to close browser and exit...")
            
        except KeyboardInterrupt:
            print("\n⏹️  Stopped by user")
        except Exception as e:
            print(f"\n❌ Error during processing: {e}")
        finally:
            # Close individual pages but keep context open until the end
            for page in platform_pages.values():
                if page:
                    page.close()
            self.stop_browser()

def main():
    """Entry point"""
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print("Auto Lister - Automated listing management")
        print("\nUsage: python lister.py")
        print("\nRequirements:")
        print("- items/ directory with item folders")
        print("- Each item folder should contain info.json")
        print("- Run setup.py first to install dependencies")
        return
    
    lister = AutoLister()
    lister.run()

if __name__ == "__main__":
    main()