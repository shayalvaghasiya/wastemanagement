import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request ,jsonify,session
from project.com.controller.LoginController import adminLogoutSession,adminLoginSession

from project.com.vo.AreaVO import AreaVO
from project import app
from project.com.dao.AreaDAO import AreaDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.dao.ZoneDAO import ZoneDAO

from project.com.vo.RegisterVO import RegisterVO
from project.com.vo.LoginVO import LoginVO



@app.route('/user/loadRegister')
def userLoadRegister():
    try:
        zoneDAO = ZoneDAO()
        zoneVOList = zoneDAO.viewZone()

        areaDAO = AreaDAO()
        areaVOList = areaDAO.viewArea()

        return render_template('user/register.html', zoneVOList=zoneVOList, areaVOList=areaVOList)
    except Exception as ex:
        print(ex)

@app.route('/user/insertRegister', methods=['POST'])
def userInsertRegister():
    try:

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        registerVO = RegisterVO()
        registerDAO = RegisterDAO()

        loginUsername = request.form['loginUsername']

        registerFirstname = request.form['registerFirstname']
        registerLastname = request.form['registerLastname']
        registerGender = request.form['registerGender']
        register_ZoneId = request.form['register_ZoneId']
        register_AreaId = request.form['register_AreaId']
        registerAddress = request.form['registerAddress']
        registerContact = request.form['registerContact']

        loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

        print("loginPassword=" + loginPassword)

        sender = "wastemanagmentwithai@gmail.com"

        receiver = loginUsername

        msg = MIMEMultipart()

        msg['From'] = sender

        msg['To'] = receiver

        msg['Subject'] = "WASTE MANAGMENT PASSWORD"

        msg.attach(MIMEText(loginPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(sender, "wasteAI1998")

        text = msg.as_string()

        server.sendmail(sender, receiver, text)

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginRole = "user"
        loginVO.loginStatus = "active"

        loginDAO.insertLogin(loginVO)

        registerVO.registerFirstname = registerFirstname
        registerVO.registerLastname = registerLastname
        registerVO.registerGender = registerGender
        registerVO.register_ZoneId = register_ZoneId
        registerVO.register_AreaId = register_AreaId
        registerVO.registerAddress = registerAddress
        registerVO.registerContact = registerContact
        registerVO.register_LoginId = loginVO.loginId

        registerDAO.insertRegister(registerVO)

        server.quit()

        return render_template("admin/Login.html")

        print('register con')

    except Exception as ex:
        print(ex)




#--------------------------------------------AJAX------------------------------------#

@app.route('/user/ajaxAreaUser',methods=['GET'])
def userAjaxArea():
    try:

        print("oooooooo")
        areaVO = AreaVO()

        areaDAO = AreaDAO()

        area_ZoneId = request.args.get('register_ZoneId')

        areaVO.area_ZoneId = area_ZoneId

        ajaxUserAreaList = areaDAO.ajaxAreaUser(areaVO)

        ajaxUserAreaJson = [i.as_dict() for i in ajaxUserAreaList]

        return jsonify(ajaxUserAreaJson)

    except Exception as ex:
        print(ex)
#------------------------------------------AJAX----------------------------------------------------#
@app.route('/user/editProfile',methods=['GET'])
def editUserProfile():
    try:
        if adminLoginSession()=='user':
            registerVO = RegisterVO()
            registerDAO = RegisterDAO()

            registerVO.register_LoginId = session['session_loginId']
            registerVOList=registerDAO.viewEditProfile(registerVO)

            zoneDAO = ZoneDAO()
            zoneVOList = zoneDAO.viewZone()

            areaDAO = AreaDAO()
            areaVOList = areaDAO.viewArea()



            return render_template('user/editUserProfile.html',registerVOList=registerVOList,zoneVOList=zoneVOList,areaVOList=areaVOList)
        else:
            adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/updateEditProfile',methods=['POST','GET'])
def UserUpdateEditProfile():
    try:
        if adminLoginSession()=='user':
            registerVO = RegisterVO()
            registerDAO = RegisterDAO()

            registerFirstname = request.form['registerFirstname']
            registerLastname = request.form['registerLastname']
            registerGender  = request.form['registerGender']
            registerAddress = request.form['registerAddress']
            registerContact = request.form['registerContact']
            registerId = request.form['registerId']
            register_ZoneId = request.form['register_ZoneId']
            register_AreaId = request.form['register_AreaId']

            registerVO.registerFirstname = registerFirstname
            registerVO.registerId = registerId
            registerVO.registerLastname = registerLastname
            registerVO.registerGender = registerGender
            registerVO.register_ZoneId = register_ZoneId
            registerVO.register_AreaId = register_AreaId

            registerVO.registerAddress = registerAddress
            registerVO.registerContact = registerContact

            registerDAO.updateEditProfile(registerVO)

            return render_template('user/index.html')
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)







