import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

print('- Importing required packages')

# Initialize WebDriver
driver = webdriver.Chrome()
time.sleep(2)

# Open LinkedIn Login Page
driver.get('https://www.linkedin.com/login')
print('- Opened LinkedIn Login Page')
time.sleep(3)

# Load credentials
with open('credentials.txt', 'r') as credential:
    username, password = [line.strip() for line in credential.readlines()]
print('- Loaded login credentials')

# Log in
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))).click()
print('- Logged in Successfully')
time.sleep(5)

# Search for profiles
search_query = input('Enter the keyword to search profiles: ')
search_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Search')]"))
)
search_field.send_keys(search_query)
search_field.send_keys("\n")
print('- Searching for profiles...')
time.sleep(5)

# Function to extract profile URLs with correct format
def get_profile_urls():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    profile_urls = set()  # Use a set to avoid duplicates

    for link in soup.find_all('a', href=True):
        href = link['href']
        if "/in/" in href:  # Ensure it's a LinkedIn profile link
            full_url = href if href.startswith("https") else f"https://www.linkedin.com{href.split('?')[0]}"
            profile_urls.add(full_url)

    return list(profile_urls)

# Scrape multiple pages without scrolling
num_pages = int(input('How many pages you want to scrape? '))
profile_urls = set()  # Use a set to avoid duplicates

for page in range(num_pages):
    print(f"- Scraping page {page + 1}")
    profile_urls.update(get_profile_urls())
    time.sleep(3)

    # Scroll to the bottom to load more results
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(5)
print(f'- Finished scraping profile URLs. Found {len(profile_urls)} profiles.')

# Save extracted profiles to CSV
with open('linkedin_profiles.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Profile URL"])
    writer.writerows([[url] for url in profile_urls])

print('- Data saved to "linkedin_profiles.csv"')

# Scrape profile data safely
with open('linkedin_profiles.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header

    with open('linkedin_profile_data.csv', 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["Name", "Title", "Location", "Profile URL"])

        for linkedin_URL in reader:
            linkedin_URL = linkedin_URL[0]  # Extract URL from list
            print(f"- Accessing profile: {linkedin_URL}")

            try:
                driver.get(linkedin_URL)
                time.sleep(5)  # Wait for page to load
                soup = BeautifulSoup(driver.page_source, "html")
                info_div = soup.body.head
                name = soup.body.h1
                information = info_div.find('.ph5').get_text(strip=True) if info_div and info_div.find('.ph5') else "N/A"

                writer.writerow([name, information, linkedin_URL])
                print(f'--- Name: {name}, info: {info_div}')

            except Exception as e:
                print(f"Error accessing {linkedin_URL}: {e}")

print('Mission Completed!')
