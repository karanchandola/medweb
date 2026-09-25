# MedPredict - Complete File Documentation

This document explains the purpose and functionality of all Python files and important configuration files in the MedPredict project.

---

## 📁 Directory Structure

```
d:\medweb/
├── check_env.py                    # Environment checker script
├── list_models.py                  # Google Gemini model lister
├── FILE_DOCUMENTATION.md           # This file
├── web_app/                        # Django project directory
│   ├── manage.py                   # Django command-line utility
│   ├── db.sqlite3                  # SQLite database file
│   ├── .env                        # Environment variables (API keys)
│   ├── disease_predictor/          # Django project settings
│   │   ├── settings.py             # Django configuration
│   │   ├── urls.py                 # Main URL routing
│   │   ├── wsgi.py                 # WSGI app for deployment
│   │   └── __init__.py             # Package marker
│   └── prediction/                 # Django app
│       ├── views.py                # View functions for handling requests
│       ├── services.py             # DiseasePredictor service class
│       ├── urls.py                 # App-specific URL routing
│       ├── apps.py                 # App configuration
│       ├── __init__.py             # Package marker
│       ├── templatetags/           # Custom template filters
│       └── templates/prediction/   # HTML templates
│           ├── base.html           # Base template with navbar
│           ├── home.html           # Homepage
│           ├── about.html          # About page
│           ├── index.html          # Symptoms selector page
│           ├── results.html        # Prediction results page
│           └── chat.html           # AI chat interface
└── Disease-prediction-using-Machine-Learning/
    ├── model.py                    # Standalone ML model script
    ├── README.md                   # Project README
    ├── Training.csv                # Training dataset
    ├── Testing.csv                 # Testing dataset
    └── clean_code.py               # Legacy data cleaning script
```

---

## 🐍 Root-Level Python Files

### **check_env.py**
**Purpose**: Environment verification utility  
**Functionality**:
- Checks Python version
- Verifies Google Generative AI library installation
- Tests both `google.genai` and `google.generativeai` imports
- Displays installed package versions

**When to Use**: Run this to diagnose environment setup issues or verify dependencies are correctly installed.

**Command**: `python check_env.py`

---

### **list_models.py**
**Purpose**: Google Gemini API model discovery tool  
**Functionality**:
- Configures the Google Generative AI API with hardcoded API key
- Lists all available Gemini models
- Filters models that support `generateContent` method
- Displays compatible models for the application

**When to Use**: Run this to:
- Check which Gemini models are available
- Verify API connectivity
- Select the best model for your needs

**Command**: `python list_models.py`

**Note**: Currently uses `gemini-2.5-flash` model in the application

---

## 🎯 Django Web App Files

### **web_app/manage.py**
**Purpose**: Django's command-line utility  
**Functionality**:
- Run development server: `python manage.py runserver`
- Manage database migrations: `python manage.py migrate`
- Create admin users: `python manage.py createsuperuser`
- Execute custom management commands

**When to Use**: Always use this for all Django-related operations

---

### **web_app/.env**
**Purpose**: Environment variables configuration file  
**Contains**:
- Google API Key for Gemini AI integration
- Database connection details (if using external DB)
- Secret configuration data

**Note**: Keep this file **SECRET** and never commit to Git. Add to `.gitignore`.

---

## ⚙️ Disease Predictor Settings

### **disease_predictor/settings.py**
**Purpose**: Django project configuration  
**Key Configurations**:
- `DEBUG = True` (Set to False in production)
- `INSTALLED_APPS`: Registers Django apps including `prediction`
- `TEMPLATES`: Configures HTML template location
- `DATABASES`: SQLite configuration
- `STATIC_URL`: Static files (CSS, JS, images) configuration
- `ALLOWED_HOSTS`: Hosts allowed to run the app

**When to Edit**: 
- Add new installed apps
- Change database settings
- Configure static files serving
- Set DEBUG mode for production

---

### **disease_predictor/urls.py**
**Purpose**: Main URL router for the entire Django project  
**Functionality**:
- Routes requests to the `prediction` app
- Includes URL patterns from `prediction/urls.py`
- May include admin URL patterns

**URL Pattern**: `http://127.0.0.1:8000/[prediction_urls]`

---

### **disease_predictor/wsgi.py**
**Purpose**: WSGI application entry point  
**Functionality**:
- Serves the Django app via WSGI servers
- Used for deployment on platforms like Heroku, AWS, etc.
- Allows web servers (Gunicorn, uWSGI) to communicate with Django

**When to Use**: Deployment to production environments

---

## 📊 Prediction App (Core Application)

### **prediction/services.py**
**Purpose**: Core machine learning service  
**Main Class**: `DiseasePredictor`  
**Functionality**:
- Implements Singleton pattern (only one instance of the model)
- Loads and trains the Random Forest classifier on startup
- Provides methods:
  - `predict_diseases()`: Returns top 3 disease predictions
  - `get_categorized_symptoms()`: Returns symptoms organized by medical categories
  - `get_symptom_descriptions()`: Returns human-readable symptom descriptions

**Key Methods**:
```python
DiseasePredictor.get_instance()  # Get/create predictor instance
predictor.predict_diseases(selected_symptoms)  # Get predictions
predictor.get_categorized_symptoms()  # Get organized symptoms
```

**When Used**: Every time a user submits symptoms for prediction

**Data Source**: `Training.csv` from `Disease-prediction-using-Machine-Learning/`

---

### **prediction/views.py**
**Purpose**: View functions to handle HTTP requests and render responses  
**Main Functions**:

| Function | Route | Purpose |
|----------|-------|---------|
| `home_view()` | `/` | Renders homepage |
| `about_view()` | `/about/` | Renders About page |
| `predict_view()` | `/predict/` | Renders symptoms selection page |
| `get_results()` | `/get-results/` (AJAX) | Processes selected symptoms and returns predictions |
| `chat_view()` | `/chat/` | Renders AI doctor chat page |
| `send_message()` | `/send-message/` (AJAX) | Processes chat messages via Google Gemini API |
| `check_allergy_remedies()` | `/check-allergy/` (AJAX) | Generates allergy analysis and home remedies |
| `download_report()` | `/download/` | Generates and downloads PDF report |
| `clear_chat()` | `/clear-chat/` | Clears chat history |

**AI Integration**: Uses `google.generativeai` library to:
- Generate detailed disease explanations
- Answer health-related questions in the chat
- Provide personalized allergy and remedy suggestions

---

### **prediction/urls.py**
**Purpose**: App-specific URL routing  
**Functionality**:
- Maps URL paths to view functions
- Example patterns:
  - `''` → `home_view`
  - `'predict/'` → `predict_view`
  - `'chat/'` → `chat_view`
  - `'get-results/'` → AJAX for predictions

---

### **prediction/apps.py**
**Purpose**: Django app configuration  
**Functionality**:
- Registers the `prediction` app with Django
- May include app-ready initialization code

---

### **prediction/templatetags/** (Directory)
**Purpose**: Custom Django template filters  
**Functionality**: 
- Extends Jinja2 template capabilities
- Custom filters for template rendering (if any exist)

---

## 🎨 HTML Templates (`prediction/templates/prediction/`)

### **base.html**
**Purpose**: Base template for all pages  
**Contains**:
- Navigation bar with links to Home, About, Prediction, Chat
- Common CSS and JavaScript imports
- Template blocks (`{% block content %}`, `{% block extra_css %}`)
- Footer with disclaimer and links

**Usage**: All other templates extend this template

---

### **home.html**
**Purpose**: Homepage landing page  
**Features**:
- Hero section with app title and CTA button
- Feature cards highlighting key capabilities
- How-it-works section with steps
- Medical disclaimer box

**Key Elements**:
- "Check My Symptoms" button (centered)
- Features: Symptom Checker, AI Predictions, Personalized Reports
- Responsive design

---

### **about.html**
**Purpose**: About page with project information  
**Contains**:
- Mission statement
- Core features explanation
- Technology stack details
- Medical disclaimer
- Team or project information

---

### **index.html** (Symptom Selector)
**Purpose**: Main symptom selection interface  
**Features**:
- Searchable symptom list organized by categories
- Multi-select checkboxes for symptoms
- Search functionality to find symptoms quickly
- "Submit" button to send symptoms for prediction

**Interaction**: User selects symptoms → AJAX call to `/get-results/`

---

### **results.html**
**Purpose**: Display prediction results  
**Shows**:
- Top 3 predicted diseases with confidence percentages
- Progress bars showing prediction confidence
- Disease descriptions
- Precautions and lifestyle changes
- Medications and workouts
- Diet recommendations
- "Update for Allergies" button to get remedy suggestions
- Download PDF report option

**Interaction**: 
- Loads prediction data via AJAX
- Displays results dynamically
- Allows allergy analysis

---

### **chat.html**
**Purpose**: AI Doctor Chat interface  
**Features**:
- Chat message display area
- Message input box
- Send button
- Markdown support for rich text responses
- Clear chat history button
- Message styling (user vs. AI responses)

**Interaction**:
- User types question → AJAX call to `/send-message/`
- AI responds using Google Gemini API
- Real-time chat display with scrolling

---

## 📊 Machine Learning Files

### **Disease-prediction-using-Machine-Learning/model.py**
**Purpose**: Standalone ML model training script  
**Functionality**:
- Loads `Training.csv` and `Testing.csv`
- Trains Random Forest Classifier
- Implements `predict_top_3_diseases()` function
- Tests model accuracy on test data

**Key Features**:
- Removes low-variance features (`fluid_overload`)
- Returns top 3 predictions with probabilities
- Matches user symptoms to training features

**Note**: This is the original standalone script. The Django app uses a similar implementation in `services.py`.

---

### **Disease-prediction-using-Machine-Learning/Training.csv**
**Purpose**: Training dataset for the ML model  
**Contains**:
- 4,920 records of symptom-disease pairs
- 131 symptom columns (binary: 0 or 1)
- 1 target column: `prognosis` (disease name)

**Usage**: Used to train the Random Forest Classifier

---

### **Disease-prediction-using-Machine-Learning/Testing.csv**
**Purpose**: Testing dataset for model validation  
**Contains**:
- Similar structure to Training.csv
- ~1,000 test samples for model evaluation
- Used to calculate model accuracy

---

### **Disease-prediction-using-Machine-Learning/clean_code.py**
**Purpose**: Legacy data cleaning and preprocessing script  
**Status**: May be outdated  
**Functionality** (if still in use):
- Cleans CSV files
- Handles missing values
- Prepares data for model training

---

## 📁 Static Files & Database

### **web_app/db.sqlite3**
**Purpose**: SQLite database file  
**Contains**:
- Django default tables (users, sessions, etc.)
- Custom models (if defined)

**When to Reset**: `python manage.py migrate` (creates new empty DB)

---

## 🔐 Important Notes

### **API Key Management**
- Google API Key is stored in `.env` file
- Never hardcode keys in `.py` files (except `list_models.py` for testing)
- Always add `.env` to `.gitignore`

### **Model Training**
- Random Forest Classifier loads on first request
- Cached in memory for performance
- Uses Singleton pattern to avoid retraining

### **AI Integration**
- Uses `google.generativeai` library (v0.8.5)
- Model: `gemini-2.5-flash`
- Handles chat, disease explanations, and allergy analysis

### **Data Flow**
1. User selects symptoms in `index.html`
2. AJAX request to `predict_view()` → `get_results()`
3. `DiseasePredictor` loads model and predicts
4. Results returned to `results.html`
5. User can ask follow-up questions in chat
6. Chat messages sent to `chat_view()` → Google Gemini API

---

## 🚀 Quick Reference Commands

| Command | Purpose |
|---------|---------|
| `python manage.py runserver` | Start development server |
| `python manage.py migrate` | Apply database migrations |
| `python check_env.py` | Verify environment setup |
| `python list_models.py` | List available Gemini models |
| `pip install -r requirements.txt` | Install dependencies |

---

**Last Updated**: December 16, 2025  
**Version**: 1.0
