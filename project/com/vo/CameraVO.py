from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.ZoneVO import ZoneVO


class CameraVO(db.Model):
    __tablename__ = 'cameramaster'
    cameraId = db.Column('cameraId', db.Integer, primary_key=True, autoincrement=True)
    cameraCode = db.Column('cameraCode', db.String(100), nullable=False)
    cameraInputFileName = db.Column('cameraInputFileName', db.String(100))
    cameraInputFilePath = db.Column('cameraInputFilePath', db.String(100))
    cameraDetectionResult = db.Column('cameraDetectionResult', db.String(100))
    cameraOutputFileName = db.Column('cameraOutputFileName', db.String(100))
    cameraOutputFilePath = db.Column('cameraOutputFilePath', db.String(100))
    camera_AreaId = db.Column('camera_AreaId', db.Integer, db.ForeignKey(AreaVO.areaId))
    camera_ZoneId = db.Column('camera_ZoneId', db.Integer, db.ForeignKey(ZoneVO.zoneId))

    def as_dict(self):
        return {
            'cameraId': self.cameraId,
            'cameraCode': self.cameraCode,
            'cameraInputFileName': self.cameraInputFileName,
            'cameraInputFilePath': self.cameraInputFilePath,
            'cameraOutputFileName':self.cameraOutputFileName,
            'cameraOutputFilePath': self.cameraOutputFilePath,
            'cameraDetectionResult':self.cameraDetectionResult,
            'cameraUploadDate': self.cameraUploadDate,
            'cameraUploadTime': self.cameraUploadTime,
            'camera_AreaId': self.camera_AreaId,
            'camera_ZoneId': self.camera_ZoneId
        }


db.create_all()
