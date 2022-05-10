import os
import smtplib
from datetime import datetime,timedelta,date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import cv2 as cv2
import imutils
import numpy as np
from flask import request, render_template, redirect, url_for, jsonify
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession, session
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.ImageDAO import ImageDAO
from project.com.dao.ZoneDAO import ZoneDAO
from project.com.vo.AreaVO import AreaVO
from project.com.vo.ImageVO import ImageVO


@app.route('/user/uploadImage', methods=['GET'])
def userLoadImage():
    try:
        if adminLoginSession() == "user":
            zoneDAO = ZoneDAO()
            areaDAO = AreaDAO()
            zoneVOList = zoneDAO.viewZone()

            areaVOList = areaDAO.viewArea()

            return render_template('user/addImage.html', zoneVOList=zoneVOList, areaVOList=areaVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

# ------------------------------------------UserAjax------------------------------------------------------#

@app.route('/user/ajaxAreauser', methods=['GET'])
def userAjaxAreaUser():
    try:
        if adminLoginSession() == 'user':
            print("oooooooo")
            areaVO = AreaVO()

            areaDAO = AreaDAO()

            area_ZoneId = request.args.get('image_ZoneId')

            areaVO.area_ZoneId = area_ZoneId

            ajaxUserAreaList = areaDAO.ajaxAreaUser(areaVO)

            ajaxUserAreaJson = [i.as_dict() for i in ajaxUserAreaList]

            return jsonify(ajaxUserAreaJson)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# --------------------------------------User--------------------------------------------------#

@app.route('/user/insertImage', methods=['POST', 'GET'])
def userInsertImage():
    try:
        if adminLoginSession() == 'user':

            modelName = 'project/static/adminResources/Garbage.model'

            INPUT_FOLDER = 'project/static/adminResources/input/'

            OUTPUT_FOLDER = 'project/static/adminResources/output/'

            app.config['INPUT_FOLDER'] = INPUT_FOLDER
            app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

            imageVO = ImageVO()
            imageDAO = ImageDAO()

            image_ZoneId = request.form['image_ZoneId']
            image_AreaId = request.form['image_AreaId']

            currentDate = str(datetime.now().date())
            currentTime = datetime.now().time().strftime('%H:%M:%S')

            file = request.files['file']

            imageInputFileName = secure_filename(file.filename)

            imageInputFilePath = os.path.join(app.config['INPUT_FOLDER'])

            file.save(os.path.join(imageInputFilePath, imageInputFileName))

            imageOutputFileName = imageInputFileName


            imageOutputFilePath = os.path.join(app.config['OUTPUT_FOLDER'])

            input_image = imageInputFilePath + imageInputFileName
            print(input_image)

            output_image = imageOutputFilePath + imageOutputFileName
            print(output_image)

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
            if (label == 'Garbage'):
                imageDetectionResult = "Garbage"
                imageWorkdoneStatus="Pending"
                date1 = datetime.now().date()
                imageWork_doneDate = date1 + timedelta(days=7)


                print(imageWork_doneDate)

                sender = "wastemanagmentwithai@gmail.com"

                receiver = session['session_loginUsername']
                print(receiver)

                notification = 'Garbage is detected. Soon it would be cleaned.'

                msg = MIMEMultipart()

                msg['From'] = sender

                msg['To'] = receiver

                msg['Subject'] = "WASTE MANAGMENT PASSWORD"

                msg.attach(MIMEText(notification, 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(sender, "wasteAI1998")

                text = msg.as_string()

                server.sendmail(sender, receiver, text)

                server.quit()

            else:
                imageDetectionResult = "Not Garbage"
                imageWorkdoneStatus= "Done"
                imageWork_doneDate="None"

            proba = garbage if garbage > notGarbage else notGarbage
            label = "{}: {:.2f}%".format(label, proba * 100)


            # email notification


            # draw the label on the image
            output = imutils.resize(orig, width=400)
            cv2.putText(output, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2)

            # show the output image
            cv2.imshow("output", output)

            cv2.waitKey(0)

            cv2.imwrite(output_image, output)

            # file.save(os.path.join(imageFilePath, imageFileName))





            imageVO.image_ZoneId = image_ZoneId
            imageVO.image_AreaId = image_AreaId
            imageVO.imageDetectionResult = imageDetectionResult

            imageVO.imageInputFileName = imageInputFileName
            imageVO.imageInputFilePath = imageInputFilePath.replace("project", "..")
            imageVO.imageOutputFileName = imageOutputFileName
            imageVO.imageOutputFilePath = imageOutputFilePath.replace("project", "..")
            imageVO.imageUploadDate = currentDate
            imageVO.imageUploadTime = currentTime
            imageVO.imageWorkdoneStatus = imageWorkdoneStatus
            imageVO.imageWork_doneDate = imageWork_doneDate
            imageVO.imageFrom_LoginId = session['session_loginId']

            imageDAO.insertImage(imageVO)


            return redirect(url_for('userViewImage'))

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewImage', methods=['GET'])
def userViewImage():
    try:
        if adminLoginSession() == "user":
            imageDAO = ImageDAO()
            imageVO = ImageVO()

            imageFrom_LoginId = session['session_loginId']
            imageVO.imageFrom_LoginId = imageFrom_LoginId

            imageVOList = imageDAO.viewUserImage(imageVO)

            print("__________________", imageVOList)
            return render_template('user/viewImage.html', imageVOList=imageVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deleteImage', methods=['GET'])
def userDeleteImage():
    try:
        if adminLoginSession() == "user":
            imageDAO = ImageDAO()
            imageVO = ImageVO()
            print('2')

            imageId = request.args.get('imageId')
            imageVO.imageId = imageId
            print(imageId)
            imageList = imageDAO.deleteImage(imageVO)
            print('1')
            imageWorkdoneStatus = imageList.imageWorkdoneStatus

            imageInputFileName = imageList.imageInputFileName
            imageInputFilePath = imageList.imageInputFilePath.replace('..', 'project')
            print('2')

            imageOutputFileName = imageList.imageOutputFileName
            imageOutputFilePath = imageList.imageOutputFilePath.replace('..', 'project')
            print('3')

            input_fullpath = imageInputFilePath + imageInputFileName
            output_fullpath = imageOutputFilePath + imageOutputFileName
            print('4')

            os.remove(input_fullpath)
            os.remove(output_fullpath)

            if imageWorkdoneStatus == 'Replied':
                imageCleanInputFileName = imageList.imageCleanInputFileName
                imageCleanInputFilePath = imageList.imageCleanInputFilePath
                imageCleanOutputFileName = imageList.imageOutputFileName
                imageOutputFilePath = imageList.imageOutputFilePath
                print('5')

                input_fullpath = imageCleanInputFileName + imageCleanInputFilePath
                output_fullpath = imageCleanOutputFileName + imageOutputFilePath
                print('6')
                os.remove(input_fullpath)
                os.remove(output_fullpath)
                print('7')

            return redirect(url_for('userViewImage'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)

    @app.route('/user/viewImageWorkdoneReply', methods=['GET'])
    def userViewImageWorkdoneReply():
        try:
            if adminLoginSession() == "user":
                imageDAO = ImageDAO()
                imageVO = ImageVO()

                imageId = request.args.get('imageId')
                imageVO.imageId = imageId
                print(imageId)

                imageVOList = imageDAO.viewUserWorkdoneRely(imageVO)
                print('view Image Reply')
                print("__________________", imageVOList)
                return render_template('user/viewImageWorkdoneReply.html', imageVOList=imageVOList)
            else:
                adminLogoutSession()
        except Exception as ex:
            print(ex)
#--------------------------------------User Side Workdone Image-----------------------------------------#
@app.route('/user/viewImageWorkdoneReply', methods=['GET'])
def userViewImageWorkdoneReply():
    try:
        if adminLoginSession() == "user":
            imageDAO = ImageDAO()
            imageVO = ImageVO()

            imageId = request.args.get('imageId')
            imageVO.imageId = imageId
            print(imageId)

            imageVOList = imageDAO.viewUserWorkdoneRely(imageVO)
            print('view Image Reply')
            print("__________________", imageVOList)
            return render_template('user/viewImageWorkdoneReply.html', imageVOList=imageVOList)
        else:
             adminLogoutSession()
    except Exception as ex:
        print(ex)
#------------------------------------------------------Admin Side-----------------------------------------------
@app.route('/admin/viewUserImage')
def adminViewUserImage():
    try:
        if adminLoginSession() == "admin":
            imageDAO = ImageDAO()
            imageVO = ImageVO()

            imageWorkdoneStatus = "Pending"
            imageDetectionResult = "Not Garbage"

            imageVO.imageWorkdoneStatus = imageWorkdoneStatus
            imageVO.imageDetectionResult = imageDetectionResult
            imageVOList = imageDAO.viewAdminUserImage(imageVO)

            print("__________________", imageVOList)

            return render_template('admin/viewUserImage.html', imageVOList=imageVOList)

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
# ----------------------------------------Admin Side Image WorkDone--------------------------------------#

@app.route('/admin/loadImageWorkdoneReply', methods=['GET'])
def loadAdminImageWorkdoneReply():
    if adminLoginSession() == 'admin':
        try:
            imageId = request.args.get('imageId')
            print(imageId)

            return render_template('admin/addImageWorkdoneReply.html', imageId=imageId)
        except Exception as ex:
            print(ex)
    else:
        adminLogoutSession()


@app.route('/admin/insertImageWorkdoneReply', methods=['GET', 'POST'])
def addAdminImageWorkdoneReply():
    if adminLoginSession() == 'admin':
        try:
            imageVO = ImageVO()
            imageDAO = ImageDAO()
            imageId = request.form['imageId']

            print(imageId)

            modelName = 'project/static/adminResources/Garbage.model'
            INPUT_FOLDER = 'project/static/adminResources/InputWorkdone/'

            OUTPUT_FOLDER = 'project/static/adminResources/OutputWorkdone/'
            print('222222')

            app.config['INPUT_FOLDER'] = INPUT_FOLDER
            app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

            currentDate = str(datetime.now().date())
            currentTime = datetime.now().strftime('%H:%M:%S')
            file = request.files['file']

            imageCleanInputFileName = secure_filename(file.filename)

            imageCleanInputFilePath = os.path.join(app.config['INPUT_FOLDER'])

            file.save(os.path.join(imageCleanInputFilePath, imageCleanInputFileName))

            imageCleanOutputFileName = imageCleanInputFileName
            print('********************************************************8')

            imageCleanOutputFilePath = os.path.join(app.config['OUTPUT_FOLDER'])

            input_image = imageCleanInputFilePath + imageCleanInputFileName
            print(input_image)

            output_image = imageCleanOutputFilePath + imageCleanOutputFileName
            print(output_image)

            image = cv2.imread(input_image)
            print('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')

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
            if (label == 'Not Garbage'):
                imageWorkdoneStatus = 'Replied'



            else:
                imageWorkdoneStatus = 'Pending'


            proba = garbage if garbage > notGarbage else notGarbage
            label = "{}: {:.2f}%".format(label, proba * 100)

            # email notification


            # draw the label on the image
            output = imutils.resize(orig, width=400)
            cv2.putText(output, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2)

            # show the output image
            cv2.imshow("output", output)

            cv2.waitKey(0)

            cv2.imwrite(output_image, output)

            # file.save(os.path.join(imageFilePath, imageFileNa

            imageVO.imageId = imageId
            print(imageId)


            imageVO.imageWorkdoneStatus = imageWorkdoneStatus

            imageVO.imageCleanInputFileName = imageCleanInputFileName
            imageVO.imageCleanInputFilePath = imageCleanInputFilePath.replace("project", "..")
            imageVO.imageCleanOutputFileName = imageCleanOutputFileName
            imageVO.imageCleanOutputFilePath = imageCleanOutputFilePath.replace("project", "..")
            imageVO.imageCleanUploadDate = currentDate
            print(currentDate)
            imageVO.imageCleanUploadTime = currentTime
            imageVO.imageTo_LoginId = session['session_loginId']

            imageDAO.inserCleantImage(imageVO)

            return redirect(url_for('adminViewUserImage'))
        except Exception as ex:
            print(ex)
    else:
        adminLogoutSession()


#------------------------------------------------------View Notification----------------------------#
# @app.route('/admin/viewNotification', methods=["GET","POST"])
# def adminViewNotification():
#     try:
#         if adminLoginSession == 'admin':
#             imageVO = ImageVO()
#             imageDAO = ImageDAO()
#             print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
#
#             imageWork_doneDate = datetime.now().date()
#             imageVO.imageWork_doneDate = imageWork_doneDate
#
#             imageWorkdoneStatus = "Pending"
#             imageVO.imageWorkdoneStatus=imageWorkdoneStatus
#
#             imageVOList=imageDAO.viewNotification(imageVO)
#
#             return render_template ('admin/viewNotification.html',imageVOList=imageVOList)
#         else:
#             adminLogoutSession()
#
#     except Exception as ex:
#         print(ex)
#
#
