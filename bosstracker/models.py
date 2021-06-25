from bosstracker import app, db


class Boss(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bossname = db.Column(db.String(80), unique=True, nullable=False)
    deathcount = db.Column(db.Integer, nullable=False, default=0)
    iscompleted = db.Column(db.Boolean, nullable=False, default=False)
    image_file = db.Column(db.String(50), nullable=False, default='default.png')

    def __repr__(self):
        return f"Boss('{self.bossname}', '{self.deathcount}')"

