import time
import random
from playwright.sync_api import sync_playwright

# Simple Config
USER_AGENTS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."]
GROUP_URLS = [
    "https://www.facebook.com/groups/SADCCarMarketBotswana",
]
COOKIE_PATH = "./facebook_cookies" 

def get_content():
    """Reads content from the post.txt file in the repo"""
    try:
        with open("post.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "⚠️ No content found in post.txt. Please update the file."

def human_type(page, selector, text):
    page.click(selector)
    time.sleep(random.uniform(0.5, 1.2))
    for char in text:
        page.press(selector, char)
        time.sleep(random.uniform(0.05, 0.3))
    time.sleep(random.uniform(1.0, 3.0))

def post_to_group(content):
    with sync_playwright() as p:
        # Check if cookies exist. 
        # If not, Playwright will ask you to login. 
        # If yes, it remembers you (Persistent Context).
        try:
            context = p.chromium.launch_persistent_context(
                COOKIE_PATH,
                headless=True, 
                user_agent=random.choice(USER_AGENTS)
            )
        except Exception:
            # Fallback if folder is corrupted
            context = p.chromium.launch_persistent_context(COOKIE_PATH, headless=True)

        page = context.new_page()
        
        for url in GROUP_URLS:
            print(f"Posting to {url}...")
            page.goto(url)
            time.sleep(random.uniform(3, 7))
            
            # --- Standard Facebook selectors (may change) ---
            try:
                btn = page.locator('div[role="button"]:has-text("Post")').first
                btn.click()
                time.sleep(random.uniform(2, 4))
                
                textbox = page.locator('div[role="textbox"]')
                human_type(textbox, content)
                
                page.locator('div[aria-label="Post"]').click()
                time.sleep(random.uniform(5, 10))
            except Exception as e:
                print(f"Selection failed on {url}: {e}")
                
        context.close()

if __name__ == "__main__":
    content = get_content()
    post_to_group(content)
