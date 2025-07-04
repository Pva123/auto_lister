import re
from playwright.sync_api import Playwright, sync_playwright, expect

#Start Playwright manually instead of using a 'with' block
playwright = sync_playwright().start()

#The rest of your recorded script
browser = playwright.chromium.launch(headless=False)
context = browser.new_context()
page = context.new_page()
page.goto("https://ebay.ca/")
page.get_by_role("link", name="My eBay").click()

# 3. Add an input() to pause the script and keep the browser open
print("\n 🔑 Please log in to your ebay account in the browser.")

#This creates an object that knows how to find your specific element.
summary_locator = page.locator("div").filter(has_text="SummaryCurrent pageRecently").nth(3)
#The script will pause here until the element appears.
summary_locator.wait_for(timeout=120000) # Wait for up to 2 minutes


print("\n✅ Login successful!")
print("Please wait for the checks...")

#listing an item
page.get_by_role("button", name="Selling").click()
page.get_by_role("link", name="Active").click()
page.get_by_role("link", name="Start a listing").click()
page.locator("#image_banner_1").get_by_role("link", name="List an item").click()
#item name below!
page.get_by_role("textbox", name="Tell us what you're selling").fill("item_name")
page.get_by_role("button", name="Search").click()
page.get_by_role("button", name="Continue without match").click()

#options:
#the code has to choose between these options!
get_by_role("button", name="New with box Brand new,")
get_by_role("button", name="New without box Brand new,")
get_by_role("button", name="New with defects Brand new")
get_by_role("button", name="Pre-owned Used, worn, or has")
#after choosing
get_by_role("button", name="Continue")

#Filling the items details:
page.get_by_role("textbox", name="Title").click()
#Item title:
page.get_by_role("textbox", name="Title").fill("Title")
#Condition:
get_by_text("New with box").nth(3)
get_by_role("menuitemradio", name="New without box")
get_by_role("menuitemradio", name="New with defects")
get_by_role("menuitemradio", name="Pre-owned Pre to owned").nth(1)
#Brand
page.get_by_role("textbox", name="Search or enter your own").fill("hi").press("Enter")
#Color
page.get_by_role("textbox", name="Search or enter your own").press("Enter")
page.get_by_role("menuitemradio", name="Black").click()
#upload photo:
page.get_by_role("button", name="Upload from computer").click()
#Describtion:
page.locator("iframe[title=\"Rich text editor\"]").content_frame.locator("div").fill("fdfsldjfkljj")
#price
page.locator("input[name=\"price\"]").first.click()
page.locator("input[name=\"price\"]").first.fill("20")
page.locator("input[name=\"price\"]").first.press("Enter")
#shipping disabled
page.get_by_role("checkbox", name="Ship your item Provide the").uncheck()
#publish
page.get_by_role("button", name="List it").click()





print("---------------------")
input("ENTER for TERMINATE/EXIT.")

