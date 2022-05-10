from datetime import datetime

from flask import render_template, url_for, redirect, request, session

from project import app
from project.com.controller.LoginController import adminLogoutSession, adminLoginSession
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.vo.FeedbackVO import FeedbackVO


@app.route('/user/loadFeedback', methods=['GET'])
def userLoadFeedback():
    try:
        if adminLoginSession() == "user":
            return render_template('user/addFeedback.html')
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/insertFeedback', methods=['POST', 'GET'])
def userInsertFeedback():
    try:
        if adminLoginSession() == "user":
            feedbackSubject = request.form['feedbackSubject']
            feedbackDescription = request.form['feedbackDescription']
            feedbackRating = request.form['feedbackRating']

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()
            feedbackDate = str(datetime.now().date())
            feedbackTime = datetime.now().strftime('%H:%M:%S')

            feedbackVO.feedbackSubject = feedbackSubject
            feedbackVO.feedbackDescription = feedbackDescription
            feedbackVO.feedbackRating = feedbackRating
            feedbackVO.feedbackDate = feedbackDate
            feedbackVO.feedbackTime = feedbackTime
            feedbackVO.feedbackFrom_LoginId = session['session_loginId']

            feedbackDAO.userInsertFeedback(feedbackVO)

            return redirect(url_for('userViewFeedback'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/viewFeedback', methods=['GET'])
def userViewFeedback():
    try:
        if adminLoginSession() == "user":
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackFrom_LoginId = session['session_loginId']
            feedbackVO.feedbackFrom_LoginId = feedbackFrom_LoginId

            feedbackVOList = feedbackDAO.userViewFeedback(feedbackVO)

            print("__________________", feedbackVOList)

            return render_template('user/viewFeedback.html', feedbackVOList=feedbackVOList)
    except Exception as ex:
        print(ex)


@app.route('/user/deleteFeedback', methods=['GET'])
def userDeleteFeedback():
    try:
        if adminLoginSession() == "user":
            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackId = request.args.get('feedbackId')

            feedbackVO.feedbackId = feedbackId
            print(feedbackVO)

            feedbackDAO.adminDeleteFeedback(feedbackVO)

            return redirect(url_for('userViewFeedback'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewFeedback', methods=['GET'])
def adminViewFeedback():
    try:
        print('admin Feedback')
        if adminLoginSession() == "admin":
            feedbackDAO = FeedbackDAO()
            feedbackVOList = feedbackDAO.adminViewFeedback()
            print(feedbackVOList)
            print("__________________", feedbackVOList)

            return render_template('admin/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertReviewFeedback', methods=['GET'])
def adminInsertReviewFeedback():
    try:
        if adminLoginSession() == 'admin':
            print('admin Review Feedback')
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackId = request.args.get('feedbackId')

            feedbackTo_LoginId = session['session_loginId']

            feedbackVO.feedbackId = feedbackId
            feedbackVO.feedbackTo_LoginId = feedbackTo_LoginId
            print(feedbackTo_LoginId)
            feedbackDAO.adminAddFeedbackReview(feedbackVO)

            return redirect(url_for('adminViewFeedback'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)
