import requests
from bs4 import BeautifulSoup

def test():
    target = 'https://vneconomy.vn/tim-kiem.htm?q=fpt'

    response = requests.get(target)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    print(soup)
    articles = soup.find_all('article', class_='story')
    print(articles)

test()

# response = requests.get('https://api.ipify.org?format=json')
# print(response.content)
