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


def search_data(start, stop, file):
    data, count = [], 0
    for j in re.findall(r'(?<={0}).*?(?={1})'.format(start, stop), file):
        data.append(
            j + re.findall(r'(?<={0}).*?(?= {1}) +({2})'.format(start, stop, stop), file)[count])
        count += 1
    return data


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
    # \s.{17, 19}
    # https: // gassmann.ch / sites / default / files / documents / AABL_KW10_2020_0.pdf
    # (' Biel Baugesuch Nr. 24’591 ', ' Gesuchsteller: Bekim & Zeljie Ajruli, Rigiweg 6, 2543 Lengnau  2. Interdiction à ')

    counter = re.findall(
        r'(\s\w+\s\w+\sNr\.\s.{6,8})(\s.{14,17}\s.{1,90}\,\s\d\d\d\d\s[A-Za-zäöüßÄÖÜẞ]+\s)(\D{17,19}\s)',
        file['content'].replace('\n', ' '))
    # counters = re.findall(r'(\s\w+\s\w+\sNr\.\s.{6,8})(\s.{14,17}\s.{1,90}\,\s\d\d\d\d\s[A-Za-zäöüßÄÖÜẞ]+\s.{17,2000}\s)',
    #                      file['content'].replace('\n', ' '))
    print(len(counter))
    for i in counter:
        print(i)

    # bauherr = search_data('Gesuchsteller:', '\d\d\d\d +[A-Za-zäöüßÄÖÜẞ]+',
    #                       file['content'].replace('\n', ' ').replace('Gesuchstellerin:', 'Gesuchsteller:'))
    # print(len(bauherr), bauherr)
    #
    # projekverfasser = search_data('Projektverfasser:', '\d\d\d\d +[A-Za-zäöüßÄÖÜẞ]+',
    #                               file['content'].replace('\n', ' ').replace('Projektverfasserin:',
    #                                                                          'Projektverfasser:'))
    # print(len(projekverfasser), projekverfasser)
    #
    # standort = re.findall(r'(?<=Standort:).*?(?=Par)', file['content'].replace('\n', ' '))
    # standort = [str(i)[:str(i).rfind(',')].strip() for i in standort]
    # con_plot = [str(i)[str(i).rfind(',') + 1:].strip() for i in standort]
    # con_street = [str(i)[:str(i).rfind(',')].strip() for i in standort]
    #
    # print(len(con_plot), con_plot)
    # print(len(con_street), con_street)
    #
    # # zone = re.findall(r'(?<=Zonenplan:).*?(?=:)', file['content'].replace('\n', ' '))
    # # print(zone)
    #
    # #примерно правильно
    # number = re.findall(
    #     r'Nr\.\s\d\d\W\d\d\d | Nr\.\s\d\d\W\d\d\d\W\S\s | Nr\.\s\d\d\d\d\d\s | Nr\.\s\d\d\d\d/\d\d\d\s | Nr\.\s\D\D\d\d\d\d\d\s | Nr\.\s\D\D\d\d\d\d\d\W\S\s',
    #     file['content'].replace('\n', ' '))
    # number = [str(i)[:str(i).rfind(' ')].strip() for i in number]
    # print(len(number), number)
    #
    # amtshblatt = str(data[key])[str(data[key]).find('_') + 1:str(data[key]).rfind('.')]
    # print(amtshblatt)
    print('&&&&&&')


def tika_pdf(data):
    data_all = []
    for key in data:
        # print(key)
        # key = 'Amtl. Anzeiger KW 11'
        data_all.append(parser_pdf(data, key, parser.from_file(data[key])))

        break

    # return data_all


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
    # print(data)
    # add_csv(data)


if __name__ == '__main__':
    main()
