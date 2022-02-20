import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

print('Введите ссылку')
#URL = str(input())

#URL = 'https://smart-lab.ru/trading/extra/'
#URL = 'https://forum.finam.ru/topics/35-Raznoe'
URL = 'https://habr.com/ru/top/daily/'

MAX_PAGE = 2
POST_NAME = []
TEXT_IN_POST = []

def Start():
    for i in range(1, MAX_PAGE):
        URL_TEMPLATE = URL + 'page' + str(i) + '/'
        r = requests.get(URL_TEMPLATE)

        soup = bs(r.text, "html.parser")

        Get_Post_Name(soup)

        links = []
        #pat_link = r'"/ru/.+/blog/\d+/"'
        z = 'href="/blog/766889.php"'
        c = 'href="/ru/company/selectel/blog/650197/"'
        pat_link = r'/blog/\d+[/|\.php]?'
        links = re.findall(pat_link, c)
        #links = re.findall(pat_link, str(soup))
        print(links)
        #Get_Post(links)
href="/ru/company/selectel/blog/650197/"
def Get_Post_Name(soup):
    """gettext = set(soup.get_text().split('\n'))
    patt = r"[А-Яа-я]{2}"
    for item in gettext:
        if re.search(patt, item):
            POST_NAME.append(re.sub('(\t|\r|\xa0)', '', item.lstrip()))
    csv_file = pd.DataFrame(data=POST_NAME)
    csv_file.to_csv('Post Name.csv')"""

def Get_Post(links):
    for i in range(len(links)):
        max_len = len(links[i])
        url = URL[0:16] + links[i][1:max_len-1]
        print(url)
        link = requests.get(url)
        new_soup = bs(link.text, "html.parser")
        #print(new_soup)
        #print(new_soup.get_text())
        TEXT_IN_POST.append(re.sub('(\n|\r)', '', str(new_soup.get_text())))
    csv_file = pd.DataFrame(data=TEXT_IN_POST)
    csv_file.to_csv('text.csv')

def main():
    Start()

if __name__ == "__main__":
    main()