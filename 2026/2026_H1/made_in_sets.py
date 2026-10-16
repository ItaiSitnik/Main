import concurrent.futures
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_price_headless(url, set_name):
    # Setup Chrome options for speed and invisibility
    options = Options()
    options.add_argument("--headless=new")  # Run without UI (invisible)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    )
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")  # Suppress console logs

    # Optimization: Block images to speed up loading
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    result = {"name": set_name, "sale_price": None, "original_price": None, "status": "Failed"}

    try:
        driver.get(url)

        # Wait for JS to render (slightly shorter since we blocked images)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Exact logic based on your debug file (aria-label)
        original_price_el = soup.find("span", attrs={"aria-label": lambda x: x and "Price before discount" in x})

        if original_price_el:
            # Case A: Discount exists
            result["original_price"] = original_price_el["aria-label"].replace("Price before discount:", "").strip()

            # The sale price is the sibling before
            sale_price_el = original_price_el.find_previous_sibling("span")
            if sale_price_el:
                result["sale_price"] = sale_price_el.get("aria-label", sale_price_el.get_text(strip=True))
        else:
            # Case B: No discount, look for active price
            current_price_el = soup.find("span", attrs={"data-is-active": "true"})
            if current_price_el:
                price_val = current_price_el.get("aria-label") or current_price_el.get_text(strip=True)
                result["sale_price"] = price_val
                result["original_price"] = price_val  # Same price

        result["status"] = "Success"

    except Exception as e:
        result["status"] = f"Error: {str(e)}"
    finally:
        driver.quit()

    return result


def main():
    start_time = time.time()

    sets = [
        ("10-Piece Set", "https://madeincookware.com/products/the-stainless-sets/10-piece"),
        ("13-Piece Set", "https://madeincookware.com/products/the-stainless-sets/13-piece"),
        ("Curated Kitchen", "https://madeincookware.com/products/the-stainless-sets/curated-kitchen"),
    ]

    print("Fetching prices in parallel (Headless Browser)...")

    results = []
    # Running 3 browsers at the same time
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_name = {executor.submit(get_price_headless, url, name): name for name, url in sets}

        for future in concurrent.futures.as_completed(future_to_name):
            data = future.result()
            results.append(data)

    print(f"\n--- Final Report (Time: {time.time() - start_time:.2f}s) ---")

    # Sort results to keep order consistent
    results.sort(key=lambda x: x["name"])

    for res in results:
        if res["status"] == "Success":
            print(f"Set: {res['name']:<20}")
            print(f"   Price:    {res['sale_price']}")
            if res["original_price"] != res["sale_price"]:
                print(f"   Original: {res['original_price']}")
            print("-" * 30)
        else:
            print(f"Set: {res['name']} | Status: {res['status']}")


if __name__ == "__main__":
    main()
