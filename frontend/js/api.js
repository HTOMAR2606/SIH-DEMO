// API Service Layer for PM Internship Allocation Engine
// Handles all backend communication with proper error handling

class APIService {
    constructor() {
        // Use network IP for cross-device access
        this.baseURL = 'http://192.168.0.119:5000/api';
        this.headers = {
            'Content-Type': 'application/json',
        };
    }

    // Generic API request handler
    async makeRequest(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: this.headers,
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Request failed:', error);
            throw error;
        }
    }

    // Health check
    async healthCheck() {
        return await this.makeRequest('/health');
    }

    // Intern/Candidate APIs
    async getAllInterns() {
        return await this.makeRequest('/interns');
    }

    async getInternById(id) {
        return await this.makeRequest(`/interns/${id}`);
    }

    async createIntern(internData) {
        return await this.makeRequest('/interns', {
            method: 'POST',
            body: JSON.stringify(internData)
        });
    }

    async updateIntern(id, internData) {
        return await this.makeRequest(`/interns/${id}`, {
            method: 'PUT',
            body: JSON.stringify(internData)
        });
    }

    // Project APIs
    async getAllProjects() {
        return await this.makeRequest('/projects');
    }

    async createProject(projectData) {
        return await this.makeRequest('/projects', {
            method: 'POST',
            body: JSON.stringify(projectData)
        });
    }

    // Mentor APIs
    async getAllMentors() {
        return await this.makeRequest('/mentors');
    }

    async createMentor(mentorData) {
        return await this.makeRequest('/mentors', {
            method: 'POST',
            body: JSON.stringify(mentorData)
        });
    }

    // Allocation APIs
    async generateAllocations() {
        return await this.makeRequest('/allocations/generate', {
            method: 'POST'
        });
    }

    async getAllocations() {
        return await this.makeRequest('/allocations');
    }

    async submitFeedback(allocationId, feedbackData) {
        return await this.makeRequest(`/allocations/${allocationId}/feedback`, {
            method: 'POST',
            body: JSON.stringify(feedbackData)
        });
    }

    // Analytics APIs
    async getDashboardAnalytics() {
        return await this.makeRequest('/analytics/dashboard');
    }

    // PM Yojana Compliance APIs
    async getYojanaCompliance(internId) {
        return await this.makeRequest(`/yojana/compliance/${internId}`);
    }

    async updateYojanaCompliance(internId, complianceData) {
        return await this.makeRequest(`/yojana/compliance/${internId}`, {
            method: 'PUT',
            body: JSON.stringify(complianceData)
        });
    }

    async getYojanaBatchReport() {
        return await this.makeRequest('/yojana/batch-report');
    }

    // AI Features APIs
    async getAIInsights(data) {
        return await this.makeRequest('/ai/insights', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async chatWithAI(query, context) {
        return await this.makeRequest('/ai/chatbot', {
            method: 'POST',
            body: JSON.stringify({ query, context })
        });
    }

    async getRealTimeUpdates(sessionId) {
        return await this.makeRequest(`/realtime/monitor/${sessionId}`);
    }
}

// Custom API methods for the original recommendation system
class RecommendationAPI extends APIService {
    constructor() {
        super();
        // For the original recommendation system that uses candidate.csv and internship.csv
        this.originalBaseURL = 'http://192.168.0.119:5000';
    }

    // Get recommendations for a candidate using the original ML model
    async getRecommendations(candidateId, numberOfRecommendations = 10) {
        try {
            const response = await fetch(`${this.originalBaseURL}/recommend`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    candidate_id: candidateId,
                    n: numberOfRecommendations
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Recommendation API failed:', error);
            throw error;
        }
    }

    // Submit application (simulate applying to internship)
    async submitApplication(candidateId, internshipId, applicationData = {}) {
        try {
            const response = await fetch(`${this.originalBaseURL}/apply`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    candidate_id: candidateId,
                    internship_id: internshipId,
                    ...applicationData
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Application submission failed:', error);
            throw error;
        }
    }

    // Get candidate applications
    async getCandidateApplications(candidateId) {
        try {
            const response = await fetch(`${this.originalBaseURL}/applications?candidate_id=${candidateId}`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Getting applications failed:', error);
            throw error;
        }
    }

    // Get candidate allotment status
    async getAllotmentStatus(candidateId) {
        try {
            const response = await fetch(`${this.originalBaseURL}/allotment?candidate_id=${candidateId}`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Getting allotment status failed:', error);
            throw error;
        }
    }

    // Admin: Run allocation algorithm
    async runAllocation() {
        try {
            const response = await fetch(`${this.originalBaseURL}/allocate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Running allocation failed:', error);
            throw error;
        }
    }
}

// Global API instances
const api = new APIService();
const recommendationAPI = new RecommendationAPI();

// Utility functions for API responses
const APIUtils = {
    // Handle API errors with user-friendly messages
    handleError(error) {
        let message = 'An unexpected error occurred. Please try again.';
        
        if (error.message.includes('404')) {
            message = 'Candidate ID not found. Please check and try again.';
        } else if (error.message.includes('500')) {
            message = 'Server error. Please contact support if the issue persists.';
        } else if (error.message.includes('Failed to fetch')) {
            message = 'Unable to connect to server. Please check your internet connection.';
        }
        
        return message;
    },

    // Format match score for display
    formatMatchScore(score) {
        return Math.round(score * 100);
    },

    // Create progress bar HTML for match scores
    createProgressBar(score) {
        const percentage = Math.round(score * 100);
        return `
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${percentage}%"></div>
            </div>
            <span>${percentage}%</span>
        `;
    },

    // Format date for display
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    // Validate candidate ID format
    isValidCandidateId(candidateId) {
        // Simple validation - should be numeric and reasonable length
        return /^\d{3,10}$/.test(candidateId.toString());
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { APIService, RecommendationAPI, APIUtils, api, recommendationAPI };
}
