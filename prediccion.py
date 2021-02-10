import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

import base64
import json

class predic:
  def __init__(self):
    self.longitud, self.altura = 224, 224
    self.cnn = load_model("modelo.h5")

  def predict(self,archivo):
    with open("t.jpg", "wb") as fh:
      fh.write(base64.b64decode(archivo.replace('data:image/jpeg;base64,','').replace(' ','+')))
    x = load_img("t.jpg",target_size=(self.longitud, self.altura))
    x = img_to_array(x)
    x = np.expand_dims(x, axis=0)
    array = self.cnn.predict(x)
    print(array)
    result = array[0]
    answer = np.argmax(result)
    return answer+1
