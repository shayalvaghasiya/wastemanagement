from project import db


class ZoneVO(db.Model):
    print('zoneVO')
    __tablename__ = 'zonemaster'
    zoneId = db.Column('zoneId', db.Integer, primary_key=True, autoincrement=True)
    zoneName = db.Column('zoneName', db.String(100))

    def as_dict(self):
        return {
            'zoneId': self.zoneId,
            'zoneName': self.zoneName
        }


db.create_all()
