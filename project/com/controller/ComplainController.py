import os
from datetime import datetime

from flask import render_template, url_for, redirect, request, session
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLogoutSession, adminLoginSession
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO


@app.route('/user/loadComplain', methods=['GET'])
def userLoadComplain():
    try:
        if adminLoginSession() == "user":
            return render_template('user/addComplain.html')
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertComplain', methods=['POST', 'GET'])
def userInsertComplain():
    try:
        if adminLoginSession() == "user":

            UPLOAD_FOLDER = 'project/static/adminResources/complainAttachment/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()
            complainDate = str(datetime.now().date())
            complainTime = datetime.now().strftime('%H:%M:%S')

            file = request.files['file']
            print(file)
            complainFileName = secure_filename(file.filename)
            complainFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(complainFilePath, complainFileName))

            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription
            complainVO.complainStatus = 'Pending'
            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime
            complainVO.complainFileName = complainFileName
            complainVO.complainFilePath = complainFilePath.replace("project", "..")
            complainVO.complainFrom_LoginId = session['session_loginId']

            complainDAO.insertComplain(complainVO)

            return redirect(url_for('userViewComplain'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewComplain')
def userViewComplain():
    try:
        if adminLoginSession() == "user":
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainFrom_LoginId = session['session_loginId']
            complainVO.complainFrom_LoginId = complainFrom_LoginId

            complainVOList = complainDAO.viewUserComplain(complainVO)

            print("__________________", complainVOList)
            return render_template('user/viewComplain.html', complainVOList=complainVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewComplainReply', methods=['GET'])
def userViewComplainReply():
    try:
        if adminLoginSession() == "user":
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainId = request.args.get('complainId')
            complainVO.complainId = complainId

            complainVOList = complainDAO.viewUserComplainReply(complainVO)
            print('view Complain Reply')
            print("__________________", complainVOList)
            return render_template('user/viewComplainReply.html', complainVOList=complainVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deleteComplain', methods=['GET'])
def userDeleteComplain():
    try:
        if adminLoginSession() == "user":
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.args.get('complainId')
            complainVO.complainId = complainId

            complainList = complainDAO.deleteComplain(complainVO)
            complainStatus = complainList.complainStatus

            print(complainStatus)

            complainFileName = complainList.complainFileName
            complainFilePath = complainList.complainFilePath

            fullPath = complainFilePath.replace('..', 'project') + complainFileName
            os.remove(fullPath)

            if complainStatus == 'Replied':
                replyFileName = complainList.replyFileName
                replyFilePath = complainList.replyFilePath

                replyfullPath = replyFilePath.replace('..', 'project') + replyFileName
                os.remove(replyfullPath)

            return redirect(url_for('userViewComplain'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# ---------------------ADMIN----------------------------------------------

@app.route('/admin/viewComplain')
def adminViewComplain():
    try:
        if adminLoginSession() == "admin":

            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainStatus = "Pending"
            complainVO.complainStatus = complainStatus

            complainVOList = complainDAO.viewAdminComplain(complainVO)

            print('view Admin Complain')
            print("__________________", complainVOList)

            return render_template('admin/viewComplain.html', complainVOList=complainVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loadComplainReply', methods=['GET'])
def adminLoadComplainReply():
    try:
        if adminLoginSession() == "admin":
            complainId = request.args.get('complainId')
            return render_template('admin/addComplainReply.html', complainId=complainId)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertComplainReply', methods=['POST', 'GET'])
def adminInsertComplainReply():
    try:
        if adminLoginSession() == "admin":

            UPLOAD_FOLDER = 'project/static/adminResources/replyAttachment/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            complainId = request.form['complainId']
            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()
            replyDate = str(datetime.now().date())
            replyTime = datetime.now().strftime('%H:%M:%S')

            file = request.files['file']
            replyFileName = secure_filename(file.filename)
            replyFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(replyFilePath, replyFileName))

            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.complainId = complainId
            complainVO.complainStatus = 'Replied'
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath.replace("project", "..")
            complainVO.complainTo_LoginId = session['session_loginId']

            complainDAO.insertComplainReply(complainVO)

            return redirect(url_for('adminViewComplain'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)
