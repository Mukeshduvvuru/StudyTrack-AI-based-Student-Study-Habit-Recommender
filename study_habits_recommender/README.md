# Study Habits Recommender System

A comprehensive data science project that provides personalized study habit recommendations based on student behavior analysis using machine learning.

## 🎯 Project Overview

This system analyzes student behavior patterns (study hours, quiz performance, attention logs, distractions) to recommend optimal study strategies. It uses unsupervised learning (K-Means clustering) to identify different learning styles and provides tailored recommendations for improved academic performance.

## ✨ Features

- **Student Portal**
  - Log daily study sessions
  - Track performance metrics
  - Receive personalized recommendations
  - View progress charts and trends
  - Weekly study schedules

- **Admin Dashboard**
  - Upload and manage datasets
  - Retrain ML models
  - View system analytics
  - Monitor student clusters
  - Track overall performance

- **ML-Powered Recommendations**
  - Behavioral clustering using K-Means
  - Pattern detection algorithms
  - Personalized study routines
  - Optimal time slot suggestions
  - Break pattern recommendations

## 📋 Student Behavior Clusters

1. **Focused Studiers** - Long sessions, minimal distractions, high performance
2. **Short Burst Learners** - Brief frequent sessions, active engagement
3. **Night Owls** - Late-night study sessions, deep concentration
4. **Distracted Learners** - High interruptions, need structured environments

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **ML/Data Science**: scikit-learn, pandas, numpy
- **Visualization**: Chart.js
- **Database**: In-memory (can be extended to SQLite/PostgreSQL)

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd study_habits_recommender
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your web browser
   - Navigate to: `http://localhost:5000`

## 🚀 Usage

### For Students

1. **Sign In**
   - Go to Student Portal
   - Enter your name and email
   - Click "Sign In"

2. **Log Study Sessions**
   - Fill in the study log form:
     - Date
     - Study duration
     - Subject
     - Study time (Morning/Afternoon/Evening/Night)
     - Study method
     - Distraction level
     - Quiz score (optional)
   - Click "Save Log"

3. **View Recommendations**
   - After logging 3+ sessions, you'll get personalized recommendations
   - View your cluster type
   - See optimal study times
   - Get recommended study methods
   - Access suggested tools

4. **Track Progress**
   - Monitor your performance charts
   - View total study hours
   - Check average quiz scores
   - Track your study streak

### For Administrators

1. **Admin Login**
   - Username: `admin`
   - Password: `admin123`

2. **Upload Data**
   - Navigate to "Data Management"
   - Upload CSV files with student behavior data
   - CSV format should include:
     - student_id
     - study_hours
     - quiz_score
     - distraction_frequency
     - preferred_time
     - study_method

3. **Retrain Model**
   - Click "Retrain Model" button
   - Wait for training to complete
   - View updated analytics

4. **View Analytics**
   - Monitor total students and sessions
   - View cluster distribution
   - Check recent study logs
   - Analyze system performance

## 📊 Project Structure

```
study_habits_recommender/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Landing page
│   ├── student_login.html     # Student login
│   ├── admin_login.html       # Admin login
│   ├── student_dashboard.html # Student dashboard
│   └── admin_dashboard.html   # Admin dashboard
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   └── js/
│       └── main.js            # JavaScript utilities
├── models/                     # ML models (auto-generated)
│   ├── kmeans_model.pkl
│   └── scaler.pkl
├── data/                       # Data files (auto-generated)
│   └── sample_student_data.csv
└── uploads/                    # Uploaded files (auto-generated)
```

## 🎓 Machine Learning Approach

### Data Preprocessing
- Handle missing values
- Normalize continuous variables
- Encode categorical features
- Feature scaling using StandardScaler

### Clustering Algorithm
- **K-Means Clustering** (4 clusters)
- Features used:
  - Study duration
  - Quiz performance
  - Distraction level
  - Preferred study time

### Recommendation Engine
- Maps students to behavior clusters
- Suggests optimal study patterns
- Recommends tools and methods
- Generates weekly schedules

## 📈 API Endpoints

### Student Endpoints
- `POST /student/login` - Student authentication
- `POST /api/log-study` - Log study session
- `GET /api/get-recommendations` - Get personalized recommendations
- `GET /api/student-stats` - Get student statistics

### Admin Endpoints
- `POST /admin/login` - Admin authentication
- `POST /api/admin/upload-data` - Upload dataset
- `POST /api/admin/retrain-model` - Retrain ML model
- `GET /api/admin/analytics` - Get system analytics

## 🔒 Security Considerations

- Passwords are hashed using Werkzeug security
- Session-based authentication
- CSRF protection (can be enhanced)
- File upload validation
- Input sanitization

## 🚀 Future Enhancements

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Email notifications
- [ ] Export reports to PDF
- [ ] Mobile responsive improvements
- [ ] More advanced ML models (DBSCAN, Hierarchical)
- [ ] Real-time collaboration features
- [ ] Integration with calendar apps
- [ ] Social features (study groups)

## 📝 Sample Data Format

CSV format for bulk upload:

```csv
student_id,study_hours,quiz_score,distraction_frequency,preferred_time,study_method
1,4.5,88,Low,Morning,Pomodoro
2,2.0,75,Medium,Afternoon,Spaced
3,3.5,82,Low,Night,Continuous
...
```

## 🤝 Contributing

This is an academic project. For improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is created for educational purposes as part of a Data Science course.

## 👥 Authors

- Data Science Student Project
- Course: Recommending Study Habits Based on Student Behavior

## 📞 Support

For questions or issues:
- Check the documentation above
- Review the code comments
- Test with sample data first

## 🎉 Acknowledgments

- Anthropic Claude for project guidance
- Flask framework documentation
- scikit-learn community
- Chart.js for visualizations

---

**Happy Learning! 📚✨**

Built with ❤️ for students, by students.
