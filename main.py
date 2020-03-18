import datetime

import requests
import csv


def get_html(url):
    response = requests.get(url)
    return response.json()


def add_href(url, date):
    href = []
    datas = url["content"]
    date_2 = datetime.datetime.strptime(date, '%d.%m.%Y')
    for data in datas:
        a = data['meta']
        i = a['publicationDate']
        da = datetime.date(int(i[:4]), int(i[5:7]), int(i[8:10])).strftime('%d.%m.%Y')
        date_1 = datetime.datetime.strptime(da, '%d.%m.%Y')

        if (date_1 - date_2).days <= 14 and (date_1 - date_2).days >= 0:
            href.append('https://amtsblatt.be.ch/api/v1/publications/{0}'.format(a['id']))

    return href


def transformations(urls):
    data_pages = []
    for url in urls:
        data_page = []
        datas = get_html(url)['meta']
        data_page.append(datas['rubric'][:2])
        data_page.append(str(datas['publicationDate'][:10]).replace('-', '.'))
        registrationOffice = datas['registrationOffice']

        data_page.append(registrationOffice['displayName'])
        data_page.append(registrationOffice['street'])
        data_page.append(registrationOffice['town'])
        data_page.append(registrationOffice['streetNumber'])

        data_page.append(datas['publicationNumber'])

        data_page.append(datas['cantons'][0])

        data_pages.append(data_page)

    return data_pages


def add_csv(data):
    name = ['rubric', 'publicationDate','displayName', 'street', 'town', 'streetNumber', 'publicationNumber',
            'cantons']
    data[0].insert(0, name)
    file = open('example.csv', 'w')
    with file:
        writer = csv.writer(file)
        writer.writerows(data[0])


def main():
    date = ((datetime.date.today() + datetime.timedelta(days=-14)).strftime('%d.%m.%Y'))
    number_page = 3
    data = [
    ]
    # pagination
    for page in range(number_page):
        data.append(transformations(
            add_href(
                get_html(
                    'https://amtsblatt.be.ch/api/v1/publications?allowRubricSelection=true&includeContent=false&pageRequest.page={0}&pageRequest.size=100&publicationStates=PUBLISHED&publicationStates=CANCELLED&rubrics=BP-BE&subRubrics=BP-BE10&subRubrics=BP-BE20&tenant=kabbe'.format(
                        page)),
                date)
        ))

    add_csv(data)


if __name__ == "__main__":
    main()

# https://amtsblatt.be.ch/api/v1/publications?allowRubricSelection=true&includeContent=false&pageRequest.page=0&pageRequest.size=100&publicationStates=PUBLISHED&publicationStates=CANCELLED&rubrics=BP-BE&subRubrics=BP-BE10&subRubrics=BP-BE20&tenant=kabbe
# https://amtsblatt.be.ch/api/v1/publications?allowRubricSelection=true&includeContent=false&pageRequest.page=1&pageRequest.size=100&publicationStates=PUBLISHED&publicationStates=CANCELLED&rubrics=BP-BE&subRubrics=BP-BE10&subRubrics=BP-BE20&tenant=kabbe


# Request URL: https://amtsblatt.be.ch/api/v1/publications/f24150a0-5aae-4bb2-a315-5d7916cd8233
# Request URL: https://amtsblatt.be.ch/api/v1/publications/62a38883-0d47-4cb2-9bff-50c07be797db
