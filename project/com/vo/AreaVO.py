from project import db
from project.com.vo.ZoneVO import ZoneVO


class AreaVO(db.Model):
    __tablename__ = 'areamaster'
    areaId = db.Column('areaId', db.Integer, primary_key=True, autoincrement=True)
    areaName = db.Column('areaName', db.String(100), nullable=False)
    areaPincode = db.Column('areaPincode', db.String(100), nullable=False)
    areaDescription = db.Column('areaDescription', db.String(1000), nullable=False)
    area_ZoneId = db.Column('area_ZoneId', db.Integer, db.ForeignKey(ZoneVO.zoneId))

    def as_dict(self):
        return {
            'areaId': self.areaId,
            'areaName': self.areaName,
            'areaPincode': self.areaPincode,
            'areaDescription': self.areaDescription,
            'area_ZoneId': self.area_ZoneId
        }


db.create_all()
