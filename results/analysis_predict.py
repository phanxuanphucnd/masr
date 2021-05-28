import matplotlib.pyplot as plt
import numpy as np

def read_file(path):

    dt = []
    lf = open(path, 'r+', encoding='utf-8')
    lines = lf.readlines()
    for line in lines:
        dt.append(line.strip())
    return dt

def analysis():

    labels = read_file(path='./labels_mmodel1.txt')
    predictions = read_file(path='./predicteds_mmodel1.txt')
    ss = {}

    wf = open('./compares.txt', 'w', encoding='utf-8')
    for i in range(len(labels)):
        lb = labels[i].split(' ')
        pd = predictions[i].split(' ')
        for j in range(len(lb)):
            try:
                s1 = lb[j]
            except IndexError:
                s1 = 'null'
            try:
                s2 = pd[j]
            except IndexError:
                s2 = 'null'
            if s1 != s2:
                wf.writelines(s1 + ' - ' + s2 + '\n')
    wf.close()

    return None

def plot():

    peoples = ["DTM1", "DTM2", "DTM3"]
    cers = [10.79, 4.51, 9.14]
    wers = [25.96, 12.62, 23.19]
    sers = [26.30, 12.97, 23.97]

    index = np.arange(3)
    width = 0.3

    plt.bar(index, cers, width, color='green', label='CER')
    plt.bar(index + width, wers, width, color='orange', label='WER')
    plt.bar(index + 2 * width, sers, width, color='gray', label='SER')
    plt.title("Kết quả đánh giá cho mỗi người nói với Model 2", fontsize=15)

    plt.ylabel("Error rate (%)", fontsize=12)
    plt.xlabel("Speakers", fontsize=12)
    plt.xticks(index + width / 2, peoples, fontsize=13)
    plt.axes().set_ylim([0, 100])
    plt.legend(loc='best')
    plt.show()

    peoples = ["DTM1", "DTM2", "DTM3"]
    cers = [92.32, 60.80, 79.42]
    wers = [97.2, 83.09, 93.35]
    sers = [97.77, 85.02, 94.43]

    index = np.arange(3)
    width = 0.3

    plt.bar(index, cers, width, color='green', label='CER')
    plt.bar(index + width, wers, width, color='orange', label='WER')
    plt.bar(index + 2 * width, sers, width, color='gray', label='SER')
    plt.title("Kết quả đánh giá cho mỗi người nói với Google API", fontsize=15)

    plt.ylabel("Error rate (%)", fontsize=12)
    plt.xlabel("Speakers", fontsize=12)
    plt.xticks(index + width / 2, peoples, fontsize=13)
    plt.axes().set_ylim([0, 150])
    plt.legend(loc='best')
    plt.show()

    peoples = ["CER", "WER", "SER"]
    model1 = [17.07, 41.70, 42.44]
    model2 = [7.73, 19.67, 20.16]
    gg = [77.51, 91.21, 92.4]

    index = np.arange(3)
    width = 0.3

    plt.bar(index, model1, width, color='green', label='Model 1')
    plt.bar(index + width, model2, width, color='orange', label='Model 2')
    plt.bar(index + 2*width, gg, width, color='gray', label='vi-Google API')
    plt.title("Compare between Model 1, Model 2 and vi-Google API", fontsize=15)

    plt.ylabel("Error rate (%)", fontsize=12)
    plt.xlabel("Metrics", fontsize=12)
    plt.xticks(index + width / 2, peoples, fontsize=13)
    plt.axes().set_ylim([0, 100])
    plt.legend(loc='best')
    plt.show()


if __name__=='__main__':

    # analysis()

    plot()