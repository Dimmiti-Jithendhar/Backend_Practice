from app.main_app import db

# Define Operator model
class Operator(db.Model):
    __tablename__ = 'operators'
    operator_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    operator_name = db.Column(db.String(100), nullable=False)
    operator_phn_no = db.Column(db.String(15), unique=True)
    operator_email = db.Column(db.String(100), unique=True)
    operator_rating = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Operator {self.operator_name}>'
