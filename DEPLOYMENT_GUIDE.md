# 🚀 PM Internship Allocation Engine - Network Deployment

## Quick Start (1-Click Deployment)

### **Option 1: Full Deployment (Recommended)**
1. **Double-click** `deploy_webapp.bat`
2. Press any key when prompted
3. ✅ **Done!** Your app is now live on the network

### **Option 2: Manual Deployment**
1. **Start Backend**: Double-click `start_backend.bat`
2. **Start Frontend**: Double-click `start_frontend.bat`
3. ✅ **Done!** Both servers are running

## 📱 Access Your Web Application

### **From ANY Device on Your WiFi Network:**

**🔗 Main URL:** `http://192.168.0.119:8080`

### **Test on Different Devices:**
- 📱 **Mobile Phone**: Open browser → Enter URL above
- 📱 **Tablet**: Open browser → Enter URL above  
- 💻 **Laptop**: Open browser → Enter URL above
- 🖥️ **Desktop**: Open browser → Enter URL above

## 👥 User Access Instructions

### **Candidate Login:**
- Role: Select **"Candidate Login"**
- ID: Enter any 3-10 digit number (e.g., `122`, `1001`, `5678`)
- Click **"Login"**

### **Admin Login:**
- Role: Select **"Admin Login"**  
- Username: `admin`
- Password: `admin123` (or leave blank)
- Click **"Login"**

## 🔥 Features Available

### **For Candidates:**
- ✅ Get AI-powered internship recommendations
- ✅ Apply to internships with one click
- ✅ Track application status
- ✅ View allotment results
- ✅ Confirm internship acceptance

### **For Administrators:**
- ✅ View system dashboard with analytics
- ✅ Manage all candidates and applications
- ✅ Run AI allocation algorithms
- ✅ Monitor allocation results
- ✅ Export data and reports

## 🛠️ Technical Details

### **Server Status:**
- **Backend API**: `http://192.168.0.119:5000`
- **Frontend Web**: `http://192.168.0.119:8080`
- **Data Source**: Your `candidates.csv` and `internship.csv` files
- **AI Engine**: Your trained TF-IDF model

### **Requirements:**
- ✅ Python 3.8+
- ✅ Flask, pandas, scikit-learn
- ✅ Modern web browser
- ✅ Same WiFi network for all devices

## 🚨 Troubleshooting

### **Can't Access from Mobile/Other Devices:**
1. **Check WiFi**: Ensure all devices are on the same WiFi network
2. **Check Firewall**: Windows Defender might block connections
   - Go to Windows Defender Firewall
   - Allow Python through firewall
3. **Try Different Browser**: Chrome, Firefox, Safari, Edge

### **Backend API Not Working:**
1. Check if `candidates.csv` and `internship.csv` are in the root directory
2. Ensure Python packages are installed: `pip install flask flask-cors pandas scikit-learn`
3. Check the API server window for error messages

### **Frontend Not Loading:**
1. Ensure frontend server is running on port 8080
2. Check if `frontend/index.html` exists
3. Try accessing `http://localhost:8080` first

## 🔒 Security Notes

- ⚠️ This deployment is for **local network only**
- ⚠️ Not suitable for production/internet deployment
- ⚠️ Change admin credentials for production use
- ✅ Safe for development, testing, and demos

## 🛑 Stop Deployment

To stop the servers:
1. Close the frontend server window (Ctrl+C)
2. Close the backend API server window (Ctrl+C)
3. Or simply close both command prompt windows

---

**🎉 Enjoy your deployed PM Internship Allocation Engine!**
