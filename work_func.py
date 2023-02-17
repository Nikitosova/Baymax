import time

import pandas as pd

import json

from scipy.spatial.distance import cosine

from help_funcs import lemmatize, create_tf_idf

df = pd.read_csv('processed_data/processed_data_ok.csv', index_col='index', encoding='utf-32')

# подгружаем словарь с пронумерованными словами
with open('processed_data/words_indices_ok.json', 'r') as f:
    words_indices = json.load(f)

# подгружаем словарь idf
with open('processed_data/idf_data_ok.json', 'r') as f:
    idf = json.load(f)

df['tf_idf'] = df['tf_idf'].apply(json.loads)


def get_best_urls(user_text: str):
    ts = time.time()
    lemmatize_text = lemmatize(user_text).split()
    good_words = []
    for word in lemmatize_text:
        if word in idf:
            good_words.append(word)

    if len(good_words) == 0:
        return []

    my_tf_idf = create_tf_idf(idf, [good_words], words_indices)[0]
    # (0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 , 0.123124124, 0 ,0 ,0 ,0 ,0  ,0 ,0 , 0.4543223432, 0,0,0,0,0)

    good_i = {}
    for i, val in enumerate(my_tf_idf):
        if val > 0:
            good_i[i] = val

    result = []
    for i, row in df.iterrows():
        check = False
        tf_idf = row['tf_idf']
        for g_i in good_i:
            if tf_idf[g_i] > 0:
                check = True
                break

        if check:
            score = cosine(tf_idf, my_tf_idf)
            if 0 < score < 1:
                result.append([score, row['link']])

    result.sort(key=lambda x: x[0])

    urls = []
    for score, link in result:
        urls.append(link)

    print('total', time.time() - ts)
    return urls


if __name__ == '__main__':
    text = 'Про любовь и отношения'
    my_urls = get_best_urls(text)
    print(*my_urls, sep='\n')
