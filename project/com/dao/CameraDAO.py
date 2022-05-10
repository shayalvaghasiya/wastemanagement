from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.CameraVO import CameraVO
from project.com.vo.ZoneVO import ZoneVO


class CameraDAO:
    def insertCamera(self, cameraVO):
        print('insertCamera')
        db.session.add(cameraVO)
        db.session.commit()

    def viewCamera(self):

        cameraList = db.session.query(CameraVO,AreaVO,ZoneVO).join(AreaVO,
                                                                     CameraVO.camera_AreaId == AreaVO.areaId).join(
            ZoneVO, CameraVO.camera_ZoneId == ZoneVO.zoneId).all()
        return cameraList

    def deleteCamera(self, cameraVO):
        print('deleteCamera')
        cameraList = CameraVO.query.get(cameraVO.cameraId)
        db.session.delete(cameraList)
        db.session.commit()
        return cameraList

    def editCamera(self, cameraVO):
        print('editCamera')
        cameraList = CameraVO.query.filter_by(cameraId=cameraVO.cameraId)
        return cameraList

    def updateCamera(self, cameraVO):
        print('updatecamera')
        db.session.merge(cameraVO)
        db.session.commit()


