import pars_for_habr
import pars_for_proglib
import gui
"""
    Hello
"""
from wordcloud import WordCloud
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

POST_NAMES = []
NAME_AND_TIME = []

# Отрисовка облаков слов по месяцам (за 2022)
def Timelaps(POST_NAMES, NAME_AND_TIME):
    for month in range(1, 13):
        cloud = ['none']
        # print("POST_NAMES size =", len(POST_NAMES))
        # print("POST_AND_TIME size =", len(NAME_AND_TIME))
        for i in range(len(POST_NAMES)):
            if (int(str(NAME_AND_TIME[i][1])[7:9]) <= month and int(str(NAME_AND_TIME[i][1])[2:6]) == 2022):
                cloud.append(POST_NAMES[i])

        nltk.download('stopwords', quiet=1)
        stop_words = stopwords.words('russian')
        wordcloud = WordCloud(width=800, height=600, max_font_size=40, stopwords=stop_words, background_color='white').generate(str(cloud))
        plt.figure()
        plt.imshow(wordcloud)#, interpolation="bilinear")
        plt.axis("off")
        plt.savefig('Cloud_' + str(month))

def Start(topic):
    x = pars_for_habr.main(topic)
    y = pars_for_proglib.main(topic)
    if (x == 1 and y == 1):
        POST_NAMES = pars_for_habr.POST_NAME + pars_for_proglib.POST_NAME
        NAME_AND_TIME = pars_for_habr.POST_NAME_AND_TIME + pars_for_proglib.POST_NAME_AND_TIME
        print("OK")

        Timelaps(POST_NAMES, NAME_AND_TIME)


def main():
    gui.main()
    print("#####################################3333")

if __name__ == "__main__":
    main()