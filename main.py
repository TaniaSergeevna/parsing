import datetime

import requests
import csv
from geopy.geocoders import Nominatim


def get_html(url):
    response = requests.get(url)
    return response.json()


def add_href(url, date):
    href, href_view = [], []
    datas = url["content"]
    date_2 = datetime.datetime.strptime(date, '%d.%m.%Y')
    for data in datas:
        a = data['meta']
        i = a['publicationDate']
        da = datetime.date(int(i[:4]), int(i[5:7]), int(i[8:10])).strftime('%d.%m.%Y')
        date_1 = datetime.datetime.strptime(da, '%d.%m.%Y')

        if (date_1 - date_2).days <= 14 and (date_1 - date_2).days >= 0:
            href.append('https://amtsblatt.be.ch/api/v1/publications/{0}'.format(a['id']))
            href_view.append('https://amtsblatt.be.ch/api/v1/publications/{0}/view'.format(a['id']))
    data = transformations2(href_view)

    return href, data


def replaces(string):
    string = str(string).replace('<div>', '').replace('<strong>', '').replace('</div>', '').replace('</strong>',
                                                                                                    '').replace(
        '<br/>',
        '   ').replace('<br />', '   ').replace('\u200b', '').replace('\u200b', '')

    return string


def add_date(string):
    data_page = []

    data_page.append(str(replaces(string)))

    bh_name = str(replaces(string))
    data_page.append(bh_name[:bh_name.find('   ')])
    bh_adress = bh_name[bh_name.find('   ') + 3:].replace('   ', ',')


    if bh_adress.count(',') == 2:
        bh_adress = (str(bh_adress[bh_adress.find(',') + 1:]))
        data_page.append(bh_adress)
    else:
        data_page.append(bh_adress)

    bh_street = str(bh_adress[:bh_adress.find(',')]).strip()
    data_page.append(bh_street[:bh_street.rfind(' ')])
    data_page.append(bh_street[bh_street.rfind(' '):])
    bh_place = str(bh_adress[bh_adress.find(',') + 1:])[
               str(bh_adress[bh_adress.find(',') + 1:]).find(',') + 1:].strip()
    data_page.append(bh_place[bh_place.find(' ') + 1:])
    data_page.append(bh_place[:bh_place.find(' ')])

    geolocator = Nominatim()
    loc = geolocator.geocode(bh_place[bh_place.find(' ') + 1:])

    data_page.append(loc.longitude)
    data_page.append(loc.latitude)

    return data_page


def transformations2(urls):
    data_pages = []
    for url in urls:
        data_page = []
        datas = get_html(url)['fields']

        for i in add_date(datas[1]['fields'][0]['fields'][0]['value']['defaultValue']):
            data_page.append(i)

        # data2
        try:
            for i in add_date(datas[2]['fields'][0]['fields'][0]['value']['defaultValue']):
                data_page.append(i)
        except:
            data_page.append('')
            data_page.append('')
            data_page.append('')
            data_page.append('')
            data_page.append('')
            data_page.append('')
            data_page.append('')

            data_page.append(' ')
            data_page.append(' ')

        try:
            data_page.append(replaces(datas[3]['fields'][0]['value']['defaultValue']))
        except:
            data_page.append(' ')

        try:
            data_page.append(replaces(datas[3]['fields'][2]['value']['defaultValue']))
        except:
            data_page.append(' ')

        try:
            data_page.append(replaces(datas[3]['fields'][1]['fields'][0]['value']['defaultValue'])[
                             :str(replaces(datas[3]['fields'][1]['fields'][0]['value']['defaultValue'])).find(',')])
        except:
            data_page.append(' ')

        try:
            geolocator = Nominatim()
            try:
                loc = geolocator.geocode(replaces(datas[3]['fields'][1]['fields'][0]['value']['defaultValue'])[
                                         str(replaces(
                                             datas[3]['fields'][1]['fields'][0]['value']['defaultValue'])).find(
                                             ',') + 1:])
            except:

                loc = geolocator.geocode((replaces(datas[3]['fields'][1]['fields'][0]['value']['defaultValue'])[
                                          :str(replaces(
                                              datas[3]['fields'][1]['fields'][0]['value']['defaultValue'])).find(
                                              ',')]))

            data_page.append(loc.longitude)
            data_page.append(loc.latitude)

        except:
            data_page.append(' ')
            data_page.append(' ')

        data_page.append('  ')
        data_page.append('  ')
        data_page.append('  ')

        data_pages.append(data_page)

    return data_pages


def content(string):
    string = str(string)[str(string).find(',') + 1:]
    return string


def municipality(string):
    try:
        string = str(string)[:str(string).find('-')]
    except:
        string = str(string)

    return string


def transformations(urls, data):
    data_pages = []
    i = 0
    for url in urls:
        data_page = []
        datas = get_html(url)['meta']
        data_page.append(datas['cantons'][0])

        data_page.append('https://amtsblatt.be.ch/#!/search/publications/detail/{0}'.format(datas['id']))

        data_page.append(str(datas['publicationDate'][:10]).replace('-', '/'))
        data_page.append('Baupublikation')
        data_page.append('Betrifft:{0}'.format(content(datas['title']['de'])))
        data_page.append(municipality(datas['registrationOffice']['displayName']))
        data_page.append((datas['publicationNumber']))
        for j in data[i]:
            data_page.append(j)
        data_pages.append(data_page)

        i += 1

    return data_pages


def add_csv(data):
    name = ['canton', 'url', 'date', 'type', 'content', 'municipality', 'number', 'bauherr', 'bh_name',
            'bh_address', 'bh_street', 'bh_number',
            'bh_place', 'bh_plz', 'bh_lon', 'bh_lat', 'projektverfasser', 'pv_address', 'pv_name', 'pv_street',
            'pv_number', 'pv_place', 'pv_plz', 'pv_lon',
            'pv_lat',
            'construction', 'con_plot', 'con_street', 'lon', 'lat', 'zone', 'exception', 'coord']
    data[0].insert(0, name)
    file = open('example.csv', 'w')
    with file:
        writer = csv.writer(file)
        writer.writerows(data[0])


def main():
    date = ((datetime.date.today() + datetime.timedelta(days=-14)).strftime('%d.%m.%Y'))
    number_page = 3
    data = []
    # pagination
    for page in range(number_page):
        url, datas = add_href(
            get_html(
                'https://amtsblatt.be.ch/api/v1/publications?allowRubricSelection=true&includeContent=false&pageRequest.'
                'page={0}&pageRequest.size=100&publicationStates=PUBLISHED&publicationStates=CANCELLED&rubrics=BP-'
                'BE&subRubrics=BP-BE10&subRubrics=BP-BE20&tenant=kabbe'.format(page)),
            date)
        data.append(transformations(url, datas))

    add_csv(data)


if __name__ == "__main__":
    main()
