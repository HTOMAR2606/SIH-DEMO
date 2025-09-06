import json
import random
from datetime import datetime, timedelta
from src.models import db, Intern, Project, Mentor, YojanaCompliance, Allocation

class PMYojanaSampleDataGenerator:
    """
    Generate realistic sample data for PM Internship Yojana integration
    """
    
    def __init__(self):
        self.indian_names = [
            "Aarav Sharma", "Vivaan Singh", "Aditya Kumar", "Vihaan Patel", "Arjun Gupta",
            "Sai Reddy", "Reyansh Joshi", "Ayaan Khan", "Krishna Rao", "Ishaan Mishra",
            "Ananya Singh", "Diya Sharma", "Aadhya Patel", "Kavya Kumar", "Arya Gupta",
            "Myra Reddy", "Anika Joshi", "Sara Khan", "Ira Rao", "Tara Mishra",
            "Priya Agarwal", "Sneha Bansal", "Ritika Chopra", "Nisha Dubey", "Pooja Garg"
        ]
        
        self.indian_colleges = [
            "Indian Institute of Technology Delhi", "Indian Institute of Technology Bombay",
            "Indian Institute of Technology Madras", "Indian Institute of Technology Kanpur",
            "Indian Institute of Technology Kharagpur", "Indian Institute of Technology Roorkee",
            "BITS Pilani", "Delhi University", "Jawaharlal Nehru University",
            "University of Mumbai", "Anna University", "Osmania University",
            "VIT University", "SRM University", "Manipal Institute of Technology",
            "National Institute of Technology Trichy", "National Institute of Technology Warangal",
            "Pune University", "Bangalore University", "Calcutta University"
        ]
        
        self.branches = [
            "Computer Science Engineering", "Electronics and Communication",
            "Mechanical Engineering", "Civil Engineering", "Electrical Engineering",
            "Information Technology", "Chemical Engineering", "Biotechnology",
            "Mathematics", "Physics", "Chemistry", "Economics", "Business Administration",
            "Commerce", "Management Studies", "Data Science", "AI and Machine Learning"
        ]
        
        self.indian_states = [
            "Delhi", "Maharashtra", "Karnataka", "Tamil Nadu", "Telangana",
            "Gujarat", "Rajasthan", "Uttar Pradesh", "West Bengal", "Madhya Pradesh",
            "Haryana", "Punjab", "Kerala", "Odisha", "Jharkhand", "Bihar",
            "Assam", "Chhattisgarh", "Uttarakhand", "Himachal Pradesh"
        ]
        
        self.categories = ["General", "OBC", "SC", "ST", "EWS"]
        
        self.pm_skills = {
            "Python": [6, 7, 8, 9],
            "Data Analysis": [5, 6, 7, 8, 9],
            "Excel": [7, 8, 9],
            "SQL": [5, 6, 7, 8],
            "Tableau": [4, 5, 6, 7],
            "PowerBI": [4, 5, 6, 7],
            "Market Research": [5, 6, 7, 8, 9],
            "Product Strategy": [4, 5, 6, 7, 8],
            "User Research": [5, 6, 7, 8],
            "Agile": [5, 6, 7, 8],
            "Scrum": [5, 6, 7],
            "Project Management": [5, 6, 7, 8, 9],
            "Presentation": [6, 7, 8, 9],
            "Communication": [7, 8, 9],
            "Leadership": [4, 5, 6, 7, 8],
            "Analytics": [5, 6, 7, 8],
            "Statistics": [4, 5, 6, 7, 8],
            "Business Model": [4, 5, 6, 7],
            "Customer Insights": [5, 6, 7, 8],
            "Competitive Analysis": [5, 6, 7, 8]
        }
        
        self.project_templates = [
            {
                "title": "Digital India Portal Enhancement",
                "description": "Enhance government portal user experience for Digital India initiative",
                "department": "Digital Services",
                "organization": "Ministry of Electronics and IT",
                "project_type": "Development",
                "required_skills": {"User Research": 7, "Product Strategy": 6, "Analytics": 7},
                "tech_stack": ["React", "Node.js", "MongoDB"],
                "difficulty_level": 3,
                "yojana_approved": True,
                "stipend_amount": 30000
            },
            {
                "title": "Startup India Ecosystem Analysis",
                "description": "Analyze startup ecosystem and create actionable insights for policy making",
                "department": "Policy Research",
                "organization": "Department for Promotion of Industry and Internal Trade",
                "project_type": "Research",
                "required_skills": {"Market Research": 8, "Data Analysis": 7, "Presentation": 8},
                "tech_stack": ["Excel", "Tableau", "Python"],
                "difficulty_level": 4,
                "yojana_approved": True,
                "stipend_amount": 28000
            },
            {
                "title": "Smart City Data Platform Development",
                "description": "Build data analytics platform for smart city initiatives",
                "department": "Urban Development",
                "organization": "Smart Cities Mission",
                "project_type": "Development",
                "required_skills": {"Python": 8, "SQL": 7, "Data Analysis": 8},
                "tech_stack": ["Python", "PostgreSQL", "Apache Kafka"],
                "difficulty_level": 5,
                "yojana_approved": True,
                "stipend_amount": 35000
            },
            {
                "title": "Healthcare Analytics for Ayushman Bharat",
                "description": "Develop healthcare analytics dashboard for Ayushman Bharat scheme",
                "department": "Healthcare",
                "organization": "National Health Authority",
                "project_type": "Analytics",
                "required_skills": {"Data Analysis": 8, "Tableau": 7, "Healthcare Domain": 5},
                "tech_stack": ["Tableau", "PowerBI", "SQL"],
                "difficulty_level": 4,
                "yojana_approved": True,
                "stipend_amount": 32000
            },
            {
                "title": "Financial Inclusion Product Strategy",
                "description": "Develop product strategy for financial inclusion initiatives",
                "department": "Financial Services",
                "organization": "Reserve Bank of India",
                "project_type": "Strategy",
                "required_skills": {"Product Strategy": 8, "Market Research": 7, "Business Model": 6},
                "tech_stack": ["Excel", "PowerPoint", "Tableau"],
                "difficulty_level": 3,
                "yojana_approved": True,
                "stipend_amount": 25000
            },
            {
                "title": "EdTech Platform for Rural Education",
                "description": "Design and develop educational technology platform for rural areas",
                "department": "Education Technology",
                "organization": "Ministry of Education",
                "project_type": "Development",
                "required_skills": {"Product Management": 7, "User Research": 8, "Technology": 6},
                "tech_stack": ["React Native", "Firebase", "AWS"],
                "difficulty_level": 4,
                "yojana_approved": True,
                "stipend_amount": 30000
            }
        ]
        
        self.mentor_profiles = [
            {
                "name": "Dr. Rajesh Kumar",
                "designation": "Director - Product Strategy",
                "organization": "TechMahindra",
                "experience_years": 12,
                "expertise_areas": ["Product Strategy", "AI/ML", "Digital Transformation"],
                "mentoring_style": "Collaborative"
            },
            {
                "name": "Ms. Priya Sharma",
                "designation": "Senior Vice President",
                "organization": "Infosys",
                "experience_years": 10,
                "expertise_areas": ["Data Analytics", "Business Intelligence", "Team Leadership"],
                "mentoring_style": "Guidance"
            },
            {
                "name": "Mr. Arjun Reddy",
                "designation": "Chief Product Officer",
                "organization": "Wipro",
                "experience_years": 15,
                "expertise_areas": ["Product Development", "Agile", "Customer Experience"],
                "mentoring_style": "Hands-on"
            },
            {
                "name": "Dr. Sneha Patel",
                "designation": "Research Head",
                "organization": "Tata Consultancy Services",
                "experience_years": 8,
                "expertise_areas": ["Market Research", "Policy Analysis", "Innovation"],
                "mentoring_style": "Collaborative"
            },
            {
                "name": "Mr. Vikash Singh",
                "designation": "Product Manager",
                "organization": "Accenture",
                "experience_years": 6,
                "expertise_areas": ["Digital Products", "User Experience", "Analytics"],
                "mentoring_style": "Guidance"
            }
        ]
    
    def generate_realistic_intern(self, index):
        """Generate a realistic intern profile for PM Internship Yojana"""
        name = self.indian_names[index % len(self.indian_names)]
        
        # Generate skills realistically
        skills = {}
        skill_items = list(self.pm_skills.keys())
        num_skills = random.randint(4, 8)
        
        for _ in range(num_skills):
            skill = random.choice(skill_items)
            if skill not in skills:
                skills[skill] = random.choice(self.pm_skills[skill])
        
        # Generate interests based on skills
        interests = []
        if "Python" in skills or "Data Analysis" in skills:
            interests.extend(["Data Science", "AI/ML", "Analytics"])
        if "Market Research" in skills:
            interests.extend(["Market Analysis", "Consumer Behavior"])
        if "Product Strategy" in skills:
            interests.extend(["Product Management", "Strategy Planning"])
        
        # Remove duplicates and limit
        interests = list(set(interests))[:4]
        
        # Generate preferences
        preferences = {
            "project_type": random.choice(["Development", "Research", "Analytics", "Strategy"]),
            "mentoring_style": random.choice(["Collaborative", "Guidance", "Hands-on"]),
            "technologies": random.sample(["Python", "React", "Tableau", "Excel", "SQL"], random.randint(2, 4)),
            "remote_preference": random.choice([True, False])
        }
        
        return {
            "name": name,
            "email": f"{name.lower().replace(' ', '.')}.{index}@college.edu",
            "phone": f"+91{random.randint(7000000000, 9999999999)}",
            "college": random.choice(self.indian_colleges),
            "branch": random.choice(self.branches),
            "year": random.randint(2, 4),
            "cgpa": round(random.uniform(6.5, 9.5), 2),
            "skills": skills,
            "interests": interests,
            "preferences": preferences,
            "availability": {
                "hours_per_week": random.randint(20, 40),
                "preferred_time": random.choice(["Morning", "Afternoon", "Evening", "Flexible"])
            },
            "aadhar_number": f"{random.randint(100000000000, 999999999999)}",
            "application_id": f"PM2025{str(index+1).zfill(3)}",
            "category": random.choice(self.categories),
            "state": random.choice(self.indian_states)
        }
    
    def generate_realistic_project(self, template, index):
        """Generate project based on template with variations"""
        project = template.copy()
        
        # Add variations
        project["title"] = f"{project['title']} - Phase {random.randint(1, 3)}"
        project["estimated_hours"] = random.randint(200, 400)
        project["duration_weeks"] = random.randint(8, 16)
        project["max_interns"] = random.randint(1, 3)
        project["remote_allowed"] = random.choice([True, False])
        
        return project
    
    def generate_realistic_mentor(self, profile, index):
        """Generate mentor based on profile with variations"""
        mentor = profile.copy()
        
        # Add email
        mentor["email"] = f"{mentor['name'].lower().replace(' ', '.').replace('dr.', '').replace('ms.', '').replace('mr.', '')}.{index}@{mentor['organization'].lower().replace(' ', '')}.com"
        
        # Add performance metrics
        mentor["rating"] = round(random.uniform(4.2, 5.0), 1)
        mentor["total_mentored"] = random.randint(10, 50)
        mentor["success_rate"] = round(random.uniform(80, 98), 1)
        mentor["max_interns"] = random.randint(2, 5)
        
        # Add availability
        mentor["availability"] = {
            "hours_per_week": random.randint(5, 15),
            "preferred_days": random.sample(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], random.randint(3, 5)),
            "time_zone": "IST"
        }
        
        return mentor
    
    def populate_database(self, num_interns=25, num_projects=15, num_mentors=8):
        """Populate database with realistic PM Yojana data"""
        
        # Clear existing data
        db.session.query(Allocation).delete()
        db.session.query(YojanaCompliance).delete()
        db.session.query(Intern).delete()
        db.session.query(Project).delete()
        db.session.query(Mentor).delete()
        db.session.commit()
        
        print(f"🧑‍🎓 Generating {num_interns} PM Internship Yojana interns...")
        
        # Generate interns
        for i in range(num_interns):
            intern_data = self.generate_realistic_intern(i)
            
            intern = Intern(
                name=intern_data["name"],
                email=intern_data["email"],
                phone=intern_data["phone"],
                college=intern_data["college"],
                branch=intern_data["branch"],
                year=intern_data["year"],
                cgpa=intern_data["cgpa"],
                skills=json.dumps(intern_data["skills"]),
                interests=json.dumps(intern_data["interests"]),
                preferences=json.dumps(intern_data["preferences"]),
                availability=json.dumps(intern_data["availability"]),
                aadhar_number=intern_data["aadhar_number"],
                application_id=intern_data["application_id"],
                category=intern_data["category"],
                state=intern_data["state"]
            )
            
            db.session.add(intern)
            
            # Create compliance record
            compliance = YojanaCompliance(
                intern_id=i+1,  # Will be updated after commit
                documents_verified=random.choice([True, False]),
                eligibility_confirmed=random.choice([True, False]),
                background_check=random.choice([True, False]),
                attendance_percentage=random.uniform(70, 95),
                weekly_reports_submitted=random.randint(0, 12)
            )
            
            db.session.add(compliance)
        
        print(f"🏢 Generating {num_projects} government-approved projects...")
        
        # Generate projects
        for i in range(num_projects):
            template = random.choice(self.project_templates)
            project_data = self.generate_realistic_project(template, i)
            
            project = Project(
                title=project_data["title"],
                description=project_data["description"],
                department=project_data["department"],
                organization=project_data["organization"],
                required_skills=json.dumps(project_data["required_skills"]),
                preferred_skills=json.dumps({}),
                difficulty_level=project_data["difficulty_level"],
                estimated_hours=project_data["estimated_hours"],
                duration_weeks=project_data["duration_weeks"],
                tech_stack=json.dumps(project_data["tech_stack"]),
                project_type=project_data["project_type"],
                remote_allowed=project_data["remote_allowed"],
                max_interns=project_data["max_interns"],
                yojana_approved=project_data["yojana_approved"],
                stipend_amount=project_data["stipend_amount"],
                certificate_provided=True
            )
            
            db.session.add(project)
        
        print(f"👨‍🏫 Generating {num_mentors} experienced mentors...")
        
        # Generate mentors
        for i in range(num_mentors):
            profile = self.mentor_profiles[i % len(self.mentor_profiles)]
            mentor_data = self.generate_realistic_mentor(profile, i)
            
            mentor = Mentor(
                name=mentor_data["name"],
                email=mentor_data["email"],
                designation=mentor_data["designation"],
                organization=mentor_data["organization"],
                experience_years=mentor_data["experience_years"],
                expertise_areas=json.dumps(mentor_data["expertise_areas"]),
                mentoring_style=mentor_data["mentoring_style"],
                max_interns=mentor_data["max_interns"],
                availability=json.dumps(mentor_data["availability"]),
                rating=mentor_data["rating"],
                total_mentored=mentor_data["total_mentored"],
                success_rate=mentor_data["success_rate"]
            )
            
            db.session.add(mentor)
        
        db.session.commit()
        
        print("✅ Sample data generation completed!")
        print(f"📊 Created: {num_interns} interns, {num_projects} projects, {num_mentors} mentors")
        
        return {
            "interns_created": num_interns,
            "projects_created": num_projects,
            "mentors_created": num_mentors,
            "yojana_compliance_records": num_interns
        }
    
    def generate_demo_scenario(self):
        """Generate specific demo scenario for hackathon presentation"""
        
        # High-quality demo interns with diverse backgrounds
        demo_interns = [
            {
                "name": "Aarav Sharma",
                "email": "aarav.sharma@iitdelhi.ac.in",
                "college": "Indian Institute of Technology Delhi",
                "branch": "Computer Science Engineering",
                "year": 3,
                "cgpa": 9.2,
                "skills": {"Python": 9, "Data Analysis": 8, "Machine Learning": 8, "Product Strategy": 7},
                "interests": ["AI/ML", "Product Management", "Data Science"],
                "preferences": {"project_type": "Development", "mentoring_style": "Collaborative"},
                "category": "General",
                "state": "Delhi",
                "application_id": "PM2025DEMO001"
            },
            {
                "name": "Priya Patel",
                "email": "priya.patel@bitspilani.ac.in",
                "college": "BITS Pilani",
                "branch": "Electronics and Communication",
                "year": 4,
                "cgpa": 8.9,
                "skills": {"Market Research": 9, "Analytics": 8, "Presentation": 9, "Excel": 8},
                "interests": ["Market Analysis", "Consumer Behavior", "Policy Research"],
                "preferences": {"project_type": "Research", "mentoring_style": "Guidance"},
                "category": "General",
                "state": "Rajasthan",
                "application_id": "PM2025DEMO002"
            },
            {
                "name": "Arjun Singh",
                "email": "arjun.singh@nittrichy.ac.in",
                "college": "National Institute of Technology Trichy",
                "branch": "Mechanical Engineering",
                "year": 3,
                "cgpa": 8.1,
                "skills": {"Project Management": 8, "Leadership": 7, "Analytics": 6, "Communication": 9},
                "interests": ["Product Strategy", "Team Management", "Process Optimization"],
                "preferences": {"project_type": "Management", "mentoring_style": "Hands-on"},
                "category": "OBC",
                "state": "Tamil Nadu",
                "application_id": "PM2025DEMO003"
            }
        ]
        
        return demo_interns

class YojanaIntegrationHelper:
    """
    Helper class for PM Internship Yojana integration features
    """
    
    @staticmethod
    def validate_yojana_eligibility(intern_data):
        """Validate intern eligibility for PM Internship Yojana"""
        criteria = {
            "age_limit": True,  # Assume age validation is done elsewhere
            "education_qualification": intern_data.get("year", 0) >= 2,
            "cgpa_requirement": intern_data.get("cgpa", 0) >= 6.0,
            "citizenship": True,  # Indian citizen
            "category_verification": intern_data.get("category") in ["General", "OBC", "SC", "ST", "EWS"]
        }
        
        eligibility_score = sum(criteria.values()) / len(criteria) * 100
        
        return {
            "eligible": eligibility_score >= 80,
            "score": eligibility_score,
            "criteria_met": criteria,
            "recommendations": YojanaIntegrationHelper.get_eligibility_recommendations(criteria)
        }
    
    @staticmethod
    def get_eligibility_recommendations(criteria):
        """Get recommendations for improving eligibility"""
        recommendations = []
        
        if not criteria["education_qualification"]:
            recommendations.append("Complete at least 2 years of undergraduate study")
        
        if not criteria["cgpa_requirement"]:
            recommendations.append("Maintain minimum CGPA of 6.0")
        
        return recommendations
    
    @staticmethod
    def generate_yojana_certificate(intern, project, mentor, allocation):
        """Generate PM Internship Yojana completion certificate data"""
        certificate_data = {
            "certificate_id": f"PM-CERT-{allocation.id}-{datetime.now().year}",
            "intern_name": intern.name,
            "project_title": project.title,
            "organization": project.organization,
            "mentor_name": mentor.name,
            "start_date": allocation.start_date.strftime("%d/%m/%Y") if allocation.start_date else "TBD",
            "completion_date": (allocation.start_date + timedelta(weeks=project.duration_weeks)).strftime("%d/%m/%Y") if allocation.start_date else "TBD",
            "duration_weeks": project.duration_weeks,
            "skills_developed": list(json.loads(project.required_skills).keys()) if project.required_skills else [],
            "performance_rating": allocation.project_rating or 0,
            "issued_date": datetime.now().strftime("%d/%m/%Y"),
            "authority": "Prime Minister's Office - Internship Yojana",
            "verification_code": f"PMY{random.randint(100000, 999999)}"
        }
        
        return certificate_data
    
    @staticmethod
    def calculate_stipend_eligibility(intern, project, compliance):
        """Calculate stipend eligibility based on performance"""
        base_stipend = project.stipend_amount or 25000
        
        # Performance multipliers
        attendance_multiplier = min(1.0, compliance.attendance_percentage / 75)  # 75% minimum
        report_multiplier = min(1.0, compliance.weekly_reports_submitted / 10)  # 10 reports minimum
        deliverable_multiplier = 1.0 if compliance.project_deliverables else 0.8
        
        final_stipend = base_stipend * attendance_multiplier * report_multiplier * deliverable_multiplier
        
        return {
            "base_stipend": base_stipend,
            "final_stipend": round(final_stipend, 2),
            "attendance_factor": round(attendance_multiplier, 2),
            "report_factor": round(report_multiplier, 2),
            "deliverable_factor": deliverable_multiplier,
            "eligible": final_stipend >= (base_stipend * 0.75)  # Minimum 75% of base stipend
        }
    
    @staticmethod
    def generate_performance_report(intern, allocation, compliance):
        """Generate comprehensive performance report for Yojana compliance"""
        
        performance_metrics = {
            "intern_details": {
                "name": intern.name,
                "application_id": intern.application_id,
                "college": intern.college,
                "category": intern.category,
                "state": intern.state
            },
            "project_performance": {
                "skill_development": "Excellent" if allocation.match_score > 85 else "Good" if allocation.match_score > 70 else "Satisfactory",
                "mentor_feedback": allocation.mentor_feedback or "Pending",
                "project_rating": allocation.project_rating or 0,
                "completion_status": allocation.status
            },
            "compliance_metrics": {
                "attendance_percentage": compliance.attendance_percentage,
                "weekly_reports": compliance.weekly_reports_submitted,
                "documents_verified": compliance.documents_verified,
                "final_presentation": compliance.final_presentation,
                "deliverables_completed": compliance.project_deliverables
            },
            "recommendations": [
                "Continue focus on technical skill development",
                "Enhance presentation and communication skills",
                "Explore advanced product management concepts"
            ],
            "next_steps": [
                "Consider advanced PM certification",
                "Apply for full-time PM roles",
                "Join PM community networks"
            ]
        }
        
        return performance_metrics

def create_yojana_integration_demo():
    """Create a comprehensive demo setup for PM Internship Yojana integration"""
    
    print("🇮🇳 Setting up PM Internship Yojana Integration Demo...")
    
    generator = PMYojanaSampleDataGenerator()
    
    # Generate comprehensive dataset
    result = generator.populate_database(
        num_interns=30,  # Realistic batch size
        num_projects=20,  # More projects than interns for better matching
        num_mentors=12    # Good mentor-to-intern ratio
    )
    
    print("\n📋 Demo Scenario Details:")
    print(f"  • Total Interns: {result['interns_created']}")
    print(f"  • Government Projects: {result['projects_created']}")
    print(f"  • Industry Mentors: {result['mentors_created']}")
    print(f"  • Compliance Records: {result['yojana_compliance_records']}")
    
    print("\n🎯 Key Demo Features:")
    print("  • AI-powered skill matching")
    print("  • Government compliance tracking")
    print("  • Real-time allocation monitoring")
    print("  • 3D visualization of matches")
    print("  • Predictive success analytics")
    print("  • Interactive AI chatbot")
    
    return result

if __name__ == "__main__":
    # For standalone testing
    create_yojana_integration_demo()
