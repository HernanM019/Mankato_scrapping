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

def safe_click(element):
    """Attempt to click an element, ensuring it is interactable."""
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(element)
        )
        element.click()
    except Exception as e:
        print(f"Error clicking element: {e}")
        # Optionally, print the element details for further debugging
        print(f"Element details: {element}")

def scroll_to_element(element):
    """Ensure the element is in view before interacting with it."""
    driver.execute_script("arguments[0].scrollIntoView();", element)

try:
    # Open the webpage
    driver.get(url)

    # Wait for the 'All Categories' link to be clickable and click it
    categories_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Directory_All_Categories_Link a")))
    safe_click(categories_link)
    time.sleep(3)

    # Wait for the category list to be present
    categories = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, ".directory_container .ListingCategories_AllCategories_CATEGORY a")))

    # Extract all categories
    for category in categories:
        category_name = category.text
        safe_click(category)  # Navigate into the category
        time.sleep(3)

        # Find all the tabs under the "tabbernav" class
        tabs = driver.find_elements(By.CSS_SELECTOR, "#tabbernav2 li a")

        # Loop through each tab and extract business data
        for tab in tabs:
            scroll_to_element(tab)  # Ensure the tab is in view
            safe_click(tab)  # Click on the tab to load the content
            time.sleep(3)  # Wait for the tab content to load

            # Collect business data within the current tab
            businesses = driver.find_elements(By.CSS_SELECTOR,
                                              ".ListingResults_All_CONTAINER.ListingResults_Level2_CONTAINER")
            for business in businesses:
                try:
                    # Extract business name
                    name_element = business.find_element(By.CSS_SELECTOR,
                                                         ".ListingResults_Level2_HEADER .ListingResults_All_ENTRYTITLELEFTBOX span[itemprop='name']")
                    name = name_element.text if name_element else "N/A"

                    # Extract address information
                    address_element = business.find_element(By.CSS_SELECTOR,
                                                            ".ListingResults_Level2_MAINLEFTBOX [itemprop='street-address']")
                    locality_element = business.find_element(By.CSS_SELECTOR,
                                                             ".ListingResults_Level2_MAINLEFTBOX [itemprop='locality']")
                    region_element = business.find_element(By.CSS_SELECTOR,
                                                           ".ListingResults_Level2_MAINLEFTBOX [itemprop='region']")
                    postal_code_element = business.find_element(By.CSS_SELECTOR,
                                                                ".ListingResults_Level2_MAINLEFTBOX [itemprop='postal-code']")

                    address = address_element.text if address_element else "N/A"
                    locality = locality_element.text if locality_element else "N/A"
                    region = region_element.text if region_element else "N/A"
                    postal_code = postal_code_element.text if postal_code_element else "N/A"

                    full_address = f"{address}, {locality}, {region}, {postal_code}"

                    # Extract phone number
                    phone_element = business.find_element(By.CSS_SELECTOR, ".ListingResults_Level2_PHONE1")
                    phone = phone_element.text if phone_element else "N/A"

                    # Append to the business data list
                    business_data.append([category_name, name, full_address, phone])

                except Exception as e:
                    print(f"Error extracting data for business: {e}")
                    continue

        driver.back()  # Return to the category list
        time.sleep(3)

finally:
    driver.quit()

# Save data to an Excel file
df = pd.DataFrame(business_data, columns=["Category", "Business Name", "Address", "Phone Number"])
df.to_excel("All_Categories.xlsx", index=False)
print("Data saved to All_Categories.xlsx")
