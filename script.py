from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

edge_user_data = os.getenv('edge_user_data')
driver_path = os.getenv('driver_path')

# Set up Edge options to use an existing profile
edge_options = Options()
edge_options.add_argument(edge_user_data)
edge_options.add_argument("profile-directory=Default")

# edge_options.add_argument("profile-directory=Profile 2")  # Alternatively, you could use this if needed

# Set up the EdgeDriver service with logging
service = Service(driver_path, log_path='msedgedriver.log')

# Initialize the WebDriver
driver = webdriver.Edge(service=service, options=edge_options)

# Set a global implicit wait (optional, as we are using explicit waits)
# driver.implicitly_wait(10)

try:
    # Step 1: Replace the following link with a zomato live show link.
    driver.get("https://www.zomato.com/events/kingfisher-octobeer-fest-bengaluru-et50273")
    
    # Optional: Wait for the page to load completely
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    # Take a screenshot after page load for debugging
    driver.save_screenshot("page_loaded.png")
    
    # Step 2: Click on the "Book Tickets" button
    try:
        book_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Book tickets']]"))
        )
        # Scroll into view if necessary
        driver.execute_script("arguments[0].scrollIntoView(true);", book_button)
        book_button.click()
    except TimeoutException:
        print("Book tickets button not found. Taking screenshot for debugging.")
        driver.save_screenshot("book_button_not_found.png")
        raise
    
    # Step 3: Select Ticket Type and Quantity ("ADD" button)
    try:
        # Find all the ADD buttons (this returns a list of WebElements)
        add_buttons = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//span[text()='ADD']/ancestor::div[contains(@class, 'gVvWyZ')]"))
        )

        # Scroll into view of the desired ADD button, for example, the 2nd ADD button (index 1)
        desired_add_button = add_buttons[0]  # Change the index here to select another button if needed
        driver.execute_script("arguments[0].scrollIntoView(true);", desired_add_button)
        
        # Click the desired ADD button
        desired_add_button.click()
    except TimeoutException:
        print("ADD button not found. Taking screenshot for debugging.")
        driver.save_screenshot("add_button_not_found.png")
        raise

    # Now, click the '+' button multiple times
    try:
        for _ in range(5):  # This will buy n+1 tickets
            plus_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'bGDlrz')]//i[contains(@class, 'kvFkqh')]"))
            )
            # Scroll into view if necessary
            driver.execute_script("arguments[0].scrollIntoView(true);", plus_button)
            plus_button.click()
            time.sleep(0)  # Add a small delay between clicks to prevent errors
    except TimeoutException:
        print("PLUS button not found. Taking screenshot for debugging.")
        driver.save_screenshot("plus_button_not_found.png")
        raise
    except Exception as e:
        print("An error occurred:", e)

        
    # Step 4: Proceed to Pay
    try:
        proceed_to_pay_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Proceed to pay']]"))
        )
        # Scroll into view if necessary
        driver.execute_script("arguments[0].scrollIntoView(true);", proceed_to_pay_button)
        proceed_to_pay_button.click()
    except TimeoutException:
        print("Proceed to pay button not found. Taking screenshot for debugging.")
        driver.save_screenshot("proceed_to_pay_not_found.png")
        raise
    
    # Step 5: Payment Page - Switch to the iframe and Enter CVV
    try:
        # Switch to the payment iframe first
        payment_iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[@id='payment_widget']"))
        )
        driver.switch_to.frame(payment_iframe)
        
        # Now locate the CVV input field inside the iframe
        cvv_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password'][@autocomplete='on']"))
        )
        
        # Scroll into view if necessary
        driver.execute_script("arguments[0].scrollIntoView(true);", cvv_input)
        
        # **Secure input method for CVV (avoid hardcoding sensitive info)**
        cvv_input.send_keys(os.getenv('cvv'))  # Replace with a secure method
        print("CVV entered successfully")
        
        # After inputting CVV, switch back to the main page
        driver.switch_to.default_content()

    except TimeoutException:
        print("CVV input field not found. Taking screenshot for debugging.")
        driver.save_screenshot("cvv_input_not_found.png")
        raise

    
    # Step 6: Click Checkout
    try:
        checkout_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Checkout']]"))
        )
        # Scroll into view if necessary
        driver.execute_script("arguments[0].scrollIntoView(true);", checkout_button)
        checkout_button.click()
    except TimeoutException:
        print("Checkout button not found. Taking screenshot for debugging.")
        driver.save_screenshot("checkout_button_not_found.png")
        raise
    
    # Allow time to see the result (increase if needed)
    time.sleep(150)
    
except Exception as e:
    print("An error occurred:", e)
    # Optionally, handle or log the exception further
finally:
    # **⚠️ Important:** Ensure the browser is closed to free up resources
    driver.quit()