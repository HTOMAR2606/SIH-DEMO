from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Intern(db.Model):
    __tablename__ = 'interns'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    college = db.Column(db.String(200))
    branch = db.Column(db.String(100))
    year = db.Column(db.Integer)
    cgpa = db.Column(db.Float)
    
    # JSON fields for complex data
    skills = db.Column(db.Text)  # JSON string of skills with proficiency levels
    interests = db.Column(db.Text)  # JSON string of interest areas
    preferences = db.Column(db.Text)  # JSON string of project/mentor preferences
    availability = db.Column(db.Text)  # JSON string of time availability
    
    # PM Internship Yojana specific fields
    aadhar_number = db.Column(db.String(12))
    application_id = db.Column(db.String(50))
    category = db.Column(db.String(20))  # General, OBC, SC, ST
    state = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    allocations = db.relationship('Allocation', backref='intern', lazy=True)
    
    def get_skills(self):
        return json.loads(self.skills) if self.skills else {}
    
    def set_skills(self, skills_dict):
        self.skills = json.dumps(skills_dict)
    
    def get_preferences(self):
        return json.loads(self.preferences) if self.preferences else {}

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    department = db.Column(db.String(100))
    organization = db.Column(db.String(200))
    
    # Project requirements
    required_skills = db.Column(db.Text)  # JSON string
    preferred_skills = db.Column(db.Text)  # JSON string
    difficulty_level = db.Column(db.Integer)  # 1-5 scale
    estimated_hours = db.Column(db.Integer)
    duration_weeks = db.Column(db.Integer)
    
    # Project details
    tech_stack = db.Column(db.Text)  # JSON string
    project_type = db.Column(db.String(100))  # Research, Development, Analysis, etc.
    remote_allowed = db.Column(db.Boolean, default=True)
    max_interns = db.Column(db.Integer, default=1)
    
    # PM Yojana compliance
    yojana_approved = db.Column(db.Boolean, default=False)
    stipend_amount = db.Column(db.Float)
    certificate_provided = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    allocations = db.relationship('Allocation', backref='project', lazy=True)
    
    def get_required_skills(self):
        return json.loads(self.required_skills) if self.required_skills else {}

class Mentor(db.Model):
    __tablename__ = 'mentors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    designation = db.Column(db.String(100))
    organization = db.Column(db.String(200))
    experience_years = db.Column(db.Integer)
    
    # Mentor capabilities
    expertise_areas = db.Column(db.Text)  # JSON string
    mentoring_style = db.Column(db.String(50))  # Hands-on, Guidance, Collaborative
    max_interns = db.Column(db.Integer, default=3)
    availability = db.Column(db.Text)  # JSON string
    
    # Performance metrics
    rating = db.Column(db.Float, default=5.0)
    total_mentored = db.Column(db.Integer, default=0)
    success_rate = db.Column(db.Float, default=100.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    allocations = db.relationship('Allocation', backref='mentor', lazy=True)

class Allocation(db.Model):
    __tablename__ = 'allocations'
    
    id = db.Column(db.Integer, primary_key=True)
    intern_id = db.Column(db.Integer, db.ForeignKey('interns.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentors.id'), nullable=False)
    
    # Allocation metrics
    match_score = db.Column(db.Float)  # Overall match confidence (0-100)
    skill_match_score = db.Column(db.Float)
    preference_match_score = db.Column(db.Float)
    availability_match_score = db.Column(db.Float)
    
    # Status tracking
    status = db.Column(db.String(20), default='pending')  # pending, active, completed, cancelled
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    
    # Feedback and performance
    intern_feedback = db.Column(db.Text)
    mentor_feedback = db.Column(db.Text)
    project_rating = db.Column(db.Float)
    learning_outcomes = db.Column(db.Text)  # JSON string
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AllocationHistory(db.Model):
    __tablename__ = 'allocation_history'
    
    id = db.Column(db.Integer, primary_key=True)
    allocation_batch_id = db.Column(db.String(50))
    total_interns = db.Column(db.Integer)
    total_projects = db.Column(db.Integer)
    total_mentors = db.Column(db.Integer)
    average_match_score = db.Column(db.Float)
    allocation_time_seconds = db.Column(db.Float)
    algorithm_version = db.Column(db.String(20))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Government Compliance Model for PM Internship Yojana
class YojanaCompliance(db.Model):
    __tablename__ = 'yojana_compliance'
    
    id = db.Column(db.Integer, primary_key=True)
    intern_id = db.Column(db.Integer, db.ForeignKey('interns.id'), nullable=False)
    
    # Documentation requirements
    documents_verified = db.Column(db.Boolean, default=False)
    eligibility_confirmed = db.Column(db.Boolean, default=False)
    background_check = db.Column(db.Boolean, default=False)
    
    # Tracking requirements
    attendance_percentage = db.Column(db.Float, default=0.0)
    weekly_reports_submitted = db.Column(db.Integer, default=0)
    mentor_evaluations = db.Column(db.Text)  # JSON string
    
    # Completion requirements
    final_presentation = db.Column(db.Boolean, default=False)
    project_deliverables = db.Column(db.Boolean, default=False)
    certificate_issued = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
