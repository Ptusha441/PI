import requests     # Библиотека для HTTP-запросов
from bs4 import BeautifulSoup as bs     # Библиотека для работы с HTML-файлами
import re       # Библиотека для регулярных строк
import pandas as pd     # Библиотека для формирования CSV-файлов
# import matplotlib.pyplot as plt
# from nltk.corpus import stopwords
# from wordcloud import WordCloud
# import nltk

# Список ссылок на темы форума
URLS = [
    "https://habr.com/ru/flows/develop/",
    "https://habr.com/ru/flows/admin/",
    "https://habr.com/ru/flows/design/",
    "https://habr.com/ru/flows/marketing/"
]

URL = ""

MAX_PAGE = 2        # Максимальное количество страниц для парсинга
POST_NAME = []      # Список названий статей
POST_LINKS = []     # Список ссылок на статьи
TEXT = []           # Список содержаний статей
TIME = []           # Список дат публикаций статей
POST_NAME_AND_TIME = [] # Список названий статей с датой их публикации

# Стартовая функция. Выборка темы осуществляется через gui
def Start(topic):
    if (int(topic) == 1):
        URL = URLS[0]
    elif (int(topic) == 2):
        URL = URLS[1]
    elif (int(topic) == 3):
        URL = URLS[2]
    elif (int(topic) == 4):
        URL = URLS[3]
    print(URL)
    Parse(URL) # Запуск функции начала парсинга

# Парсинг главной страницы. Собираются названия статей, ссылки на статьи и дата публикации
def Parse(URL):
    for i in range(1, MAX_PAGE+1):  # Цикл по страницам
        URL_TEMPLATE = URL + 'page' + str(i) + '/'  # Формирование правильной ссылки на страницу форума
        r = requests.get(URL_TEMPLATE)  # Запрос страницы
        soup = bs(r.text, "html.parser")
        post = soup.find_all('a', class_='tm-article-snippet__title-link')  # Поиск части кода с данными поста
        time_post = soup.find_all('time')   # Поиск даты поста
        Get_Post_Name(post) # Запуск функции выделения названия статьи
        Get_Post_Link(post) # Запуск функции выделения ссылки статьи
        Get_Time(time_post) # Запуск функции выделения даты публикации статьи

# Сбор названий статей без тегов в список
def Get_Post_Name(post_name):
    pattern_span = "<span>"
    pattern_span1 = "</span>"
    for name in post_name:
        buf = re.sub(pattern_span, "", str(name.span))  # Удаление первого HTML-тега
        POST_NAME.append(re.sub(pattern_span1, "", buf))    # Удаление второго HTML-тега и добавление в список

# Сбор ссылок на посты в список
def Get_Post_Link(post):
    pattern_href = r"/ru/post/[\d]+/"
    links = re.findall(pattern_href, str(post)) # Поиск ссылок на посты
    for i in range(len(links)):
        POST_LINKS.append("https://habr.com" + links[i])    # Формирование правильных ссылок на посты и добавление в список
    Get_Text_Post() # Запуск функции сбора текста постов

# Сбор чистого текста статей в список
def Get_Text_Post():
    for i in range(len(POST_LINKS)):    # Цикл по ссылкам постов
        url = POST_LINKS[i]
        req_post = requests.get(url)    # Запрос страницы с постом
        soup_post = bs(req_post.text, "html.parser")
        text3 = re.sub(' xmlns="http://www.w3.org/1999/xhtml"', '',
                       str(soup_post.find_all('div', xmlns="http://www.w3.org/1999/xhtml")))    # Выборка текста из поста
        clear_text = re.sub(r'\<[^>]*\>', ' ', text3)   # Очистка текста от HTML-тегов
        TEXT.append(clear_text) # Сбор текста в список

# Создание csv файлов. Первый с текстом статей, второй название статей + дата публикации
def Collect_CSV():
    df_post = pd.DataFrame(data=TEXT)
    df_post.to_csv('POST_habr.csv') # Создание CSV-фалка с содержимым статей
    for i in range(len(POST_NAME)):
        POST_NAME_AND_TIME.append([POST_NAME[i], TIME[i]])  # Сбор списка с названиями статей и датами публикации
    df_postName = pd.DataFrame(data=POST_NAME_AND_TIME)
    df_postName.to_csv('POST_NAME_habr.csv')    # Создание CSV-файлов с названиями статей и датами публикации

# Сбор даты публикации в список
def Get_Time(time_post):
    for i in range(len(time_post)):
        patt_time = 'datetime="(.+)" '
        TIME.append(re.findall(patt_time, str(time_post[i])))   # Добавление дат публикации в список

def main(topic):
    Start(topic)    # Запуск стартовой функции
    Collect_CSV()   # Запуск функции для сборки CSV-файлов
    return int(1)

if __name__ == "__main__":
    main(None)