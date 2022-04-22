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
    "https://proglib.io/?tags%5B%5D=da3eaa9f-1111-4e25-83dd-8780deff020b&tags%5B%5D=84df170c-1733-43c4-8e5b-36c3a36539c7&tags%5B%5D=da3eaa9f-a824-4e25-83dd-8780deff020b&tags%5B%5D=da3eaa9f-3333-4e25-83dd-8780deff020b&tags%5B%5D=47511cec-0b77-49f8-9e2d-ddf9c987c08c&tags%5B%5D=1ea972a3-6255-471f-b2ff-7596d52bc1d8&tags%5B%5D=9c30ee82-d9a5-471f-be1c-3fb9af74dee8&tags%5B%5D=a35fb609-2a3f-40b8-bac4-34f90c91215f&tags%5B%5D=109de3e7-0e45-4bc6-934d-871133e27038&tags%5B%5D=ec6c74b7-a1b8-4252-b9b8-8288c9cbbf7e&tags%5B%5D=f208d8df-97e7-4877-b651-3e1001d52c12&tags%5B%5D=b5331f63-039e-453f-a339-586c0f11159a&page=1",   # Проектирование / Разработка
    "https://proglib.io/?tags%5B%5D=5dc3675d-3e03-4be9-bacc-f5ec303ae8f1&tags%5B%5D=3730cd81-5bd0-4043-b784-05e16b303b71&tags%5B%5D=c337ab66-809e-45f7-933f-18ac8c9e8b4a&tags%5B%5D=c6de2dc9-3fff-4872-9176-95b9213e81c0&tags%5B%5D=628742d6-e054-43ce-808e-e13acbc3e0d4&tags%5B%5D=f89a93e0-40d6-46fd-8e62-22bc8e261a98&tags%5B%5D=871ae764-771b-4cac-bf87-3cd4fa60a934&page=1",   # Менеджмент     / Администрирование
    "https://proglib.io/?tags%5B%5D=a1a14be3-fb53-463e-9fce-77cf85e5625e&tags%5B%5D=e6db1ab0-5d79-4f4a-a4f7-f65e66d87915&page=1", # Дизайн
    "https://proglib.io/?tags%5B%5D=56c14bc3-6e0d-4115-bd68-907fc3fcf2e8&tags%5B%5D=20c0330b-e151-4e50-adda-d1ac6c0dbd95&tags%5B%5D=9447d3de-6fe4-4d10-b5c7-eaa307d2e14b&tags%5B%5D=f8493fc5-3cbe-406b-9cdb-5d1d7764e59e&page=1"    # Бизнес         / Маркетинг
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
        URL_TEMPLATE = URL[:len(URL)-1] + str(i)  # Формирование правильной ссылки на страницу форума
        r = requests.get(URL_TEMPLATE)  # Запрос страницы
        soup = bs(r.text, "html.parser")
        post = soup.find_all('div', class_='preview-card__content')  # Поиск части кода с данными поста
        Get_Post_Name(post) # Запуск функции выделения названия статьи
        Get_Post_Link(post) # Запуск функции выделения ссылки статьи
        Get_Time()          # Запуск функции выделения даты публикации статьи

# Сбор названий статей без тегов в список
def Get_Post_Name(post_name):
    pattern_1 = "<h2 class=\"preview-card__title\">"
    pattern_2 = "</h2>"

    for name in post_name:
        buf = str(name)[str(name).find(pattern_1) + 32 : str(name).find(pattern_2)] # Поиск названия статей
        POST_NAME.append(re.sub(pattern_2, "", buf))    # Удаление второго HTML-тега и добавление в список

# Сбор ссылок на посты в список
def Get_Post_Link(post):
    pattern_link = r"/p/\S+\""

    for link in post:
        buf = re.findall(pattern_link, str(link))[0] # Поиск ссылок на посты
        POST_LINKS.append("https://proglib.io" + buf[:len(buf) - 1])    # Формирование правильных ссылок на посты и добавление в список
    Get_Text_Post() # Запуск функции сбора текста постов

# Сбор чистого текста статей в список
def Get_Text_Post():
    for url in POST_LINKS:    # Цикл по ссылкам постов
        req_post = requests.get(url)    # Запрос страницы с постом
        soup_post = bs(req_post.text, "html.parser")
        text = str(soup_post.find_all('div', class_='block__content ugc entity__content'))    # Выборка текста из поста
        clear_text = re.sub(r'\<[^>]*\>', ' ', text)   # Очистка текста от HTML-тегов
        TEXT.append(clear_text) # Сбор текста в список

# Создание csv файлов. Первый с текстом статей, второй название статей + дата публикации
def Collect_CSV():
    df_post = pd.DataFrame(data=TEXT)
    df_post.to_csv('POST_proglib.csv') # Создание CSV-фалка с содержимым статей
    for i in range(len(POST_NAME)):
        POST_NAME_AND_TIME.append([POST_NAME[i], TIME[i]])  # Сбор списка с названиями статей и датами публикации
    df_postName = pd.DataFrame(data=POST_NAME_AND_TIME)
    df_postName.to_csv('POST_NAME_proglib.csv')    # Создание CSV-файлов с названиями статей и датами публикации

# Сбор даты публикации в список
def Get_Time():
    for i in range(len(POST_LINKS)):
        TIME.append("##" + str(POST_LINKS[i][len(POST_LINKS[i]) - 10 :]))   # Добавление дат публикации в список

def main(topic):
    Start(topic)    # Запуск стартовой функции
    Collect_CSV()   # Запуск функции для сборки CSV-файлов
    return int(1)

if __name__ == "__main__":
    main(None)