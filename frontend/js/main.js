// Main Application Controller
// Handles page management, UI utilities, loading states, and app initialization

class AppController {
    constructor() {
        this.currentPage = 'loginPage';
        this.isLoading = false;
        this.toastTimeout = null;
    }

    // Initialize the application
    init() {
        console.log('🚀 PM Internship Allocation Engine - Frontend Starting...');
        
        // Initialize authentication
        initAuth();
        
        // Setup global event listeners
        this.setupGlobalEventListeners();
        
        // Initialize UI components
        this.initializeUI();
        
        console.log('✅ Frontend Application Ready');
    }

    // Setup global event listeners
    setupGlobalEventListeners() {
        // Handle window resize for responsive design
        window.addEventListener('resize', this.handleResize.bind(this));
        
        // Handle offline/online status
        window.addEventListener('online', () => {
            showToast('Connection restored', 'success');
        });
        
        window.addEventListener('offline', () => {
            showToast('You are offline. Some features may not work.', 'warning');
        });

        // Prevent form submissions from refreshing page
        document.addEventListener('submit', (e) => {
            if (e.target.tagName === 'FORM') {
                e.preventDefault();
            }
        });

        // Handle keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyboardShortcuts.bind(this));
    }

    // Handle keyboard shortcuts
    handleKeyboardShortcuts(e) {
        // Escape key closes overlays
        if (e.key === 'Escape') {
            this.hideLoading();
            this.closeToast();
        }

        // Ctrl/Cmd + R for refresh (admin only)
        if ((e.ctrlKey || e.metaKey) && e.key === 'r' && authManager.hasRole('admin')) {
            e.preventDefault();
            if (confirm('Reload dashboard data?')) {
                location.reload();
            }
        }
    }

    // Handle window resize
    handleResize() {
        // Update mobile navigation if needed
        this.updateMobileLayout();
    }

    // Update layout for mobile devices
    updateMobileLayout() {
        const isMobile = window.innerWidth <= 768;
        document.body.classList.toggle('mobile-layout', isMobile);
    }

    // Initialize UI components
    initializeUI() {
        // Update mobile layout
        this.updateMobileLayout();
        
        // Initialize tooltips (if needed)
        this.initializeTooltips();
    }

    // Initialize tooltips
    initializeTooltips() {
        // Add simple tooltip functionality
        const elementsWithTitles = document.querySelectorAll('[title]');
        elementsWithTitles.forEach(element => {
            element.addEventListener('mouseenter', this.showTooltip.bind(this));
            element.addEventListener('mouseleave', this.hideTooltip.bind(this));
        });
    }

    // Show tooltip
    showTooltip(e) {
        const title = e.target.getAttribute('title');
        if (!title) return;

        e.target.setAttribute('data-original-title', title);
        e.target.removeAttribute('title');

        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = title;
        tooltip.style.position = 'absolute';
        tooltip.style.zIndex = '9999';
        tooltip.style.background = 'rgba(0,0,0,0.8)';
        tooltip.style.color = 'white';
        tooltip.style.padding = '0.5rem';
        tooltip.style.borderRadius = '4px';
        tooltip.style.fontSize = '0.8rem';
        tooltip.style.pointerEvents = 'none';
        
        document.body.appendChild(tooltip);
        
        const rect = e.target.getBoundingClientRect();
        tooltip.style.left = rect.left + 'px';
        tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
    }

    // Hide tooltip
    hideTooltip(e) {
        const originalTitle = e.target.getAttribute('data-original-title');
        if (originalTitle) {
            e.target.setAttribute('title', originalTitle);
            e.target.removeAttribute('data-original-title');
        }

        const tooltip = document.querySelector('.tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    }
}

// Global app controller instance
const appController = new AppController();

// Page Management Functions
function showPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });

    // Show selected page
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.classList.add('active');
        appController.currentPage = pageId;
        
        // Scroll to top of new page
        window.scrollTo(0, 0);
        
        console.log(`📄 Switched to page: ${pageId}`);
    }
}

// Loading State Management
function showLoading(message = 'Loading...') {
    appController.isLoading = true;
    const overlay = document.getElementById('loadingOverlay');
    const messageElement = overlay.querySelector('p');
    
    if (messageElement) {
        messageElement.textContent = message;
    }
    
    overlay.classList.add('show');
    document.body.style.overflow = 'hidden';
}

function hideLoading() {
    appController.isLoading = false;
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.remove('show');
    document.body.style.overflow = '';
}

// Toast Notification System
function showToast(message, type = 'info', duration = 4000) {
    const toast = document.getElementById('toast');
    const messageElement = document.getElementById('toastMessage');
    
    // Clear existing timeout
    if (appController.toastTimeout) {
        clearTimeout(appController.toastTimeout);
    }
    
    // Remove existing type classes
    toast.classList.remove('success', 'error', 'warning', 'info');
    
    // Set message and type
    messageElement.textContent = message;
    toast.classList.add(type, 'show');
    
    // Auto-hide after duration
    appController.toastTimeout = setTimeout(() => {
        closeToast();
    }, duration);
    
    console.log(`🔔 Toast: ${type.toUpperCase()} - ${message}`);
}

function closeToast() {
    const toast = document.getElementById('toast');
    toast.classList.remove('show');
    
    if (appController.toastTimeout) {
        clearTimeout(appController.toastTimeout);
        appController.toastTimeout = null;
    }
}

// Utility Functions
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Error Handling
function handleGlobalError(error) {
    console.error('🚨 Global Error:', error);
    showToast('An unexpected error occurred. Please refresh the page.', 'error');
}

// Setup global error handlers
window.addEventListener('error', (e) => {
    handleGlobalError(e.error);
});

window.addEventListener('unhandledrejection', (e) => {
    handleGlobalError(e.reason);
});

// Data Export Utilities
function exportToCSV(data, filename) {
    if (!data || data.length === 0) {
        showToast('No data to export', 'warning');
        return;
    }

    const headers = Object.keys(data[0]);
    const csvContent = [
        headers.join(','),
        ...data.map(row => headers.map(header => `"${row[header] || ''}"`).join(','))
    ].join('\\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (link.download !== undefined) {
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', `${filename}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showToast(`Exported ${filename}.csv successfully`, 'success');
    } else {
        showToast('CSV export not supported in this browser', 'error');
    }
}

// Performance Monitoring
function measurePerformance(name, func) {
    return async function(...args) {
        const start = performance.now();
        const result = await func.apply(this, args);
        const end = performance.now();
        
        console.log(`⏱️  ${name} took ${(end - start).toFixed(2)}ms`);
        return result;
    };
}

// Local Storage Utilities
const StorageManager = {
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (error) {
            console.error('Failed to save to localStorage:', error);
            return false;
        }
    },

    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('Failed to read from localStorage:', error);
            return defaultValue;
        }
    },

    remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (error) {
            console.error('Failed to remove from localStorage:', error);
            return false;
        }
    },

    clear() {
        try {
            localStorage.clear();
            return true;
        } catch (error) {
            console.error('Failed to clear localStorage:', error);
            return false;
        }
    }
};

// Theme Management (for future enhancement)
const ThemeManager = {
    currentTheme: 'default',
    
    setTheme(theme) {
        document.body.classList.remove(`theme-${this.currentTheme}`);
        document.body.classList.add(`theme-${theme}`);
        this.currentTheme = theme;
        StorageManager.set('app_theme', theme);
    },
    
    loadTheme() {
        const savedTheme = StorageManager.get('app_theme', 'default');
        this.setTheme(savedTheme);
    }
};

// Accessibility Helpers
function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.style.position = 'absolute';
    announcement.style.left = '-10000px';
    announcement.style.width = '1px';
    announcement.style.height = '1px';
    announcement.style.overflow = 'hidden';
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    
    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('🌟 PM Internship Allocation Engine - Government of India');
    console.log('🔧 Initializing Application...');
    
    // Load theme
    ThemeManager.loadTheme();
    
    // Initialize app
    appController.init();
    
    // Announce to screen readers
    announceToScreenReader('PM Internship Allocation Portal loaded successfully');
});

// Service Worker Registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('✅ SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('❌ SW registration failed: ', registrationError);
            });
    });
}

// Export functions for global use
window.showPage = showPage;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.showToast = showToast;
window.closeToast = closeToast;
window.exportToCSV = exportToCSV;
window.StorageManager = StorageManager;
window.ThemeManager = ThemeManager;
