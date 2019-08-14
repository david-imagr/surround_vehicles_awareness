
#import tensorflow.keras as keras
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input, Dropout, Reshape, Concatenate 
from tensorflow.keras.applications import ResNet50


def SDPN(summary=True):
    """
    Create and return Semantic-aware Dense Prediction Network.

    Parameters
    ----------
    summary : bool
        If True, network summary is printed to stout.

    Returns
    -------
    model : keras Model
        Model of SDPN

    """
    input_coords = Input(shape=(4,))
    #input_crop = Input(shape=(3, 224, 224))
    input_crop = Input(shape=(224, 224, 3))

    # extract feature from image crop
    resnet = ResNet50(include_top=False, weights='imagenet')
    for layer in resnet.layers:  # set resnet as non-trainable
        layer.trainable = False

    crop_encoded = resnet(input_crop)  # shape of `crop_encoded` is 2018x1x1
    crop_encoded = Reshape(target_shape=(2048,))(crop_encoded)

    # encode input coordinates
    h = Dense(256, activation='relu')(input_coords)
    h = Dropout(0.25)(h)
    h = Dense(256, activation='relu')(h)
    h = Dropout(0.25)(h)
    h = Dense(256, activation='relu')(h)

    # merge feature vectors from crop and coords
    merged = tf.keras.layers.concatenate([crop_encoded, h])
    #merge([crop_encoded, h], mode='concat')

    # decoding into output coordinates
    h = Dense(1024, activation='relu')(merged)
    h = Dropout(0.25)(h)
    h = Dense(1024, activation='relu')(h)
    h = Dropout(0.25)(h)
    h = Dense(512, activation='relu')(h)
    h = Dropout(0.25)(h)
    h = Dense(256, activation='relu')(h)
    h = Dropout(0.25)(h)
    h = Dense(128, activation='relu')(h)
    h = Dropout(0.25)(h)

    output_coords = Dense(4, activation='tanh')(h)

    model = Model(inputs=[input_coords, input_crop], outputs=output_coords)

    if summary:
        model.summary()

    return model
