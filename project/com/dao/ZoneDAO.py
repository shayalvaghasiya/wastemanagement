from project import db
from project.com.vo.ZoneVO import ZoneVO


class ZoneDAO:
    def insertZone(self, zoneVO):
        print('insertzone')
        db.session.add(zoneVO)
        db.session.commit()

    def viewZone(self):
        print('view Zone')

        zoneList = ZoneVO.query.all()

        return zoneList

    def deleteZone(self, zoneVO):
        print('delete')

        zoneList = ZoneVO.query.get(zoneVO.zoneId)

        db.session.delete(zoneList)

        db.session.commit()

    def editZone(self, zoneVO):
        print('editzone')
        zoneList = ZoneVO.query.filter_by(zoneId=zoneVO.zoneId).all()
        return zoneList

    def updateZone(self, zoneVO):
        db.session.merge(zoneVO)
        db.session.commit()
        print('updatezone')


print('zoneDao')
