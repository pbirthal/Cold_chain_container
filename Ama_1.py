from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the WebDriver
service = Service('path_to_chromedriver')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Open Amazon.in and search for 'laptop'
driver.get('https://www.amazon.in')
search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
search_box.send_keys('laptop')
search_box.send_keys(Keys.ENTER)

# Wait for the search results to load
wait = WebDriverWait(driver, 10)
time.sleep(2)  # Short sleep to stabilize

# Store laptop data in a list
laptop_data = []

# Loop through pages
while True:
    # Wait for search results to load
    wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 's-main-slot')]//div[@data-component-type='s-search-result']")))

    # Collect the titles, prices, and reviews on the current page
    laptops = driver.find_elements(By.XPATH, "//div[contains(@class, 's-main-slot')]//div[@data-component-type='s-search-result']")
    
    for laptop in laptops:
        try:
            # Title
            title = laptop.find_element(By.XPATH, ".//h2/a/span").text

            # Price (Discounted)
            try:
                discounted_price = laptop.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
            except:
                discounted_price = "Price not available"

            # Average Review Score
            try:
                average_review = laptop.find_element(By.XPATH, ".//span[@class='a-icon-alt']").get_attribute("innerHTML").split()[0]
            except:
                average_review = "No reviews"

            # Append data to list
            laptop_data.append({
                'Title': title,
                'Discounted Price': discounted_price,
                'Average Review': f"{average_review} out of 5" if average_review != "No reviews" else "No reviews"
            })
        except Exception as e:
            print(f"Error while extracting data for a laptop: {e}")
            continue

    # Move to the next page if available
    try:
        next_button = driver.find_element(By.XPATH, "//a[contains(@class, 's-pagination-next')]")
        if 'disabled' in next_button.get_attribute("class"):
            break  # No more pages, exit the loop
        else:
            next_button.click()  # Go to the next page
            time.sleep(3)  # Wait for page to load
    except:
        break  # Exit if next button not found

# Print out the results
for item in laptop_data:
    print(item)

# Close the driver
driver.quit()
