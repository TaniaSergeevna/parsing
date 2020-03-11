import requests
import csv


def get_html(url):
    response = requests.get(url)
    return (response.json())


def transformations(url):
    dates = url["content"]
    myData = [["date", "rubric", "language", "name", "street", "town"]
              ]
    for data in dates:
        print(data['meta'])
        a = data['meta']
        m = []
        m.append(a['updateDate'])
        m.append(a['rubric'])
        m.append(a['language'])
        b = a['registrationOffice']
        m.append(b['displayName'])
        m.append(b['street'])
        m.append(b['town'])
        myData.append(m)
    myFile = open('example2.csv', 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(myData)

    print("Writing complete")


def main():
    transformations(get_html(
        'https://amtsblatt.be.ch/api/v1/publications?allowRubricSelection=true&includeContent=false&pageRequest.page=0&pageRequest.size=100&publicationStates=PUBLISHED&publicationStates=CANCELLED&rubrics=BP-BE&subRubrics=BP-BE10&subRubrics=BP-BE20&tenant=kabbe'))


if __name__ == "__main__":
    main()
