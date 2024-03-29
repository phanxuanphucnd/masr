from __future__ import absolute_import, division, print_function

import argparse
import json
import os
import wave


def main(data_directory, output_file):
    labels = []
    durations = []
    keys = []
    for speaker in os.listdir(data_directory):
        if speaker.startswith('.'):
            continue
        labels_file = os.path.join(data_directory, speaker,
                                   'data_description.txt')
        for line in open(labels_file):
            split = line.strip().split()
            file_id = split[0]
            label = ' '.join(split[1:]).lower()
            audio_file = os.path.join(data_directory, speaker,
                                      file_id) + '.wav'
            audio = wave.open(audio_file)
            duration = float(audio.getnframes()) / audio.getframerate()
            audio.close()
            keys.append(audio_file)
            durations.append(duration)
            labels.append(label)
    with open(output_file, 'w') as out_file:
        for i in range(len(keys)):
            line = json.dumps({'key': keys[i], 'duration': durations[i],
                              'text': labels[i]})
            out_file.write(line + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data_directory', type=str,
                        help='Path to data directory')
    parser.add_argument('output_file', type=str,
                        help='Path to output file')
    args = parser.parse_args()
    main(args.data_directory, args.output_file)