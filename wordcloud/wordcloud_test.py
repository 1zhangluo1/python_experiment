import jieba
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

with open('report.txt', 'r', encoding='utf-8') as f:
    text = f.read()

wordlist = jieba.cut(text, cut_all=False)
word_space_split = " ".join(wordlist)

mask = np.array(Image.open('mask.png'))

wordcloud = WordCloud(
    font_path='simhei.ttf',
    background_color='white',
    max_words=2000,
    mask=mask,
    contour_color='green',
    contour_width=5
)

wordcloud.generate(word_space_split)

plt.figure(figsize=(20, 20))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

wordcloud.to_file('mask_report_wordcloud.png')
