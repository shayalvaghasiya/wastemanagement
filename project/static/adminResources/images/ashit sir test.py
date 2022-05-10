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

# inputVideoPath = "input/"

# inputVideoName = 'gv-4.mp4'

# outputVideoPath = "output/"

# outputVideoName = inputVideoName

# output_video = outputVideoPath + outputVideoName

modelName = 'Garbage.model'

# input_video = inputVideoPath + inputVideoName

cap = cv2.VideoCapture(r'input/NotGarbage-2.mp4')
writer = None

i = 0
while (cap.isOpened()):
    ret, image = cap.read()

    orig = image.copy()
    if not ret:
        break
    # cv2.imwrite(r'image/frame' + str(i) + '.jpg', image)

    # image = cv2.imread(input_image)

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

    # show the output image
    output = cv2.flip(output, 0)

    if writer is None:
        fourcc = cv2.VideoWriter_fourcc(*'VP80')
        writer = cv2.VideoWriter(r'image/output.webm', fourcc, 20.0, (image.shape[1], image.shape[0]))

    writer.write(output)

    cv2.putText(output, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2)

    # cv2.waitKey(5)
    # cv2.imwrite(r'image/frame' + str(i) + '.jpg', output)
    if cv2.waitKey(1) & 0XFF == ('q'):
        break

# cv2.waitKey(0)

# cv2.imwrite(output_image, output)
cap.release()
writer.release()
cv2.destroyAllWindows()
