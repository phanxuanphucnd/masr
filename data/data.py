import random


def get_words_in_train_corpus():
    all_words_train = []
    cf = open('./corpus3k.txt', 'r+', encoding='utf-8')
    lines = cf.readlines()
    for line in lines:
        tmp = line.strip()
        if tmp not in all_words_train:
            all_words_train.append(tmp)

    return all_words_train

def get_words_in_lexicon():
    lf = open('./lexicon_vietnamese_phoneme.txt', 'r+', encoding='utf-8')
    lines = lf.readlines()
    all_words = []
    for line in lines:
        all_words.append(line.strip().split()[0])

    return all_words

def get_random_compound_words():
    f = open('./Vietnamese-Compound-Words.txt', 'r+', encoding='utf-8')
    lines = f.readlines()
    compound_words = []
    ids = []
    for i in range(300):
        ids.append(random.randint(0, len(lines)))

    for id in ids:
        compound_words.append(lines[id].strip().lower())

    wf = open('./test_compound_corpus.txt', 'w', encoding='utf-8')
    for w in compound_words:
        wf.writelines(w + '\n')
    wf.close()

def analysis_test_data():

    all_words_train = get_words_in_train_corpus()

    f = open('./test_compound_corpus.txt', 'r+', encoding='utf-8')
    lines = f.readlines()
    oow_train = []
    for line in lines:
        words = line.strip().split(' ')
        for word in words:
            if word not in all_words_train:
                oow_train.append(word)

    return oow_train

# get_random_compound_words()

# oow_train = analysis_test_data()

f = open('./test_compound_corpus.txt', 'r', encoding='utf-8')
lines = f.readlines()
wf = open('./test/12/data_desc.txt', 'w', encoding='utf-8')
for i in range(len(lines)):
    wf.writelines('600_' + str(i+1) + ' ' + lines[i].strip() + '\n')

wf.close()