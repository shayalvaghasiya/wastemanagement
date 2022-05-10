# USAGE
# python Test.py --model Garbage.model --image input/180.jpg

import cv2
import imutils
import numpy as np
from keras.models import load_model
# import the necessary packages
from keras.preprocessing.image import img_to_array

# construct the argument parse and parse the arguments
# load the image

inputImagePath = "input/"

inputImageName = '180.jpg'

outputImagePath = "output/"

outputImageName = inputImageName

output_image = outputImagePath + outputImageName

modelName = 'Garbage.model'

input_image = inputImagePath + inputImageName

image = cv2.imread(input_image)

orig = image.copy()

# pre-process the image for classification
image = cv2.resize(image, (28, 28))
image = image.astype("float") / 255.0
image = img_to_array(image)
image = np.expand_dims(image, axis=0)

# load the trained convolutional neural network
print("[INFO] loading network...")
model = load_model(modelName)

# classify the input image
(notGarbage, garbage) = model.predict(image)[0]

# build the label
label = "Garbage" if garbage > notGarbage else "Not Garbage"
proba = garbage if garbage > notGarbage else notGarbage
label = "{}: {:.2f}%".format(label, proba * 100)

# draw the label on the image
output = imutils.resize(orig, width=400)
cv2.putText(output, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (0, 255, 0), 2)

# show the output image
cv2.imshow("output", output)

cv2.waitKey(0)

cv2.imwrite(output_image, output)
