from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import json
import uuid
from datetime import datetime, timedelta

# Import our custom modules
from src.models import db, Intern, Project, Mentor, Allocation, AllocationHistory, YojanaCompliance
from src.allocation_engine import SmartAllocationEngine, RealTimeAllocationMonitor, AIInsightsGenerator, AllocationChatBot

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'smart-allocation-engine-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pm_allocation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
CORS(app)

# Initialize AI components
allocation_engine = SmartAllocationEngine()
realtime_monitor = RealTimeAllocationMonitor()
insights_generator = AIInsightsGenerator()
ai_chatbot = AllocationChatBot(allocation_engine)

# API Routes

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'components': {
            'database': 'connected',
            'ai_engine': 'ready',
            'realtime_monitor': 'active'
        }
    })

# Intern Management APIs
@app.route('/api/interns', methods=['GET', 'POST'])
def manage_interns():
    if request.method == 'POST':
        data = request.json
        
        # Create new intern
        intern = Intern(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            college=data.get('college'),
            branch=data.get('branch'),
            year=data.get('year'),
            cgpa=data.get('cgpa'),
            skills=json.dumps(data.get('skills', {})),
            interests=json.dumps(data.get('interests', [])),
            preferences=json.dumps(data.get('preferences', {})),
            availability=json.dumps(data.get('availability', {})),
            aadhar_number=data.get('aadhar_number'),
            application_id=data.get('application_id'),
            category=data.get('category', 'General'),
            state=data.get('state')
        )
        
        db.session.add(intern)
        db.session.commit()
        
        return jsonify({'message': 'Intern created successfully', 'id': intern.id}), 201
    
    else:
        # Get all interns
        interns = Intern.query.all()
        return jsonify([{
            'id': intern.id,
            'name': intern.name,
            'email': intern.email,
            'college': intern.college,
            'branch': intern.branch,
            'year': intern.year,
            'cgpa': intern.cgpa,
            'skills': intern.get_skills(),
            'category': intern.category,
            'state': intern.state,
            'created_at': intern.created_at.isoformat()
        } for intern in interns])

@app.route('/api/interns/<int:intern_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_single_intern(intern_id):
    intern = Intern.query.get_or_404(intern_id)
    
    if request.method == 'GET':
        return jsonify({
            'id': intern.id,
            'name': intern.name,
            'email': intern.email,
            'phone': intern.phone,
            'college': intern.college,
            'branch': intern.branch,
            'year': intern.year,
            'cgpa': intern.cgpa,
            'skills': intern.get_skills(),
            'interests': json.loads(intern.interests) if intern.interests else [],
            'preferences': intern.get_preferences(),
            'availability': json.loads(intern.availability) if intern.availability else {},
            'aadhar_number': intern.aadhar_number,
            'application_id': intern.application_id,
            'category': intern.category,
            'state': intern.state
        })
    
    elif request.method == 'PUT':
        data = request.json
        
        # Update intern details
        for key, value in data.items():
            if key in ['skills', 'interests', 'preferences', 'availability']:
                setattr(intern, key, json.dumps(value))
            else:
                setattr(intern, key, value)
        
        db.session.commit()
        return jsonify({'message': 'Intern updated successfully'})
    
    elif request.method == 'DELETE':
        db.session.delete(intern)
        db.session.commit()
        return jsonify({'message': 'Intern deleted successfully'})

# Project Management APIs
@app.route('/api/projects', methods=['GET', 'POST'])
def manage_projects():
    if request.method == 'POST':
        data = request.json
        
        project = Project(
            title=data['title'],
            description=data.get('description'),
            department=data.get('department'),
            organization=data.get('organization'),
            required_skills=json.dumps(data.get('required_skills', {})),
            preferred_skills=json.dumps(data.get('preferred_skills', {})),
            difficulty_level=data.get('difficulty_level', 3),
            estimated_hours=data.get('estimated_hours'),
            duration_weeks=data.get('duration_weeks'),
            tech_stack=json.dumps(data.get('tech_stack', [])),
            project_type=data.get('project_type'),
            remote_allowed=data.get('remote_allowed', True),
            max_interns=data.get('max_interns', 1),
            yojana_approved=data.get('yojana_approved', False),
            stipend_amount=data.get('stipend_amount'),
            certificate_provided=data.get('certificate_provided', True)
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({'message': 'Project created successfully', 'id': project.id}), 201
    
    else:
        projects = Project.query.all()
        return jsonify([{
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'department': project.department,
            'organization': project.organization,
            'required_skills': project.get_required_skills(),
            'difficulty_level': project.difficulty_level,
            'duration_weeks': project.duration_weeks,
            'project_type': project.project_type,
            'yojana_approved': project.yojana_approved,
            'stipend_amount': project.stipend_amount
        } for project in projects])

# Mentor Management APIs
@app.route('/api/mentors', methods=['GET', 'POST'])
def manage_mentors():
    if request.method == 'POST':
        data = request.json
        
        mentor = Mentor(
            name=data['name'],
            email=data['email'],
            designation=data.get('designation'),
            organization=data.get('organization'),
            experience_years=data.get('experience_years'),
            expertise_areas=json.dumps(data.get('expertise_areas', [])),
            mentoring_style=data.get('mentoring_style', 'Collaborative'),
            max_interns=data.get('max_interns', 3),
            availability=json.dumps(data.get('availability', {})),
            rating=data.get('rating', 5.0)
        )
        
        db.session.add(mentor)
        db.session.commit()
        
        return jsonify({'message': 'Mentor created successfully', 'id': mentor.id}), 201
    
    else:
        mentors = Mentor.query.all()
        return jsonify([{
            'id': mentor.id,
            'name': mentor.name,
            'email': mentor.email,
            'designation': mentor.designation,
            'organization': mentor.organization,
            'experience_years': mentor.experience_years,
            'expertise_areas': json.loads(mentor.expertise_areas) if mentor.expertise_areas else [],
            'mentoring_style': mentor.mentoring_style,
            'max_interns': mentor.max_interns,
            'rating': mentor.rating,
            'total_mentored': mentor.total_mentored
        } for mentor in mentors])

# Core Allocation APIs
@app.route('/api/allocations/generate', methods=['POST'])
def generate_allocations():
    """Main allocation generation endpoint"""
    try:
        # Get all unallocated interns
        allocated_intern_ids = db.session.query(Allocation.intern_id).filter(
            Allocation.status.in_(['pending', 'active'])
        ).all()
        allocated_intern_ids = [id[0] for id in allocated_intern_ids]
        
        interns = Intern.query.filter(~Intern.id.in_(allocated_intern_ids)).all()
        
        # Get available projects
        allocated_project_ids = db.session.query(Allocation.project_id).filter(
            Allocation.status.in_(['pending', 'active'])
        ).all()
        allocated_project_ids = [id[0] for id in allocated_project_ids]
        
        projects = Project.query.filter(~Project.id.in_(allocated_project_ids)).all()
        
        # Get available mentors
        mentors = Mentor.query.all()
        
        # Generate allocations
        result = allocation_engine.generate_optimal_allocation(interns, projects, mentors)
        
        # Save allocations to database
        saved_allocations = []
        batch_id = str(uuid.uuid4())
        
        for allocation_data in result['allocations']:
            allocation = Allocation(
                intern_id=allocation_data['intern_id'],
                project_id=allocation_data['project_id'],
                mentor_id=allocation_data['mentor_id'],
                match_score=allocation_data['final_score'],
                skill_match_score=allocation_data['skill_match'],
                preference_match_score=allocation_data['preference_match'],
                availability_match_score=allocation_data['availability_match'],
                status='pending',
                start_date=datetime.now() + timedelta(days=7)  # Start next week
            )
            
            db.session.add(allocation)
            saved_allocations.append(allocation)
        
        # Save allocation history
        history = AllocationHistory(
            allocation_batch_id=batch_id,
            total_interns=len(interns),
            total_projects=len(projects),
            total_mentors=len(mentors),
            average_match_score=result['average_score'],
            allocation_time_seconds=result['processing_time'],
            algorithm_version=result['algorithm_version']
        )
        
        db.session.add(history)
        db.session.commit()
        
        # Generate AI insights
        insights = insights_generator.generate_advanced_insights(result)
        
        # Start real-time monitoring
        realtime_monitor.start_monitoring_session(batch_id, result['allocations'])
        
        return jsonify({
            'success': True,
            'batch_id': batch_id,
            'allocations': result['allocations'],
            'summary': {
                'total_allocations': result['total_matches'],
                'average_score': result['average_score'],
                'processing_time': result['processing_time']
            },
            'insights': insights
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/allocations', methods=['GET'])
def get_allocations():
    """Get all allocations with details"""
    allocations = db.session.query(Allocation).join(Intern).join(Project).join(Mentor).all()
    
    result = []
    for allocation in allocations:
        result.append({
            'id': allocation.id,
            'intern': {
                'id': allocation.intern.id,
                'name': allocation.intern.name,
                'email': allocation.intern.email,
                'college': allocation.intern.college,
                'skills': allocation.intern.get_skills()
            },
            'project': {
                'id': allocation.project.id,
                'title': allocation.project.title,
                'department': allocation.project.department,
                'organization': allocation.project.organization,
                'difficulty_level': allocation.project.difficulty_level
            },
            'mentor': {
                'id': allocation.mentor.id,
                'name': allocation.mentor.name,
                'designation': allocation.mentor.designation,
                'organization': allocation.mentor.organization,
                'rating': allocation.mentor.rating
            },
            'scores': {
                'overall_match': allocation.match_score,
                'skill_match': allocation.skill_match_score,
                'preference_match': allocation.preference_match_score,
                'availability_match': allocation.availability_match_score
            },
            'status': allocation.status,
            'start_date': allocation.start_date.isoformat() if allocation.start_date else None,
            'created_at': allocation.created_at.isoformat()
        })
    
    return jsonify(result)

@app.route('/api/allocations/<allocation_id>/feedback', methods=['POST'])
def submit_feedback(allocation_id):
    """Submit feedback for an allocation"""
    data = request.json
    allocation = Allocation.query.get_or_404(allocation_id)
    
    allocation.intern_feedback = data.get('intern_feedback')
    allocation.mentor_feedback = data.get('mentor_feedback')
    allocation.project_rating = data.get('project_rating')
    allocation.learning_outcomes = json.dumps(data.get('learning_outcomes', []))
    allocation.updated_at = datetime.now()
    
    db.session.commit()
    
    return jsonify({'message': 'Feedback submitted successfully'})

# Wow Factor APIs

@app.route('/api/realtime/monitor/<session_id>', methods=['GET'])
def get_realtime_updates(session_id):
    """Get real-time monitoring updates"""
    update = realtime_monitor.simulate_realtime_updates(session_id)
    
    if update:
        return jsonify({
            'success': True,
            'update': update,
            'session_metrics': realtime_monitor.active_sessions.get(session_id, {}).get('metrics', {})
        })
    else:
        return jsonify({'success': False, 'message': 'Session not found'}), 404

@app.route('/api/ai/insights', methods=['POST'])
def get_ai_insights():
    """Get AI-generated insights for allocations"""
    data = request.json
    allocations = data.get('allocations', [])
    historical_data = data.get('historical_data')
    
    insights = insights_generator.generate_advanced_insights(allocations, historical_data)
    
    return jsonify({
        'success': True,
        'insights': insights,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/ai/chatbot', methods=['POST'])
def chat_with_ai():
    """AI chatbot for allocation queries"""
    data = request.json
    query = data.get('query', '')
    context_data = data.get('context')
    
    response = ai_chatbot.process_query(query, context_data)
    
    return jsonify({
        'success': True,
        'response': response,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/analytics/dashboard', methods=['GET'])
def get_analytics_dashboard():
    """Get comprehensive analytics for dashboard"""
    # Get allocation statistics
    total_interns = Intern.query.count()
    total_projects = Project.query.count()
    total_mentors = Mentor.query.count()
    total_allocations = Allocation.query.count()
    
    # Get recent allocations
    recent_allocations = Allocation.query.order_by(Allocation.created_at.desc()).limit(10).all()
    
    # Calculate success metrics
    completed_allocations = Allocation.query.filter_by(status='completed').all()
    avg_rating = db.session.query(db.func.avg(Allocation.project_rating)).filter(
        Allocation.project_rating.isnot(None)
    ).scalar() or 0
    
    # Get allocation history
    allocation_history = AllocationHistory.query.order_by(AllocationHistory.created_at.desc()).limit(5).all()
    
    return jsonify({
        'summary': {
            'total_interns': total_interns,
            'total_projects': total_projects,
            'total_mentors': total_mentors,
            'total_allocations': total_allocations,
            'success_rate': len([a for a in completed_allocations if (a.project_rating or 0) >= 4]) / max(len(completed_allocations), 1) * 100,
            'average_rating': round(avg_rating, 2)
        },
        'recent_activity': [{
            'allocation_id': a.id,
            'intern_name': a.intern.name,
            'project_title': a.project.title,
            'mentor_name': a.mentor.name,
            'match_score': a.match_score,
            'status': a.status,
            'created_at': a.created_at.isoformat()
        } for a in recent_allocations],
        'performance_trends': [{
            'batch_id': h.allocation_batch_id,
            'date': h.created_at.strftime('%Y-%m-%d'),
            'average_score': h.average_match_score,
            'total_allocations': h.total_interns,
            'processing_time': h.allocation_time_seconds
        } for h in allocation_history]
    })

# PM Internship Yojana Integration APIs
@app.route('/api/yojana/compliance/<int:intern_id>', methods=['GET', 'PUT'])
def manage_yojana_compliance(intern_id):
    """Manage PM Internship Yojana compliance for interns"""
    intern = Intern.query.get_or_404(intern_id)
    
    if request.method == 'GET':
        compliance = YojanaCompliance.query.filter_by(intern_id=intern_id).first()
        
        if not compliance:
            # Create default compliance record
            compliance = YojanaCompliance(intern_id=intern_id)
            db.session.add(compliance)
            db.session.commit()
        
        return jsonify({
            'intern_id': intern_id,
            'intern_name': intern.name,
            'documents_verified': compliance.documents_verified,
            'eligibility_confirmed': compliance.eligibility_confirmed,
            'background_check': compliance.background_check,
            'attendance_percentage': compliance.attendance_percentage,
            'weekly_reports_submitted': compliance.weekly_reports_submitted,
            'final_presentation': compliance.final_presentation,
            'project_deliverables': compliance.project_deliverables,
            'certificate_issued': compliance.certificate_issued,
            'compliance_score': calculate_compliance_score(compliance)
        })
    
    elif request.method == 'PUT':
        data = request.json
        compliance = YojanaCompliance.query.filter_by(intern_id=intern_id).first()
        
        if not compliance:
            compliance = YojanaCompliance(intern_id=intern_id)
        
        # Update compliance fields
        for key, value in data.items():
            if hasattr(compliance, key):
                setattr(compliance, key, value)
        
        compliance.updated_at = datetime.now()
        
        db.session.add(compliance)
        db.session.commit()
        
        return jsonify({'message': 'Compliance updated successfully'})

@app.route('/api/yojana/batch-report', methods=['GET'])
def generate_yojana_batch_report():
    """Generate comprehensive report for PM Internship Yojana"""
    interns = Intern.query.all()
    total_interns = len(interns)
    
    # Category-wise distribution
    category_distribution = {}
    state_distribution = {}
    
    for intern in interns:
        category = intern.category or 'General'
        state = intern.state or 'Unknown'
        
        category_distribution[category] = category_distribution.get(category, 0) + 1
        state_distribution[state] = state_distribution.get(state, 0) + 1
    
    # Compliance statistics
    compliance_records = YojanaCompliance.query.all()
    verified_docs = len([c for c in compliance_records if c.documents_verified])
    completed_interns = len([c for c in compliance_records if c.certificate_issued])
    
    return jsonify({
        'batch_summary': {
            'total_interns': total_interns,
            'category_distribution': category_distribution,
            'state_distribution': state_distribution,
            'documents_verified': verified_docs,
            'completed_interns': completed_interns,
            'completion_rate': (completed_interns / max(total_interns, 1)) * 100
        },
        'compliance_metrics': {
            'average_attendance': db.session.query(db.func.avg(YojanaCompliance.attendance_percentage)).scalar() or 0,
            'reports_submitted': db.session.query(db.func.sum(YojanaCompliance.weekly_reports_submitted)).scalar() or 0,
            'presentations_completed': len([c for c in compliance_records if c.final_presentation])
        },
        'generated_at': datetime.now().isoformat()
    })

# Utility Functions
def calculate_compliance_score(compliance):
    """Calculate overall compliance score for Yojana requirements"""
    criteria = [
        compliance.documents_verified,
        compliance.eligibility_confirmed,
        compliance.background_check,
        compliance.attendance_percentage >= 75,  # Minimum attendance requirement
        compliance.weekly_reports_submitted >= 8,  # Assuming 12-week program
        compliance.final_presentation,
        compliance.project_deliverables
    ]
    
    score = (sum(criteria) / len(criteria)) * 100
    return round(score, 2)

# Initialize database function
def create_tables():
    """Create database tables"""
    with app.app_context():
        db.create_all()

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    print("🚀 PM Smart Allocation Engine Starting...")
    print("🤖 AI Engine: Ready")
    print("📊 Real-time Monitor: Active")
    print("💡 Insights Generator: Online")
    print("🎯 Allocation Engine: Initialized")
    print("\n✨ Access the dashboard at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
