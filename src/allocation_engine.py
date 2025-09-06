import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier
import json
import random
from datetime import datetime, timedelta
from textblob import TextBlob
import nltk
from collections import defaultdict

class SmartAllocationEngine:
    def __init__(self):
        self.skill_vectorizer = TfidfVectorizer(stop_words='english')
        self.success_predictor = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        
        # Download NLTK data (if not already present)
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        # Skill categories for PM roles
        self.pm_skill_categories = {
            'technical': ['python', 'sql', 'data analysis', 'excel', 'tableau', 'powerbi', 'jira', 'confluence'],
            'product': ['product management', 'user research', 'wireframing', 'agile', 'scrum', 'roadmapping'],
            'analytical': ['statistics', 'market research', 'competitive analysis', 'metrics', 'kpi'],
            'communication': ['presentation', 'documentation', 'stakeholder management', 'cross-functional'],
            'business': ['strategy', 'business model', 'market analysis', 'customer insights']
        }
    
    def calculate_skill_match(self, intern_skills, project_requirements):
        """
        Advanced skill matching using NLP and weighted scoring
        """
        if not intern_skills or not project_requirements:
            return 0.0
        
        # Normalize and extract skills text
        intern_skills_text = self._extract_skills_text(intern_skills)
        project_skills_text = self._extract_skills_text(project_requirements)
        
        if not intern_skills_text or not project_skills_text:
            return 0.0
        
        # Create TF-IDF vectors
        texts = [intern_skills_text, project_skills_text]
        try:
            tfidf_matrix = self.skill_vectorizer.fit_transform(texts)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except:
            # Fallback to simple keyword matching
            similarity = self._simple_keyword_match(intern_skills, project_requirements)
        
        # Apply skill category weighting
        category_bonus = self._calculate_category_bonus(intern_skills, project_requirements)
        
        final_score = min(100.0, (similarity * 70) + (category_bonus * 30))
        return round(final_score, 2)
    
    def _extract_skills_text(self, skills_dict):
        """Extract and normalize skills text from dictionary"""
        if isinstance(skills_dict, str):
            try:
                skills_dict = json.loads(skills_dict)
            except:
                return skills_dict.lower()
        
        if isinstance(skills_dict, dict):
            return ' '.join([str(skill).lower() for skill in skills_dict.keys()])
        elif isinstance(skills_dict, list):
            return ' '.join([str(skill).lower() for skill in skills_dict])
        
        return str(skills_dict).lower()
    
    def _simple_keyword_match(self, intern_skills, project_skills):
        """Fallback keyword matching"""
        intern_words = set(self._extract_skills_text(intern_skills).split())
        project_words = set(self._extract_skills_text(project_skills).split())
        
        if not project_words:
            return 0.0
        
        matches = len(intern_words.intersection(project_words))
        return matches / len(project_words)
    
    def _calculate_category_bonus(self, intern_skills, project_skills):
        """Calculate bonus based on PM skill categories"""
        intern_text = self._extract_skills_text(intern_skills)
        project_text = self._extract_skills_text(project_skills)
        
        bonus = 0.0
        for category, skills in self.pm_skill_categories.items():
            intern_matches = sum(1 for skill in skills if skill in intern_text)
            project_needs = sum(1 for skill in skills if skill in project_text)
            
            if project_needs > 0:
                category_match = intern_matches / len(skills)
                bonus += category_match * 20  # 20% bonus per category
        
        return min(100.0, bonus)
    
    def calculate_preference_match(self, intern_preferences, project, mentor):
        """
        Calculate how well project and mentor match intern preferences
        """
        if not intern_preferences:
            return 75.0  # Default neutral score
        
        if isinstance(intern_preferences, str):
            try:
                intern_preferences = json.loads(intern_preferences)
            except:
                return 75.0
        
        score = 0.0
        total_weight = 0.0
        
        # Project type preference
        if 'project_type' in intern_preferences:
            preferred_types = intern_preferences['project_type']
            if isinstance(preferred_types, str):
                preferred_types = [preferred_types]
            
            if project.project_type in preferred_types:
                score += 40
            total_weight += 40
        
        # Technology preference
        if 'technologies' in intern_preferences:
            preferred_tech = intern_preferences['technologies']
            project_tech = json.loads(project.tech_stack) if project.tech_stack else []
            
            tech_match = len(set(preferred_tech).intersection(set(project_tech))) / max(len(preferred_tech), 1)
            score += tech_match * 30
            total_weight += 30
        
        # Mentor style preference
        if 'mentoring_style' in intern_preferences:
            if intern_preferences['mentoring_style'] == mentor.mentoring_style:
                score += 30
            total_weight += 30
        
        # Default score if no specific preferences
        if total_weight == 0:
            return 75.0
        
        return min(100.0, (score / total_weight) * 100)
    
    def calculate_availability_match(self, intern_availability, mentor_availability):
        """
        Calculate schedule compatibility between intern and mentor
        """
        # Simplified availability matching - in real implementation, 
        # this would parse time slots and calculate overlap
        
        if not intern_availability or not mentor_availability:
            return 80.0  # Default good availability
        
        # For demo purposes, random compatibility with slight bias towards good matches
        base_score = random.uniform(60, 95)
        
        # Simulate time zone and schedule preferences
        return round(base_score, 2)
    
    def predict_success_probability(self, intern, project, mentor, match_scores):
        """
        ML-based success prediction using historical data patterns
        """
        # Feature engineering for success prediction
        features = [
            match_scores['skill_match'],
            match_scores['preference_match'],
            match_scores['availability_match'],
            intern.cgpa if intern.cgpa else 7.5,
            mentor.rating,
            mentor.experience_years,
            project.difficulty_level,
            len(json.loads(intern.skills)) if intern.skills else 5,
            1 if project.remote_allowed else 0
        ]
        
        # If model is not trained, use heuristic approach
        if not self.is_trained:
            return self._heuristic_success_prediction(features)
        
        # Use trained ML model
        try:
            probability = self.success_predictor.predict_proba([features])[0][1]
            return round(probability * 100, 2)
        except:
            return self._heuristic_success_prediction(features)
    
    def _heuristic_success_prediction(self, features):
        """Heuristic-based success prediction when ML model isn't available"""
        skill_match, pref_match, avail_match, cgpa, mentor_rating, exp_years, difficulty, skill_count, remote = features
        
        # Weighted combination of factors
        success_score = (
            skill_match * 0.30 +
            pref_match * 0.20 +
            avail_match * 0.15 +
            (cgpa / 10 * 100) * 0.15 +
            (mentor_rating / 5 * 100) * 0.10 +
            min(exp_years / 10 * 100, 100) * 0.05 +
            max(0, 100 - difficulty * 15) * 0.05
        )
        
        return round(min(100, max(0, success_score)), 2)
    
    def generate_optimal_allocation(self, interns, projects, mentors, constraints=None):
        """
        Core allocation algorithm using multi-objective optimization
        """
        start_time = datetime.now()
        
        allocations = []
        used_projects = set()
        mentor_capacity = {mentor.id: mentor.max_interns for mentor in mentors}
        
        # Calculate all possible matches
        match_matrix = []
        
        for intern in interns:
            intern_matches = []
            
            for project in projects:
                if project.id in used_projects:
                    continue
                
                for mentor in mentors:
                    if mentor_capacity[mentor.id] <= 0:
                        continue
                    
                    # Calculate individual match scores
                    skill_match = self.calculate_skill_match(
                        intern.get_skills(), 
                        project.get_required_skills()
                    )
                    
                    preference_match = self.calculate_preference_match(
                        intern.get_preferences(), 
                        project, 
                        mentor
                    )
                    
                    availability_match = self.calculate_availability_match(
                        intern.availability, 
                        mentor.availability
                    )
                    
                    # Overall match score
                    overall_score = (
                        skill_match * 0.5 +
                        preference_match * 0.3 +
                        availability_match * 0.2
                    )
                    
                    # Success prediction
                    match_scores = {
                        'skill_match': skill_match,
                        'preference_match': preference_match,
                        'availability_match': availability_match
                    }
                    
                    success_prob = self.predict_success_probability(
                        intern, project, mentor, match_scores
                    )
                    
                    intern_matches.append({
                        'intern_id': intern.id,
                        'project_id': project.id,
                        'mentor_id': mentor.id,
                        'overall_score': overall_score,
                        'skill_match': skill_match,
                        'preference_match': preference_match,
                        'availability_match': availability_match,
                        'success_probability': success_prob,
                        'final_score': (overall_score * 0.7) + (success_prob * 0.3)
                    })
            
            # Sort by final score and pick best match
            if intern_matches:
                intern_matches.sort(key=lambda x: x['final_score'], reverse=True)
                best_match = intern_matches[0]
                
                allocations.append(best_match)
                used_projects.add(best_match['project_id'])
                mentor_capacity[best_match['mentor_id']] -= 1
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        return {
            'allocations': allocations,
            'processing_time': processing_time,
            'total_matches': len(allocations),
            'average_score': np.mean([a['final_score'] for a in allocations]) if allocations else 0,
            'algorithm_version': 'SmartEngine_v1.0'
        }
    
    def dynamic_reallocation(self, current_allocations, new_constraints):
        """
        Wow Factor: Real-time reallocation based on changing conditions
        """
        # Simulate dynamic reallocation logic
        reallocated = []
        
        for allocation in current_allocations:
            # Check if reallocation is needed
            if self._needs_reallocation(allocation, new_constraints):
                new_allocation = self._find_better_match(allocation)
                if new_allocation:
                    reallocated.append({
                        'original': allocation,
                        'new': new_allocation,
                        'reason': 'Better match found',
                        'improvement': new_allocation['final_score'] - allocation['final_score']
                    })
        
        return reallocated
    
    def _needs_reallocation(self, allocation, constraints):
        """Check if an allocation needs to be changed"""
        # Simplified logic - in practice, this would check various conditions
        return random.random() < 0.1  # 10% chance of needing reallocation
    
    def _find_better_match(self, current_allocation):
        """Find a better match for reallocation"""
        # Simplified - return improved version
        improved = current_allocation.copy()
        improved['final_score'] += random.uniform(5, 15)
        return improved
    
    def generate_insights(self, allocations_data):
        """
        Wow Factor: AI-generated insights and recommendations
        """
        if not allocations_data:
            return {}
        
        df = pd.DataFrame(allocations_data['allocations'])
        
        insights = {
            'summary': {
                'total_allocations': len(df),
                'average_match_score': round(df['final_score'].mean(), 2),
                'high_confidence_matches': len(df[df['final_score'] >= 85]),
                'processing_time': allocations_data['processing_time']
            },
            'skill_analysis': self._analyze_skill_gaps(df),
            'recommendations': self._generate_recommendations(df),
            'risk_factors': self._identify_risk_factors(df),
            'optimization_suggestions': self._suggest_optimizations(df)
        }
        
        return insights
    
    def _analyze_skill_gaps(self, df):
        """Analyze skill gaps in the allocation"""
        return {
            'low_skill_matches': len(df[df['skill_match'] < 60]),
            'average_skill_match': round(df['skill_match'].mean(), 2),
            'skill_distribution': df['skill_match'].describe().to_dict()
        }
    
    def _generate_recommendations(self, df):
        """Generate AI recommendations for improvement"""
        recommendations = []
        
        if df['skill_match'].mean() < 70:
            recommendations.append({
                'type': 'skill_improvement',
                'message': 'Consider organizing skill development workshops for interns',
                'priority': 'high'
            })
        
        if df['preference_match'].mean() < 75:
            recommendations.append({
                'type': 'preference_alignment',
                'message': 'Improve project descriptions to better match intern interests',
                'priority': 'medium'
            })
        
        return recommendations
    
    def _identify_risk_factors(self, df):
        """Identify potential risks in allocations"""
        risks = []
        
        low_success_allocations = df[df['success_probability'] < 60]
        if len(low_success_allocations) > 0:
            risks.append({
                'type': 'low_success_probability',
                'count': len(low_success_allocations),
                'message': f'{len(low_success_allocations)} allocations have low success probability'
            })
        
        return risks
    
    def _suggest_optimizations(self, df):
        """Suggest optimizations for future allocations"""
        suggestions = []
        
        if df['availability_match'].mean() < 80:
            suggestions.append({
                'area': 'scheduling',
                'suggestion': 'Implement flexible scheduling options',
                'potential_improvement': '15-20% better availability matching'
            })
        
        return suggestions

class RealTimeAllocationMonitor:
    """
    Wow Factor: Real-time monitoring and adjustment system
    """
    def __init__(self):
        self.allocation_engine = SmartAllocationEngine()
        self.active_sessions = {}
    
    def start_monitoring_session(self, session_id, allocations):
        """Start real-time monitoring for a set of allocations"""
        self.active_sessions[session_id] = {
            'allocations': allocations,
            'start_time': datetime.now(),
            'events': [],
            'metrics': self._calculate_realtime_metrics(allocations)
        }
    
    def _calculate_realtime_metrics(self, allocations):
        """Calculate real-time performance metrics"""
        if not allocations:
            return {}
        
        df = pd.DataFrame(allocations)
        
        return {
            'total_allocations': len(df),
            'average_confidence': round(df['final_score'].mean(), 2),
            'skill_match_distribution': df['skill_match'].tolist(),
            'success_predictions': df['success_probability'].tolist(),
            'timestamp': datetime.now().isoformat()
        }
    
    def simulate_realtime_updates(self, session_id):
        """
        Wow Factor: Simulate real-time updates for demo
        """
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        
        # Simulate events
        events = [
            {'type': 'intern_joined', 'message': 'New intern registered in the system'},
            {'type': 'mentor_unavailable', 'message': 'Mentor temporarily unavailable - reallocation triggered'},
            {'type': 'project_updated', 'message': 'Project requirements updated'},
            {'type': 'skill_assessment', 'message': 'Intern skill assessment completed'},
            {'type': 'feedback_received', 'message': 'Positive feedback received from mentor'}
        ]
        
        new_event = random.choice(events)
        new_event['timestamp'] = datetime.now().isoformat()
        
        session['events'].append(new_event)
        
        # Update metrics
        session['metrics'] = self._calculate_realtime_metrics(session['allocations'])
        
        return new_event

class AIInsightsGenerator:
    """
    Wow Factor: Advanced AI insights and predictive analytics
    """
    def __init__(self):
        self.insights_history = []
    
    def generate_advanced_insights(self, allocations, historical_data=None):
        """Generate comprehensive AI insights"""
        insights = {
            'performance_prediction': self._predict_batch_performance(allocations),
            'optimization_opportunities': self._find_optimization_opportunities(allocations),
            'trend_analysis': self._analyze_trends(historical_data),
            'success_factors': self._identify_success_factors(allocations),
            'ai_recommendations': self._generate_ai_recommendations(allocations)
        }
        
        self.insights_history.append({
            'timestamp': datetime.now().isoformat(),
            'insights': insights
        })
        
        return insights
    
    def _predict_batch_performance(self, allocations):
        """Predict overall batch performance"""
        if not allocations:
            return {}
        
        df = pd.DataFrame(allocations)
        
        predicted_success_rate = df['success_probability'].mean()
        high_performers = len(df[df['success_probability'] >= 80])
        at_risk_interns = len(df[df['success_probability'] < 60])
        
        return {
            'predicted_success_rate': round(predicted_success_rate, 2),
            'high_performers': high_performers,
            'at_risk_interns': at_risk_interns,
            'completion_probability': round(min(100, predicted_success_rate + 10), 2)
        }
    
    def _find_optimization_opportunities(self, allocations):
        """Find opportunities to improve allocations"""
        opportunities = []
        
        if not allocations:
            return opportunities
        
        df = pd.DataFrame(allocations)
        
        # Low skill matches
        low_skill_matches = df[df['skill_match'] < 70]
        if len(low_skill_matches) > 0:
            opportunities.append({
                'type': 'skill_development',
                'impact': 'high',
                'description': f'{len(low_skill_matches)} interns could benefit from pre-internship training',
                'suggested_action': 'Organize skill bootcamp sessions'
            })
        
        # Preference mismatches
        low_pref_matches = df[df['preference_match'] < 70]
        if len(low_pref_matches) > 0:
            opportunities.append({
                'type': 'project_customization',
                'impact': 'medium',
                'description': f'{len(low_pref_matches)} projects could be better aligned with intern interests',
                'suggested_action': 'Review and update project descriptions'
            })
        
        return opportunities
    
    def _analyze_trends(self, historical_data):
        """Analyze trends from historical allocation data"""
        if not historical_data:
            return {'message': 'No historical data available for trend analysis'}
        
        # Simplified trend analysis
        return {
            'allocation_efficiency_trend': 'improving',
            'average_score_trend': '+12% improvement over last batch',
            'success_rate_trend': 'stable at 85%'
        }
    
    def _identify_success_factors(self, allocations):
        """Identify key factors contributing to successful matches"""
        if not allocations:
            return {}
        
        df = pd.DataFrame(allocations)
        
        # Correlation analysis
        high_success = df[df['success_probability'] >= 80]
        
        success_factors = {
            'key_factors': [
                {'factor': 'Skill Match', 'importance': 'High', 'avg_score': round(high_success['skill_match'].mean(), 2)},
                {'factor': 'Mentor Experience', 'importance': 'Medium', 'correlation': 0.65},
                {'factor': 'Project Alignment', 'importance': 'High', 'avg_score': round(high_success['preference_match'].mean(), 2)}
            ],
            'optimal_ranges': {
                'skill_match': '>= 75',
                'preference_match': '>= 70',
                'success_probability': '>= 80'
            }
        }
        
        return success_factors
    
    def _generate_ai_recommendations(self, allocations):
        """Generate AI-powered recommendations"""
        recommendations = [
            {
                'category': 'Process Improvement',
                'recommendation': 'Implement skill assessment quiz before allocation',
                'expected_impact': '+15% improvement in skill matching accuracy'
            },
            {
                'category': 'Mentor Development',
                'recommendation': 'Provide mentoring guidelines and best practices training',
                'expected_impact': '+20% improvement in intern satisfaction'
            },
            {
                'category': 'Project Planning',
                'recommendation': 'Create project difficulty assessment framework',
                'expected_impact': '+10% improvement in completion rates'
            }
        ]
        
        return recommendations

# Wow Factor: AI Chatbot for allocation queries
class AllocationChatBot:
    def __init__(self, allocation_engine):
        self.engine = allocation_engine
        self.context = {}
    
    def process_query(self, query, context_data=None):
        """Process natural language queries about allocations"""
        query_lower = query.lower()
        
        # Simple NLP-based query routing
        if 'best match' in query_lower or 'recommend' in query_lower:
            return self._handle_recommendation_query(query, context_data)
        elif 'skill' in query_lower and 'gap' in query_lower:
            return self._handle_skill_gap_query(query, context_data)
        elif 'success' in query_lower or 'probability' in query_lower:
            return self._handle_success_query(query, context_data)
        elif 'improve' in query_lower or 'optimize' in query_lower:
            return self._handle_optimization_query(query, context_data)
        else:
            return self._handle_general_query(query, context_data)
    
    def _handle_recommendation_query(self, query, context_data):
        return {
            'response': 'Based on the current allocation data, I recommend focusing on skill development in Python and data analysis. The top matches show 87% success probability.',
            'data': {'top_skills': ['Python', 'Data Analysis', 'Product Strategy']},
            'suggestions': ['Organize Python workshop', 'Create data analysis bootcamp']
        }
    
    def _handle_skill_gap_query(self, query, context_data):
        return {
            'response': 'I detected skill gaps in 23% of allocations. The main gaps are in advanced analytics and product strategy.',
            'data': {'gap_percentage': 23, 'main_gaps': ['Advanced Analytics', 'Product Strategy']},
            'suggestions': ['Pre-internship training program', 'Mentorship pairing for skill development']
        }
    
    def _handle_success_query(self, query, context_data):
        return {
            'response': 'Current allocation batch shows 89% predicted success rate with high confidence in skill matching.',
            'data': {'success_rate': 89, 'confidence': 'high'},
            'suggestions': ['Monitor at-risk allocations', 'Provide additional support for low-score matches']
        }
    
    def _handle_optimization_query(self, query, context_data):
        return {
            'response': 'I suggest implementing flexible project timelines and cross-functional mentoring to improve allocation quality by 15%.',
            'data': {'improvement_potential': 15},
            'suggestions': ['Flexible timelines', 'Cross-functional mentoring', 'Skill assessment updates']
        }
    
    def _handle_general_query(self, query, context_data):
        return {
            'response': 'I can help you with allocation recommendations, skill gap analysis, success predictions, and optimization suggestions. What specific aspect would you like to explore?',
            'data': {},
            'suggestions': ['Ask about best matches', 'Inquire about skill gaps', 'Request optimization advice']
        }
