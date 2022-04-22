import pars_for_habr
import pars_for_proglib
import gui

from wordcloud import WordCloud     # Библиотека для сборки облака слов
import nltk     # Библиотека для готовых стоп-слов для облака слов
import matplotlib.pyplot as plt     # Библиотека для формирования изображения облака слов
from nltk.corpus import stopwords   # Список готовых стоп-слов

POST_NAMES = []     # Список названий статей
NAME_AND_TIME = []  # Список названий статей с датой публикации

# Отрисовка облаков слов по месяцам (за 2022)
def Timelaps(POST_NAMES, NAME_AND_TIME):
    # Цикл по месяцам
    for month in range(1, 13):
        cloud = ['none']
        for i in range(len(POST_NAMES)):
            # Для каждого поста идет проверка даты публикации
            if (int(str(NAME_AND_TIME[i][1])[7:9]) <= month and int(str(NAME_AND_TIME[i][1])[2:6]) == 2022):
                cloud.append(POST_NAMES[i])     # Выборка статей, соответствующих дате
        # Формирование облака слов
        nltk.download('stopwords', quiet=1)
        stop_words = stopwords.words('russian')
        wordcloud = WordCloud(width=800, height=600, max_font_size=40, stopwords=stop_words, background_color='white').generate(str(cloud))
        plt.figure()        # Отрисовка изображения облака слов
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.savefig('Cloud_' + str(month))      # Сохранение изображения в папку с приложением

# Стартовая функция
def Start(topic):
    x = pars_for_habr.main(topic)
    y = pars_for_proglib.main(topic)
    if (x == 1 and y == 1):     # Проверка отработки парсеров
        # Объединение списков из двух парсеров
        POST_NAMES = pars_for_habr.POST_NAME + pars_for_proglib.POST_NAME
        NAME_AND_TIME = pars_for_habr.POST_NAME_AND_TIME + pars_for_proglib.POST_NAME_AND_TIME
        print("OK")
        # Запуск функции сборки и отрисовки облаков-слов
        Timelaps(POST_NAMES, NAME_AND_TIME)


def main():
    gui.main()  # Запуск GUI
    print("#####################################END")

if __name__ == "__main__":
    main()