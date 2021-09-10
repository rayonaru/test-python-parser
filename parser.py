import csv
import requests
import shutil
from bs4 import BeautifulSoup as soup

page = 0
result = []
while True:
    request = requests.get('https://www.proplan.ru/dog/breeds/?page=' + str(page))
    response = soup(request.content, 'html.parser')
    items = response.select('.nppe-pro-plan-owners-breeds > .views-row')

    if len(items) == 0:
        print("[LOG]:site parsed")
        break
    
    for item in items:
        
        link = item.select("a", href=True)[0]['href']
        request = requests.get('https://www.proplan.ru' + str(link))
        response = soup(request.content, 'html.parser')

        photoUrl = response.select('.desktop img')[0]['src']
        print(photoUrl)

        photo = requests.get('https://www.proplan.ru' + str(photoUrl), stream = True)

        with open('photos/' + photoUrl.split("/")[-1],'wb') as f:
            shutil.copyfileobj(photo.raw, f)

        infotable = response.select('.info-table > tbody > tr')
        name = ''
        height = ''
        weigth = ''
        purpose = ''
        row = ';'
        for info in infotable:
            data = info.select('td')
            if data[0].text.find('Название породы') != -1:
               name = data[1].text.replace('\n\n', '').replace('\n', '')
            if data[0].text.find('Рост') != -1:
               height = data[1].text.replace('\n\n', '').replace('\n', '')
            if data[0].text.find('Вес') != -1:
               weigth = data[1].text.replace('\n\n', '').replace('\n', '')
            if data[0].text.find('Тип породы') != -1:
               purpose = data[1].text.replace('\n\n', '').replace('\n', '')

        if (name != ''):
            temp = [name, height, weigth, purpose]
            result.append(temp)

    page+=1

for item in result:
    print(item)

with open('test.csv', 'w', newline='') as mycsv:
     wr = csv.writer(mycsv, quoting=csv.QUOTE_ALL)
     wr.writerows(result)
