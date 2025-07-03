#!/usr/bin/env python3
"""
Auto Lister - A helper to log into platforms and record listing steps.
"""

import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import shutil

class AutoLister:
    def __init__(self, browser_data_dir="browser_data"):
        self.browser_data_dir = Path(browser_data_dir)
        # Clean up old session data for a fresh start
        if self.browser_data_dir.exists():
            shutil.rmtree(self.browser_data_dir)
        self.browser_data_dir.mkdir(exist_ok=True)
        
        self.platforms = {
            'facebook': {
                'url': 'https://www.facebook.com/login',
                'name': 'Facebook'
            },
            'kijiji': {
                'url': 'https://www.kijiji.ca/t-login.html',
                'name': 'Kijiji'
            },
            'ebay': {
                'url': 'https://signin.ebay.ca/signin/',
                'name': 'eBay'
            }
        }
        
        self.playwright = None
        self.context = None

    def start_browser(self):
        """Start browser with persistent context"""
        try:
            self.playwright = sync_playwright().start()
            
            self.context = self.playwright.chromium.launch_persistent_context(
                user_data_dir=str(self.browser_data_dir),
                headless=False,
                args=['--no-sandbox', '--disable-dev-shm-usage'],
                viewport={'width': 1280, 'height': 720}
            )
            
            print("✓ Browser started with a fresh session.")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start browser: {e}")
            print("\nHave you run the setup script? Try running: python setup.py")
            return False

    def stop_browser(self):
        """Clean up browser resources"""
        if self.context:
            self.context.close()
        if self.playwright:
            self.playwright.stop()

    def ask_platform_preferences(self):
        """Ask user which platforms they want to use"""
        print("\n🔧 Which platforms do you want to log into?")
        print("=" * 40)
        
        selected_platforms = []
        
        for platform_key, platform_info in self.platforms.items():
            while True:
                response = input(f"Use {platform_info['name']}? (y/n): ").strip().lower()
                if response in ['y', 'yes']:
                    selected_platforms.append(platform_key)
                    break
                elif response in ['n', 'no']:
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
        
        if not selected_platforms:
            print("\n❌ No platforms selected. Exiting.")
            return None
        
        print(f"\n✅ Great! We will open login pages for: {', '.join([self.platforms[p]['name'] for p in selected_platforms])}")
        return selected_platforms

    def open_login_pages_and_wait(self, selected_platforms):
        """Open login page for each platform and wait for user to log in."""
        print("\n🔐 Please log into each platform.")
        print("=" * 40)
        
        for platform_key in selected_platforms:
            platform_info = self.platforms[platform_key]
            page = self.context.new_page()
            
            print(f"📂 Opening {platform_info['name']} login page...")
            page.goto(platform_info['url'])
        
        input("Press Enter here after you have logged into all platforms...")
        print("✅ Logins complete!")

    def show_codegen_instructions(self):
        """Display instructions for the user to start recording with Playwright Codegen."""
        print("\n🔴 Now, let's record your actions!")
        print("=" * 40)
        print("I have saved your login session. You can now record the steps to post an item.")
        print("Open a NEW terminal and run the following command:")
        
        codegen_command = f"playwright codegen --target python -o 'lister.py' --load-storage='{self.browser_data_dir}/storage.json'"
        
        print("\n" + "="*len(codegen_command))
        print(codegen_command)
        print("="*len(codegen_command) + "\n")

        print("This will open a new browser window connected to your session.")
        print("Perform the actions you want to automate (e.g., post one item).")
        print("When you are done, close the browser window, and the recorded code will be saved to 'lister.py'.")
        print("You can then copy the relevant parts into your script.")

    def run(self):
        """Main execution method"""
        print("🚀 Auto Lister Recording Helper 🚀")
        print("=" * 50)
        
        selected_platforms = self.ask_platform_preferences()
        if not selected_platforms:
            return
        
        if not self.start_browser():
            return
        
        try:
            self.open_login_pages_and_wait(selected_platforms)
            
            # Save storage state to be used by codegen
            storage_path = self.browser_data_dir / "storage.json"
            self.context.storage_state(path=str(storage_path))
            print(f"✓ Session state saved to: {storage_path}")

            self.show_codegen_instructions()
            
            print("\nBrowser will remain open. Follow the instructions above in a new terminal.")
            input("Press Enter in this terminal to close the browser and exit...")
            
        except KeyboardInterrupt:
            print("\n⏹️  Stopped by user.")
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")
        finally:
            self.stop_browser()
            print("\n👋 Goodbye!")

def main():
    """Entry point"""
    lister = AutoLister()
    lister.run()

if __name__ == "__main__":
    main()