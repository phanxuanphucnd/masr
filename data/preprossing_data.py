import sox
import os
from pprint import pprint

numbers_map = {
    '0':'không',
    '1': 'một',
    '2': 'hai',
    '3': 'ba',
    '4': 'bốn',
    '5': 'năm',
    '6': 'sáu',
    '7': 'bảy',
    '8': 'tám',
    '9': 'chín'
}

def segment_data(path):
    # id    = [1		2		3		4
    starts  = [0.5,	2.9,	4.9,	6.9]
    ends    = [2.9,  4.9,    6.9, 	9.5]
    starts2 = [0.0,	1.9,	3.9,	5.9]
    ends2   = [1.9,  3.9,    5.9, 	9.0]
    for folder in os.listdir(path):
        print('folder', folder)
        p_folder = path + folder
        if folder != "NB":
            if folder == "DTM3":
                s = starts2
                e = ends2
            else:
                s = starts
                e = ends
            for file in os.listdir(p_folder):
                tmps = file.split('.')
                if tmps[-1] == 'wav':
                    for i in range(len(s)):
                        tfm = sox.Transformer()
                        tfm.trim(start_time=s[i], end_time=e[i])
                        # tfm.compand()
                        # tfm.fade(fade_in_len=1.0, fade_out_len=0.5)
                        input = p_folder + '/' + file
                        print('Input', input)
                        output = p_folder + '/split/' + tmps[0] + '_' + str(i+1) + '.wav'
                        print(output + '\n')
                        tfm.build(input, output)
        else:
            print("Done!!!")

def index_to_description():

    f = open('./corpus3k.txt', 'r+', encoding='utf-8')
    res = f.readlines()
    idx2des = {}
    for i in range(len(res)):
        idx2des[str(i)] = res[i].strip()

    return idx2des

def generate_description(path, idx2des):

    for folder in os.listdir(path=path):
        if folder == "NB":
            p_folder = path + folder
            wf = open(p_folder + "/data_description.txt", 'w', encoding='utf-8')
            for file in os.listdir(p_folder):
                tmps = file.split('.')
                if tmps[-1] == 'wav':
                    rets = file.split('_')
                    text = tmps[0] + " " + numbers_map[rets[2]]
                    wf.write(text + '\n')

            wf.close()
        else:
            p_folder = path + folder
            wf = open(p_folder + "/data_description.txt", 'w', encoding='utf-8')
            for file in os.listdir(p_folder):
                tmps = file.split('.')
                if tmps[-1] == 'wav':
                    rets = tmps[0].split('_')
                    text = tmps[0] + " " + idx2des[rets[1]]
                    # print(text)
                    wf.write(text + '\n')

            wf.close()
    return None


def gen_test_desc():
    f = open('./test/DTM/test_corpus.txt', 'r+')
    lines = f.readlines()

    wf = open('./test/DTM/data_description.txt', 'w+')
    for line in lines:
        tmps = line.strip().split(' ')
        id = tmps[0]
        desc = ' '.join(tmps[1:]).lower()
        wr = '400_' + str(id) + ' ' + desc
        wf.writelines(wr + '\n')

    wf.close()

if __name__ == '__main__':

    # segment data
    # segment_data(path="./wav/")
    # generate mapping between index with description

    idx2des = index_to_description()

    # generate description for each file in each folder
    generate_description(path="./wav/", idx2des=idx2des)