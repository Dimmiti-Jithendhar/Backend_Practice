from app.main_app import db
from app.main_app import models


# Define Features model
class Feature(db.Model):
    __tablename__ = 'features'
    feature_id = db.Column(db.Integer, primary_key=True)
    feature_name = db.Column(db.String(50), unique=True, nullable=False)  # e.g., AC, WiFi, Charging

    def __repr__(self):
        return f'<Feature {self.feature_name}>'



# inserting features
def insert_features():
    features_to_add = ['AC', 'WiFi', 'Charging', 'Snack Service']
    
    for feature_name in features_to_add:
        existing_feature = Feature.query.filter_by(feature_name=feature_name).first()
        if not existing_feature:
            new_feature = Feature(feature_name=feature_name)
            db.session.add(new_feature)

    db.session.commit()















