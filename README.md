# ransomware_monitor
🛡️ Anti-Ransomware File Integrity Monitor
Real-time file integrity monitoring system using SHA-256 cryptographic hashing with a modern web dashboard.
🚀 Quick Start
1. Install Flask
bashpip install flask
2. Run the Application
bashpython app.py
3. Open Your Browser
http://localhost:5000
📖 How to Use
Step 1: Set Directory

Enter the path to monitor (e.g., ./documents or C:\Users\YourName\Documents)
Click "Set Directory"

Step 2: Create Baseline

Click "Create Baseline"
This generates SHA-256 hashes for all files
Wait for confirmation

Step 3: Start Monitoring

Set scan interval (default: 5 seconds)
Click "Start Monitoring"
Dashboard updates automatically

Step 4: Monitor Results

View statistics in real-time
See color-coded file status
Get instant security alerts

🎨 Features
Monitoring
✅ Real-time file integrity checking
✅ SHA-256 cryptographic hashing
✅ Detects modified files
✅ Detects deleted files
✅ Detects new suspicious files
✅ Configurable scan intervals (1-60 seconds)
Dashboard
✅ Live statistics
✅ Color-coded file status
✅ Real-time alert feed
✅ Auto-refreshing data
✅ Modern responsive design
✅ Keyboard shortcuts
⌨️ Keyboard Shortcuts

Ctrl+Enter: Start monitoring
Escape: Stop monitoring

🎯 Status Colors

🟢 Green: Secure/Unchanged files
🔴 Red: Modified/Deleted files (ALERT!)
🟡 Yellow: New files detected
⚫ Gray: Deleted files

🧪 Test It
Create Test Environment
bash# Create test directory
mkdir test_monitor
cd test_monitor

# Create test files
echo "Important data" > file1.txt
echo "Secret info" > file2.txt
echo "Confidential" > file3.txt
Simulate Ransomware
bash# Modify files
echo "ENCRYPTED" > test_monitor/file1.txt
echo "ENCRYPTED" > test_monitor/file2.txt

# Delete file
rm test_monitor/file3.txt

# Add suspicious file
echo "malware" > test_monitor/virus.exe
Watch the dashboard detect all changes in real-time! 🎯
🔧 Configuration
Change Port
Edit app.py:
pythonapp.run(debug=True, host='127.0.0.1', port=8080)
Allow Network Access
Edit app.py:
pythonapp.run(debug=True, host='0.0.0.0', port=5000)
⚠️ Warning: Only use 0.0.0.0 on trusted networks!
📊 API Endpoints

POST /api/set-directory - Set monitoring directory
POST /api/create-baseline - Create baseline hashes
POST /api/scan - Perform single scan
POST /api/start-monitoring - Start continuous monitoring
POST /api/stop-monitoring - Stop monitoring
GET /api/data - Get current monitoring data

🔒 Security Concepts
What This Demonstrates

SHA-256 Hashing: Cryptographic fingerprinting
Integrity Verification: Detecting unauthorized changes
Baseline Comparison: Reference point for security
Real-time Monitoring: Proactive threat detection

Educational Value
This project teaches:

File I/O operations
Cryptographic hashing
Web application development
Real-time data updates
Ransomware behavior patterns

🛠️ Technologies Used

Python 3.7+: Backend language
Flask: Web framework
SHA-256: Cryptographic hashing
JavaScript: Frontend interactivity
HTML/CSS: User interface
Threading: Background monitoring

⚠️ Important Notes
For Educational Use
This is a learning tool demonstrating:

File integrity monitoring concepts
Cryptographic hashing principles
Web application architecture
Real-time threat detection

For Production Use
Consider adding:

User authentication
HTTPS/SSL encryption
Email/SMS alerts
Database storage
File backup integration
Advanced anomaly detection

🐛 Troubleshooting
Port Already in Use
bash# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
Baseline Not Found

Click "Create Baseline" first
Check if baseline.json exists
Verify directory path is correct

Files Not Updating

Check if monitoring is active (green status)
Verify scan interval is reasonable
Check browser console for errors

📚 Learn More
Cryptography Concepts

Hash Functions: One-way cryptographic functions
SHA-256: Secure Hash Algorithm (256-bit)
File Integrity: Ensuring data hasn't been tampered
Digital Fingerprints: Unique identifiers for files

How Ransomware Works

Encrypts files without permission
Changes file extensions
Deletes original files
Demands ransom for decryption

How This Tool Detects It

Creates baseline of file hashes
Continuously monitors for changes
Alerts when hashes don't match
Detects rapid file modifications

🤝 Contributing
Feel free to extend this project with:

Email notifications
Database storage (SQLite, PostgreSQL)
Machine learning anomaly detection
File backup integration
Multi-user support
Mobile app version

📄 License
Educational project - Free to use and modify
👨‍💻 About
Created as a cryptography learning project demonstrating:

Real-world application of SHA-256 hashing
File integrity monitoring techniques
Ransomware detection methods
Web application development
Full-stack programming


⚠️ Disclaimer: This is an educational tool. For production ransomware protection, use enterprise-grade security solutions with professional support.
🛡️ Stay Safe: Always maintain regular backups of important files!
