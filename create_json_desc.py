from __future__ import absolute_import, division, print_function

import argparse
import json
import os
import wave


def main(data_directory, output_file, output_file_2):
    labels = []
    durations = []
    keys = []
    labels2 = []
    durations2 = []
    keys2 = []
    for speaker in os.listdir(data_directory):
        if speaker.startswith('.'):
            continue
        labels_file = os.path.join(data_directory, speaker,
                                   'data_description.txt')
        for line in open(labels_file):
            split = line.strip().split()
            file_id = split[0]
            tmps = file_id.split('_')
            label = ' '.join(split[1:]).lower()
            audio_file = os.path.join(data_directory, speaker,
                                      file_id) + '.wav'
            audio = wave.open(audio_file)
            duration = float(audio.getnframes()) / audio.getframerate()
            audio.close()
            if tmps[-1] == "4":
                keys2.append(audio_file)
                durations2.append(duration)
                labels2.append(label)
            else:
                keys.append(audio_file)
                durations.append(duration)
                labels.append(label)
    with open(output_file, 'w') as out_file:
        for i in range(len(keys)):
            line = json.dumps({'key': keys[i], 'duration': durations[i],
                              'text': labels[i]})
            out_file.write(line + '\n')

    with open(output_file_2, 'w') as out_file:
        for i in range(len(keys2)):
            line = json.dumps({'key': keys2[i], 'duration': durations2[i],
                              'text': labels2[i]})
            out_file.write(line + '\n')

def balacing_data():

    words_add = []
    wf = open('./data/words_add.txt', 'r+', encoding='utf-8')
    lines = wf.readlines()
    for line in lines:
        words_add.append(line.strip())

    descs = []
    df = open('./train_corpus.json', 'r+', encoding='utf-8')
    lines = df.readlines()
    for line in lines:
        descs.append(line.strip())

    wf = open('./data_augument.json', 'w', encoding='utf-8')
    for word in words_add:
        for desc in descs:
            ret = json.loads(desc)
            if word == ret['text']:
                wf.writelines(desc + '\n')
    wf.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data_directory', type=str,
                        help='Path to data directory')
    parser.add_argument('output_file', type=str,
                        help='Path to output file')

    parser.add_argument('output_file_2', type=str,
                        help='Path to output file 2')
    args = parser.parse_args()
    main(args.data_directory, args.output_file, args.output_file_2)

    # balacing_data()