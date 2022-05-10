from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO
from project.com.vo.ZoneVO import ZoneVO
from project.com.vo.AreaVO import AreaVO

class LoginDAO:
    def validateLogin(self, loginVO):
        print('loginDAO')
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername, loginPassword=loginVO.loginPassword)
        return loginList

    def insertLogin(self, loginVO):
        print('insertdataset')
        db.session.add(loginVO)
        db.session.commit()

    def viewUser(self):
        registerList = db.session.query(RegisterVO, LoginVO, AreaVO, ZoneVO) \
            .join(LoginVO, RegisterVO.register_LoginId == LoginVO.loginId) \
            .join(AreaVO, RegisterVO.register_AreaId == AreaVO.areaId) \
            .join(ZoneVO, RegisterVO.register_ZoneId == ZoneVO.zoneId).all()
        return registerList

    def updateLogin(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def viewLoginUsername(self,loginVO):
        print('Check the username')
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername)
        return loginList

    def updateNewPassword(self,loginVO):
        print('New Password Update')
        db.session.merge(loginVO)
        db.session.commit()

    def viewLoginPassWord(self,loginVO):
        print('Check old password')
        loginList = LoginVO.query.get(loginVO.loginId)
        print('exit')
        return loginList

    def viewLoginHeaderUsername(self,loginVO):
        print('Check the username')
        loginVOList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername)
        return loginVOList
