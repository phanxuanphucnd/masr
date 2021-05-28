from keras import backend as K
from keras.models import Model
from keras.layers import (BatchNormalization, Conv1D, Dense, Input, 
    TimeDistributed, Activation, Bidirectional, SimpleRNN, GRU)

def cnn_output_length(input_length, filter_size, border_mode, stride,
                       dilation=1):

    if input_length is None:
        return None
    assert border_mode in {'same', 'valid'}
    if border_mode == 'same':
        output_length = input_length
    elif border_mode == 'valid':
        dilated_filter_size = filter_size + (filter_size - 1) * (dilation - 1)
        output_length = input_length - dilated_filter_size + 1
    return (output_length + stride - 1) // stride

def mmodel(input_dim, filters, kernel_size, conv_stride,
           conv_border_mode, units, output_dim=95):
    input_data = Input(name='the_input', shape=(None, input_dim))
    #TODO: Add conv1d layer
    conv1d_1 = Conv1D(filters, kernel_size, strides=conv_stride,
                    padding=conv_border_mode, activation='relu',
                    name='Conv1D_1')(input_data)
    conv1d_2 = Conv1D(filters, kernel_size, strides=conv_stride,
                    padding=conv_border_mode, activation='relu',
                    name='Conv1D_2')(conv1d_1)
    #TODO: Add batch norm
    bn_cnn = BatchNormalization(name='bn_conv1d')(conv1d_2)
    #TODO: Add recurrent layer
    rnn_1 = GRU(units, return_sequences=True, dropout=0.4, name='rnn_1')(bn_cnn)
    bn_rnn_1 = BatchNormalization(name='bn_rnn_1')(rnn_1)
    rnn_2 = GRU(units, return_sequences=True, dropout=0.4, name='rnn_2')(bn_rnn_1)
    bn_rnn_2 = BatchNormalization(name='bn_rnn_2')(rnn_2)
    rnn_3 = GRU(units, return_sequences=True, dropout=0.4, name='rnn_3')(bn_rnn_2)
    bn_rnn_3 = BatchNormalization(name='bn_rnn_3')(rnn_3)
    #TODO: Add TimeDistributed layer
    time_dense = TimeDistributed(Dense(output_dim))(bn_rnn_3)
    #TODO: Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)

    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: cnn_output_length(
        x, kernel_size, conv_border_mode, conv_stride)
    print(model.summary())

    return model

def mmodel1(input_dim, filters, kernel_size, conv_stride,
    conv_border_mode, units,output_dim=95):
    
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # TODO: Specify the layers in your network
    #TODO: Add convolutional layer
    conv1d_1 = Conv1D(filters, kernel_size, 
                     strides=conv_stride, 
                     padding=conv_border_mode,
                     activation='relu',
                     name='conv1d_1')(input_data)
    #TODO: Add batchnorm
    bn_cnn = BatchNormalization(name='bn_conv_1d')(conv1d_1)
    #TODO: Add recurrent layer and batchnorm
    bidir_rnn_1 = Bidirectional(GRU(units, return_sequences=True, name='bidir_rnn_1', dropout=0.5),
                                merge_mode='sum')(bn_cnn)
    bn_rnn_1 = BatchNormalization(name='bn_rnn_1')(bidir_rnn_1)
    bidir_rnn_2 = Bidirectional(GRU(units, return_sequences=True, name='bidir_rnn_2', dropout=0.5),
                                merge_mode='sum')(bn_rnn_1)
    bn_rnn_2 = BatchNormalization(name='bn_rnn_2')(bidir_rnn_2)
    # bidir_rnn_3 = Bidirectional(GRU(units, return_sequences=True, name='bidir_rnn_3', dropout=0.5),
    #                             merge_mode='sum')(bn_rnn_2)
    # bn_rnn_3 = BatchNormalization(name='bn_rnn_3')(bidir_rnn_3)
    # TODO: add TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(bn_rnn_2)
    # TODO: add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    # TODO: add Specify model.output_length
    model.output_length = lambda x: cnn_output_length(
        x, kernel_size, conv_border_mode, conv_stride)
    print(model.summary())
    return model

def mmodel2(input_dim=13, filters=640, kernel_sizes=[5, 5], strides=[1, 1], units_birnn=1280,
              units_fc=800, conv_border_mode='same', output_dim=95):
    input_data = Input(name='the_input', shape=(None, input_dim))
    #TODO: batch normalize input
    bn_1 = BatchNormalization(axis=-1, name="BN_1")(input_data)
    #TODO: 1D Convs
    conv_1d_1 = Conv1D(filters=filters, kernel_size=kernel_sizes[0], strides=strides[0], padding=conv_border_mode,
                       activation='relu', name='Conv1D_1')(bn_1)
    conv_1d_2 = Conv1D(filters=filters, kernel_size=kernel_sizes[1], strides=strides[1], padding=conv_border_mode,
                       activation='relu', name='Conv1D_2')(conv_1d_1)
    #TODO: batchnorm
    bn_2 = BatchNormalization(axis=-1, name="BN_2")(conv_1d_2)
    # biRNNs
    bi_rnn_1 = Bidirectional(SimpleRNN(units_birnn, return_sequences=True, name="BiRNN_1"),
                             merge_mode='sum')(bn_2)
    bi_rnn_2 = Bidirectional(SimpleRNN(units_birnn, return_sequences=True, name="BiRNN_1"),
                             merge_mode='sum')(bi_rnn_1)
    bi_rnn_3 = Bidirectional(SimpleRNN(units_birnn, return_sequences=True, name="BiRNN_1"),
                             merge_mode='sum')(bi_rnn_2)
    #TODO: batchnorm
    bn_3 = BatchNormalization(axis=-1, name="BN_3")(bi_rnn_3)
    #TODO: TimeDistributed(Dense(output_dim))
    time_dense = TimeDistributed(Dense(units_fc, activation='relu', name="FC_1"))(bn_3)
    y_pred = TimeDistributed(Dense(output_dim, activation='softmax', name='y_pred'))(time_dense)

    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: cnn_output_length(
        x, filter_size=5,  border_mode=conv_border_mode, stride=1)

    print(model.summary())
    
    return model