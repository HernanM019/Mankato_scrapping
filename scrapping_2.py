import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Selenium WebDriver
options = Options()
options.add_argument("--headless")  # Run browser in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Path to ChromeDriver
service = Service("C:/chromedriver-win64/chromedriver.exe")  # Update this with the correct path
driver = webdriver.Chrome(service=service, options=options)

# Define the URL
url = "https://gmg.greatermankato.com/allcategories"

# Initialize an empty list to store business data
business_data = []

# Set up WebDriver wait
wait = WebDriverWait(driver, 20)  # Increase timeout duration

try:
    # Open the webpage
    driver.get(url)

    # Wait for the 'All Categories' link to be clickable
    categories_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Directory_All_Categories_Link a")))

    # Click on the 'All Categories' link
    categories_link.click()
    time.sleep(3)

    # Wait for the category list to be present
    categories = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='/category']")))  # Adjust the selector as needed

    # Extract all categories
    for category in categories:
        category_name = category.text
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
df.to_excel("All_Categories.xlsx", index=False)
print("Data saved to All_Categories.xlsx")
