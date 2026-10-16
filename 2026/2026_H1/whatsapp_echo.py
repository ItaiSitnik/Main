import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
TARGET_GROUP_NAME = "צקצקד"
CHECK_INTERVAL = 2


def start_echo_debug():
    print(">>> Launching Browser...")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://web.whatsapp.com")

    print(">>> Waiting 30 seconds for login... (Please scan QR)")
    time.sleep(30)

    try:
        # --- OPEN CHAT LOGIC ---
        print(f">>> Attempting to open group: '{TARGET_GROUP_NAME}'...")
        try:
            # Try finding the search box
            search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@role="textbox"]')
            search_box.click()
            search_box.send_keys(TARGET_GROUP_NAME)
            time.sleep(2)
            search_box.send_keys(Keys.ENTER)
            print(">>> Pressed Enter. Waiting for chat to load...")
            time.sleep(3)
        except Exception as e:
            print(f"❌ Could not auto-open chat: {e}")
            print(">>> PLEASE OPEN THE CHAT MANUALLY NOW.")
            time.sleep(5)

        # --- ECHO LOOP WITH DEBUGGING ---
        print("\n>>> STARTING DEBUG LOOP (Press Ctrl+C to stop)")
        last_processed_message = "NONE"  # Initial state

        while True:
            try:
                # 1. FIND MESSAGES
                # We look for ANY message container that is "incoming" (white bubble)
                # Note: 'message-in' is the classic class. If this list is empty, the class changed.
                incoming_messages = driver.find_elements(By.CSS_SELECTOR, "div.message-in")

                print(f"DEBUG: Found {len(incoming_messages)} incoming messages in DOM.")

                if incoming_messages:
                    # Look at the very last message
                    last_msg_container = incoming_messages[-1]

                    try:
                        # 2. EXTRACT TEXT
                        # We try to find the specific text span.
                        # If this fails, we try to print the whole container text for debugging.
                        try:
                            text_element = last_msg_container.find_element(By.CSS_SELECTOR, "span.selectable-text")
                            current_text = text_element.text
                        except NoSuchElementException:
                            # Fallback: Just get all text in the bubble (might include time/sender name)
                            current_text = last_msg_container.text

                        # Clean up text (remove newlines from metadata)
                        current_text = current_text.split("\n")[0]

                        # 3. COMPARE AND PRINT DEBUG INFO
                        print(f"   --> Last Msg: '{current_text}' | Saved: '{last_processed_message}'")

                        if current_text != last_processed_message and current_text != "":
                            print(f"   --> !!! NEW MESSAGE DETECTED !!! Attempting to reply...")

                            # 4. SEND REPLY
                            # Footer input box
                            input_box = driver.find_element(By.XPATH, '//footer//div[@contenteditable="true"][@role="textbox"]')

                            input_box.click()
                            input_box.send_keys(current_text)
                            time.sleep(0.5)
                            input_box.send_keys(Keys.ENTER)

                            print(f"   --> REPLIED: {current_text}")
                            last_processed_message = current_text
                        else:
                            print("   --> No new message to reply to.")

                    except StaleElementReferenceException:
                        print("   --> Element became stale (chat updated), retrying next loop...")

                else:
                    print("   --> WARNING: No 'message-in' elements found. Selector might be wrong.")

            except Exception as e:
                print(f"   --> Loop Error: {e}")

            print("-" * 30)
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\n>>> Stopped by user.")
    except Exception:
        traceback.print_exc()
    finally:
        input("\n>>> Press ENTER to close browser...")
        driver.quit()


if __name__ == "__main__":
    start_echo_debug()
