# Quick Start Guide - Study Habits Recommender

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

Open terminal/command prompt in the project folder and run:

**Windows:**
```cmd
python -m pip install -r requirements.txt
```

**macOS/Linux:**
```bash
python3 -m pip install -r requirements.txt
```

### Step 2: Run the Application

**Option A - Using run scripts (Recommended):**

Windows:
```cmd
run.bat
```

macOS/Linux:
```bash
./run.sh
```

**Option B - Manual:**
```bash
python app.py
```

### Step 3: Access the Application

Open your browser and go to:
```
http://localhost:5000
```

## 🎓 Student Portal Quick Guide

1. **Login**
   - Click "Student Portal"
   - Enter your name and email
   - Click "Sign In"

2. **Log Your First Study Session**
   - Fill in the form with your study details
   - Click "Save Log"
   - Repeat for at least 3 sessions

3. **Get Recommendations**
   - After 3+ sessions, view your personalized recommendations
   - See your learning cluster type
   - Follow the suggested study plan

## 👨‍💼 Admin Portal Quick Guide

1. **Login**
   - Click "Admin Portal"
   - Username: `admin`
   - Password: `admin123`

2. **View Dashboard**
   - See total students and sessions
   - View cluster distribution
   - Monitor recent activity

3. **Upload Data (Optional)**
   - Prepare CSV file with columns:
     ```
     student_id, study_hours, quiz_score, distraction_frequency, preferred_time, study_method
     ```
   - Click "Upload Dataset"
   - Select your CSV file

4. **Retrain Model**
   - Click "Retrain Model"
   - Wait for completion
   - View updated analytics

## 📊 Understanding Your Cluster

### Focused Studiers 🌟
- **You are**: Disciplined with long study sessions
- **Best time**: Morning (8am-12pm)
- **Recommended**: Pomodoro Technique with 25-min breaks
- **Tools**: Focus music, digital notes, Pomodoro timer

### Short Burst Learners ⚡
- **You are**: Active learner with brief sessions
- **Best time**: Afternoon (2pm-6pm)
- **Recommended**: Spaced repetition
- **Tools**: Flashcards, video tutorials, quick quizzes

### Night Owls 🌙
- **You are**: Late-night studier with deep focus
- **Best time**: Night (8pm-12am)
- **Recommended**: Deep work sessions
- **Tools**: Site blockers, ambient sounds, practice problems

### Distracted Learners 🔀
- **You are**: Easily interrupted, need structure
- **Best time**: Evening (6pm-8pm)
- **Recommended**: Structured environment
- **Tools**: Website blockers, study groups, accountability apps

## 🛠️ Troubleshooting

### Application won't start
- Check Python version: `python --version` (need 3.8+)
- Reinstall dependencies: `pip install -r requirements.txt`
- Check if port 5000 is available

### Can't see recommendations
- Log at least 3 study sessions first
- Make sure to include quiz scores
- Try refreshing the recommendations

### Upload fails
- Check CSV format matches expected columns
- File size should be under 16MB
- Use UTF-8 encoding

### Model training fails
- Ensure CSV has valid data
- Check for missing values
- Verify numeric columns are numbers

## 📝 Tips for Best Results

1. **Log Consistently**: Track your study sessions daily
2. **Be Honest**: Accurate logs = better recommendations
3. **Include Quiz Scores**: Helps the system learn what works
4. **Try Recommendations**: Follow suggestions for at least a week
5. **Adjust**: Feedback helps improve your profile

## 🎯 Sample Study Log

```
Date: 2025-10-29
Study Hours: 3.5
Subject: Data Science
Study Time: Morning
Method: Pomodoro
Distractions: Low
Quiz Score: 85
```

## 🔍 Need More Help?

- Read the full README.md
- Check code comments in app.py
- Review the project documentation PDF
- Test with sample data first

## ✨ Pro Tips

- **Morning people**: Study 8am-12pm for complex topics
- **Night owls**: Use 10pm-2am for deep work
- **Easily distracted**: Use website blockers actively
- **Visual learners**: Add videos to study routine
- **Auditory learners**: Try explaining concepts aloud

---

**Happy Studying! 📚**

Remember: Consistency beats intensity. Study smart, not just hard!
