import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request, url_for, session, redirect, json

from project import app
from project.com.dao.ImageDAO import ImageDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.vo.ImageVO import ImageVO
from project.com.vo.LoginVO import LoginVO


@app.route('/')
def adminLoadLogin():
    try:

        print("in login")
        return render_template('admin/login.html')

    except Exception as ex:
        print(ex)


@app.route("/admin/validateLogin", methods=['POST'])
def adminValidateLogin():
    try:
        print('adminValidateLogin')
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword

        loginVOList = loginDAO.validateLogin(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]

        print(loginDictList)

        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:

            msg = 'Username Or Password is Incorrect !'

            return render_template('admin/Login.html', error=msg)

        elif loginDictList[0]['loginStatus'] == 'inactive':

            blockMsg = "You are temporarily blocked by Admin !!!"

            return render_template('admin/login.html', error=blockMsg)

        else:

            for row1 in loginDictList:

                print('In forloop')

                loginId = row1['loginId']

                loginUsername = row1['loginUsername']

                loginRole = row1['loginRole']

                session['session_loginId'] = loginId

                session['session_loginUsername'] = loginUsername

                session['session_loginRole'] = loginRole

                session.permanent = True

                if loginRole == 'admin':
                    return redirect(url_for('adminLoadDashboard'))
                elif loginRole == 'user':
                    return redirect(url_for('userLoadDashboard'))

    except Exception as ex:
        print(ex)


@app.route('/admin/loadDashboard')
def adminLoadDashboard():
    try:
        if adminLoginSession() == "admin":
            imageVO = ImageVO()
            imageDAO = ImageDAO()
            imageVO.imageDetectionResult = "Garbage"
            garbageList = imageDAO.adminGetDataForGarbageGraph(imageVO)

            print("garbageList >>>>> ", garbageList)

            imageVO.imageDetectionResult = "Not Garbage"
            notGarbageList = imageDAO.adminGetDataForNotGarbageGraph(imageVO)
            print("notGarbageList >>>>>>>>>>>>>>>>>> ", notGarbageList)

            graphDict = {}
            for i in garbageList:
                for j in notGarbageList:
                    if i[1] == j[1]:
                        dict1 = {i[0]: {"Username": i[1],"Garbage": i[2],"NotGarbage": j[2]}}

                        graphDict.update(dict1)

            print("graphDict>>>>>>>>>", graphDict)

            json_object = json.dumps(graphDict)

            print("json_object>>>>>>>>", json_object)

            var = "var data='" + str(json_object) + "';"

            print("var>>>>>>", var)

            with open('project/static/adminResources/data.json', 'w') as f:
                f.write(var)
            return render_template('admin/index.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/loadDashboard')
def userLoadDashboard():
    try:
        if adminLoginSession() == "user":

            imageVO = ImageVO()
            imageDAO = ImageDAO()
            imageVO.imageFrom_LoginId = session['session_loginId']
            graphVOList = imageDAO.UserGetDataGraph(imageVO)
            print('graphList >>>>>>>>>>>> ', graphVOList)
            return render_template('user/index.html',  graphVOList=graphVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loginSession')
def adminLoginSession():
    try:

        if 'session_loginId' and 'session_loginRole' in session:

            if session['session_loginRole'] == 'admin':
                return 'admin'
            elif session['session_loginRole'] == 'user':
                return 'user'

            print("<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>")

        else:

            print("<<<<<<<<<<<<<<<<False>>>>>>>>>>>>>>>>>>>>")

            return False
    except Exception as ex:
        print(ex)


@app.route("/admin/logoutSession", methods=['GET'])
def adminLogoutSession():
    try:
        session.clear()
        return redirect('/')
    except Exception as ex:
        print(ex)


@app.route('/admin/viewUser', methods=['GET'])
def adminViewUser():
    try:
        if adminLoginSession() == 'admin':
            loginDAO = LoginDAO()
            registerVOList = loginDAO.viewUser()
            return render_template('admin/viewUser.html', registerVOList=registerVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/blockUser', methods=['GET'])
def adminBlockUser():
    try:
        if adminLoginSession() == 'admin':
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginId = request.args.get('loginId')

            loginStatus = "inactive"

            loginVO.loginId = loginId

            loginVO.loginStatus = loginStatus

            loginDAO.updateLogin(loginVO)

            return redirect(url_for('adminViewUser'))
        else:

            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/unblockUser', methods=['GET'])
def adminUnblockUser():
    try:
        if adminLoginSession() == 'admin':
            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginId = request.args.get('loginId')

            loginStatus = "active"

            loginVO.loginId = loginId

            loginVO.loginStatus = loginStatus

            loginDAO.updateLogin(loginVO)

            return redirect(url_for('adminViewUser'))
        else:

            return adminLogoutSession()
    except Exception as ex:
        print(ex)


# -------------------------------------FORGET PASSWORD--------------------------------------#
@app.route('/user/forgetPassword')
def userForgetPassword():
    try:
        print("forget Password")
        return render_template('user/forgetPassword.html')
    except Exception as ex:
         print(ex)



@app.route('/user/changePassword', methods=['POST', 'GET'])
def userChangePassword():
    try:
        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginUsername = request.form['loginUsername']
        loginVO.loginUsername = loginUsername
        loginVOList = loginDAO.viewLoginUsername(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]

        for row1 in loginDictList:
            print('In forloop')

            loginId = row1['loginId']

            loginUsername = row1['loginUsername']

            session['session_loginId'] = loginId

            session['session_loginUsername'] = loginUsername

            session.permanent = True

        print(loginDictList)

        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:

            msg = 'Username is Incorrect !'

            return render_template('user/forgetPassword.html', error=msg)

        else:
            otp = ''.join((random.choice(string.digits)) for x in range(4))

            session['otp'] = otp

            print("OTP=" + otp)

            sender = "wastemanagmentwithai@gmail.com"

            receiver = loginUsername

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['Subject'] = "WASTE MANAGMENT OTP"

            msg.attach(MIMEText(otp, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "wasteAI1998")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            server.quit()
            return render_template('user/user.OTP.html')
    except Exception as ex:
        print(ex)


@app.route('/user/updatePassword', methods=['POST', 'GET'])
def userNewPassword():
    try:

        loginVO = LoginVO()
        loginDAO = LoginDAO()
        loginOTP = request.form['loginotp']
        print(loginOTP)

        if loginOTP == session['otp']:

            loginVO.loginId = session['session_loginId']

            newloginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

            print("newloginPassword=" + newloginPassword)

            sender = "wastemanagmentwithai@gmail.com"

            receiver = session['session_loginUsername']

            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = "WASTE MANAGMENT PASSWORD"
            msg.attach(MIMEText(newloginPassword, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, "wasteAI1998")
            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            loginVO.loginPassword = newloginPassword
            loginVO.loginId = session['session_loginId']

            loginDAO.updateNewPassword(loginVO)

            server.quit()
            session.clear()
            return render_template('admin/Login.html')

        else:
            msg = 'OTP is Incorrect !'
            return render_template('user/user.OTP.html', error=msg)

    except Exception as ex:
        print(ex)


# ----------------------------ResetPassword---------------------------------#

@app.route('/user/resetPassword', methods=['GET'])
def userResetPassword():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/userResetPassword.html')
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/updateResetPassword', methods=['POST', 'GET'])
def userUpdateResetPassword():
    try:
        if adminLoginSession() == 'user':
            loginVO = LoginVO()
            loginDAO = LoginDAO()
            loginVO.loginId = session['session_loginId']
            print(loginVO)
            loginList = loginDAO.viewLoginPassWord(loginVO)
            print(loginList)
            loginPassword = loginList.loginPassword
            print(loginPassword)
            oldLoginPassword = request.form['oldLoginPassword']
            if loginPassword == oldLoginPassword:
                newLoginPassword = request.form['newLoginPassword']
                confrimLoginPassword = request.form['confrimLoginPassword']

                if newLoginPassword == confrimLoginPassword:
                    loginVO.loginPassword = confrimLoginPassword
                    loginVO.loginId = session['session_loginId']

                    loginDAO.updateNewPassword(loginVO)
                    return render_template('user/index.html')

                else:
                    message = 'Sorry,New Passwrd you entered did not match with Confrim Password.Please try Again'
                    return render_template('user/userResetPassword.html', error=message)
            else:
                mssg = 'Password is incorrect.Enter the correct password'
                return render_template('user/userResetPassword.html', error=mssg)

        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
