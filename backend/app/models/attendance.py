from datetime import datetime
from app import db

class Attendance(db.Model):
    """Attendance model"""
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    status = db.Column(db.String(10), nullable=False)  # 'Present' or 'Absent'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint: one attendance record per subject per day
    __table_args__ = (db.UniqueConstraint('subject_id', 'date', name='unique_subject_date'),)
    
    def to_dict(self):
        """Convert attendance to dictionary"""
        return {
            'id': self.id,
            'subject_id': self.subject_id,
            'date': self.date.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
