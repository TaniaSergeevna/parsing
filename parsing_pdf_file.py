# https://www.gassmann.ch/de/unternehmen/gassmann-media#amtl-anzeiger-bielleubringen
import csv

import requests
from bs4 import BeautifulSoup
from tika import parser

import re


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


def data_refactoring(data, n, l):
    datas = ''
    for i in data:
        if i != '':
            datas = (i.replace(n, '').replace(l, ''))
        else:
            datas = ''

    return datas


def parser_pdf(data, key, file):
    '''
    Gesuchsteller = bauherr
    Projektverfasser = projekverfasser
    Standort = con_plot + con_street
    Bauvorhaben = construction
    Zonenplan = zone
    Stadt Biel in title = municipality

    Baugesuch Nr. = number
    KW13_2020 = amtshblatt
    '''

    counter = re.findall(
        r'(?<=Stadt Biel Baugesuch Nr. ).*?(?=Auf)',
        file['content'].replace('\n', ' '))

    i = 0
    number, bauherr, projekverfasser, standort, construction, zone, municipality = [], [], [], [], [], [], []
    municipality = re.findall(
        r'(Stadt\sBiel\s\w+\sNr\.\s.{6,8})',
        file['content'].replace('\n', ' '))

    while i < len(counter):
        number.append((re.findall(r'(.{6,8}\sGesu)', counter[i]))[0].replace('Gesu', ''))
        bauherr.append(
            data_refactoring(re.findall(r'(:\s.{1,200}Proje)', counter[i]), ':', 'Proje'))
        projekverfasser.append(
            data_refactoring(re.findall(r'(Proje.{1,200}Stan)', counter[i]), 'Projektverfasser:', 'Stan'))
        standort.append(
            data_refactoring(re.findall(r'(Stan.{1,200}Bauvo)', counter[i]), 'Standort:', 'Bauvo'))
        construction.append(
            data_refactoring(re.findall(r'(Bauvo.{1,200}Zone)', counter[i]), 'Bauvorhaben:', 'Zone'))
        zone.append(
            data_refactoring(re.findall(r'(Zone.{1,200}Sch)', counter[i]), 'Zonenplan:', 'Sch'))
        i += 1

    con_plot = [str(i)[str(i).rfind(',') + 1:].strip() for i in standort]
    con_street = [str(i)[:str(i).rfind(',')].strip() for i in standort]

    amtshblatt = [str(data[key])[str(data[key]).find('_') + 1:str(data[key]).rfind('.')] for i in range(len(counter))]

    data_s = []
    for i in range(len(municipality)):
        data_s.append(
            [municipality[i],
             number[i], amtshblatt[i], bauherr[i], projekverfasser[i], con_plot[i], con_street[i], construction[i],
             zone[i], counter[i]])
    return data_s


def tika_pdf(data):
    data_all = []
    for key in data:
        a = parser_pdf(data, key, parser.from_file(data[key]))
        for i in a:
            data_all.append(i)

    return data_all


def add_csv(data):
    name = ["municipality", "number", "amtshblatt", "bauherr", "projekverfasser", "con_plot", "con_street",
            "construction", "zone", "counter"]
    data.insert(0, name)
    file = open('data_pdf.csv', 'w', encoding='utf-8')
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
