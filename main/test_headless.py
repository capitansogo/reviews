from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # Add this line if you want to run in headless mode

# Specify the URL of your remote WebDriver
remote_url = 'http://localhost:4444/wd/hub'

# Create a WebDriver with the specified options
driver = webdriver.Remote(command_executor=remote_url, options=chrome_options)

url = "https://stackoverflow.com/questions/53657215/running-selenium-with-headless-chrome-webdriver"
driver.get(url)
driver.implicitly_wait(5)

# Fix the syntax error in the next line, closing square bracket is missing
h1 = driver.find_element(By.XPATH, '//h1[@itemprop="name"]').text
print(h1)

driver.quit()