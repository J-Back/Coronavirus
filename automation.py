from bs4 import BeautifulSoup
import pandas as pd
import requests

url = 'https://www.livescience.com/coronavirus-updates-united-states.html'

DATA = []

def get_links():
    content = BeautifulSoup(requests.get(
        'https://www.livescience.com/coronavirus-updates-united-states.html').text, 'html.parser')

    URL = []

    for link in content.find('div', class_='fancy_box_body').find_all('a'):
        COUNT = ''
        DEATHS = ''

        if len(link.find('strong').find_next('strong').text.split()) > 1:
            if len(link.find('strong').find_next('strong').text.split()) == 2:

                if ':' in list(link.find('strong').find_next('strong').text.split()[1]):
                    COUNT = link.find('strong').find_next('strong').text.split()[1].split(':')[0]
                else:
                    COUNT = link.find('strong').find_next('strong').text.split()[1]

            if len(link.find('strong').find_next('strong').text.split()) == 3:
                if ':' in list(link.find('strong').find_next('strong').text.split()[0]):
                    COUNT = link.find('strong').find_next('strong').text.split()[0].split(':')[1]

                DEATHS = link.find('strong').find_next('strong').text.split()[1].split('(')[1]

            if len(link.find('strong').find_next('strong').text.split()) == 4:
                COUNT = link.find('strong').find_next('strong').text.split()[1]
                DEATHS = link.find('strong').find_next('strong').text.split()[2].split('(')[1]

        object = {
            'STATE': link.find('strong').text,
            'URL': link['href'],
            'COUNT': COUNT,
            'DEATHS': DEATHS
        }

        URL.append(object)

    return URL

def parse():
    for link in get_links():
        try:
            listInformation = BeautifulSoup(requests.get(link['URL']).text, 'html.parser').find('div', id='article-body').find('ul').find_all('li')

            print(listInformation[0].text)

            if 'Deadliest' in listInformation[0].text.split():
                CITY = {
                    'STATE': link['STATE'],
                    'COUNTY': '',
                    'COUNT': link['COUNT'],
                    'DEATHS': link['DEATHS'],
                }

                DATA.append(CITY)

                continue
                
            for object in listInformation:
                numberDeaths = 0

                try:
                    numberInfected = object.text.split(':')[1]
                    countyName = object.text.split(':')[0]

                    if len(object.text.split(':')[1].split()) > 1:
                        numberInfected = object.text.split(':')[1].split('(')[0]
                        numberDeaths = object.text.split(':')[1].split('(')[1].split()[0]

                except:
                    if '-' in list(object.text):
                        if len(object.text.split('-')) > 2:
                            countyName = ' '.join(object.text.split()[0:2])
                            numberInfected = object.text.split()[3]
                        else:
                            countyName = object.text.split('-')[0]
                            numberInfected = object.text.split('-')[1]
                    else:
                        numberInfected = object.text.split()[1]
                        countyName = object.text.split()[0]

                CITY = {
                    'STATE': link['STATE'],
                    'COUNTY': countyName,
                    'COUNT': numberInfected,
                    'DEATHS': numberDeaths
                }

                DATA.append(CITY)

        except:
            CITY = {
                'STATE': link['STATE'],
                'COUNTY': '',
                'COUNT': link['COUNT'],
                'DEATHS': link['DEATHS'],
            }

            DATA.append(CITY)

def main():
    response = requests.get('https://www.livescience.com/coronavirus-updates-united-states.html')

    if response.status_code == 200:
        parse()

        data = pd.DataFrame(data = DATA)
        data.to_csv('data.csv')

    else:
        print('Error')

if __name__ == '__main__':
    main()
