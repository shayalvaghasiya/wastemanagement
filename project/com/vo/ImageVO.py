from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.ZoneVO import ZoneVO


class ImageVO(db.Model):
    __tablename__ = 'imagemaster'
    imageId = db.Column('imageId', db.Integer, primary_key=True, autoincrement=True)
    imageInputFileName = db.Column('imageInputFileName', db.String(100))
    imageInputFilePath = db.Column('imageInputFilePath', db.String(100))
    imageOutputFileName = db.Column('imageOutputFileName', db.String(100))
    imageOutputFilePath = db.Column('imageOutputFilePath', db.String(100))
    imageDetectionResult = db.Column('imageDetectionResult', db.String(100))
    imageUploadDate = db.Column('imageUploadDate', db.String(100))
    imageUploadTime = db.Column('imageUploadTime', db.String(100))
    imageWork_doneDate=db.Column('imageWork_doneDate',db.String(100))
    imageWorkdoneStatus = db.Column('imageWorkdoneStatus',  db.String(100))
    imageCleanInputFilePath = db.Column('imageCleanInputFilePath', db.String(100))
    imageCleanInputFileName = db.Column('imageCleanInputFileName', db.String(100))
    imageCleanOutputFilePath = db.Column('imageCleanOutputFilePath', db.String(100))
    imageCleanOutputFileName = db.Column('imageCleanOutputFileName', db.String(100))
    imageCleanUploadDate =db.Column('imageCleanUploadDate', db.String(100))
    imageCleanUploadTime = db.Column('imageCleanUploadTime',db.String(100))
    imageTo_LoginId = db.Column('imageTo_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))
    imageFrom_LoginId = db.Column('imageFrom_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))
    image_AreaId = db.Column('image_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId))
    image_ZoneId = db.Column('image_ZoneId', db.Integer, db.ForeignKey(ZoneVO.zoneId))

    def as_dict(self):
        return {
            'imageId': self.imageId,
            'imageInputFileName': self.imageInputFileName,
            'imageInputFilePath': self.imageInputFilePath,
            'imageOutputFileName': self.imageOutputFileName,
            'imageOutputFilePath': self.imageOutputFilePath,
            'imageDetectionResult': self.imageDetectionResult,
            'imageWorkdoneStatus':self.imageWorkdoneStatus,
            'imageCleanInputFilePath':self.imageCleanInputFilePath,
            'imageCleanInputFileName':self.imageCleanInputFileName,
            'imageCleanOutputFileName':self.imageCleanOutputFileName,
            'imageCleanOutputFilePath':self.imageCleanOutputFilePath,
            'imageCleanUploadDate':self.imageCleanUploadDate,
            'imageCleanUploadTime':self.imageCleanUploadTime,
            'imageUploadDate': self.imageUploadDate,
            'imageUploadTime': self.imageUploadTime,
            'imageWork_doneDate':self.imageWork_doneDate,
            'imageTo_LoginId':self. imageTo_LoginId,
            'imageFrom_LoginId':self.imageFrom_LoginId,
            'image_AreaId': self.image_AreaId,
            'image_ZoneId': self.image_ZoneId,


        }


db.create_all()
