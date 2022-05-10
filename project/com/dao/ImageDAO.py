from sqlalchemy import func , or_,and_

from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.ImageVO import ImageVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.ZoneVO import ZoneVO


class ImageDAO:
    def insertImage(self, imageVO):
        print('imageInsert')
        db.session.add(imageVO)
        db.session.commit()

    def viewUserImage(self, imageVO):
        print('imageView')
        imageVOList = db.session.query(ImageVO,ZoneVO,AreaVO).join(ZoneVO,ImageVO.image_ZoneId ==ZoneVO.zoneId).join(AreaVO,ImageVO.image_AreaId==AreaVO.areaId).filter(imageVO.imageFrom_LoginId==ImageVO.imageFrom_LoginId).all()

        print('Return')
        return imageVOList

    def viewAdminUserImage(self,imageVO):
        imageVOList = db.session.query(ImageVO, LoginVO, ZoneVO, AreaVO) \
            .join(LoginVO, ImageVO.imageFrom_LoginId == LoginVO.loginId) \
            .join(ZoneVO, ImageVO.image_ZoneId == ZoneVO.zoneId) \
            .join(AreaVO, ImageVO.image_AreaId == AreaVO.areaId).filter(or_((imageVO.imageDetectionResult==ImageVO.imageDetectionResult),(imageVO.imageWorkdoneStatus==ImageVO.imageWorkdoneStatus))).all()
        return imageVOList

    def deleteImage(self, imageVO):
        print('imageDelete')
        imageList = ImageVO.query.get(imageVO.imageId)
        db.session.delete(imageList)
        db.session.commit()
        print('@')
        return imageList

    def ajaxAreaUser(self, areaVO):
        areaList = AreaVO.query.filter_by(zone_AreaId=areaVO.area_ZoneId).all()
        return areaList

    def inserCleantImage(self,imageVO):
        print('clean')
        db.session.merge(imageVO)
        db.session.commit()

    def viewUserWorkdoneRely(self, imageVO):
        imageVOList = db.session.query(ImageVO,ZoneVO,AreaVO).join(ZoneVO,ImageVO.image_ZoneId==ZoneVO.zoneId).join(AreaVO,ImageVO.image_AreaId==AreaVO.areaId).filter(imageVO.imageId==ImageVO.imageId).all()
        return imageVOList

    def viewNotification(self,imageVO):
        imageVOList = db.session.query(ImageVO, LoginVO, ZoneVO, AreaVO) \
            .join(LoginVO, ImageVO.imageFrom_LoginId == LoginVO.loginId) \
            .join(ZoneVO, ImageVO.image_ZoneId == ZoneVO.zoneId) \
            .join(AreaVO, ImageVO.image_AreaId == AreaVO.areaId).filter(and_((imageVO.imageWork_doneDate==ImageVO.imageWork_doneDate),(imageVO.imageWorkdoneStatus==ImageVO.imageWorkdoneStatus))).all()
        return imageVOList

    def adminGetDataForGarbageGraph(self, imageVO):
        graphList = db.session.query(LoginVO.loginId, LoginVO.loginUsername, func.count(ImageVO.imageDetectionResult)) \
            .join(ImageVO, LoginVO.loginId == ImageVO.imageFrom_LoginId) \
            .filter(ImageVO.imageDetectionResult == imageVO.imageDetectionResult) \
            .group_by(ImageVO.imageFrom_LoginId).all()
        return graphList

    def UserGetDataGraph(self, imageVO):
        graphList = db.session.query(ImageVO.imageDetectionResult, func.count(ImageVO.imageFrom_LoginId)) \
            .filter(ImageVO.imageFrom_LoginId == imageVO.imageFrom_LoginId) \
            .group_by(ImageVO.imageDetectionResult).all()
        return graphList

    def adminGetDataForNotGarbageGraph(self, imageVO):
        graphList = db.session.query(LoginVO.loginId, LoginVO.loginUsername, func.count(ImageVO.imageDetectionResult)) \
            .join(ImageVO, LoginVO.loginId == ImageVO.imageFrom_LoginId) \
            .filter(ImageVO.imageDetectionResult == imageVO.imageDetectionResult) \
            .group_by(ImageVO.imageFrom_LoginId).all()
        return graphList
