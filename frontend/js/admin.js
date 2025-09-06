// Admin Dashboard Functionality
// Handles candidate management, allocation controls, and analytics

class AdminManager {
    constructor() {
        this.currentCandidates = [];
        this.currentAllocations = [];
        this.dashboardStats = {};
        this.activeTab = 'overview';
    }

    // Initialize admin dashboard
    async initDashboard() {
        if (!requireAuth('admin')) return;

        // Load initial data
        await this.loadDashboardStats();
        await this.loadCandidates();
        await this.loadAllocations();

        // Setup tab navigation
        this.setupTabNavigation();
        
        // Show overview tab by default
        this.switchTab('overview');
    }

    // Load dashboard statistics
    async loadDashboardStats() {
        try {
            showLoading('Loading dashboard statistics...');

            // Try to load from new backend API
            try {
                const stats = await api.getDashboardAnalytics();
                this.dashboardStats = stats.summary;
                this.displayDashboardStats();
                hideLoading();
                return;
            } catch (newAPIError) {
                console.log('New API not available, using mock data...');
            }

            // Fallback to mock data
            this.dashboardStats = await this.getMockDashboardStats();
            this.displayDashboardStats();
            hideLoading();

        } catch (error) {
            hideLoading();
            console.error('Error loading dashboard stats:', error);
            showToast('Failed to load dashboard statistics', 'error');
        }
    }

    // Get mock dashboard statistics
    async getMockDashboardStats() {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1000));

        return {
            total_interns: 1247,
            total_projects: 89,
            total_mentors: 156,
            total_allocations: 892,
            success_rate: 94.2,
            average_rating: 4.3
        };
    }

    // Display dashboard statistics
    displayDashboardStats() {
        document.getElementById('totalInterns').textContent = this.dashboardStats.total_interns || 0;
        document.getElementById('totalProjects').textContent = this.dashboardStats.total_projects || 0;
        document.getElementById('totalMentors').textContent = this.dashboardStats.total_mentors || 0;
        document.getElementById('totalAllocations').textContent = this.dashboardStats.total_allocations || 0;
    }

    // Load candidates data
    async loadCandidates() {
        try {
            // Try new backend API
            try {
                this.currentCandidates = await api.getAllInterns();
                this.displayCandidates();
                return;
            } catch (newAPIError) {
                console.log('New API not available, using mock data...');
            }

            // Fallback to mock data
            this.currentCandidates = await this.getMockCandidates();
            this.displayCandidates();

        } catch (error) {
            console.error('Error loading candidates:', error);
        }
    }

    // Get mock candidates data
    async getMockCandidates() {
        return [
            {
                id: 122,
                name: "Arjun Kumar",
                email: "arjun.kumar@email.com",
                college: "IIT Delhi",
                branch: "Computer Science",
                skills: { "Python": 85, "React": 75, "Machine Learning": 80 },
                category: "General",
                state: "Delhi",
                status: "active"
            },
            {
                id: 123,
                name: "Priya Sharma",
                email: "priya.sharma@email.com",
                college: "NIT Bangalore",
                branch: "Information Technology",
                skills: { "Java": 90, "Spring Boot": 80, "Database": 85 },
                category: "General",
                state: "Karnataka",
                status: "active"
            },
            {
                id: 124,
                name: "Rajesh Patel",
                email: "rajesh.patel@email.com",
                college: "BITS Pilani",
                branch: "Electronics",
                skills: { "IoT": 80, "Embedded Systems": 85, "Python": 70 },
                category: "OBC",
                state: "Rajasthan",
                status: "allocated"
            },
            {
                id: 125,
                name: "Sneha Reddy",
                email: "sneha.reddy@email.com",
                college: "IIIT Hyderabad",
                branch: "Computer Science",
                skills: { "Data Science": 90, "Machine Learning": 85, "Python": 90 },
                category: "General",
                state: "Telangana",
                status: "active"
            },
            {
                id: 126,
                name: "Mohammed Ali",
                email: "mohammed.ali@email.com",
                college: "Jamia Millia Islamia",
                branch: "Software Engineering",
                skills: { "JavaScript": 85, "Node.js": 80, "MongoDB": 75 },
                category: "Minority",
                state: "Delhi",
                status: "active"
            }
        ];
    }

    // Display candidates in table
    displayCandidates() {
        const tableBody = document.querySelector('#candidatesTable tbody');
        
        if (this.currentCandidates.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="6">No candidates found</td></tr>';
            return;
        }

        tableBody.innerHTML = '';

        this.currentCandidates.forEach(candidate => {
            const row = document.createElement('tr');
            
            const skills = candidate.skills || {};
            const skillsList = Object.keys(skills).slice(0, 3).join(', ');
            const statusClass = `status-${candidate.status || 'active'}`;
            
            row.innerHTML = `
                <td><strong>${candidate.id}</strong></td>
                <td>${candidate.name}</td>
                <td>${candidate.email}</td>
                <td>${candidate.college}</td>
                <td>
                    <div class="skills-cell">
                        ${skillsList}
                        ${Object.keys(skills).length > 3 ? '...' : ''}
                    </div>
                </td>
                <td>
                    <span class="status-badge ${statusClass}">
                        ${(candidate.status || 'active').toUpperCase()}
                    </span>
                </td>
            `;
            
            tableBody.appendChild(row);
        });
    }

    // Load allocations data
    async loadAllocations() {
        try {
            // Try new backend API
            try {
                this.currentAllocations = await api.getAllocations();
                this.displayAllocations();
                return;
            } catch (newAPIError) {
                console.log('New API not available, using mock data...');
            }

            // Fallback to mock data
            this.currentAllocations = await this.getMockAllocations();
            this.displayAllocations();

        } catch (error) {
            console.error('Error loading allocations:', error);
        }
    }

    // Get mock allocations data
    async getMockAllocations() {
        return [
            {
                id: 1,
                intern: { name: "Arjun Kumar", id: 122 },
                project: { title: "AI-Powered Healthcare Analytics", organization: "HealthTech Solutions" },
                mentor: { name: "Dr. Meera Singh", designation: "Senior Data Scientist" },
                match_score: 0.92,
                status: "active",
                start_date: "2025-01-15"
            },
            {
                id: 2,
                intern: { name: "Priya Sharma", id: 123 },
                project: { title: "E-commerce Backend Development", organization: "ShopEasy India" },
                mentor: { name: "Mr. Vikram Joshi", designation: "Lead Backend Developer" },
                match_score: 0.88,
                status: "pending",
                start_date: "2025-01-20"
            },
            {
                id: 3,
                intern: { name: "Rajesh Patel", id: 124 },
                project: { title: "IoT-based Smart Agriculture", organization: "AgriTech Solutions" },
                mentor: { name: "Dr. Sunita Gupta", designation: "IoT Specialist" },
                match_score: 0.85,
                status: "completed",
                start_date: "2024-12-01"
            }
        ];
    }

    // Display allocations in table
    displayAllocations() {
        const tableBody = document.querySelector('#allocationsTable tbody');
        
        if (this.currentAllocations.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="6">No allocations found</td></tr>';
            return;
        }

        tableBody.innerHTML = '';

        this.currentAllocations.forEach(allocation => {
            const row = document.createElement('tr');
            
            const matchScore = APIUtils.formatMatchScore(allocation.match_score);
            const statusClass = `status-${allocation.status}`;
            
            row.innerHTML = `
                <td>
                    <div class="intern-info">
                        <strong>${allocation.intern.name}</strong>
                        <small>ID: ${allocation.intern.id}</small>
                    </div>
                </td>
                <td>
                    <div class="project-info">
                        <strong>${allocation.project.title}</strong>
                        <small>${allocation.project.organization}</small>
                    </div>
                </td>
                <td>
                    <div class="mentor-info">
                        <strong>${allocation.mentor.name}</strong>
                        <small>${allocation.mentor.designation}</small>
                    </div>
                </td>
                <td>
                    <div class="score-cell">
                        ${APIUtils.createProgressBar(allocation.match_score)}
                    </div>
                </td>
                <td>
                    <span class="status-badge ${statusClass}">
                        ${allocation.status.toUpperCase()}
                    </span>
                </td>
                <td>
                    <div class="action-buttons">
                        <button class="btn-secondary btn-small" onclick="adminManager.viewAllocationDetails(${allocation.id})">
                            <i class="fas fa-eye"></i> View
                        </button>
                    </div>
                </td>
            `;
            
            tableBody.appendChild(row);
        });
    }

    // Run smart allocation
    async runAllocation() {
        if (!requireAuth('admin')) return;

        if (!confirm('This will generate new allocations for unassigned candidates. Continue?')) {
            return;
        }

        try {
            showLoading('Running smart allocation algorithm...');

            // Try new backend API
            try {
                const result = await api.generateAllocations();
                
                hideLoading();
                showToast(`Allocation completed! Generated ${result.summary.total_allocations} new allocations.`, 'success');
                
                // Reload data
                await this.loadDashboardStats();
                await this.loadAllocations();
                
                return;
            } catch (newAPIError) {
                console.log('New API not available, using simulated allocation...');
            }

            // Fallback to simulated allocation
            await this.simulateAllocation();
            
            hideLoading();
            showToast('Smart allocation completed successfully!', 'success');
            
            // Reload data
            await this.loadDashboardStats();
            await this.loadAllocations();

        } catch (error) {
            hideLoading();
            console.error('Allocation error:', error);
            showToast('Failed to run allocation. Please try again.', 'error');
        }
    }

    // Simulate allocation process
    async simulateAllocation() {
        // Simulate processing time
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        // Add some new mock allocations
        const newAllocations = [
            {
                id: this.currentAllocations.length + 1,
                intern: { name: "Sneha Reddy", id: 125 },
                project: { title: "Machine Learning for Finance", organization: "FinTech Analytics" },
                mentor: { name: "Mr. Ravi Kumar", designation: "ML Engineer" },
                match_score: 0.94,
                status: "pending",
                start_date: "2025-01-25"
            },
            {
                id: this.currentAllocations.length + 2,
                intern: { name: "Mohammed Ali", id: 126 },
                project: { title: "Web Development for NGO", organization: "SocialTech Foundation" },
                mentor: { name: "Ms. Anita Chopra", designation: "Full Stack Developer" },
                match_score: 0.87,
                status: "pending",
                start_date: "2025-01-28"
            }
        ];

        this.currentAllocations.push(...newAllocations);
        
        // Update stats
        this.dashboardStats.total_allocations = this.currentAllocations.length;
    }

    // Setup tab navigation
    setupTabNavigation() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        
        tabButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const tabName = btn.dataset.tab;
                this.switchTab(tabName);
            });
        });
    }

    // Switch between admin tabs
    switchTab(tabName) {
        // Update active tab button
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update active tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        
        document.getElementById(`${tabName}Tab`).classList.add('active');

        this.activeTab = tabName;

        // Update navigation bar active states
        this.updateAdminNavigation(tabName);
    }

    // Update admin navigation active states
    updateAdminNavigation(activeTab) {
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.classList.remove('active');
        });

        // Find and activate the corresponding nav link
        const tabMapping = {
            'overview': 'Overview',
            'candidates': 'Candidates',
            'allocations': 'Allocations'
        };

        navLinks.forEach(link => {
            if (link.textContent.trim().includes(tabMapping[activeTab])) {
                link.classList.add('active');
            }
        });
    }

    // View allocation details (placeholder)
    viewAllocationDetails(allocationId) {
        const allocation = this.currentAllocations.find(a => a.id === allocationId);
        if (!allocation) return;

        alert(`Allocation Details:\n\nIntern: ${allocation.intern.name}\nProject: ${allocation.project.title}\nMentor: ${allocation.mentor.name}\nMatch Score: ${APIUtils.formatMatchScore(allocation.match_score)}%\nStatus: ${allocation.status.toUpperCase()}`);
    }

    // Export data (placeholder)
    exportData(dataType) {
        showToast(`Exporting ${dataType} data...`, 'success');
        // In real implementation, this would generate and download CSV/Excel files
    }
}

// Global admin manager instance
const adminManager = new AdminManager();

// Global functions for HTML onclick handlers
async function runAllocation() {
    await adminManager.runAllocation();
}

function switchAdminTab(tabName) {
    adminManager.switchTab(tabName);
}

function loadAdminDashboard() {
    adminManager.initDashboard();
}

// Add admin-specific CSS
const adminCSS = `
.skills-cell {
    font-size: 0.9rem;
    color: var(--gray-700);
}

.intern-info strong,
.project-info strong,
.mentor-info strong {
    display: block;
    color: var(--primary-blue);
    font-size: 0.95rem;
}

.intern-info small,
.project-info small,
.mentor-info small {
    display: block;
    color: var(--gray-600);
    font-size: 0.8rem;
    margin-top: 0.2rem;
}

.score-cell {
    min-width: 120px;
}

.action-buttons {
    display: flex;
    gap: 0.5rem;
}

.btn-small {
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
}

.admin-tabs .tab-btn {
    position: relative;
}

.admin-tabs .tab-btn.active::after {
    content: '';
    position: absolute;
    bottom: -0.5rem;
    left: 50%;
    transform: translateX(-50%);
    width: 30px;
    height: 3px;
    background: var(--orange-accent);
    border-radius: 2px;
}

.export-actions {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--gray-200);
}

.export-actions button {
    margin-right: 0.5rem;
}
`;

// Add the admin CSS to the page
const adminStyle = document.createElement('style');
adminStyle.textContent = adminCSS;
document.head.appendChild(adminStyle);
