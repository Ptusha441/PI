from wordcloud import WordCloud
import nltk
import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

URLS = [
    "https://proglib.io/?tags%5B%5D=da3eaa9f-1111-4e25-83dd-8780deff020b&tags%5B%5D=84df170c-1733-43c4-8e5b-36c3a36539c7&tags%5B%5D=da3eaa9f-a824-4e25-83dd-8780deff020b&tags%5B%5D=da3eaa9f-3333-4e25-83dd-8780deff020b&tags%5B%5D=47511cec-0b77-49f8-9e2d-ddf9c987c08c&tags%5B%5D=1ea972a3-6255-471f-b2ff-7596d52bc1d8&tags%5B%5D=9c30ee82-d9a5-471f-be1c-3fb9af74dee8&tags%5B%5D=a35fb609-2a3f-40b8-bac4-34f90c91215f&tags%5B%5D=109de3e7-0e45-4bc6-934d-871133e27038&tags%5B%5D=ec6c74b7-a1b8-4252-b9b8-8288c9cbbf7e&tags%5B%5D=f208d8df-97e7-4877-b651-3e1001d52c12&tags%5B%5D=b5331f63-039e-453f-a339-586c0f11159a&page=1",   # Проектирование / Разработка
    "https://proglib.io/?tags%5B%5D=5dc3675d-3e03-4be9-bacc-f5ec303ae8f1&tags%5B%5D=3730cd81-5bd0-4043-b784-05e16b303b71&tags%5B%5D=c337ab66-809e-45f7-933f-18ac8c9e8b4a&tags%5B%5D=c6de2dc9-3fff-4872-9176-95b9213e81c0&tags%5B%5D=628742d6-e054-43ce-808e-e13acbc3e0d4&tags%5B%5D=f89a93e0-40d6-46fd-8e62-22bc8e261a98&tags%5B%5D=871ae764-771b-4cac-bf87-3cd4fa60a934&page=1",   # Менеджмент     / Администрирование
    "https://proglib.io/?tags%5B%5D=a1a14be3-fb53-463e-9fce-77cf85e5625e&tags%5B%5D=e6db1ab0-5d79-4f4a-a4f7-f65e66d87915&page=1", # Дизайн
    "https://proglib.io/?tags%5B%5D=56c14bc3-6e0d-4115-bd68-907fc3fcf2e8&tags%5B%5D=20c0330b-e151-4e50-adda-d1ac6c0dbd95&tags%5B%5D=9447d3de-6fe4-4d10-b5c7-eaa307d2e14b&tags%5B%5D=f8493fc5-3cbe-406b-9cdb-5d1d7764e59e&page=1"    # Бизнес         / Маркетинг
]

URL = ""

MAX_PAGE = 2
POST_NAME = []
POST_LINKS = []
TEXT = []
TIME = []
POST_NAME_AND_TIME = []

def Start(topic):
    """
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
        URL = URLS[3]"""

    if (int(topic) == 1):
        URL = URLS[0]
    elif (int(topic) == 2):
        URL = URLS[1]
    elif (int(topic) == 3):
        URL = URLS[2]
    elif (int(topic) == 4):
        URL = URLS[3]

    print(URL)
    Parse(URL)

# Парсинг главной страницы. Собираются названия статей, ссылки на статьи и дата публикации
def Parse(URL):
    for i in range(1, MAX_PAGE):
        URL_TEMPLATE = URL[:len(URL)-1] + str(i)
        r = requests.get(URL_TEMPLATE)
        soup = bs(r.text, "html.parser")
        #print(soup)
        #post = soup.find_all('h2', class_='preview-card__title')
        post = soup.find_all('div', class_='preview-card__content')
        #time_post = soup.find_all('a', class_='block__img')


        Get_Post_Name(post)
        Get_Post_Link(post)
        Get_Time()

# Сбор названий статей без тегов в список
def Get_Post_Name(post_name):
    pattern_1 = "<h2 class=\"preview-card__title\">"
    pattern_2 = "</h2>"

    for name in post_name:
        buf = str(name)[str(name).find(pattern_1) + 32 : str(name).find(pattern_2)]
        #buf = re.sub(pattern_1, "", str(name))
        POST_NAME.append(re.sub(pattern_2, "", buf))

# Сбор ссылок на посты в список
def Get_Post_Link(post):
    pattern_link = r"/p/\S+\""

    for link in post:
        buf = re.findall(pattern_link, str(link))[0]
        POST_LINKS.append("https://proglib.io" + buf[:len(buf) - 1])
    #print(POST_LINKS)
    Get_Text_Post()

# Сбор чистого текста статей в список
def Get_Text_Post():
    for url in POST_LINKS:
        req_post = requests.get(url)
        soup_post = bs(req_post.text, "html.parser")
        text = str(soup_post.find_all('div', class_='block__content ugc entity__content'))

        #print(re.findall(r"<h2>.+</h2>", text))
        #print(re.findall(r"<span>.+</span>", text))

        clear_text = re.sub(r'\<[^>]*\>', ' ', text)
        #print(clear_text)

        TEXT.append(clear_text)

# Создание csv файлов. Первый с текстом статей, второй название статей + дата публикации
def Collect_CSV():
    df_post = pd.DataFrame(data=TEXT)
    df_post.to_csv('POST_proglib.csv')
    for i in range(len(POST_NAME)):
        POST_NAME_AND_TIME.append([POST_NAME[i], TIME[i]])
    df_postName = pd.DataFrame(data=POST_NAME_AND_TIME)
    df_postName.to_csv('POST_NAME_proglib.csv')

# Сбор даты публикации в список
def Get_Time():
    for i in range(len(POST_LINKS)):
        TIME.append("##" + str(POST_LINKS[i][len(POST_LINKS[i]) - 10 :]))

# Отрисовка облаков слов по месяцам (за 2022)
"""def Timelaps():
    for month in range(1, 13):
        cloud = ['none']
        for i in range(len(POST_NAME)):
            if (int(str(POST_NAME_AND_TIME[i][1])[7:9]) <= month and int(str(POST_NAME_AND_TIME[i][1])[2:6]) == 2022):
                cloud.append(POST_NAME[i])

        nltk.download('stopwords', quiet=1)
        stop_words = stopwords.words('russian')
        wordcloud = WordCloud(max_font_size=40, stopwords=stop_words).generate(str(cloud))
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig('Cloud_' + str(month))"""


def main(topic):
    Start(topic)
    Collect_CSV()

    # Timelaps()
    return int(1)
    #World_Cloud()


if __name__ == "__main__":
    main(None)