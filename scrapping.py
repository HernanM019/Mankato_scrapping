from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Set up Selenium WebDriver
options = Options()
options.add_argument("--headless")  # Run browser in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Replace with your local path to ChromeDriver
service = Service("path/to/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

# Define the URL
url = "https://gmg.greatermankato.com/allcategories"

# Initialize an empty list to store business data
business_data = []

try:
    # Open the webpage
    driver.get(url)
    time.sleep(3)  # Wait for the page to load

    # Extract categories starting with 'A'
    categories = driver.find_elements(By.CSS_SELECTOR, ".category-list a")
    for category in categories:
        category_name = category.text
        if category_name.startswith("A"):  # Only process categories starting with 'A'
            category.click()  # Navigate into the category
            time.sleep(3)

            # Collect business data within the category
            while True:  # Handle pagination
                businesses = driver.find_elements(By.CSS_SELECTOR, ".business-card")
                for business in businesses:
                    name = business.find_element(By.CSS_SELECTOR, ".business-name").text
                    address = business.find_element(By.CSS_SELECTOR, ".business-address").text
                    phone = business.find_element(By.CSS_SELECTOR, ".business-phone").text
                    business_data.append([category_name, name, address, phone])

                # Check if there's a 'Next' button to navigate
                try:
                    next_button = driver.find_element(By.LINK_TEXT, "Next")
                    next_button.click()
                    time.sleep(3)
                except:
                    break  # No more pages

            driver.back()  # Return to the category list
            time.sleep(3)

finally:
    driver.quit()

# Save data to an Excel file
df = pd.DataFrame(business_data, columns=["Category", "Business Name", "Address", "Phone Number"])
df.to_excel("Categories_A.xlsx", index=False)
print("Data saved to Categories_A.xlsx")