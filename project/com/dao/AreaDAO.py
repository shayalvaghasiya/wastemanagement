from project import db
from project.com.vo.AreaVO import AreaVO
from project.com.vo.ZoneVO import ZoneVO


class AreaDAO:
    def insertArea(self, areaVO):
        print('insertArea')
        db.session.add(areaVO)
        db.session.commit()

    def viewArea(self):
        print('viewArea')
        areaList = db.session.query(AreaVO, ZoneVO).join(ZoneVO, AreaVO.area_ZoneId == ZoneVO.zoneId).all()
        return areaList

    def deleteArea(self, areaId):
        print('deleteArea')

        areaList = AreaVO.query.get(areaId)
        print('areaList')

        db.session.delete(areaList)
        print('session delete')

        db.session.commit()
        print('commit')

    def editArea(self, areaVO):
        areaList = AreaVO.query.filter_by(areaId=areaVO.areaId)

        return areaList

    def updateArea(self, areaVO):
        print('updateArea')
        db.session.merge(areaVO)
        db.session.commit()

    def ajaxAreaAdmin(self, areaVO):
        print("areaDAO")
        areaList = AreaVO.query.filter_by(area_ZoneId=areaVO.area_ZoneId).all()
        return areaList

    def ajaxAreaUser(self, areaVO):
        print("areaDAO")
        areaList = AreaVO.query.filter_by(area_ZoneId=areaVO.area_ZoneId).all()
        return areaList

print('areaDAO')
