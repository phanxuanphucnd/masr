from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np

def get_phonemes():
    phonemes_count = {}
    f = open('./phonemes.txt', 'r+', encoding='utf-8')
    lines = f.readlines()
    phonemes = []
    for i in range(len(lines)):
        tmp = lines[i].strip()
        phonemes.append(tmp)
        phonemes_count[tmp] = 0

    return phonemes, phonemes_count

def get_lexicon_phonemes():
    word2phonemes = {}
    f = open('./lexicon_vietnamese_phoneme.txt', 'r+', encoding='utf-8')
    lines = f.readlines()
    for i in range(len(lines)):
        word = lines[i].split(' ')
        phonemes = []
        for p in range(1, len(word)):
            phonemes.append(word[p].strip())
        word2phonemes[word[0]] = phonemes
    return word2phonemes

def stat_phonemes_in_corpus():
    all_phonemes, phonemes_count = get_phonemes()
    word2phonemes = get_lexicon_phonemes()

    f = open('./corpus3k.txt', 'r+', encoding='utf-8')
    words = f.readlines()
    phonemes_corpus = []
    for i in range(len(words)):
        ws = words[i].strip().split()
        for w in ws:
            if w in word2phonemes:
                phonemes = word2phonemes[w]
                for phoneme in phonemes:
                    tmp = phoneme.strip()
                    phonemes_count[tmp] += 1
                    if tmp not in phonemes_corpus:
                        phonemes_corpus.append(tmp)


    n_phonemes = []
    for phoneme in all_phonemes:
        if phoneme not in phonemes_corpus:
            n_phonemes.append(phoneme)

    return phonemes_count

def plot(labels, values, name):

    indexs = np.arange(len(labels))
    plt.bar(indexs, values)
    plt.xlabel('Phoneme', fontsize=7)
    plt.ylabel('Number of phoneme', fontsize=7)
    plt.xticks(indexs, labels, fontsize=6, rotation='vertical')
    plt.title(name)
    plt.show()
    # plt.savefig('./' + name + '.png')


def visualize_distribution_phonemes(phonemes_stat):

    labels = []
    values = []
    for key, value in phonemes_stat.items():
        labels.append(key)
        values.append(value)

    sids = sorted(range(len(values)), key=lambda k: values[k])

    min_labels = [labels[i] for i in sids[:10]]
    min_values = [values[i] for i in sids[:10]]

    max_labels = [labels[i] for i in sids[-10:]]
    max_values = [values[i] for i in sids[-10:]]

    plot(labels=min_labels, values=min_values, name='10_least_phonemes')
    plot(labels=max_labels, values=max_values, name='10_most_phonemes')

def get_words_by_phoneme(phoneme, sp_corpus, lp_corpus):
    word2phones = get_lexicon_phonemes()
    max = 10
    min = 0
    for key, values in word2phones.items():
        if phoneme in values:
            tmp = 0
            ret = 0
            for phone in values:
                if phone in lp_corpus:
                    tmp += 1
                if phone in sp_corpus:
                    ret += 1
            if (tmp < max) or (ret > min):
                result = key
    return result

def analysis_corpus():

    corpus = []
    f = open('./corpus3k.txt', 'r+', encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        corpus.append(line.strip())

    count_sigle = 0
    count_double = 0
    count_triple = 0
    count_other = 0
    for i in range(len(corpus)):
        ret = corpus[i].split(' ')
        if len(ret) == 1:
            count_sigle += 1
        elif len(ret) == 2:
            count_double += 1
        elif len(ret) == 3:
            count_triple += 1
        else:
            count_other += 1

    count = [count_sigle, count_double, count_triple, count_other]

    return count

def get_words_add(phonemes_stat):
    word2phones = get_lexicon_phonemes()
    labels = []
    values = []
    sp_corpus = []
    lp_corpus = []
    for key, value in phonemes_stat.items():
        labels.append(key)
        values.append(value)

    sids = sorted(range(len(values)), key=lambda k: values[k])
    min_values = values[sids[0]]
    max_values = values[sids[-1]]
    _avg = 100
    for id in sids:
        if values[id] < _avg:
            sp_corpus.append(labels[id])
        else:
            lp_corpus.append(labels[id])
    # print(len(sp_corpus))
    # print(len(lp_corpus))
    words_add = []
    while True:
        for phone in sp_corpus:
            word = get_words_by_phoneme(phoneme=phone, sp_corpus=sp_corpus, lp_corpus=lp_corpus)
            words_add.append(word)
            phonemes = word2phones[word]
            for phoneme in phonemes:
                phonemes_stat[phoneme] += 1
                if (phonemes_stat[phoneme] >= _avg) and (phoneme in sp_corpus):
                    sp_corpus.remove(phoneme)
        if len(sp_corpus) == 0:
            break
    # print(words_add)
    # print(phonemes_stat)
    phonemes = []
    count = []
    for key, value in phonemes_stat.items():
        if value <= 400:
            phonemes.append(key)
            count.append(value)

    plot(phonemes, count, name="Distribution phonemes after Balancing")
    wf = open('./words_add.txt', 'w', encoding='utf-8')
    for word in words_add:
        wf.writelines(word + '\n')
    wf.close()

    return words_add, phonemes_stat


# if __name__=='__main__':

    # phonemes_stat = stat_phonemes_in_corpus()
    # visualize_distribution_phonemes(phonemes_stat)
    #
    # get_words_add(phonemes_stat)

    # print(analysis_corpus())
