from datetime import datetime

import requests
import csv

# options = Options()
# options.add_argument("start-maximized")
# options.add_argument('--disable-gpu')
# options.add_argument("disable-infobars")
# options.add_argument("--disable-extensions")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# driver = webdriver.Chrome(executable_path= '/home/tatiana/snap/ChromeDriver/chromedriver_linux64/chromedriver')
# driver.set_window_size(1120,550)

# def get_html(url):
#     response = requests.get(url)
#     return (response.json())
#
#
# def transformations(url):
#     dates = url["content"]
#     myData = [["date", "rubric", "language", "name", "street", "town"]
#               ]
#     for data in dates:
#         print(data['meta'])
#         a = data['meta']
#         m = []
#         m.append(a['updateDate'])
#         m.append(a['rubric'])
#         m.append(a['language'])
#         b = a['registrationOffice']
#         m.append(b['displayName'])
#         m.append(b['street'])
#         m.append(b['town'])
#         myData.append(m)
#     myFile = open('example2.csv', 'w')
#     with myFile:
#         writer = csv.writer(myFile)
#         writer.writerows(myData)
#
#     print("Writing complete")
#
#
# def main():
#     transformations(get_html(
#         'https://amtsblatt.be.ch/api/v1/publications?allowRubricSelection=true&includeContent=false&pageRequest.page=0&pageRequest.size=100&publicationStates=PUBLISHED&publicationStates=CANCELLED&rubrics=BP-BE&subRubrics=BP-BE10&subRubrics=BP-BE20&tenant=kabbe'))
#
#
# if __name__ == "__main__":
#     main()
import datetime

now = (datetime.date.today() + datetime.timedelta(days=-14)).strftime("%d.%m.%Y")

print((datetime.date.today() + datetime.timedelta(days=-14)).strftime("%d.%m.%Y"))

print(now)

date1_str = '5.02.2015'
date2_str = '3.02.2015'
date1 = datetime.datetime.strptime(date1_str, '%d.%m.%Y')
date2 = datetime.datetime.strptime(date2_str, '%d.%m.%Y')
if (date2 - date1).days >= 0:
    print("llll")
else:
    print("llkd")
print((date2 - date1).days)
