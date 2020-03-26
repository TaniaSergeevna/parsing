# https://www.gassmann.ch/de/unternehmen/gassmann-media#amtl-anzeiger-bielleubringen
import csv

import requests
from bs4 import BeautifulSoup
from tika import parser


def get_html(url):
    response = requests.get(url)
    return response


def parsing_html(response):
    soup = BeautifulSoup(response.text, 'lxml')

    date = {}
    for link in soup.find_all(class_="file clearfix"):

        try:
            str(link.find('a').text).index('Amtl. Anzeiger KW')
            date[link.find('a').text] = link.find('a').get('href')

        except ValueError:
            pass

    return date


def parser_pdf(data, key, file):
    data_all = []
    data_all.append(key)  # name
    data_all.append(data[key])  # url
    data_all.append(str(file['metadata']['date'])[:10].replace('-', '/'))

    data_all.append(file['content'][:500].replace('\n', ''))  # content
    return data_all

def tika_pdf(data):
    data_all = []
    for key in data:
        data_all.append(parser_pdf(data, key, parser.from_file(data[key])))

    return data_all


def add_csv(data):
    name = ['name', 'url', 'date', 'content']
    data.insert(0, name)
    file = open('data_pdf.csv', 'w')
    with file:
        writer = csv.writer(file)
        writer.writerows(data)


def main():
    data = tika_pdf(
        parsing_html(
            get_html(
                'https://www.gassmann.ch/de/unternehmen/gassmann-media#amtl-anzeiger-bielleubringen'
            )
        )
    )
    print(data)
    add_csv(data)


if __name__ == '__main__':
    main()
