import speech_recognition as sr
import os

r = sr.Recognizer()

def _recognition(path):
    '''
    Using google api for recognize speech and return a text describe input file.
    Language : vietnamese
    :param path: path to raw audio file
    :return: text - The output is the recognized text
    '''

    with sr.WavFile(path) as source:
        audio = r.record(source)

    try:
        tmp = r.recognize_google(audio, language='vi-VN')
        return tmp
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return None


if __name__=='__main__':

    corpus = []
    f = open('./data/corpus3k.txt', 'r', encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        corpus.append(line.strip())


    speakers = ["DTM1", "DTM2", "DTM3"]

    for speaker in speakers:
        audio_files = []
        path = './data/test/' + speaker

        for file in os.listdir(path):
            audio_files.append(os.path.join(path, file))

        wf1 = open("./results/gg_predicts_" + speaker + ".txt", 'a+', encoding='utf-8')
        wf2 = open("./results/gg_labels_" + speaker + ".txt", 'a+', encoding='utf-8')
        for audio in audio_files:
            # print(audio)
            splits = audio.split('_')
            res = _recognition(audio)
            wf1.writelines(res.lower() + "\n")
            wf2.writelines(corpus[int(splits[1])] + "\n")

        wf1.close()
        wf2.close()