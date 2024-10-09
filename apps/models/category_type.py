from datetime import datetime
from apps import db

class CategoryType(db.Model):
    __tablename__ = 'category_type'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    category_type = db.Column(db.String(255), nullable=True, comment='international, domestic')
    category_description = db.Column(db.String(255), nullable=True)
    status = db.Column(db.SmallInteger, nullable=True)  # 1 for active, 0 for inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CategoryType {self.category_type} - Status: {self.status}>'
