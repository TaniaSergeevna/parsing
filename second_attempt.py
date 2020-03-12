from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox(
    executable_path='/home/tatiana/Рабочий стол/geckodriver/geckodriver-v0.26.0-linux64/geckodriver')

driver.get("https://amtsblatt.be.ch/#!/search/publications?filterId=3cb0327e-2236-11ea-a385-0050569db5fb")

element = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "list-row"))
)

now = str(datetime.now().strftime("%d.%m.%Y"))

count = 0
times = []
contents = []
numbers = []
hrefs = []

for option in driver.find_elements_by_class_name("publication-info"):

    if now >= option.text[:10] and count < 7:
        times.append(option.text[:10])

        numbers.append(option.text[13:31])

        contents.append(driver.find_elements_by_class_name("list-col-highlighted")[count].text)

        hrefs.append(driver.find_element_by_link_text(
            driver.find_elements_by_class_name("list-col-highlighted")[count].text).get_attribute("href"))

        count += 1

print(times)
print(contents)
print(hrefs)
print(numbers)
driver.quit()

# p = webdriver.Firefox(
#     executable_path='/home/tatiana/Рабочий стол/geckodriver/geckodriver-v0.26.0-linux64/geckodriver')
# # print(hrefs[0])
# p.get(hrefs[0])
#
# elements = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.CLASS_NAME, "field-value"))
# )
#
# p.page_source
#
# p.quit()


