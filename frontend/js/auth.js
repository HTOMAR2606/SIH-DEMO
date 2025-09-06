// Authentication System for PM Internship Allocation Engine
// Handles login, logout, and role-based access

class AuthManager {
    constructor() {
        this.currentUser = null;
        this.currentRole = null;
        this.sessionKey = 'pm_internship_session';
        
        // Initialize auth state from localStorage
        this.loadSession();
    }

    // Save session to localStorage
    saveSession(user, role) {
        const sessionData = {
            user: user,
            role: role,
            timestamp: new Date().toISOString(),
            expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 24 hours
        };
        
        localStorage.setItem(this.sessionKey, JSON.stringify(sessionData));
        this.currentUser = user;
        this.currentRole = role;
    }

    // Load session from localStorage
    loadSession() {
        try {
            const sessionData = localStorage.getItem(this.sessionKey);
            if (!sessionData) return null;

            const parsed = JSON.parse(sessionData);
            const now = new Date();
            const expiresAt = new Date(parsed.expiresAt);

            // Check if session has expired
            if (now > expiresAt) {
                this.clearSession();
                return null;
            }

            this.currentUser = parsed.user;
            this.currentRole = parsed.role;
            return parsed;
        } catch (error) {
            console.error('Error loading session:', error);
            this.clearSession();
            return null;
        }
    }

    // Clear session
    clearSession() {
        localStorage.removeItem(this.sessionKey);
        this.currentUser = null;
        this.currentRole = null;
    }

    // Check if user is logged in
    isLoggedIn() {
        return this.currentUser !== null && this.currentRole !== null;
    }

    // Get current user
    getCurrentUser() {
        return this.currentUser;
    }

    // Get current role
    getCurrentRole() {
        return this.currentRole;
    }

    // Check if current user has specific role
    hasRole(role) {
        return this.currentRole === role;
    }

    // Login function
    async login(candidateId, password = null, role = 'candidate') {
        try {
            // For candidate login, we mainly need candidate ID
            // For admin login, we would check password (simplified for demo)
            
            if (role === 'candidate') {
                // Validate candidate ID format
                if (!APIUtils.isValidCandidateId(candidateId)) {
                    throw new Error('Invalid candidate ID format');
                }

                // For demo purposes, we'll accept any valid format candidate ID
                // In real implementation, this would verify against database
                const userData = {
                    id: candidateId,
                    name: `Candidate ${candidateId}`,
                    type: 'candidate'
                };

                this.saveSession(userData, 'candidate');
                return { success: true, user: userData, role: 'candidate' };

            } else if (role === 'admin') {
                // Simple admin authentication (in real app, this would be more secure)
                if (candidateId === 'admin' && (password === 'admin123' || password === null)) {
                    const userData = {
                        id: 'admin',
                        name: 'System Administrator',
                        type: 'admin'
                    };

                    this.saveSession(userData, 'admin');
                    return { success: true, user: userData, role: 'admin' };
                } else {
                    throw new Error('Invalid admin credentials');
                }
            }

            throw new Error('Invalid role specified');

        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    }

    // Logout function
    logout() {
        this.clearSession();
        
        // Redirect to login page
        showPage('loginPage');
        updateNavigation();
        
        // Clear any cached data
        this.clearCachedData();
        
        showToast('You have been logged out successfully', 'success');
    }

    // Clear cached application data
    clearCachedData() {
        // Clear any application-specific cached data
        const keysToRemove = [
            'cached_recommendations',
            'cached_applications',
            'cached_allotment'
        ];
        
        keysToRemove.forEach(key => {
            localStorage.removeItem(key);
        });
    }

    // Auto logout on session expiry
    startSessionMonitor() {
        setInterval(() => {
            const session = this.loadSession();
            if (!session && this.isLoggedIn()) {
                console.log('Session expired, logging out...');
                this.logout();
                showToast('Your session has expired. Please login again.', 'warning');
            }
        }, 5 * 60 * 1000); // Check every 5 minutes
    }

    // Extend session (reset expiry time)
    extendSession() {
        if (this.isLoggedIn()) {
            this.saveSession(this.currentUser, this.currentRole);
        }
    }
}

// Global auth manager instance
const authManager = new AuthManager();

// Authentication-related UI functions
function setupLoginForm() {
    const loginForm = document.getElementById('loginForm');
    const roleButtons = document.querySelectorAll('.role-btn');
    const passwordGroup = document.getElementById('passwordGroup');
    const candidateIdInput = document.getElementById('candidateId');
    let selectedRole = 'candidate';

    // Handle role selection
    roleButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Update active state
            roleButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            selectedRole = btn.dataset.role;
            
            // Show/hide password field based on role
            if (selectedRole === 'admin') {
                passwordGroup.style.display = 'block';
                candidateIdInput.placeholder = 'Enter admin username';
                candidateIdInput.querySelector('label').textContent = 'Admin Username';
            } else {
                passwordGroup.style.display = 'none';
                candidateIdInput.placeholder = 'Enter your Candidate ID';
                candidateIdInput.querySelector('label').textContent = 'Candidate ID';
            }
        });
    });

    // Handle form submission
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const candidateId = document.getElementById('candidateId').value.trim();
        const password = document.getElementById('password').value;

        if (!candidateId) {
            showToast('Please enter your credentials', 'error');
            return;
        }

        showLoading('Authenticating...');

        try {
            const result = await authManager.login(candidateId, password, selectedRole);
            
            if (result.success) {
                hideLoading();
                showToast(`Welcome ${result.user.name}!`, 'success');
                
                // Redirect based on role
                if (result.role === 'admin') {
                    showPage('adminDashboard');
                    loadAdminDashboard();
                } else {
                    showPage('candidateDashboard');
                    setupCandidateDashboard();
                }
                
                updateNavigation();
            }
        } catch (error) {
            hideLoading();
            showToast(APIUtils.handleError(error), 'error');
        }
    });
}

// Update navigation based on user role
function updateNavigation() {
    const navLinks = document.getElementById('navLinks');
    
    if (!authManager.isLoggedIn()) {
        navLinks.innerHTML = '';
        return;
    }

    const user = authManager.getCurrentUser();
    const role = authManager.getCurrentRole();

    let navHTML = '';

    if (role === 'candidate') {
        navHTML = `
            <a href="#" class="nav-link" onclick="showPage('candidateDashboard')">
                <i class="fas fa-tachometer-alt"></i> Dashboard
            </a>
            <a href="#" class="nav-link" onclick="scrollToRecommendations()">
                <i class="fas fa-search"></i> Recommendations
            </a>
            <a href="#" class="nav-link" onclick="scrollToApplications()">
                <i class="fas fa-file-alt"></i> Applications
            </a>
            <a href="#" class="nav-link" onclick="scrollToAllotment()">
                <i class="fas fa-check-circle"></i> Allotment
            </a>
            <span class="nav-user">Welcome, ${user.name}</span>
            <a href="#" class="nav-link" onclick="authManager.logout()">
                <i class="fas fa-sign-out-alt"></i> Logout
            </a>
        `;
    } else if (role === 'admin') {
        navHTML = `
            <a href="#" class="nav-link active" onclick="switchAdminTab('overview')">
                <i class="fas fa-chart-line"></i> Overview
            </a>
            <a href="#" class="nav-link" onclick="switchAdminTab('candidates')">
                <i class="fas fa-users"></i> Candidates
            </a>
            <a href="#" class="nav-link" onclick="switchAdminTab('allocations')">
                <i class="fas fa-tasks"></i> Allocations
            </a>
            <span class="nav-user">Welcome, ${user.name}</span>
            <a href="#" class="nav-link" onclick="authManager.logout()">
                <i class="fas fa-sign-out-alt"></i> Logout
            </a>
        `;
    }

    navLinks.innerHTML = navHTML;
}

// Helper functions for navigation
function scrollToRecommendations() {
    document.getElementById('recommendationsCard').scrollIntoView({ behavior: 'smooth' });
}

function scrollToApplications() {
    document.getElementById('applicationsContainer').scrollIntoView({ behavior: 'smooth' });
}

function scrollToAllotment() {
    document.getElementById('allotmentContainer').scrollIntoView({ behavior: 'smooth' });
}

// Role-based access control
function requireAuth(requiredRole = null) {
    if (!authManager.isLoggedIn()) {
        showToast('Please login to access this feature', 'warning');
        showPage('loginPage');
        return false;
    }

    if (requiredRole && !authManager.hasRole(requiredRole)) {
        showToast('Access denied. Insufficient privileges.', 'error');
        return false;
    }

    // Extend session on activity
    authManager.extendSession();
    return true;
}

// Initialize authentication system
function initAuth() {
    // Check if user is already logged in
    if (authManager.isLoggedIn()) {
        const role = authManager.getCurrentRole();
        
        if (role === 'admin') {
            showPage('adminDashboard');
            loadAdminDashboard();
        } else {
            showPage('candidateDashboard');
            setupCandidateDashboard();
        }
        
        updateNavigation();
    } else {
        showPage('loginPage');
    }

    // Setup login form
    setupLoginForm();
    
    // Start session monitoring
    authManager.startSessionMonitor();
}

// Global logout function
function logout() {
    authManager.logout();
}
