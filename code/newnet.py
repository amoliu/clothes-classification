import os
import keras as k

from keras import regularizers, initializers
from keras.models import Model, Sequential
from keras.layers import Input, InputLayer, Dense, Dropout, Flatten, Activation, concatenate
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization, GlobalAveragePooling2D
from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19
from keras.applications.resnet50 import ResNet50
from keras.applications.inception_v3 import InceptionV3
from keras.layers.merge import add

import densenet, densenet121


def model1(input_dim):
    model = Sequential()
    model.add(BatchNormalization(input_shape=(input_dim, input_dim, 3)))
    model.add(Conv2D(32, kernel_size=(3, 3), padding='same', activation='relu'))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, kernel_size=(3, 3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(128, kernel_size=(3, 3), padding='same', activation='relu'))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(256, kernel_size=(3, 3), padding='same', activation='relu'))
    model.add(Conv2D(256, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(17, activation='sigmoid'))
    return model

def model2(input_dim):
    model_ = Sequential()
    model_.add(Conv2D(64, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=(input_dim, input_dim, 3)))

    model_.add(Conv2D(64, (3, 3), activation='relu'))
    model_.add(MaxPooling2D(pool_size=(2, 2)))

    model_.add(Conv2D(128, (3, 3), activation='relu'))

    model_.add(Conv2D(128, (3, 3), activation='relu'))
    model_.add(MaxPooling2D(pool_size=(2, 2)))
    model_.add(Dropout(0.25))
    model_.add(Flatten())
    model_.add(Dense(128, activation='relu'))
    model_.add(Dropout(0.5))
    model_.add(Dense(17, activation='sigmoid'))
    return model_

def model11(input_dim):
    model = Sequential()
    model.add(BatchNormalization(input_shape=(input_dim, input_dim, 3)))
    model.add(Conv2D(32, kernel_size=(3, 3), padding='same', activation='relu'))
    model.add(Conv2D(32, (3, 3), padding='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, kernel_size=(3, 3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(128, kernel_size=(3, 3), padding='same', activation='relu'))
    model.add(Conv2D(128, (3, 3), padding='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Conv2D(128, (3, 3)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(256, kernel_size=(3, 3), padding='same', activation='relu'))
    model.add(Conv2D(256, (3, 3), padding='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Conv2D(256, (3, 3)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(17, activation='sigmoid'))
    return model


def block(in_layer, nchan):
    b1 = Conv2D(nchan, (3, 3), padding='same', kernel_initializer='he_uniform')(in_layer)
    b1 = BatchNormalization()(b1)
    b1 = Activation('relu')(b1)
    b2 = Conv2D(nchan, (3, 3), padding='same')(b1)
    b2 = BatchNormalization()(b2)
    b2 = Activation('relu')(b2)
    b3 = Conv2D(nchan, (3, 3), padding='same')(b2)
    b3 = BatchNormalization()(b3)
    b3 = Activation('relu')(b3)
    out_layer = concatenate([b1, b3], axis=3)
    out_layer = Conv2D(nchan, (1, 1), padding='same')(out_layer)
    return out_layer

def model3(input_dim, output_dim=17):
    inputs = Input(shape=(input_dim, input_dim, 3))

    down0 = block(inputs, 16)
    down0_pool = MaxPooling2D((2,2), strides=(2,2))(down0)

    down1 = block(down0_pool, 32)
    down1_pool = MaxPooling2D((2, 2), strides=(2, 2))(down1)

    down2 = block(down1_pool, 64)
    down2_pool = MaxPooling2D((2, 2), strides=(2, 2))(down2)

    down3 = block(down2_pool, 128)
    down3_pool = MaxPooling2D((2, 2), strides=(2, 2))(down3)

    down4 = block(down3_pool, 256)
    down4_pool = MaxPooling2D((2, 2), strides=(2, 2))(down4)

    feat = Flatten()(down4_pool)

    feat = Dropout(0.25)(feat)
    # feat = BatchNormalization()(feat)
    feat = Dense(512, activation='relu', name='clothes_encoding')(feat)

    output = Dropout(0.5)(feat)
    # feat = BatchNormalization()(feat)
    output = Dense(output_dim, activation='sigmoid')(output)
    return Model(inputs=inputs, outputs=output)

def model4(input_dim):
    # preprocess
    x = InputLayer(input_shape = (input_dim,input_dim,3)).input
    y1 = x
    x = Conv2D(16, kernel_size=(1, 1), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    # x = Conv2D(16, kernel_size=(7, 7), strides=(2,2), padding='valid', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(x)


    y2 = x
    x = Conv2D(32, kernel_size=(3, 3), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Conv2D(32, (3, 3), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Conv2D(32, (3, 3), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    y2 = Conv2D(32, (1, 1), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(y2)
    x = add([x, y2])
    x = MaxPooling2D(pool_size=(2, 2))(x)

    y3 = x
    x = Conv2D(64, kernel_size=(3, 3), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Conv2D(64, (3, 3), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Conv2D(64, (3, 3), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    y3 = Conv2D(64, (1, 1), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(y3)
    x = add([x, y3])
    x = MaxPooling2D(pool_size=(2, 2))(x)

    y4 = x
    x = Conv2D(128, kernel_size=(3, 3), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Conv2D(128, (3, 3), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Conv2D(128, (3, 3), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    y4 = Conv2D(128, (1, 1), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(y4)
    x = add([x, y4])
    x = MaxPooling2D(pool_size=(2, 2))(x)

    y5 = x
    x = Conv2D(256, kernel_size=(3, 3), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Conv2D(256, (3, 3), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Conv2D(256, (3, 3), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    y5 = Conv2D(256, (1, 1), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(y5)
    x = add([x, y5])
    x = MaxPooling2D(pool_size=(2, 2))(x)

    x = Conv2D(16, (1, 1), padding='same', kernel_regularizer=regularizers.L1L2(l2=1E-4), bias_regularizer=regularizers.L1L2(l2=1E-4))(x)

    x = Flatten()(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(17, activation='sigmoid')(x)

    return Model(input=y1, output=x)

def vgg16():
    base_model = VGG16(weights=None, include_top=False, input_shape = (224,224,3))
    # Classification block
    x = Flatten(name='flatten', input_shape=base_model.output_shape[1:])(base_model.output)
    x = Dense(512, activation='relu', name='fc1')(x)
    x = Dense(512, activation='relu', name='fc2')(x)
    x = Dense(17, activation='softmax', name='predictions')(x)

    model = Model(inputs=base_model.input, outputs=x)
    return model

def vgg16(input_dim, output_dim):
    base_model = VGG16(weights='imagenet', include_top=False, input_shape = (input_dim,input_dim,3))
    # base_model.load_weights('../weights/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5')
    # Classification block
    x = Flatten(name='flatten')(base_model.output)
    x = Dense(4096, activation='relu', name='fc1')(x)
    x = Dense(512, activation='relu', name='clothes_encoding')(x)
    x = Dense(output_dim, activation='softmax', name='predictions')(x)

    model = Model(inputs=base_model.input, outputs=x)
    return model

def vgg19():
    base_model = VGG19(weights=None, include_top=False, input_shape = (224,224,3))
    x = Flatten(name='flatten')(base_model.output)
    x = Dense(512, activation='relu', name='fc1')(x)
    x = Dense(512, activation='relu', name='fc2')(x)
    x = Dense(17, activation='softmax', name='predictions')(x)

    model = Model(inputs=base_model.input, outputs=x)
    return model


def resNet50(input_dim):
    base_model = ResNet50(weights=None, include_top=False, pooling='avg', input_shape = (input_dim,input_dim,3))
    base_model.load_weights("../weights/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5")
    # x = Flatten()(base_model.output)
    x = base_model.output
    x = Dropout(0.25)(x)
    x = Dense(1024, activation='relu', name='fc', kernel_initializer='he_uniform')(x)
    x = Dropout(0.5)(x)
    x = Dense(17, activation='softmax', name='predictions', kernel_initializer='he_uniform')(x)
    model = Model(inputs=base_model.input, outputs=x)
    # for layer in model.layers[:25]:
    #     layer.trainable = False
    return model

def inceptionV3(input_dim):
    base_model = InceptionV3(weights=None, include_top=False, input_shape = (input_dim,input_dim,3))
    # Classification block
    x = GlobalAveragePooling2D(name='avg_pool')(base_model.output)
    x = Dense(17, activation='softmax', name='predictions')(x)
    model = Model(inputs=base_model.input, outputs=x)
    return model

def denseNet(input_dim):
    base_model = densenet.DenseNet(input_shape=(input_dim, input_dim, 3), classes=17, dropout_rate=0.2, weights=None, include_top=False)
    x = Dense(17, activation='softmax', kernel_regularizer=regularizers.L1L2(l2=1E-4),
              bias_regularizer=regularizers.L1L2(l2=1E-4))(base_model.output)
    model = Model(inputs=base_model.input, outputs=x)

    # Load model
    weights_file = "../weights/DenseNet-40-12CIFAR10-tf.h5"
    if os.path.exists(weights_file):
        model.load_weights(weights_file)
        print("Model loaded.")
    return model


def denseNet121(input_dim, nd_classes):
    weights_path = '../weights/densenet121_weights_tf.h5'

    # Test pretrained model
    # base_model = densenet121.DenseNet(reduction=0.5, classes=1000, weights_path=weights_path)
    model = densenet121.densenet121_model(img_rows=input_dim, img_cols=input_dim, color_type=3, num_classes=nd_classes, weights_path = weights_path)
    return model
