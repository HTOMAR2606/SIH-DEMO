#!/usr/bin/env python3
"""
Simple Flask API to serve the recommendation system
Connects the original ML model with the new frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Global variables for loaded model
tfidf_vectorizer = None
internship_matrix = None
candidates_df = None
internship_df = None

def load_model_and_data():
    """Load the ML model and data files"""
    global tfidf_vectorizer, internship_matrix, candidates_df, internship_df
    
    try:
        # Load the pickled model artifacts
        if os.path.exists('tfidf_vectorizer.pkl'):
            with open('tfidf_vectorizer.pkl', 'rb') as f:
                tfidf_vectorizer = pickle.load(f)
        
        if os.path.exists('internship_tfidf_matrix.pkl'):
            with open('internship_tfidf_matrix.pkl', 'rb') as f:
                internship_matrix = pickle.load(f)
        
        # Load CSV files
        if os.path.exists('candidates.csv'):
            candidates_df = pd.read_csv('candidates.csv')
        
        if os.path.exists('internship.csv'):
            internship_df = pd.read_csv('internship.csv')
            
        print("✅ Model and data loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error loading model/data: {e}")
        return False

# Original preprocessing function
def preprocess_text(text):
    """Preprocess text for ML model"""
    if not isinstance(text, str):
        return ""
    
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', '', text, re.I | re.A)
    text = text.lower()
    tokens = text.split()
    

    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    filtered_tokens = [word for word in tokens if word not in stopwords]
    
    return " ".join(filtered_tokens)

def recommendation_internship(candidate_id, n=10):

    global tfidf_vectorizer, internship_matrix, candidates_df, internship_df
    
    if candidates_df is None or internship_df is None:
        raise Exception("Data not loaded")
    
    # Find candidate
    candidate_rows = candidates_df[candidates_df['candidate_id'] == candidate_id]
    if candidate_rows.empty:
        raise Exception(f"Candidate ID {candidate_id} not found")
    
    candidate_index = candidate_rows.index[0]
    
    if tfidf_vectorizer is not None and internship_matrix is not None:

        candidate_resume = candidates_df.iloc[candidate_index]['resume']
        processed_resume = preprocess_text(candidate_resume)
        
    
        candidate_vector = tfidf_vectorizer.transform([processed_resume])
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(candidate_vector, internship_matrix).flatten()
        
        # Get top N recommendations
        top_indices = np.argsort(similarity_scores)[-n:][::-1]
        
        # Get internship details
        top_internships = internship_df.iloc[top_indices]
        
        recommendations = []
        for idx, (_, internship) in enumerate(top_internships.iterrows()):
            recommendations.append({
                'Company_name': internship.get('Company_name', 'Unknown Company'),
                'job_title': internship.get('job_title', 'Unknown Position'),
                'matchscore': float(similarity_scores[top_indices[idx]]),
                'job_description': internship.get('job_description', 'No description available')
            })
        
        return recommendations
    
    else:
        # Fallback: Simple keyword-based matching
        candidate_resume = candidates_df.iloc[candidate_index]['resume'].lower()
        
        # Simple keyword matching
        recommendations = []
        for _, internship in internship_df.iterrows():
            job_desc = str(internship.get('job_description', '')).lower()
            title = str(internship.get('job_title', '')).lower()
            
            # Simple scoring based on common words
            common_words = set(candidate_resume.split()) & set((job_desc + ' ' + title).split())
            score = len(common_words) / max(len(candidate_resume.split()), 1)
            
            recommendations.append({
                'Company_name': internship.get('Company_name', 'Unknown Company'),
                'job_title': internship.get('job_title', 'Unknown Position'),
                'matchscore': min(score, 1.0),  # Cap at 1.0
                'job_description': internship.get('job_description', 'No description available')
            })
        
        # Sort by score and return top N
        recommendations.sort(key=lambda x: x['matchscore'], reverse=True)
        return recommendations[:n]

# API Routes

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': tfidf_vectorizer is not None,
        'data_loaded': candidates_df is not None and internship_df is not None
    })

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    """Get recommendations for a candidate"""
    try:
        data = request.json
        candidate_id = int(data.get('candidate_id'))
        n = int(data.get('n', 10))
        
        recommendations = recommendation_internship(candidate_id, n)
        
        return jsonify({
            'success': True,
            'candidate_id': candidate_id,
            'recommendations': recommendations,
            'total_found': len(recommendations)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/apply', methods=['POST'])
def apply_to_internship():
    """Simulate application submission"""
    try:
        data = request.json
        candidate_id = data.get('candidate_id')
        company_name = data.get('company_name')
        job_title = data.get('job_title')
        
        # Simulate successful application
        application_id = f"APP_{candidate_id}_{hash(company_name + job_title) % 10000}"
        
        return jsonify({
            'success': True,
            'application_id': application_id,
            'message': f'Application submitted successfully to {company_name}',
            'status': 'pending'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/applications', methods=['GET'])
def get_applications():
    """Get applications for a candidate"""
    try:
        candidate_id = request.args.get('candidate_id')
        
        # Return mock applications data
        mock_applications = [
            {
                'application_id': f'APP_{candidate_id}_1001',
                'company_name': 'Tech Solutions India',
                'job_title': 'Software Development Intern',
                'status': 'pending',
                'applied_date': '2024-12-20',
                'match_score': 0.89
            }
        ]
        
        return jsonify({
            'success': True,
            'applications': mock_applications
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/allotment', methods=['GET'])
def get_allotment():
    """Get allotment status for a candidate"""
    try:
        candidate_id = request.args.get('candidate_id')
        
        # Simulate allotment data (random chance)
        import random
        
        if random.random() > 0.5:  # 50% chance of having allotment
            allotment = {
                'candidate_id': candidate_id,
                'company_name': 'Tech Solutions India',
                'job_title': 'Software Development Intern',
                'status': 'allocated',
                'start_date': '2025-01-15',
                'mentor_name': 'Dr. Rajesh Kumar',
                'location': 'Bengaluru, Karnataka'
            }
            
            return jsonify({
                'success': True,
                'allotment': allotment
            })
        else:
            return jsonify({
                'success': True,
                'allotment': None,
                'message': 'No allotment available yet'
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/allocate', methods=['POST'])
def run_allocation():
    """Admin endpoint to run allocation algorithm"""
    try:
        # Simulate allocation process
        result = {
            'success': True,
            'message': 'Allocation completed successfully',
            'total_allocations': 15,
            'processing_time': 2.3,
            'summary': {
                'candidates_processed': 50,
                'internships_available': 25,
                'successful_matches': 15,
                'average_match_score': 0.82
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/candidates', methods=['GET'])
def get_all_candidates():
    """Get all candidates (admin endpoint)"""
    try:
        if candidates_df is not None:
            candidates_list = candidates_df.to_dict('records')
            return jsonify({
                'success': True,
                'candidates': candidates_list,
                'total': len(candidates_list)
            })
        else:
            # Return mock data
            mock_candidates = [
                {
                    'candidate_id': 122,
                    'name': 'Arjun Kumar',
                    'email': 'arjun@example.com',
                    'college': 'IIT Delhi',
                    'skills': 'Python, Machine Learning',
                    'status': 'active'
                }
            ]
            
            return jsonify({
                'success': True,
                'candidates': mock_candidates,
                'total': len(mock_candidates)
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting PM Internship Recommendation API...")
    
    # Load model and data
    if load_model_and_data():
        print("📊 Model and data ready")
    else:
        print("⚠️  Running with mock data only")
    
    # Get local IP address
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("\n🌐 PM Internship Allocation API Server")
    print("="*50)
    print(f"🏠 Local access:     http://localhost:5000")
    print(f"📱 Network access:   http://{local_ip}:5000")
    print(f"📱 Mobile/Tablet:    http://192.168.0.119:5000")
    print("\n📋 Available endpoints:")
    print("  GET  /health         - Health check")
    print("  POST /recommend      - Get recommendations")
    print("  POST /apply          - Submit application")
    print("  GET  /applications   - Get candidate applications")
    print("  GET  /allotment      - Get allotment status")
    print("  POST /allocate       - Run allocation (admin)")
    print("  GET  /candidates     - Get all candidates (admin)")
    print("\n📱 Frontend URL: http://192.168.0.119:8080")
    print("🔥 Ready for connections!")
    print("="*50)
    
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
