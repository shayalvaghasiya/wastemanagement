from project import db
from project.com.vo.FeedbackVO import FeedbackVO
from project.com.vo.LoginVO import LoginVO


class FeedbackDAO:
    def userInsertFeedback(self, feedbackVO):
        print('insertfeedback')
        db.session.add(feedbackVO)
        db.session.commit()

    def userViewFeedback(self, feedbackVO):
        print('viewFeedback')
        feedbackList = FeedbackVO.query.filter_by(feedbackFrom_LoginId=feedbackVO.feedbackFrom_LoginId).all()
        return feedbackList

    def adminViewFeedback(self):
        print('admin View Feedback')
        feedbackList = db.session.query(FeedbackVO, LoginVO).join(LoginVO,
                                                                  FeedbackVO.feedbackFrom_LoginId == LoginVO.loginId).all()
        return feedbackList

    def adminAddFeedbackReview(self, feedbackVO):
        print('addAdminFeedbackReview')
        db.session.merge(feedbackVO)
        db.session.commit()

    def adminDeleteFeedback(self, feedbackVO):
        feedbackList = FeedbackVO.query.get(feedbackVO.feedbackId)
        db.session.delete(feedbackList)
        db.session.commit()
