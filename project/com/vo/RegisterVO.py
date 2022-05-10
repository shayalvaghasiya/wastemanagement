from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.ZoneVO import ZoneVO


class RegisterVO(db.Model):
    __tablename__ = 'registermaster'
    registerId = db.Column('registerId', db.Integer, primary_key=True, autoincrement=True)
    registerFirstname = db.Column('registerFirstname', db.String(100), nullable=False)
    registerLastname = db.Column('registerLastname', db.String(100), nullable=False)
    registerGender = db.Column('registerGender', db.String(100), nullable=False)
    registerAddress = db.Column('registerAddress', db.String(100), nullable=False)
    registerContact = db.Column('registerContact', db.String(100), nullable=False)
    register_AreaId = db.Column('register_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId))
    register_ZoneId = db.Column('register_ZoneId', db.Integer, db.ForeignKey(ZoneVO.zoneId))
    register_LoginId = db.Column('register_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'registerId': self.registerId,
            'registerFirstname': self.registerFirstname,
            'registerLastname': self.registerLastname,
            'registerGender': self.registerGender,
            'registerAddress': self.registerAddress,
            'registerContact': self.registerContact,
            'register_ZoneId': self.register_ZoneId,
            'register_AreaId': self.register_AreaId,
            'register_LoginId': self.register_LoginId
        }


db.create_all()
