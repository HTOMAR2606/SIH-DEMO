// Candidate Dashboard Functionality
// Handles recommendations, applications, and allotment tracking

class CandidateManager {
    constructor() {
        this.currentRecommendations = [];
        this.currentApplications = [];
        this.allotmentStatus = null;
    }

    // Initialize candidate dashboard
    async initDashboard() {
        if (!requireAuth('candidate')) return;

        const user = authManager.getCurrentUser();
        
        // Update welcome message
        document.getElementById('welcomeMessage').textContent = `Welcome, ${user.name}!`;
        document.getElementById('candidateIdInput').value = user.id;

        // Load existing data if available
        await this.loadApplications();
        await this.loadAllotmentStatus();
    }

    // Get recommendations for candidate
    async getRecommendations(candidateId, numberOfRecommendations = 10) {
        if (!requireAuth('candidate')) return;

        if (!candidateId || !APIUtils.isValidCandidateId(candidateId)) {
            showToast('Please enter a valid candidate ID', 'error');
            return;
        }

        showLoading('Getting your personalized recommendations...');

        try {
            // First try the new backend API
            try {
                const recommendations = await this.getRecommendationsFromNewAPI(candidateId, numberOfRecommendations);
                this.displayRecommendations(recommendations);
                hideLoading();
                return;
            } catch (newAPIError) {
                console.log('New API not available, trying original recommendation system...');
            }

            // Fallback to original recommendation system
            const result = await this.getRecommendationsFromOriginalAPI(candidateId, numberOfRecommendations);
            this.displayRecommendations(result);
            
            hideLoading();
            showToast(`Found ${result.length} recommendations for you!`, 'success');

        } catch (error) {
            hideLoading();
            console.error('Recommendation error:', error);
            showToast(APIUtils.handleError(error), 'error');
        }
    }

    // Get recommendations from new backend API
    async getRecommendationsFromNewAPI(candidateId, n) {
        // This would connect to your Flask backend
        const intern = await api.getInternById(candidateId);
        const projects = await api.getAllProjects();
        
        // Simple matching algorithm as fallback
        const recommendations = projects.slice(0, n).map((project, index) => ({
            Company_name: project.organization || 'Unknown Company',
            job_title: project.title,
            matchscore: Math.random() * 0.3 + 0.7, // Random score between 0.7-1.0
            job_description: project.description || 'No description available',
            project_id: project.id
        }));

        return recommendations;
    }

    // Get recommendations from original ML model
    async getRecommendationsFromOriginalAPI(candidateId, n) {
        // Create mock data based on the original backend structure
        // In real implementation, this would call your original recommendation endpoint
        const mockRecommendations = [
            {
                Company_name: "Tech Solutions India",
                job_title: "Software Development Intern",
                matchscore: 0.89,
                job_description: "Full-stack web development using React, Node.js, and MongoDB. Work on real client projects and gain hands-on experience."
            },
            {
                Company_name: "Digital Innovation Labs",
                job_title: "Machine Learning Intern",
                matchscore: 0.85,
                job_description: "Work on AI/ML projects using Python, TensorFlow, and data analysis. Contribute to cutting-edge research."
            },
            {
                Company_name: "Green Energy Corp",
                job_title: "Data Analytics Intern",
                matchscore: 0.82,
                job_description: "Analyze energy consumption data and create insights using Python, SQL, and visualization tools."
            },
            {
                Company_name: "FinTech Solutions",
                job_title: "Backend Developer Intern",
                matchscore: 0.78,
                job_description: "Develop APIs and microservices using Java Spring Boot. Work on financial technology solutions."
            },
            {
                Company_name: "Healthcare Analytics",
                job_title: "Data Science Intern",
                matchscore: 0.75,
                job_description: "Apply machine learning to healthcare data. Work with medical datasets and predictive modeling."
            },
            {
                Company_name: "E-commerce Platform",
                job_title: "Frontend Developer Intern",
                matchscore: 0.72,
                job_description: "Build responsive web applications using React, CSS, and modern frontend technologies."
            },
            {
                Company_name: "Cloud Services Inc",
                job_title: "DevOps Intern",
                matchscore: 0.68,
                job_description: "Learn cloud infrastructure, Docker, Kubernetes, and CI/CD pipelines on AWS platform."
            },
            {
                Company_name: "Mobile App Studio",
                job_title: "Mobile Developer Intern",
                matchscore: 0.65,
                job_description: "Develop mobile applications for iOS and Android using React Native and Flutter."
            }
        ];

        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1000));

        return mockRecommendations.slice(0, n);
    }

    // Display recommendations in the table
    displayRecommendations(recommendations) {
        this.currentRecommendations = recommendations;
        
        const recommendationsCard = document.getElementById('recommendationsCard');
        const tableBody = document.querySelector('#recommendationsTable tbody');
        
        if (recommendations.length === 0) {
            recommendationsCard.style.display = 'none';
            showToast('No recommendations found for this candidate ID', 'warning');
            return;
        }

        // Clear existing rows
        tableBody.innerHTML = '';

        // Add new rows
        recommendations.forEach((rec, index) => {
            const row = document.createElement('tr');
            
            const matchScore = APIUtils.formatMatchScore(rec.matchscore);
            const progressBar = APIUtils.createProgressBar(rec.matchscore);
            
            row.innerHTML = `
                <td><strong>${rec.Company_name}</strong></td>
                <td>${rec.job_title}</td>
                <td>
                    <div class="match-score-cell">
                        ${progressBar}
                    </div>
                </td>
                <td>
                    <div class="description-cell">
                        ${rec.job_description.length > 100 ? 
                          rec.job_description.substring(0, 100) + '...' : 
                          rec.job_description}
                    </div>
                </td>
                <td>
                    <button class="btn-primary" onclick="candidateManager.applyToInternship(${index})">
                        <i class="fas fa-paper-plane"></i> Apply
                    </button>
                </td>
            `;
            
            tableBody.appendChild(row);
        });

        recommendationsCard.style.display = 'block';
        recommendationsCard.scrollIntoView({ behavior: 'smooth' });
    }

    // Apply to an internship
    async applyToInternship(recommendationIndex) {
        if (!requireAuth('candidate')) return;

        const recommendation = this.currentRecommendations[recommendationIndex];
        if (!recommendation) return;

        const user = authManager.getCurrentUser();

        try {
            showLoading('Submitting your application...');

            // Simulate application submission
            const applicationData = {
                candidate_id: user.id,
                company_name: recommendation.Company_name,
                job_title: recommendation.job_title,
                match_score: recommendation.matchscore,
                applied_at: new Date().toISOString(),
                status: 'pending'
            };

            // In real implementation, this would call the backend API
            await this.simulateApplicationSubmission(applicationData);

            // Add to local applications
            this.currentApplications.push(applicationData);
            this.saveApplicationsToCache();
            this.displayApplications();

            hideLoading();
            showToast(`Application submitted successfully to ${recommendation.Company_name}!`, 'success');

            // Update button state
            const buttons = document.querySelectorAll('#recommendationsTable button');
            if (buttons[recommendationIndex]) {
                buttons[recommendationIndex].innerHTML = '<i class="fas fa-check"></i> Applied';
                buttons[recommendationIndex].disabled = true;
                buttons[recommendationIndex].classList.remove('btn-primary');
                buttons[recommendationIndex].classList.add('btn-secondary');
            }

        } catch (error) {
            hideLoading();
            console.error('Application submission error:', error);
            showToast('Failed to submit application. Please try again.', 'error');
        }
    }

    // Simulate application submission (replace with real API call)
    async simulateApplicationSubmission(applicationData) {
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        return { success: true, application_id: Date.now().toString() };
    }

    // Load and display applications
    async loadApplications() {
        try {
            // Try to load from cache first
            this.loadApplicationsFromCache();
            
            // In real implementation, load from backend API
            // const applications = await recommendationAPI.getCandidateApplications(user.id);
            
            this.displayApplications();
        } catch (error) {
            console.error('Error loading applications:', error);
        }
    }

    // Display applications
    displayApplications() {
        const container = document.getElementById('applicationsContainer');
        
        if (this.currentApplications.length === 0) {
            container.innerHTML = '<p>No applications submitted yet.</p>';
            return;
        }

        let applicationsHTML = '';
        this.currentApplications.forEach((app, index) => {
            const statusClass = `status-${app.status}`;
            const appliedDate = APIUtils.formatDate(app.applied_at);
            
            applicationsHTML += `
                <div class="application-card">
                    <div class="application-header">
                        <h4>${app.job_title}</h4>
                        <span class="status-badge ${statusClass}">${app.status.toUpperCase()}</span>
                    </div>
                    <div class="application-details">
                        <p><strong>Company:</strong> ${app.company_name}</p>
                        <p><strong>Match Score:</strong> ${APIUtils.formatMatchScore(app.match_score)}%</p>
                        <p><strong>Applied On:</strong> ${appliedDate}</p>
                    </div>
                </div>
            `;
        });

        container.innerHTML = applicationsHTML;
    }

    // Load and display allotment status
    async loadAllotmentStatus() {
        if (!requireAuth('candidate')) return;

        const user = authManager.getCurrentUser();

        try {
            // In real implementation, call backend API
            // const allotment = await recommendationAPI.getAllotmentStatus(user.id);
            
            // Simulate allotment data
            this.allotmentStatus = this.getSimulatedAllotment();
            this.displayAllotmentStatus();

        } catch (error) {
            console.error('Error loading allotment status:', error);
        }
    }

    // Get simulated allotment (replace with real API call)
    getSimulatedAllotment() {
        // Simulate different allotment states
        const scenarios = [
            null, // No allotment yet
            {
                company_name: "Tech Solutions India",
                job_title: "Software Development Intern",
                status: "allocated",
                start_date: "2025-01-15",
                mentor_name: "Dr. Rajesh Kumar",
                location: "Bengaluru, Karnataka"
            },
            {
                company_name: "Digital Innovation Labs",
                job_title: "Machine Learning Intern",
                status: "confirmed",
                start_date: "2025-01-20",
                mentor_name: "Ms. Priya Sharma",
                location: "Hyderabad, Telangana"
            }
        ];

        // Return random scenario for demo
        return scenarios[Math.floor(Math.random() * scenarios.length)];
    }

    // Display allotment status
    displayAllotmentStatus() {
        const container = document.getElementById('allotmentContainer');

        if (!this.allotmentStatus) {
            container.innerHTML = `
                <div class="allotment-pending">
                    <i class="fas fa-clock"></i>
                    <p>Allotment process is in progress. You will be notified once allocations are complete.</p>
                </div>
            `;
            return;
        }

        const startDate = APIUtils.formatDate(this.allotmentStatus.start_date);
        const statusClass = this.allotmentStatus.status === 'confirmed' ? 'status-approved' : 'status-pending';

        container.innerHTML = `
            <div class="allotment-card">
                <div class="allotment-header">
                    <h4><i class="fas fa-trophy"></i> Congratulations!</h4>
                    <span class="status-badge ${statusClass}">${this.allotmentStatus.status.toUpperCase()}</span>
                </div>
                <div class="allotment-details">
                    <div class="detail-row">
                        <strong>Company:</strong> ${this.allotmentStatus.company_name}
                    </div>
                    <div class="detail-row">
                        <strong>Position:</strong> ${this.allotmentStatus.job_title}
                    </div>
                    <div class="detail-row">
                        <strong>Start Date:</strong> ${startDate}
                    </div>
                    <div class="detail-row">
                        <strong>Mentor:</strong> ${this.allotmentStatus.mentor_name}
                    </div>
                    <div class="detail-row">
                        <strong>Location:</strong> ${this.allotmentStatus.location}
                    </div>
                </div>
                <div class="allotment-actions">
                    ${this.allotmentStatus.status === 'allocated' ? 
                        '<button class="btn-primary" onclick="candidateManager.confirmAllotment()"><i class="fas fa-check"></i> Confirm Acceptance</button>' :
                        '<p class="confirmation-note"><i class="fas fa-check-circle"></i> Your acceptance has been confirmed!</p>'
                    }
                </div>
            </div>
        `;
    }

    // Confirm allotment acceptance
    async confirmAllotment() {
        if (!requireAuth('candidate')) return;

        try {
            showLoading('Confirming your acceptance...');

            // Simulate confirmation API call
            await new Promise(resolve => setTimeout(resolve, 1000));

            this.allotmentStatus.status = 'confirmed';
            this.displayAllotmentStatus();

            hideLoading();
            showToast('Allotment confirmed successfully!', 'success');

        } catch (error) {
            hideLoading();
            showToast('Failed to confirm allotment. Please try again.', 'error');
        }
    }

    // Cache management
    saveApplicationsToCache() {
        localStorage.setItem('cached_applications', JSON.stringify(this.currentApplications));
    }

    loadApplicationsFromCache() {
        try {
            const cached = localStorage.getItem('cached_applications');
            if (cached) {
                this.currentApplications = JSON.parse(cached);
            }
        } catch (error) {
            console.error('Error loading cached applications:', error);
            this.currentApplications = [];
        }
    }
}

// Global candidate manager instance
const candidateManager = new CandidateManager();

// Global functions for HTML onclick handlers
async function getRecommendations() {
    const candidateId = document.getElementById('candidateIdInput').value.trim();
    await candidateManager.getRecommendations(candidateId);
}

function setupCandidateDashboard() {
    candidateManager.initDashboard();
}

// Add some CSS for the new elements
const additionalCSS = `
.match-score-cell {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.description-cell {
    max-width: 300px;
    word-wrap: break-word;
}

.allotment-pending {
    text-align: center;
    padding: 2rem;
    color: var(--gray-700);
}

.allotment-pending i {
    font-size: 3rem;
    color: var(--orange-accent);
    margin-bottom: 1rem;
}

.allotment-card {
    border: 2px solid var(--success);
    border-radius: var(--border-radius);
    overflow: hidden;
}

.allotment-header {
    background: linear-gradient(135deg, var(--success) 0%, #66bb6a 100%);
    color: var(--white);
    padding: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.allotment-details {
    padding: 1rem;
}

.detail-row {
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--gray-200);
}

.detail-row:last-child {
    border-bottom: none;
}

.allotment-actions {
    padding: 1rem;
    background: var(--gray-50);
    text-align: center;
}

.confirmation-note {
    color: var(--success);
    font-weight: 500;
    margin: 0;
}

.confirmation-note i {
    margin-right: 0.5rem;
}
`;

// Add the additional CSS to the page
const style = document.createElement('style');
style.textContent = additionalCSS;
document.head.appendChild(style);
