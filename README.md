# MedPredict - AI-Powered Disease Prediction System

MedPredict is an advanced web application designed to help users identify potential health issues based on their symptoms. By combining traditional Machine Learning algorithms with modern Generative AI (Google Gemini), MedPredict offers accurate disease predictions, personalized health advice, and an interactive AI doctor chat.

## 🚀 Features

- **Symptom Checker**: Select from a comprehensive list of symptoms to get an instant analysis.
- **Disease Prediction**: Uses a Random Forest Classifier trained on medical datasets to predict potential diseases with high accuracy.
- **AI Doctor Chat**: Interactive chat interface powered by Google Gemini 2.5 Flash to answer your health-related queries.
- **Smart Reports**: Detailed prediction results including:
  - Disease description
  - Precautions and lifestyle changes
  - Medications and workouts
  - Diet recommendations
- **Allergy & Remedy Analysis**: AI-driven suggestions for allergies and home remedies.
- **Responsive Design**: Modern, user-friendly interface that works on all devices.

## 🛠️ Technology Stack

- **Backend**: Django 6.0 (Python 3.13)
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **AI Integration**: Google Generative AI (Gemini 2.5 Flash)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (Default Django DB)

## 📋 Prerequisites

- Python 3.10 or higher
- Google Gemini API Key

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/medpredict.git
   cd medpredict
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**
   Create a `.env` file in the project root (or set directly in your environment) and add your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the App**
   Open your browser and go to `http://127.0.0.1:8000/`

## 🧠 How It Works

1. **Data Processing**: The system uses a pre-trained Machine Learning model (`model.py`) based on the `Training.csv` dataset.
2. **Prediction**: When a user submits symptoms, the backend processes the input and queries the ML model.
3. **AI Enhancement**: The application leverages Google's Gemini AI to provide human-like explanations, additional context, and answer follow-up questions in the chat.

## ⚠️ Disclaimer

**MedPredict is for informational purposes only.** It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
