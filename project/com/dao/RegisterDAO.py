from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.AreaVO import AreaVO
from project.com.vo.RegisterVO import RegisterVO
from project.com.vo.ZoneVO import ZoneVO


class RegisterDAO:
    def insertRegister(self, registerVO):
        print('insert Register')
        db.session.add(registerVO)
        db.session.query(RegisterVO, AreaVO, ZoneVO).join(AreaVO, RegisterVO.register_AreaId == AreaVO.areaId).join(
            ZoneVO, RegisterVO.register_ZoneId == ZoneVO.zoneId).all()
        db.session.commit()

    def viewEditProfile(self,registerVO):
        print('View Edit Profile')
        registerList=db.session.query(RegisterVO,LoginVO).join(LoginVO,RegisterVO.register_LoginId==LoginVO.loginId)\
            .filter(registerVO.register_LoginId==RegisterVO.register_LoginId).all()
        return registerList

    def updateEditProfile(self,registerVO):
        print('Update Edit Profile')
        db.session.merge(registerVO)
        db.session.commit()







print('dao Register run')
