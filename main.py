import argparse
import tensorflow as tf
import os
from datetime import datetime

from keras.backend.tensorflow_backend import set_session
from models import *
from train_utils import train_model

# config = tf.ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0
# set_session(tf.Session(config=config))


def main(input_dim, train_desc_file, valid_desc_file, pickle_path, save_model_path, epochs=20):

    # model = mmodel(input_dim=input_dim, filters=1280, kernel_size=11,
    #                conv_stride=2, conv_border_mode='same', units=800, output_dim=95)
        
    model = mmodel1(input_dim=input_dim, filters=512, kernel_size=5, conv_stride=1,
                    conv_border_mode='same', units=1024, output_dim=95)

#     model = mmodel2(input_dim=input_dim, filters=640, kernel_sizes=[5, 5], 
#                       strides=[1, 1], units_birnn=1280, units_fc=800, 
#                       conv_border_mode='same', output_dim=95)
    train_model(input_to_softmax=model,
                train_json=train_desc_file,
                valid_json=valid_desc_file,
                pickle_path=pickle_path,
                save_model_path=save_model_path,
                epochs=epochs)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--input_dim', type=int, default=13,
                        help='Number of input dim')
    parser.add_argument('--train_desc_file', type=str, default='train_corpus.json',
                        help='Path to a JSON-line file that contains'
                             'training labels and paths to the audio files.')
    parser.add_argument('--valid_desc_file', type=str, default='valid_corpus.json',
                        help='Path to a JSON-line file that contains '
                             'validation labels and paths to the audio files.')
    parser.add_argument('--save_model_path', type=str, default='model.h5',
                        help='Directory to store the model.'
                             'This will create if no exist')
    parser.add_argument('--pickle_path', type=str, default='model.pickle',
                        help='Directory to store history model.'
                             'This will create if no exist')
    parser.add_argument('--epochs', type=int, default=20,
                        help='Number of epochs to train the model')
    args = parser.parse_args()

    start = datetime.now()
    
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"
    main(input_dim=args.input_dim, train_desc_file=args.train_desc_file,valid_desc_file=args.valid_desc_file,
         pickle_path=args.pickle_path, save_model_path=args.save_model_path, epochs=args.epochs)
    
    print('Training Time is : ', datetime.now() - start)