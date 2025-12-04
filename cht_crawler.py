import re
import time
import sys
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Launch browser (headless=False to see what's happening if needed)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        url = "https://bms.cht.com.tw/mbms/NewApply/findAvailableProc.jsp"
        print(f"Navigating to {url}...")
        
        try:
            page.goto(url, timeout=60000)
        except Exception as e:
            print(f"Error navigating to URL: {e}")
            return

        # Get all options from the "First 4 digits" dropdown (name="head4G")
        try:
            page.wait_for_selector('select[name="head4G"]', timeout=30000)
            options = page.eval_on_selector_all('select[name="head4G"] option', 
                                                'options => options.map(o => o.value)')
            prefixes = [opt for opt in options if opt and opt.isdigit()]
            print(f"Found {len(prefixes)} prefixes: {prefixes}")
        except Exception as e:
            print(f"Error extracting prefixes: {e}")
            return
        
        found_numbers = []
        
        for prefix in prefixes:
            print(f"Checking prefix: {prefix}")
            
            try:
                # Ensure we are on the right page or element is present
                if not page.is_visible('select[name="head4G"]'):
                    page.goto(url, timeout=60000)
                    page.wait_for_selector('select[name="head4G"]', timeout=30000)

                # Select the prefix
                page.select_option('select[name="head4G"]', prefix)
                
                # Select "Last 6 digits" (value="2" or by text)
                page.click('text=後六碼')
                
                # Input "??9196" into the text field
                page.fill('input[name="tel"]', '??9196')
                
                # Click Search (Submit)
                with page.expect_navigation(timeout=60000):
                    page.click('input[type="submit"], button[type="submit"], input[alt="Submit"]')
                
                # Wait for content to load
                page.wait_for_load_state('networkidle')
                
                # Check for results
                content = page.content()
                if "查無符合" in content:
                    print(f"  No results for {prefix}")
                else:
                    text = page.inner_text('body')
                    # Look for numbers starting with prefix and ending with 9196
                    matches = re.findall(rf"{prefix}\d{{6}}", text.replace("-", ""))
                    valid_matches = [m for m in matches if m.endswith("9196")]
                    
                    if valid_matches:
                        print(f"  Found {len(valid_matches)} numbers: {valid_matches}")
                        found_numbers.extend(valid_matches)
                    else:
                        print(f"  No matching numbers found in page text.")
                
                # Go back to the search page for the next iteration
                # Using goto is more reliable than go_back() for forms
                page.goto(url, timeout=60000)
                
                # Add a delay to avoid rate limiting and ensure page load
                time.sleep(2)
                
            except Exception as e:
                print(f"  Error processing prefix {prefix}: {e}")
                # Try to recover
                try:
                    page.goto(url, timeout=60000)
                except:
                    pass

        print("\nSearch complete.")
        print(f"Total found numbers: {len(found_numbers)}")
        
        with open("found_numbers.txt", "w", encoding="utf-8") as f:
            for num in found_numbers:
                f.write(num + "\n")
        print("Results saved to found_numbers.txt")
        
        browser.close()

if __name__ == "__main__":
    run()
