# PM Internship Allocation Engine - Frontend

A modern, responsive web application for the AI-powered PM Internship Allocation Engine. Built following Government of India portal design standards.

## 🌟 Features

### For Candidates
- **Government Portal Style Login** - Professional authentication system
- **AI-Powered Recommendations** - Get personalized internship matches based on your profile
- **Application Tracking** - Monitor status of submitted applications
- **Allotment Management** - View and confirm internship allocations
- **Progress Visualization** - Match scores displayed with interactive progress bars

### For Administrators
- **Dashboard Analytics** - Comprehensive overview of system statistics
- **Candidate Management** - View and manage all candidate profiles
- **Smart Allocation Engine** - Run AI-powered allocation algorithms
- **Real-time Monitoring** - Track allocation process and results

### Design & UX
- **Government Portal Theme** - Blue/white color scheme with orange accents
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Accessibility Compliant** - Screen reader support and keyboard navigation
- **Loading States** - Professional loading animations and error handling

## 🏗️ Architecture

### Frontend Structure
```
frontend/
├── index.html          # Main application HTML
├── css/
│   └── styles.css      # Government portal styling
├── js/
│   ├── api.js          # API integration layer
│   ├── auth.js         # Authentication system
│   ├── candidate.js    # Candidate dashboard functionality
│   ├── admin.js        # Admin dashboard functionality
│   └── main.js         # Main application controller
└── README.md          # This documentation
```

### Technology Stack
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with CSS Variables, Flexbox, Grid
- **Icons**: Font Awesome 6.0
- **Fonts**: Open Sans (Google Fonts)
- **API Communication**: Fetch API
- **Storage**: LocalStorage for session management

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ (for backend API)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Basic understanding of web development

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd pm-smart-allocation-engine
   ```

2. **Install Python dependencies** (for backend):
   ```bash
   pip install flask flask-cors pandas numpy scikit-learn
   ```

3. **Prepare your data files** (place in root directory):
   - `candidates.csv` - Candidate data with resumes
   - `internship.csv` - Internship opportunities data
   - `tfidf_vectorizer.pkl` - Trained ML model (optional)
   - `internship_tfidf_matrix.pkl` - Pre-computed matrix (optional)

4. **Start the backend API**:
   ```bash
   python recommendation_api.py
   ```
   The API will start on `http://localhost:5000`

5. **Open the frontend**:
   - Simply open `frontend/index.html` in your web browser
   - Or serve it using a local server:
     ```bash
     # Using Python's built-in server
     cd frontend
     python -m http.server 8080
     ```
   - Then visit `http://localhost:8080`

## 👥 User Guide

### Candidate Login
1. **Access the Portal**:
   - Open the application in your browser
   - You'll see the government portal style login page

2. **Login as Candidate**:
   - Select "Candidate Login" (default selection)
   - Enter your Candidate ID (numeric, 3-10 digits)
   - Click "Login"

3. **Get Recommendations**:
   - Enter your Candidate ID in the recommendation form
   - Click "Get Recommendations"
   - View personalized internship matches with progress bars
   - Each recommendation shows:
     - Company name and job title
     - Match score (percentage)
     - Job description
     - Apply button

4. **Apply to Internships**:
   - Click "Apply" button for any recommendation
   - Application will be submitted and tracked
   - Button changes to "Applied" state

5. **Track Applications**:
   - View all submitted applications in "My Applications" section
   - See application status, company details, and dates

6. **Check Allotment**:
   - View your final allocation in "Allotment Status" section
   - Confirm acceptance if allocated

### Admin Access
1. **Login as Admin**:
   - Select "Admin Login"
   - Username: `admin`
   - Password: `admin123` (or leave blank for demo)
   - Click "Login"

2. **Dashboard Overview**:
   - View system statistics
   - Monitor total interns, projects, mentors, allocations
   - Access AI allocation controls

3. **Manage Candidates**:
   - Switch to "Candidates" tab
   - View all registered candidates
   - See candidate details, skills, and status

4. **Run Allocations**:
   - Use "Run Smart Allocation" button
   - Monitor allocation process
   - View results in "Allocations" tab

5. **View Allocations**:
   - Switch to "Allocations" tab
   - See all intern-project matches
   - View match scores and status
   - Access detailed allocation information

## 🔧 Configuration

### API Configuration
The frontend connects to the backend API running on `localhost:5000`. To change this:

1. Edit `js/api.js`:
   ```javascript
   // Line 5-6
   this.baseURL = 'http://your-server:port/api';
   this.originalBaseURL = 'http://your-server:port';
   ```

### Styling Customization
The application uses CSS variables for easy theming:

```css
:root {
    --primary-blue: #1a237e;
    --secondary-blue: #3949ab;
    --orange-accent: #ff6f00;
    /* ... more variables */
}
```

### Authentication Settings
Session duration and other auth settings in `js/auth.js`:

```javascript
// Line 19: Session expiry (default 24 hours)
expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
```

## 📱 Responsive Design

The application is fully responsive with breakpoints:
- **Desktop**: 1200px+ (full layout)
- **Tablet**: 768px-1199px (adapted layout)
- **Mobile**: <768px (mobile-optimized)

### Mobile Features
- Collapsible navigation
- Touch-friendly buttons
- Optimized table layouts
- Simplified forms

## 🔒 Security Features

### Authentication
- Session-based authentication
- Role-based access control (candidate/admin)
- Session expiry monitoring
- Secure logout functionality

### Data Protection
- Client-side data validation
- Secure API communication
- No sensitive data in localStorage
- CORS-enabled backend

### Input Validation
- Candidate ID format validation
- Form input sanitization
- Error message sanitization
- XSS prevention measures

## 🎨 UI/UX Guidelines

### Government Portal Standards
- Blue (#1a237e, #3949ab) and white primary colors
- Orange (#ff6f00) accent for actions and highlights
- Official government emblem and branding
- Professional typography (Open Sans)
- Clean, minimal interface design

### Accessibility
- ARIA labels and roles
- Keyboard navigation support
- Screen reader announcements
- High contrast ratios
- Focus indicators
- Semantic HTML structure

### Loading States
- Professional loading overlays
- Progress indicators
- Toast notifications for feedback
- Error state handling
- Offline detection

## 🔧 API Integration

### Available Endpoints

#### Recommendation System
```javascript
// Get recommendations
POST /recommend
{
  "candidate_id": 122,
  "n": 10
}

// Submit application
POST /apply
{
  "candidate_id": 122,
  "company_name": "Tech Solutions",
  "job_title": "Developer Intern"
}
```

#### Data Management
```javascript
// Get candidates (admin)
GET /candidates

// Health check
GET /health
```

### Error Handling
- Network error detection
- User-friendly error messages
- Automatic retry logic
- Fallback to mock data

## 🐛 Troubleshooting

### Common Issues

1. **"Cannot connect to server"**:
   - Ensure backend API is running on port 5000
   - Check CORS settings
   - Verify network connectivity

2. **"Candidate ID not found"**:
   - Verify candidate exists in candidates.csv
   - Check ID format (numeric, 3-10 digits)

3. **Recommendations not loading**:
   - Check if data files exist
   - Verify ML model files are present
   - Check browser console for errors

4. **Styling issues**:
   - Clear browser cache
   - Check CSS file loading
   - Verify internet connection for external fonts

### Debug Mode
Enable debug logging by opening browser console and checking for:
- API request/response logs
- Authentication state changes
- Page navigation events
- Error messages

## 🚀 Deployment

### Production Deployment

1. **Prepare Files**:
   - Minify CSS and JavaScript
   - Optimize images and assets
   - Configure production API endpoints

2. **Server Configuration**:
   - Use HTTPS in production
   - Configure proper CORS settings
   - Set up reverse proxy if needed
   - Enable gzip compression

3. **Security Checklist**:
   - Change default admin credentials
   - Implement proper authentication
   - Enable HTTPS
   - Configure CSP headers
   - Regular security updates

### Environment Variables
```bash
# Backend API
FLASK_ENV=production
API_HOST=0.0.0.0
API_PORT=5000

# Frontend
API_BASE_URL=https://your-api-domain.com
```

## 📈 Performance

### Optimization Features
- Lazy loading of components
- Efficient DOM manipulation
- Minimal API calls
- Local storage caching
- Debounced user inputs

### Browser Support
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+
- Mobile browsers

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Follow coding standards
4. Add tests if applicable
5. Submit pull request

### Code Standards
- Use ES6+ features
- Follow consistent naming conventions
- Add comments for complex logic
- Maintain accessibility standards
- Test across browsers

## 📄 License

This project is developed for the Government of India PM Internship Program. All rights reserved.

## 📞 Support

For technical support:
- Email: support@pminternship.gov.in
- GitHub Issues: [Repository Issues Page]
- Documentation: [Official Documentation]

---

**Built with ❤️ for the PM Internship Program - Government of India**
