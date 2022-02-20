from wordcloud import WordCloud
import nltk
import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

URLS = [
    "https://habr.com/ru/flows/develop/",
    "https://habr.com/ru/flows/admin/",
    "https://habr.com/ru/flows/design/",
    "https://habr.com/ru/flows/marketing/"
]

URL = ""

MAX_PAGE = 2
POST_NAME = []
POST_LINKS = []
TEXT = []
TIME = []
POST_NAME_AND_TIME = []

# Выборка темы, пока просто вписываем, потом через gui
def Start():
    print("Выберите одну из предложенных тем:")
    print("Разработка")
    print("Администрирование")
    print("Дизайн")
    print("Маркетинг")
    topic = str(input())
    if (topic == "Разработка"):
        URL = URLS[0]
    elif (topic == "Администрирование"):
        URL = URLS[1]
    elif (topic == "Дизайн"):
        URL = URLS[2]
    elif (topic == "Маркетинг"):
        URL = URLS[3]
    print(URL)
    Parse(URL)

# Парсинг главной страницы. Собираются названия статей, ссылки на статьи и дата публикации
def Parse(URL):
    for i in range(1, MAX_PAGE):
        URL_TEMPLATE = URL + 'page' + str(i) + '/'
        r = requests.get(URL_TEMPLATE)
        soup = bs(r.text, "html.parser")

        post = soup.find_all('a', class_='tm-article-snippet__title-link')
        time_post = soup.find_all('time')
        #print(time_post)
        Get_Post_Name(post)
        Get_Post_Link(post)
        Get_Time(time_post)

        #Timelaps(time_post)

# Сбор названий статей без тегов в список
def Get_Post_Name(post_name):
    pattern_span = "<span>"
    pattern_span1 = "</span>"
    for name in post_name:
        buf = re.sub(pattern_span, "", str(name.span))
        POST_NAME.append(re.sub(pattern_span1, "", buf))

# Сбор ссылок на посты в список
def Get_Post_Link(post):
    pattern_href = r"/ru/post/[\d]+/"
    links = re.findall(pattern_href, str(post))
    for i in range(len(links)):
        POST_LINKS.append("https://habr.com" + links[i])
    #print(POST_LINKS)
    Get_Text_Post()

# Сбор чистого текста статей в список
def Get_Text_Post():
    for i in range(len(POST_LINKS)):
        url = POST_LINKS[i]
        #print(url)
        req_post = requests.get(url)
        soup_post = bs(req_post.text, "html.parser")
        #text = soup_post.find_all('div', id='post-content-body')
        #text1 = soup_post.find_all('div', class_="article-formatted-body article-formatted-body_version-2")
        #text2 = soup_post.find_all('div', xmlns="http://www.w3.org/1999/xhtml")
        text3 = re.sub(' xmlns="http://www.w3.org/1999/xhtml"', '', str(soup_post.find_all('div', xmlns="http://www.w3.org/1999/xhtml")))
        #print(text3)

        clear_text = re.sub(r'\<[^>]*\>', ' ', text3)

        TEXT.append(clear_text)

# Создание csv файлов. Первый с текстом статей, второй название статей + дата публикации
def Collect_CSV():
    df_post = pd.DataFrame(data=TEXT)
    df_post.to_csv('POST.csv')
    for i in range(len(POST_NAME)):
        POST_NAME_AND_TIME.append([POST_NAME[i], TIME[i]])
    df_postName = pd.DataFrame(data=POST_NAME_AND_TIME)
    df_postName.to_csv('POST_NAME.csv')

# Сбор облака слов по названиям статей (не используется)
# def World_Cloud():
#     nltk.download('stopwords')
#     stop_words = stopwords.words('russian')
#     wordcloud = WordCloud(max_font_size=40, stopwords=stop_words).generate(str(POST_NAME))
#     plt.figure()
#     plt.imshow(wordcloud, interpolation="bilinear")
#     plt.axis("off")
#     plt.savefig('Cloud')

# Сбор даты публикации в список
def Get_Time(time_post):
    for i in range(len(time_post)):
        patt_time = 'datetime="(.+)" '
        TIME.append(re.findall(patt_time, str(time_post[i])))

# Отрисовка облаков слов по месяцам (без привязки к году)
def Timelaps():
    for month in range(1, 13):
        cloud = ['none']
        for i in range(len(POST_NAME)):
            if (int(str(POST_NAME_AND_TIME[0][1])[7:9]) <= month):
                cloud.append(POST_NAME[i])

        nltk.download('stopwords', quiet=1)
        stop_words = stopwords.words('russian')
        print(stop_words)
        wordcloud = WordCloud(max_font_size=40, stopwords=stop_words).generate(str(cloud))
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig('Cloud_' + str(month))

def main():
    Start()
    Collect_CSV()
    #World_Cloud()
    Timelaps()

if __name__ == "__main__":
    main()