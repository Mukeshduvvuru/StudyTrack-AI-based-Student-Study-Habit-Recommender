from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta
import json
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pickle
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('models', exist_ok=True)
os.makedirs('data', exist_ok=True)

# In-memory database (replace with SQLite/PostgreSQL in production)
students_db = {}
study_logs_db = []
clusters_db = {}
recommendations_db = []
admin_users = {'admin': generate_password_hash('admin123')}

# Sample behavioral clusters
CLUSTER_PROFILES = {
    0: {
        'name': 'Focused Studiers',
        'description': 'Long sessions, few distractions',
        'avg_study_duration': 4.2,
        'preferred_time': 'Morning (8am-12pm)',
        'distraction_level': 'Low',
        'quiz_performance': 88,
        'common_tools': ['Pomodoro', 'Notes'],
        'recommended_hours': 3.5,
        'break_interval': 25,
        'suggested_method': 'Pomodoro Technique',
        'recommended_tools': ['Pomodoro Timer', 'Focus Music', 'Digital Notes']
    },
    1: {
        'name': 'Short Burst Learners',
        'description': 'Brief, frequent sessions',
        'avg_study_duration': 1.8,
        'preferred_time': 'Afternoon (2pm-6pm)',
        'distraction_level': 'Medium',
        'quiz_performance': 75,
        'common_tools': ['Flashcards', 'Videos'],
        'recommended_hours': 2.0,
        'break_interval': 15,
        'suggested_method': 'Spaced Repetition',
        'recommended_tools': ['Flashcard Apps', 'Video Tutorials', 'Quick Quizzes']
    },
    2: {
        'name': 'Night Owls',
        'description': 'Late night study sessions',
        'avg_study_duration': 3.5,
        'preferred_time': 'Night (8pm-12am)',
        'distraction_level': 'Low',
        'quiz_performance': 82,
        'common_tools': ['Reading', 'Practice'],
        'recommended_hours': 3.0,
        'break_interval': 30,
        'suggested_method': 'Deep Work Sessions',
        'recommended_tools': ['Site Blocker', 'Ambient Sounds', 'Practice Problems']
    },
    3: {
        'name': 'Distracted Learners',
        'description': 'High interruption frequency',
        'avg_study_duration': 2.2,
        'preferred_time': 'Evening (6pm-8pm)',
        'distraction_level': 'High',
        'quiz_performance': 68,
        'common_tools': ['Apps', 'Groups'],
        'recommended_hours': 1.5,
        'break_interval': 10,
        'suggested_method': 'Structured Environment',
        'recommended_tools': ['Website Blockers', 'Study Groups', 'Accountability Apps']
    }
}

def generate_sample_data():
    """Generate sample student behavior data for demonstration"""
    np.random.seed(42)
    n_students = 1248
    
    data = {
        'student_id': range(1, n_students + 1),
        'study_hours': np.random.uniform(1, 8, n_students),
        'quiz_score': np.random.randint(50, 100, n_students),
        'distraction_frequency': np.random.choice(['Low', 'Medium', 'High'], n_students),
        'preferred_time': np.random.choice(['Morning', 'Afternoon', 'Evening', 'Night'], n_students),
        'study_method': np.random.choice(['Pomodoro', 'Continuous', 'Spaced', 'Intensive'], n_students)
    }
    
    df = pd.DataFrame(data)
    df.to_csv('data/sample_student_data.csv', index=False)
    return df

def train_clustering_model():
    """Train the clustering model on student behavior data"""
    try:
        df = pd.read_csv('data/sample_student_data.csv')
    except:
        df = generate_sample_data()
    
    # Feature engineering
    df['distraction_encoded'] = df['distraction_frequency'].map({'Low': 0, 'Medium': 1, 'High': 2})
    df['time_encoded'] = df['preferred_time'].map({'Morning': 0, 'Afternoon': 1, 'Evening': 2, 'Night': 3})
    
    features = df[['study_hours', 'quiz_score', 'distraction_encoded', 'time_encoded']]
    
    # Standardize features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Train K-Means clustering
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(features_scaled)
    
    # Save model and scaler
    with open('models/kmeans_model.pkl', 'wb') as f:
        pickle.dump(kmeans, f)
    with open('models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    return kmeans, scaler, df

def predict_cluster(study_hours, quiz_score, distraction_level, preferred_time):
    """Predict cluster for a new student"""
    try:
        with open('models/kmeans_model.pkl', 'rb') as f:
            kmeans = pickle.load(f)
        with open('models/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
    except:
        kmeans, scaler, _ = train_clustering_model()
    
    distraction_map = {'None': 0, 'Low': 0, 'Medium': 1, 'High': 2}
    time_map = {'Morning': 0, 'Afternoon': 1, 'Evening': 2, 'Night': 3}
    
    features = np.array([[
        study_hours,
        quiz_score,
        distraction_map.get(distraction_level, 1),
        time_map.get(preferred_time, 0)
    ]])
    
    features_scaled = scaler.transform(features)
    cluster = kmeans.predict(features_scaled)[0]
    
    return int(cluster)

# Initialize clustering model on startup
try:
    train_clustering_model()
except:
    pass

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student')
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))
    return render_template('student_dashboard.html')

@app.route('/admin')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    
    # Calculate statistics
    total_students = len(students_db)
    total_logs = len(study_logs_db)
    
    # Get recent logs
    recent_logs = sorted(study_logs_db, key=lambda x: x.get('date', ''), reverse=True)[:10]
    
    return render_template('admin_dashboard.html', 
                         total_students=total_students,
                         total_logs=total_logs,
                         recent_logs=recent_logs,
                         clusters=CLUSTER_PROFILES)

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        
        if email and name:
            student_id = email
            if student_id not in students_db:
                students_db[student_id] = {
                    'name': name,
                    'email': email,
                    'cluster_id': None,
                    'created_at': datetime.now().isoformat()
                }
            
            session['student_id'] = student_id
            session['student_name'] = name
            return jsonify({'success': True, 'redirect': url_for('student_dashboard')})
        
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 400
    
    return render_template('student_login.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username in admin_users and check_password_hash(admin_users[username], password):
            session['admin'] = username
            return jsonify({'success': True, 'redirect': url_for('admin_dashboard')})
        
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    return render_template('admin_login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/log-study', methods=['POST'])
def log_study():
    if 'student_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    data = request.get_json()
    
    log_entry = {
        'log_id': len(study_logs_db) + 1,
        'student_id': session['student_id'],
        'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
        'study_hours': float(data.get('study_hours', 0)),
        'subject': data.get('subject', ''),
        'study_time': data.get('study_time', ''),
        'method_used': data.get('method_used', ''),
        'distractions': data.get('distractions', 'None'),
        'quiz_score': int(data.get('quiz_score', 0)) if data.get('quiz_score') else None
    }
    
    study_logs_db.append(log_entry)
    
    # Update student cluster if we have enough data
    student_logs = [log for log in study_logs_db if log['student_id'] == session['student_id']]
    
    if len(student_logs) >= 3:
        avg_hours = np.mean([log['study_hours'] for log in student_logs])
        avg_score = np.mean([log['quiz_score'] for log in student_logs if log['quiz_score']])
        most_common_distraction = max(set([log['distractions'] for log in student_logs]), 
                                      key=[log['distractions'] for log in student_logs].count)
        most_common_time = max(set([log['study_time'] for log in student_logs]), 
                              key=[log['study_time'] for log in student_logs].count)
        
        cluster = predict_cluster(avg_hours, avg_score, most_common_distraction, most_common_time)
        students_db[session['student_id']]['cluster_id'] = cluster
    
    return jsonify({'success': True, 'log_id': log_entry['log_id']})

@app.route('/api/get-recommendations')
def get_recommendations():
    if 'student_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    student = students_db.get(session['student_id'])
    
    if not student or student.get('cluster_id') is None:
        return jsonify({
            'success': True,
            'has_recommendations': False,
            'message': 'Log at least 3 study sessions to get personalized recommendations'
        })
    
    cluster_id = student['cluster_id']
    cluster_profile = CLUSTER_PROFILES.get(cluster_id, CLUSTER_PROFILES[0])
    
    # Get student's recent performance
    student_logs = [log for log in study_logs_db if log['student_id'] == session['student_id']]
    recent_logs = sorted(student_logs, key=lambda x: x['date'], reverse=True)[:7]
    
    performance_data = {
        'dates': [log['date'] for log in recent_logs][::-1],
        'study_hours': [log['study_hours'] for log in recent_logs][::-1],
        'quiz_scores': [log['quiz_score'] for log in recent_logs if log['quiz_score']][::-1]
    }
    
    recommendation = {
        'success': True,
        'has_recommendations': True,
        'cluster_name': cluster_profile['name'],
        'cluster_description': cluster_profile['description'],
        'recommended_hours': cluster_profile['recommended_hours'],
        'break_interval': cluster_profile['break_interval'],
        'suggested_method': cluster_profile['suggested_method'],
        'recommended_tools': cluster_profile['recommended_tools'],
        'preferred_time': cluster_profile['preferred_time'],
        'performance_data': performance_data,
        'weekly_schedule': generate_weekly_schedule(cluster_profile)
    }
    
    return jsonify(recommendation)

def generate_weekly_schedule(cluster_profile):
    """Generate a weekly study schedule based on cluster profile"""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    base_hours = cluster_profile['recommended_hours']
    
    # Vary hours slightly across the week
    schedule = []
    for i, day in enumerate(days):
        variation = np.random.uniform(-0.5, 0.5)
        hours = max(1.0, base_hours + variation)
        schedule.append({
            'day': day,
            'hours': round(hours, 1)
        })
    
    return schedule

@app.route('/api/student-stats')
def student_stats():
    if 'student_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    student_logs = [log for log in study_logs_db if log['student_id'] == session['student_id']]
    
    if not student_logs:
        return jsonify({
            'total_sessions': 0,
            'total_hours': 0,
            'avg_score': 0,
            'current_streak': 0
        })
    
    total_hours = sum(log['study_hours'] for log in student_logs)
    scores = [log['quiz_score'] for log in student_logs if log['quiz_score']]
    avg_score = np.mean(scores) if scores else 0
    
    # Calculate streak
    dates = sorted(set(log['date'] for log in student_logs), reverse=True)
    streak = 0
    current_date = datetime.now().date()
    
    for date_str in dates:
        log_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if (current_date - log_date).days == streak:
            streak += 1
        else:
            break
    
    return jsonify({
        'total_sessions': len(student_logs),
        'total_hours': round(total_hours, 1),
        'avg_score': round(avg_score, 1),
        'current_streak': streak
    })

@app.route('/api/admin/upload-data', methods=['POST'])
def upload_data():
    if 'admin' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400
    
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_data.csv')
        file.save(filepath)
        
        # Copy to data folder for processing
        import shutil
        shutil.copy(filepath, 'data/sample_student_data.csv')
        
        return jsonify({'success': True, 'message': 'File uploaded successfully'})
    
    return jsonify({'success': False, 'message': 'Invalid file format'}), 400

@app.route('/api/admin/retrain-model', methods=['POST'])
def retrain_model():
    if 'admin' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        kmeans, scaler, df = train_clustering_model()
        
        return jsonify({
            'success': True,
            'message': 'Model retrained successfully',
            'clusters': 4,
            'samples': len(df)
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/admin/analytics')
def admin_analytics():
    if 'admin' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    # Generate analytics data
    analytics = {
        'total_students': len(students_db),
        'total_logs': len(study_logs_db),
        'active_students': len(set(log['student_id'] for log in study_logs_db)),
        'avg_study_hours': round(np.mean([log['study_hours'] for log in study_logs_db]) if study_logs_db else 0, 2),
        'cluster_distribution': {}
    }
    
    # Count students per cluster
    for student in students_db.values():
        cluster_id = student.get('cluster_id')
        if cluster_id is not None:
            cluster_name = CLUSTER_PROFILES[cluster_id]['name']
            analytics['cluster_distribution'][cluster_name] = \
                analytics['cluster_distribution'].get(cluster_name, 0) + 1
    
    return jsonify(analytics)

@app.route('/api/clustering-insights')
def clustering_insights():
    """Get detailed clustering insights for visualization"""
    try:
        df = pd.read_csv('data/sample_student_data.csv')
        
        # Calculate cluster statistics
        insights = {
            'cluster_profiles': CLUSTER_PROFILES,
            'total_students': len(df),
            'data_quality': 82  # Placeholder
        }
        
        return jsonify(insights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
