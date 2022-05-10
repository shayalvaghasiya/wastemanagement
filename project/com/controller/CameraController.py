import os
from datetime import datetime

import cv2
import imutils
import numpy as np
from flask import render_template, url_for, redirect, request, jsonify
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.CameraDAO import CameraDAO
from project.com.dao.ImageDAO import ImageDAO
from project.com.dao.ZoneDAO import ZoneDAO
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CameraVO import CameraVO
from project.com.vo.ImageVO import ImageVO


@app.route('/admin/loadCamera', methods=['GET'])
def adminLoadCamera():
    print('loadCamera')
    try:
        if adminLoginSession() == "admin":

            zoneDAO = ZoneDAO()
            zoneVOList = zoneDAO.viewZone()

            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()

            return render_template('admin/addCamera.html', zoneVOList=zoneVOList, areaVOList=areaVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertCamera', methods=['POST', 'GET'])
def adminInsertCamera():
    try:
        if adminLoginSession() == "admin":
            modelName = 'project/static/adminResources/Garbage.model'

            INPUT_FOLDER = 'project/static/adminResources/input/'

            OUTPUT_FOLDER = 'project/static/adminResources/output/'

            app.config['INPUT_FOLDER'] = INPUT_FOLDER
            app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

            cameraVO = CameraVO()
            cameraDAO = CameraDAO()

            cameraCode = request.form['cameraCode']
            camera_AreaId = request.form['camera_AreaId']
            camera_ZoneId = request.form['camera_ZoneId']

            currentDate = str(datetime.now().date())
            currentTime = datetime.now().time().strftime('%H:%M:%S')

            file = request.files['file']

            cameraInputFileName = secure_filename(file.filename)

            cameraInputFilePath = os.path.join(app.config['INPUT_FOLDER'])

            file.save(os.path.join(cameraInputFilePath, cameraInputFileName))

            cameraOutputFileName = cameraInputFileName.replace('.mp4','.webm')
            print(cameraOutputFileName)

            cameraOutputFilePath = os.path.join(app.config['OUTPUT_FOLDER'])
            print(cameraOutputFilePath)

            input_video = cameraInputFilePath + cameraInputFileName
            print(input_video)

            output_video = cameraOutputFilePath + cameraOutputFileName
            print(output_video)

            cap = cv2.VideoCapture(input_video)
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))
            print(frame_width, frame_height)
            i = 0.0
            n = 0.0
            fourcc = cv2.VideoWriter_fourcc(*'VP80')
            out = cv2.VideoWriter(output_video, fourcc, 5.0, (frame_width, frame_height))
            print('4')
            while cap.isOpened():
                ret, image = cap.read()
                if not ret:
                    break
                print('4')
                print(image.shape)
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

                if label == 'Garbage':
                    i = i + 1
                else:
                    n = n + 1

                proba = garbage if garbage > notGarbage else notGarbage

                label = "{}: {:.2f}%".format(label, proba * 100)

                # draw the label on the image
                output = imutils.resize(orig, width=frame_width)  # , height=frame_height)

                # output = cv2.rotate(output, cv2.ROTATE_90_CLOCKWISE)
                cv2.putText(output, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 255, 0), 2)

                print("Output shape", output.shape)

                out.write(output)

                cv2.imshow("output", output)

                if cv2.waitKey(1) & 0XFF == ord('q'):
                    break

            if (i > n):
                print('Yes')
                cameraDetectionResult = "Garbage"

            else:
                print('NO')
                cameraDetectionResult = "Not Garbage"
            out.release()
            cap.release()
            cv2.destroyAllWindows()

            cameraVO.cameraCode = cameraCode
            cameraVO.camera_AreaId = camera_AreaId
            cameraVO.camera_ZoneId = camera_ZoneId
            cameraVO.cameraInputFileName = cameraInputFileName
            cameraVO.cameraInputFilePath = cameraInputFilePath.replace("project", "..")
            cameraVO.cameraDetectionResult = cameraDetectionResult
            cameraVO.cameraOutputFileName = cameraOutputFileName
            cameraVO.cameraOutputFilePath = cameraOutputFilePath.replace("project", "..")
            cameraVO.cameraUploadTime = currentTime
            cameraVO.cameraUploadDate = currentDate

            cameraDAO.insertCamera(cameraVO)

            return redirect(url_for('adminViewCamera'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewCamera')
def adminViewCamera():
    try:
        if adminLoginSession() == "admin":
            print('viewCamera')
            cameraDAO = CameraDAO()

            cameraVOList = cameraDAO.viewCamera()
            print(cameraVOList)

            print("__________________", cameraVOList)
            return render_template('admin/viewCamera.html', cameraVOList=cameraVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/deleteCamera', methods=['GET'])
def adminDeleteCamera():
    try:
        if adminLoginSession() == "admin":
            cameraVO = CameraVO()
            cameraDAO = CameraDAO()

            cameraId = request.args.get('cameraId')

            cameraVO.cameraId = cameraId

            cameraList = cameraDAO.deleteCamera(cameraVO)
            print('1222222')

            cameraInputFileName = cameraList.cameraInputFileName
            cameraInputFilePath = cameraList.cameraInputFilePath.replace('..', 'project')
            print('3333333333333')

            cameraOutputFileName = cameraList.cameraOutputFileName
            cameraOutputFilePath = cameraList.cameraOutputFilePath.replace('..', 'project')
            print('111111111111')
            print(cameraOutputFilePath)

            input_fullpath = cameraInputFilePath + cameraInputFileName
            output_fullpath = cameraOutputFilePath + cameraOutputFileName

            os.remove(input_fullpath)
            os.remove(output_fullpath)

            return redirect(url_for('adminViewCamera'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)



@app.route('/admin/editCamera', methods=['GET'])
def adminEditCamera():
    try:
        if adminLoginSession() == "admin":

            cameraVO = CameraVO()
            cameraDAO = CameraDAO()
            zoneDAO = ZoneDAO()
            areaDAO = AreaDAO()

            cameraId = request.args.get('cameraId')

            cameraVO.cameraId = cameraId

            cameraVOList = cameraDAO.editCamera(cameraVO)

            zoneVOList = zoneDAO.viewZone()

            areaVOList = areaDAO.viewArea()

            print('cameraVOList:::', cameraVOList)

            return render_template('admin/editCamera.html', zoneVOList=zoneVOList, areaVOList=areaVOList,
                                   cameraVOList=cameraVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updateCamera', methods=['POST', 'GET'])
def adminUpdateCamera():
    try:
        if adminLoginSession() == "admin":

            cameraCode = request.form['cameraCode']
            camera_AreaId = request.form['camera_AreaId']
            camera_ZoneId = request.form['camera_ZoneId']
            cameraId = request.form['cameraId']

            cameraVO = CameraVO()
            cameraDAO = CameraDAO()

            cameraVO.cameraId = cameraId
            cameraVO.camera_AreaId = camera_AreaId
            cameraVO.camera_ZoneId = camera_ZoneId
            cameraVO.cameraCode = cameraCode
            cameraDAO.updateCamera(cameraVO)

            print('3333333333333333333333333333333333333333333')

            return redirect(url_for('adminViewCamera'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# ------------------------------------------------Ajax------------------------------------#

@app.route('/admin/ajaxAreaAdmin', methods=['GET'])
def adminAjaxAreaAdmin():
    try:
        if adminLoginSession() == 'admin':

            areaVO = AreaVO()

            areaDAO = AreaDAO()

            area_ZoneId = request.args.get('camera_ZoneId')

            areaVO.area_ZoneId = area_ZoneId

            ajaxAdminAreaList = areaDAO.ajaxAreaAdmin(areaVO)

            ajaxAdminAreaJson = [i.as_dict() for i in ajaxAdminAreaList]

            return jsonify(ajaxAdminAreaJson)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)



#------------------------------------------------------View Notification----------------------------#
@app.route('/admin/viewNotification', methods=["GET"])
def adminViewNotification():
    try:
        if adminLoginSession() == 'admin':
            imageVO = ImageVO()
            imageDAO = ImageDAO()
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

            imageWork_doneDate = datetime.now().date()
            imageVO.imageWork_doneDate = imageWork_doneDate


            imageWorkdoneStatus = "Pending"
            imageVO.imageWorkdoneStatus=imageWorkdoneStatus


            imageVOList=imageDAO.viewNotification(imageVO)


            return render_template ('admin/viewNotification.html',imageVOList=imageVOList)
        else:
            adminLogoutSession()

    except Exception as ex:
        print(ex)


