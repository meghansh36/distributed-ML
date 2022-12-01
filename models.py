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

def run_inference_on_InceptionV3(image_files: list):

    modelObj = InceptionV3(weights='imagenet')

    results = []
    
    for image_file in image_files:

        # print(f"ModelInceptionV3: performing prediction on {image_file}")

        img = tf.keras.utils.load_img(image_file, target_size=(299,299))

        input_img = tf.keras.utils.img_to_array(img)
        input_img = np.expand_dims(input_img, axis=0)
        input_img = inception_v3.preprocess_input(input_img)

        predict_img = modelObj.predict(input_img)

        top_five_predict = inception_v3.decode_predictions(predict_img, top=5)

        results.append(top_five_predict)

    return results

def run_inference_on_ResNet50(image_files: list):

    modelObj = ResNet50(weights='imagenet')

    results = []
    
    for image_file in image_files:

        # print(f"ResNet50: performing prediction on {image_file}")

        img = tf.keras.utils.load_img(image_file, target_size=(224, 224))

        input_img = tf.keras.utils.img_to_array(img)
        input_img = np.expand_dims(input_img, axis=0)
        input_img = resnet50.preprocess_input(input_img)

        predict_img = modelObj.predict(input_img)

        top_five_predict = resnet50.decode_predictions(predict_img, top=5)

        results.append(top_five_predict)

    return results


async def perform_inference(model_name, files):
    
    function = None
    if model_name == "InceptionV3":
        function = run_inference_on_InceptionV3
    elif model_name == "ResNet50":
        function = run_inference_on_ResNet50
    else:
        return "Invalid model"
    
    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        call: partial[List[str]] = partial(function, files)
        call_coros = []
        call_coros.append(loop.run_in_executor(process_pool, call))

        results = await asyncio.gather(*call_coros)

        for result in results:
            pprint(result)