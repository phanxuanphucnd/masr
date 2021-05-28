import numpy as np
from data_generator import AudioGenerator
from utils import int_sequence_to_text
from models import *
from datetime import datetime
import json
import os
import argparse

def get_predictions(index, partition, input_to_softmax, model_path):
    '''
    Get the model's decoded predictions to caculate metrics
    '''
    # load the train and test data
    data_gen = AudioGenerator()
    data_gen.load_train_data()
    data_gen.load_validation_data()

    # obtain the true transcription and the audio features
    if partition == 'valid':
        transcr = data_gen.valid_texts[index]
        audio_path = data_gen.valid_audio_paths[index]
        data_point = data_gen.normalize(data_gen.featurize(audio_path))
    elif partition == 'train':
        transcr = data_gen.train_texts[index]
        audio_path = data_gen.train_audio_paths[index]
        data_point = data_gen.normalize(data_gen.featurize(audio_path))
    else:
        raise Exception('Invalid')

    # obtain and decode the acoustic model's predictions
    input_to_softmax.load_weights(model_path)
    prediction = input_to_softmax.predict(np.expand_dims(data_point, axis=0))
    output_length = [input_to_softmax.output_length(data_point.shape[0])]
    pred_ints = (K.eval(K.ctc_decode(
        prediction, output_length)[0][0]) + 1).flatten().tolist()

    label = transcr
    predicted =''.join(int_sequence_to_text(pred_ints))

    return label, predicted

def _predict(name="200_32_3.wav"):
    '''
    Get the predicted results of a single sample
    :param name:
    '''

    # load the train and test data
    data_gen = AudioGenerator()
    data_gen.load_train_data()
    data_gen.load_validation_data()

    audio_path_valid = data_gen.valid_audio_paths
    audio_path_train = data_gen.train_audio_paths
    idx = -1
    partition = "valid"
    for i in range(len(audio_path_valid)):
        rets = audio_path_valid[i].split('/')
        if rets[-1] == name:
            idx = i
            break
    if idx == -1:
        for i in range(len(audio_path_train)):
            rets = audio_path_train[i].split('/')
            if rets[-1] == name:
                idx = i
                partition = "train"
                break

    start = datetime.now()
    label, predicted = get_predictions(index=idx,
                                       partition=partition,
                                       input_to_softmax=mmodel1(input_dim=13,
                                                                filters=512,
                                                                kernel_size=5,
                                                                conv_stride=1,
                                                                conv_border_mode='same',
                                                                units=1024,
                                                                output_dim=95),
                                       model_path='results/mmodel1.h5')
    time = datetime.now() - start
    return label, predicted, str(time)

def evaluate(flabel_name, fpredict_name):
    input_dim = 13
    labels = []
    predicteds = []
    # read valid data
    jvf = open('./valid_corpus.json', 'r+', encoding='utf-8')
    valids_data = jvf.readlines()

    for i in range(len(valids_data)):
        label, predicted = get_predictions(index=i,
                                          partition='valid',
                                          input_to_softmax=mmodel1(input_dim=input_dim,
                                                                  filters=512,
                                                                  kernel_size=5,
                                                                  conv_stride=1,
                                                                  conv_border_mode='same',
                                                                  units=1024,
                                                                  output_dim=95),
                                          model_path='results/mmodel1.h5')

        label_wf = open(flabel_name, 'a', encoding='utf-8')
        predicted_wf = open(fpredict_name, 'a', encoding='utf-8')

        labels.append(label)
        label_wf.writelines(label + '\n')
        predicteds.append(predicted)
        predicted_wf.writelines(predicted + '\n')
        print('Example : ', predicted)

        predicted_wf.close()


if __name__=='__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--r', type=str, default="labels.txt",
                        help='file path save labels')
    parser.add_argument('--t', type=str, default='predictions.txt',
                        help='file path save predictions.')
    args = parser.parse_args()
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    _predict(name="200_32_4.wav")
    # evaluate(flabel_name=args.r, fpredict_name=args.t)