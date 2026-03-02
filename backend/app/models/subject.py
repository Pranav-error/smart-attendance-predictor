from datetime import datetime
from app import db

class Subject(db.Model):
    """Subject model"""
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    subject_name = db.Column(db.String(100), nullable=False)
    minimum_required_percentage = db.Column(db.Integer, default=75)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    attendance_records = db.relationship('Attendance', backref='subject', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert subject to dictionary"""
        return {
            'id': self.id,
            'subject_name': self.subject_name,
            'minimum_required_percentage': self.minimum_required_percentage,
            'created_at': self.created_at.isoformat()
        }
