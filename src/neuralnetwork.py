# Python 3.11.3
import numpy as np
import tensorflow as tf
import json

from PIL import Image
    

def preprocess_image(file_path):
    return tf.image.decode_image(tf.io.read_file(file_path))  
      
def resnet_batched(image_list, model):
    file_tensors = []
    for im in image_list:
        image = tf.cast(im, tf.float32)
        image = tf.image.resize(image, (224, 224))
        image = tf.keras.applications.resnet50.preprocess_input(image)
        file_tensors.append(image)
    
    if len(image_list) == 1:
        image_batch = image[None, ...]
    else:
        image_batch = tf.stack(file_tensors, axis=0)

    image_probs = model.predict(image_batch)
    class_indices = np.argmax(image_probs, axis = 1)
    return image_probs, [np.argmax(image_probs[i]) for i in range(len(image_list))]
    

