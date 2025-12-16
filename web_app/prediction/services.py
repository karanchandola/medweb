import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from django.conf import settings

class DiseasePredictor:
    _instance = None
    _model = None
    _valid_features = None
    _classes = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._model is None:
            self._train_model()

    def _train_model(self):
        # Define paths to CSV files
        # Assuming the structure:
        # d:\medweb\web_app\ (Django Project)
        # d:\medweb\Disease-prediction-using-Machine-Learning\ (Data)
        
        base_dir = settings.BASE_DIR
        data_dir = base_dir.parent / 'Disease-prediction-using-Machine-Learning'
        
        train_path = data_dir / "Training.csv"
        test_path = data_dir / "Testing.csv"

        if not train_path.exists():
            raise FileNotFoundError(f"Training data not found at {train_path}")

        train_df = pd.read_csv(train_path)
        # test_df = pd.read_csv(test_path) # Not strictly needed for prediction, only for validation

        unimportant_columns = ['fluid_overload']
        X_train = train_df.drop(columns=['prognosis'] + unimportant_columns)
        y_train = train_df['prognosis']

        self._model = RandomForestClassifier(random_state=42)
        self._model.fit(X_train, y_train)
        
        self._valid_features = X_train.columns.tolist()
        self._classes = self._model.classes_

    def get_all_symptoms(self):
        if self._valid_features is None:
            self._train_model()
        return self._valid_features

    def get_categorized_symptoms(self):
        if self._valid_features is None:
            self._train_model()
            
        # Define categories based on user request
        categories = {
            "General": [
                "fever", "high_fever", "mild_fever", "fatigue", "chills", "shivering", "sweating", "dehydration", 
                "headache", "dizziness", "weight_loss", "weight_gain", "lethargy", "restlessness", "malaise", 
                "excessive_hunger", "loss_of_appetite", "increased_appetite", "polyuria"
            ],
            "Respiratory": [
                "cough", "breathlessness", "phlegm", "throat_irritation", "sinus_pressure", "runny_nose", 
                "congestion", "continuous_sneezing", "mucoid_sputum", "rusty_sputum", "blood_in_sputum"
            ],
            "Digestive": [
                "stomach_pain", "acidity", "vomiting", "nausea", "indigestion", "constipation", "abdominal_pain", 
                "diarrhoea", "stomach_bleeding", "distention_of_abdomen", "bloody_stool", "pain_during_bowel_movements", 
                "pain_in_anal_region", "irritation_in_anus", "passage_of_gases", "belly_pain"
            ],
            "Skin": [
                "itching", "skin_rash", "nodal_skin_eruptions", "ulcers_on_tongue", "patches_in_throat", 
                "yellowish_skin", "bruising", "red_spots_over_body", "dischromic _patches", "pus_filled_pimples", 
                "blackheads", "scurring", "skin_peeling", "silver_like_dusting", "small_dents_in_nails", 
                "inflammatory_nails", "blister", "red_sore_around_nose", "yellow_crust_ooze", "internal_itching"
            ],
            "Musculoskeletal": [
                "joint_pain", "muscle_wasting", "muscle_weakness", "back_pain", "neck_pain", "knee_pain", 
                "hip_joint_pain", "swelling_joints", "movement_stiffness", "muscle_pain", "painful_walking", 
                "stiff_neck", "swollen_legs", "swollen_extremeties", "prominent_veins_on_calf"
            ],
            "Neurological": [
                "anxiety", "mood_swings", "depression", "irritability", "altered_sensorium", "lack_of_concentration", 
                "visual_disturbances", "coma", "slurred_speech", "loss_of_balance", "unsteadiness", 
                "weakness_of_one_body_side", "spinning_movements", "loss_of_smell"
            ],
            "Cardiovascular": [
                "chest_pain", "fast_heart_rate", "palpitations", "swollen_blood_vessels"
            ],
            "Other": [
                "burning_micturition", "spotting_ urination", "dark_urine", "yellow_urine", "pain_behind_the_eyes", 
                "blurred_and_distorted_vision", "redness_of_eyes", "yellowing_of_eyes", "watering_from_eyes", 
                "puffy_face_and_eyes", "sunken_eyes", "family_history", "history_of_alcohol_consumption", 
                "receiving_blood_transfusion", "receiving_unsterile_injections", "abnormal_menstruation", 
                "bladder_discomfort", "foul_smell_of urine", "continuous_feel_of_urine", "acute_liver_failure", 
                "fluid_overload", "swelling_of_stomach", "swelled_lymph_nodes", "enlarged_thyroid", 
                "drying_and_tingling_lips", "irregular_sugar_level", "cold_hands_and_feets", "brittle_nails"
            ]
        }
        
        # Ensure all valid features are included, even if I missed some in the manual mapping
        categorized_data = {k: [] for k in categories.keys()}
        categorized_data["Uncategorized"] = []
        
        # Create a set of all mapped symptoms for quick lookup
        mapped_symptoms = set()
        for cat_list in categories.values():
            mapped_symptoms.update(cat_list)
            
        # Populate the result dictionary
        for feature in self._valid_features:
            feature_clean = feature.strip()
            found = False
            for category, symptoms in categories.items():
                if feature_clean in symptoms:
                    categorized_data[category].append(feature)
                    found = True
                    break
            if not found:
                categorized_data["Uncategorized"].append(feature)
                
        # Remove empty categories
        return {k: sorted(v) for k, v in categorized_data.items() if v}

    def get_remedies(self, disease):
        # Basic remedy database (can be expanded or moved to a database model)
        remedies_db = {
            "Fungal infection": ["Keep area dry and clean", "Use antifungal creams", "Wear loose cotton clothes", "Avoid sharing personal items"],
            "Allergy": ["Avoid known allergens", "Take antihistamines", "Use saline nasal sprays", "Keep windows closed during pollen season"],
            "GERD": ["Avoid spicy and fatty foods", "Eat smaller meals", "Don't lie down immediately after eating", "Elevate head while sleeping"],
            "Chronic cholestasis": ["Low-fat diet", "Vitamin supplements (A, D, E, K)", "Cool baths for itching", "Stay hydrated"],
            "Drug Reaction": ["Stop the suspected medication immediately", "Apply cool compresses", "Wear loose clothing", "Drink plenty of water"],
            "Peptic ulcer diseae": ["Avoid spicy foods", "Limit alcohol and caffeine", "Eat probiotic-rich foods", "Manage stress"],
            "AIDS": ["Follow antiretroviral therapy strictly", "Eat a balanced, nutritious diet", "Practice safe hygiene", "Get regular rest"],
            "Diabetes ": ["Monitor blood sugar regularly", "Follow a low-carb diet", "Exercise daily", "Stay hydrated"],
            "Gastroenteritis": ["Drink plenty of fluids (ORS)", "Eat bland foods (BRAT diet)", "Rest", "Avoid dairy and caffeine"],
            "Bronchial Asthma": ["Use inhalers as prescribed", "Avoid triggers (smoke, dust)", "Practice breathing exercises", "Keep warm"],
            "Hypertension ": ["Reduce salt intake", "Exercise regularly", "Manage stress", "Limit alcohol"],
            "Migraine": ["Rest in a dark, quiet room", "Apply cold or warm compresses", "Stay hydrated", "Practice relaxation techniques"],
            "Cervical spondylosis": ["Neck exercises", "Maintain good posture", "Use a supportive pillow", "Apply heat or cold packs"],
            "Paralysis (brain hemorrhage)": ["Physical therapy", "Speech therapy", "Healthy diet", "Regular medical checkups"],
            "Jaundice": ["Rest", "Drink plenty of fluids", "Eat light, digestible foods", "Avoid alcohol"],
            "Malaria": ["Take prescribed antimalarial medication", "Rest", "Drink fluids", "Use mosquito nets"],
            "Chicken pox": ["Calamine lotion for itching", "Cool baths with baking soda", "Rest", "Stay isolated"],
            "Dengue": ["Rest", "Drink plenty of fluids", "Take paracetamol for fever (avoid aspirin)", "Monitor platelet count"],
            "Typhoid": ["Antibiotics as prescribed", "Drink boiled water", "Eat soft, cooked foods", "Rest"],
            "hepatitis A": ["Rest", "Hydration", "Avoid alcohol", "Eat small, frequent meals"],
            "Hepatitis B": ["Antiviral medications", "Rest", "Healthy diet", "Avoid alcohol"],
            "Hepatitis C": ["Antiviral medications", "Avoid alcohol", "Healthy diet", "Regular checkups"],
            "Hepatitis D": ["Interferon therapy", "Supportive care", "Avoid alcohol", "Healthy lifestyle"],
            "Hepatitis E": ["Rest", "Hydration", "Avoid alcohol", "Good hygiene"],
            "Alcoholic hepatitis": ["Stop alcohol consumption immediately", "Nutritional support", "Medical supervision", "Hydration"],
            "Tuberculosis": ["Complete course of antibiotics", "Good nutrition", "Rest", "Cover mouth while coughing"],
            "Common Cold": ["Rest", "Hydration", "Warm salt water gargle", "Steam inhalation"],
            "Pneumonia": ["Antibiotics (if bacterial)", "Rest", "Fluids", "Humidifier"],
            "Dimorphic hemmorhoids(piles)": ["High-fiber diet", "Sitz baths", "Stay hydrated", "Avoid straining"],
            "Heart attack": ["Immediate medical attention", "Lifestyle changes", "Medication adherence", "Cardiac rehabilitation"],
            "Varicose veins": ["Compression stockings", "Elevate legs", "Exercise", "Avoid standing for long periods"],
            "Hypothyroidism": ["Thyroid hormone replacement", "Balanced diet", "Regular exercise", "Stress management"],
            "Hyperthyroidism": ["Antithyroid medications", "Beta-blockers", "Radioactive iodine", "Surgery (if needed)"],
            "Hypoglycemia": ["Consume fast-acting sugar (juice, candy)", "Regular meals", "Monitor blood sugar", "Carry snacks"],
            "Osteoarthristis": ["Exercise", "Weight management", "Pain relief creams", "Physical therapy"],
            "Arthritis": ["Anti-inflammatory diet", "Gentle exercise", "Hot/cold therapy", "Joint protection"],
            "(vertigo) Paroymsal  Positional Vertigo": ["Epley maneuver", "Brandt-Daroff exercises", "Avoid sudden head movements", "Sleep with head elevated"],
            "Acne": ["Keep face clean", "Use non-comedogenic products", "Avoid touching face", "Over-the-counter creams"],
            "Urinary tract infection": ["Drink plenty of water", "Cranberry juice", "Antibiotics", "Good hygiene"],
            "Psoriasis": ["Moisturize", "Sunlight exposure (moderate)", "Medicated creams", "Avoid triggers"],
            "Impetigo": ["Antibiotic ointment", "Keep area clean", "Wash clothes in hot water", "Avoid scratching"]
        }
        return remedies_db.get(disease, ["Consult a doctor for specific advice", "Rest and hydration", "Monitor symptoms"])

    def is_severe(self, disease):
        severe_diseases = [
            "Heart attack", "Paralysis (brain hemorrhage)", "AIDS", "Hepatitis B", "Hepatitis C", 
            "Hepatitis D", "Typhoid", "Malaria", "Dengue", "Tuberculosis", "Pneumonia", "Hypoglycemia"
        ]
        return disease in severe_diseases

    def predict(self, user_symptoms):
        if self._model is None:
            self._train_model()

        # Create an input vector of zeros
        input_vector = np.zeros(len(self._valid_features))
        
        # Match user symptoms to the feature columns
        feature_map = {f.strip().lower(): i for i, f in enumerate(self._valid_features)}
        
        matched_symptoms = []
        for symptom in user_symptoms:
            clean_symptom = symptom.strip().lower()
            if clean_symptom in feature_map:
                index = feature_map[clean_symptom]
                input_vector[index] = 1
                matched_symptoms.append(self._valid_features[index])
        
        if not matched_symptoms:
            return None, "No valid symptoms provided."

        # Create DataFrame for prediction to avoid warning
        input_df = pd.DataFrame([input_vector], columns=self._valid_features)

        # Predict probabilities
        probs = self._model.predict_proba(input_df)[0]
        
        # Get indices of the top 3 probabilities
        top_3_indices = probs.argsort()[-3:][::-1]
        
        results = []
        for i in top_3_indices:
            if probs[i] > 0: # Only return if there is some probability
                disease_name = self._classes[i]
                results.append({
                    'disease': disease_name,
                    'probability': round(probs[i] * 100, 2),
                    'remedies': self.get_remedies(disease_name),
                    'is_severe': self.is_severe(disease_name)
                })
            
        return results, None
