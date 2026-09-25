import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier

# 1. Load the Datasets
# Assuming the files are in the same directory. Change path if needed.
script_dir = os.path.dirname(os.path.abspath(__file__))
train_df = pd.read_csv(os.path.join(script_dir, "Training.csv"))
test_df = pd.read_csv(os.path.join(script_dir, "Testing.csv"))

# 2. Preprocessing & Feature Selection
# We remove 'fluid_overload' because it has no variance (it's always 0).
# We also drop the 'prognosis' column from the features (X).
unimportant_columns = ['fluid_overload']
X_train = train_df.drop(columns=['prognosis'] + unimportant_columns)
y_train = train_df['prognosis']

X_test = test_df.drop(columns=['prognosis'] + unimportant_columns)
y_test = test_df['prognosis']

# 3. Train the Model
# Random Forest is robust and handles binary symptom data very well.
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Check accuracy (Optional)
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy on Test Data: {accuracy * 100:.2f}%")

# 4. Prediction Function
def predict_top_3_diseases(user_symptoms):
    """
    Takes a list of symptoms (strings) and returns the top 3 predicted diseases.
    """
    # Get all valid feature names from the training data
    valid_features = X_train.columns.tolist()
    
    # Create an input vector of zeros (size equal to number of symptoms)
    input_vector = np.zeros(len(valid_features))
    
    # Match user symptoms to the feature columns
    # We use a simple normalization (strip spaces) to be more forgiving
    feature_map = {f.strip().lower(): i for i, f in enumerate(valid_features)}
    
    matched_symptoms = []
    for symptom in user_symptoms:
        clean_symptom = symptom.strip().lower()
        if clean_symptom in feature_map:
            index = feature_map[clean_symptom]
            input_vector[index] = 1
            matched_symptoms.append(valid_features[index])
        else:
            print(f"Warning: Symptom '{symptom}' not recognized. Ignored.")

    if not matched_symptoms:
        return "No valid symptoms provided."

    # Create a DataFrame for prediction to avoid the warning
    input_df = pd.DataFrame([input_vector], columns=valid_features)

    # Predict probabilities
    # Reshape input to (1, n_features) because we are predicting for a single instance
    probs = model.predict_proba(input_df)[0]
    
    # Get indices of the top 3 probabilities
    top_3_indices = probs.argsort()[-3:][::-1]
    
    # Get the corresponding disease names and probabilities
    classes = model.classes_
    results = []
    for i in top_3_indices:
        results.append((classes[i], probs[i]))
        
    return results

# ==========================================
# Example Usage
# ==========================================

# 1. List of all valid symptoms (User can choose from here)
print("\n--- Valid Symptoms List ---")
print(X_train.columns.tolist())

# 2. User Input Example
user_input = ['itching', 'skin_rash', 'chills'] 

print(f"\nUser Symptoms: {user_input}")
predictions = predict_top_3_diseases(user_input)

print("\n--- Top 3 Predicted Diseases ---")
for i, (disease, probability) in enumerate(predictions, 1):
    print(f"{i}. {disease} (Probability: {probability:.2f})")