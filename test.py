from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import difflib
import time

DRIVER_PATH = '/usr/bin/chromedriver'

service = Service(executable_path=DRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(service = service, options=options)

# Retrieve the capabilities
capabilities = driver.capabilities

if 'browserName' in capabilities and capabilities['browserName'] == 'chrome':
    browser_version = capabilities.get('browserVersion', 'Unknown')
    chromedriver_version = capabilities.get('chrome', {}).get('chromedriverVersion', 'Unknown').split(' ')[0]
    print(f"Browser Name: Chrome")
    print(f"Browser Version: {browser_version}")
    print(f"ChromeDriver Version: {chromedriver_version}")

#DRIVER_PATH = '/path/to/chromedriver'

# Set up Chrome WebDriver
#driver = webdriver.Chrome(executable_path=DRIVER_PATH)

dynamic_ids = ["guestbook_comments"]

login_page = "http://127.0.0.1:80/DVWA/vulnerabilities/xss_s"
credentials = {
    'username': 'admin',
    'password': 'password'
}
driver.get("http://127.0.0.1:80/DVWA/vulnerabilities/xss_s")
def login(driver, url, credentials):
    driver.get(url)
    username_field = driver.find_element("xpath", "//input[@type='text']")
    username_field.send_keys(credentials['username'])  # Replace YOUR_USERNAME with your username

    # Enter password
    password_field = driver.find_element("xpath", "//input[@type='password']")
    password_field.send_keys(credentials['password'])  # Replace YOUR_PASSWORD with your password

    # Click the login button
    login_button = driver.find_element("xpath", "//input[@value='Login']")
    login_button.click()

login(driver, login_page, credentials)

time.sleep(5)

# Navigate to Hacker News
driver.get("http://127.0.0.1:80/DVWA/vulnerabilities/xss_s")

# Retrieve the page source
html = driver.page_source

# print(html)


with open("selenium_output.html", "w", encoding="utf-8") as f:
    f.write(html)

# Close the driver
driver.quit()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# # print(soup.prettify())

# #dynamic_classes = ["post-title", "post-content"]

# #static_soup = soup.select(','.join(dynamic_classes))

with open("/home/tcminh/index.html", "r", encoding="utf-8") as f1, open("selenium_output.html", "r", encoding="utf-8") as f2:
    f1_soup = BeautifulSoup(f1, 'html.parser').find('html')
    f2_soup = BeautifulSoup(f2, 'html.parser').find('html')
    for id in dynamic_ids:
        f1_soup_tags = f1_soup.find_all(id=id)
        for tag in f1_soup_tags:

            tag.extract()
        f2_soup_tags = f2_soup.find_all(id=id)
        for tag in f2_soup_tags:
            # print(f'Is manipulated: {bool(BeautifulSoup(tag.get_text(), "html.parser").find())}')
            if bool(BeautifulSoup(tag.get_text(), "html.parser").find()):
                print("The dynamic field text has been defaced with Stored XSS")
                print("The text is: " + tag.get_text())
                break
            tag.extract()
    diff = difflib.ndiff(f1_soup.prettify().strip().splitlines(), f2_soup.prettify().strip().splitlines())

    # diff = difflib.ndiff(f1.read().strip().splitlines(), f2.read().strip().splitlines())
    for line in diff:
        if line.startswith('+ ') or line.startswith('- '):
            print(line)
    m = difflib.SequenceMatcher(None, f1_soup.prettify().strip(), f2_soup.prettify().strip())
    print(m.ratio())