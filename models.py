import pprint
import numpy as np
from keras.preprocessing import image
import tensorflow.compat.v1 as tf

from tensorflow.keras.applications import inception_v3
from tensorflow.keras.applications.inception_v3 import InceptionV3

from tensorflow.keras.applications import resnet50
from tensorflow.keras.applications.resnet50 import ResNet50

import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import List


class ModelInceptionV3:

    def __init__(self) -> None:
        
        self.model = InceptionV3(weights='imagenet')
    
    def predict(self, image_path):

        img = tf.keras.utils.load_img(image_path, target_size=(299,299))

        input_img = tf.keras.utils.img_to_array(img)
        input_img = np.expand_dims(input_img, axis=0)
        input_img = inception_v3.preprocess_input(input_img)

        predict_img = self.model.predict(input_img)

        top_five_predict = inception_v3.decode_predictions(predict_img, top=5)

        return top_five_predict


class ModelResNet50:

    def __init__(self) -> None:
        
        self.model = ResNet50(weights='imagenet')
    
    def predict(self, image_path):

        img = tf.keras.utils.load_img(image_path, target_size=(224, 224))

        input_img = tf.keras.utils.img_to_array(img)
        input_img = np.expand_dims(input_img, axis=0)
        input_img = resnet50.preprocess_input(input_img)

        predict_img = self.model.predict(input_img)

        top_five_predict = resnet50.decode_predictions(predict_img, top=5)

        return top_five_predict
    
    def multi_predict(self, images):

        results = []

        for image in images:
            results.append(self.predict(image))
        
        return results


async def perform_inference(model, files):
    with ProcessPoolExecutor() as process_pool:

        batch_files = []

        single_batch = []
        for file in files:
            if len(single_batch) <= 10:
                single_batch.append(file)
            else:
                batch_files.append(single_batch)
                single_batch = []
                single_batch.append(file)
        
        if len(single_batch) != 0:
            batch_files.append(single_batch)
            single_batch = []

        loop: AbstractEventLoop = asyncio.get_running_loop()
        calls: List[partial[int]] = [partial(model.multi_predict, batch) for batch in batch_files]
        call_coros = []

        for call in calls:
            call_coros.append(loop.run_in_executor(process_pool, call))

        results = await asyncio.gather(*call_coros)

        for result in results:
            pprint(result)
