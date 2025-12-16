from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from .services import DiseasePredictor
import google.generativeai as genai
import json
import uuid
from datetime import datetime
from django.conf import settings

def home_view(request):
    return render(request, 'prediction/home.html')

def about_view(request):
    return render(request, 'prediction/about.html')

def predict_view(request):
    predictor = DiseasePredictor.get_instance()
    raw_categorized_symptoms = predictor.get_categorized_symptoms()
    
    # Symptom descriptions mapping
    symptom_descriptions = {
        'itching': 'Irritating sensation that makes you want to scratch',
        'skin_rash': 'Noticeable change in the texture or color of your skin',
        'nodal_skin_eruptions': 'Small, raised bumps on the skin',
        'continuous_sneezing': 'Sneezing that happens repeatedly without stopping',
        'shivering': 'Involuntary shaking of the body',
        'chills': 'Feeling cold with shivering',
        'joint_pain': 'Discomfort or soreness in joints',
        'stomach_pain': 'Pain in the abdominal area',
        'acidity': 'Burning sensation in the chest or throat',
        'ulcers_on_tongue': 'Open sores on the tongue',
        'muscle_wasting': 'Loss of muscle mass',
        'vomiting': 'Forceful expulsion of stomach contents',
        'burning_micturition': 'Pain or burning sensation during urination',
        'spotting_ urination': 'Small amounts of blood in urine',
        'fatigue': 'Feeling tired or exhausted',
        'weight_gain': 'Abnormal increase in body weight',
        'anxiety': 'Feeling of worry, nervousness, or unease',
        'cold_hands_and_feets': 'Extremities feel cold to the touch',
        'mood_swings': 'Rapid changes in mood',
        'weight_loss': 'Unexplained decrease in body weight',
        'restlessness': 'Inability to rest or relax',
        'lethargy': 'Lack of energy and enthusiasm',
        'patches_in_throat': 'White or red patches in the throat',
        'irregular_sugar_level': 'Fluctuating blood sugar levels',
        'cough': 'Expelling air from the lungs with a sudden sound',
        'high_fever': 'Body temperature significantly above normal',
        'sunken_eyes': 'Eyes appearing hollow or dark',
        'breathlessness': 'Difficulty breathing or shortness of breath',
        'sweating': 'Perspiring more than usual',
        'dehydration': 'Loss of body fluids',
        'indigestion': 'Discomfort in the upper abdomen',
        'headache': 'Pain in the head or neck region',
        'yellowish_skin': 'Skin turning yellow (Jaundice)',
        'dark_urine': 'Urine appearing darker than normal',
        'nausea': 'Feeling of sickness with an inclination to vomit',
        'loss_of_appetite': 'Reduced desire to eat',
        'pain_behind_the_eyes': 'Discomfort located behind the eyes',
        'back_pain': 'Physical discomfort occurring anywhere on the spine or back',
        'constipation': 'Difficulty in emptying the bowels',
        'abdominal_pain': 'Pain in the belly area',
        'diarrhoea': 'Loose, watery stools',
        'mild_fever': 'Slightly elevated body temperature',
        'yellow_urine': 'Bright yellow colored urine',
        'yellowing_of_eyes': 'Whites of the eyes turning yellow',
        'acute_liver_failure': 'Rapid loss of liver function',
        'fluid_overload': 'Excess fluid in the body',
        'swelling_of_stomach': 'Abdominal distension',
        'swelled_lymph_nodes': 'Enlarged lymph nodes',
        'malaise': 'General feeling of discomfort or illness',
        'blurred_and_distorted_vision': 'Unclear or warped sight',
        'phlegm': 'Thick mucus secreted by the respiratory system',
        'throat_irritation': 'Scratchy or sore throat',
        'redness_of_eyes': 'Eyes appearing red or bloodshot',
        'sinus_pressure': 'Pain or pressure in the face/sinuses',
        'runny_nose': 'Excess drainage from the nose',
        'congestion': 'Blocked or stuffy nose',
        'chest_pain': 'Discomfort or pain in the chest',
        'weakness_in_limbs': 'Loss of strength in arms or legs',
        'fast_heart_rate': 'Heart beating faster than normal',
        'pain_during_bowel_movements': 'Discomfort when passing stool',
        'pain_in_anal_region': 'Pain in or around the anus',
        'bloody_stool': 'Blood present in feces',
        'irritation_in_anus': 'Itching or discomfort in the anal area',
        'neck_pain': 'Discomfort in the neck area',
        'dizziness': 'Feeling lightheaded or unsteady',
        'cramps': 'Sudden, involuntary muscle contractions',
        'bruising': 'Discoloration of the skin from injury',
        'obesity': 'Excessive body fat',
        'swollen_legs': 'Enlargement of the legs due to fluid',
        'swollen_blood_vessels': 'Enlarged veins or arteries',
        'puffy_face_and_eyes': 'Swelling in the face and eye area',
        'enlarged_thyroid': 'Swelling in the neck (Goiter)',
        'brittle_nails': 'Nails that break or crumble easily',
        'swollen_extremeties': 'Swelling in hands or feet',
        'excessive_hunger': 'Feeling unusually hungry',
        'extra_marital_contacts': 'History of sexual contact outside relationship',
        'drying_and_tingling_lips': 'Dry, prickly sensation on lips',
        'slurred_speech': 'Difficulty articulating words',
        'knee_pain': 'Discomfort in the knee joint',
        'hip_joint_pain': 'Pain in the hip area',
        'muscle_weakness': 'Reduced muscle strength',
        'stiff_neck': 'Difficulty moving the neck',
        'swelling_joints': 'Enlarged or puffy joints',
        'movement_stiffness': 'Difficulty moving freely',
        'spinning_movements': 'Sensation of spinning (Vertigo)',
        'loss_of_balance': 'Difficulty maintaining stability',
        'unsteadiness': 'Feeling wobbly or unstable',
        'weakness_of_one_body_side': 'Loss of strength on one side',
        'loss_of_smell': 'Inability to perceive odors',
        'bladder_discomfort': 'Pain or pressure in the bladder',
        'foul_smell_of urine': 'Unpleasant odor from urine',
        'continuous_feel_of_urine': 'Constant urge to urinate',
        'passage_of_gases': 'Passing gas (flatulence)',
        'internal_itching': 'Itching sensation inside the body',
        'toxic_look_(typhos)': 'Appearing very ill or exhausted',
        'depression': 'Persistent feeling of sadness',
        'irritability': 'Easily annoyed or angered',
        'muscle_pain': 'Aching or pain in muscles',
        'altered_sensorium': 'Changes in awareness or consciousness',
        'red_spots_over_body': 'Small red marks on the skin',
        'belly_pain': 'Pain in the stomach region',
        'abnormal_menstruation': 'Irregular or painful periods',
        'dischromic _patches': 'Discolored patches on skin',
        'watering_from_eyes': 'Excessive tearing',
        'increased_appetite': 'Wanting to eat more than usual',
        'polyuria': 'Frequent urination',
        'family_history': 'Genetic predisposition to conditions',
        'mucoid_sputum': 'Mucus-like substance coughed up',
        'rusty_sputum': 'Reddish-brown phlegm',
        'lack_of_concentration': 'Difficulty focusing',
        'visual_disturbances': 'Problems with vision',
        'receiving_blood_transfusion': 'History of blood transfusion',
        'receiving_unsterile_injections': 'History of unsafe injections',
        'coma': 'State of prolonged unconsciousness',
        'stomach_bleeding': 'Blood in vomit or stool',
        'distention_of_abdomen': 'Swollen belly',
        'history_of_alcohol_consumption': 'Regular alcohol use',
        'fluid_overload': 'Retention of fluid',
        'blood_in_sputum': 'Coughing up blood',
        'prominent_veins_on_calf': 'Visible veins on lower legs',
        'palpitations': 'Noticeable heartbeats',
        'painful_walking': 'Pain when walking',
        'pus_filled_pimples': 'Acne with pus',
        'blackheads': 'Small dark bumps on skin',
        'scurring': 'Scarring of skin',
        'skin_peeling': 'Outer layer of skin shedding',
        'silver_like_dusting': 'Scaly skin texture',
        'small_dents_in_nails': 'Pitting on nail surface',
        'inflammatory_nails': 'Red, swollen nails',
        'blister': 'Fluid-filled bubble on skin',
        'red_sore_around_nose': 'Painful red spots near nose',
        'yellow_crust_ooze': 'Yellowish discharge from sores'
    }

    # Pre-process symptoms for display to avoid custom template filters
    categorized_symptoms = {}
    for category, symptoms in raw_categorized_symptoms.items():
        formatted_symptoms = []
        for symptom in symptoms:
            formatted_symptoms.append({
                'id': symptom,
                'name': symptom.replace('_', ' ').title(),
                'description': symptom_descriptions.get(symptom, 'Common symptom')
            })
        categorized_symptoms[category] = formatted_symptoms
    
    predictions = None
    error = None
    selected_symptoms = []

    if request.method == 'POST':
        # Try to get from multi-select
        selected_symptoms = request.POST.getlist('symptoms')
        
        # If empty, check if it came from a text input (optional fallback)
        if not selected_symptoms:
             raw_input = request.POST.get('raw_symptoms')
             if raw_input:
                 selected_symptoms = [s.strip() for s in raw_input.split(',') if s.strip()]
        
        if selected_symptoms:
            predictions, error = predictor.predict(selected_symptoms)
            if not error:
                # Fetch disease descriptions using Gemini
                api_key = getattr(settings, 'GEMINI_API_KEY', None) or request.session.get('gemini_api_key')
                
                if api_key and predictions:
                    try:
                        disease_names = [p['disease'] for p in predictions]
                        
                        # Configure the Gemini API
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        
                        prompt = f"""
                        Provide detailed medical information for the following diseases: {', '.join(disease_names)}.
                        For each disease, provide a JSON object with the following keys:
                        1. "description": Brief description (what it is, causes, key symptoms). Use **bold** for key terms.
                        2. "severity": One of "Low", "Medium", "High".
                        3. "precautions": A list of 3-4 important precautions.
                        4. "remedies": A list of 3-4 effective home remedies (e.g., ginger tea, turmeric milk, steam inhalation).
                        
                        Format the output as a JSON object where keys are the exact disease names and values are the objects described above.
                        Example JSON: 
                        {{
                            "Disease Name": {{
                                "description": "...",
                                "severity": "Medium",
                                "precautions": ["Rest", "Hydration"],
                                "remedies": ["Ginger tea", "Honey"]
                            }}
                        }}
                        """
                        
                        response = model.generate_content(
                            prompt,
                            generation_config=genai.types.GenerationConfig(
                                response_mime_type="application/json"
                            )
                        )
                        
                        details = json.loads(response.text)
                        
                        # Merge details into predictions
                        for pred in predictions:
                            d = details.get(pred['disease'], {})
                            pred['description'] = d.get('description', "Description unavailable.")
                            pred['severity'] = d.get('severity', "Unknown")
                            pred['precautions'] = d.get('precautions', [])
                            pred['remedies'] = d.get('remedies', [])
                            
                    except Exception as e:
                        print(f"Error fetching descriptions: {e}")
                        import traceback
                        traceback.print_exc()
                        error_msg = str(e)
                        for pred in predictions:
                            pred['description'] = f"Description unavailable. Error: {error_msg}"
                            pred['severity'] = "Unknown"
                            pred['precautions'] = []
                            pred['remedies'] = []

                # Format selected symptoms for display
                formatted_selected_symptoms = [s.replace('_', ' ').title() for s in selected_symptoms]

                return render(request, 'prediction/results.html', {
                    'predictions': predictions,
                    'error': None,
                    'selected_symptoms': formatted_selected_symptoms
                })
        else:
            error = "Please select at least one symptom."

    return render(request, 'prediction/index.html', {
        'categorized_symptoms': categorized_symptoms,
        'predictions': predictions,
        'error': error,
        'selected_symptoms': selected_symptoms
    })

def check_allergy_remedies(request):
    if request.method == 'POST':
        disease = request.POST.get('disease')
        allergies = request.POST.get('allergies')
        
        api_key = getattr(settings, 'GEMINI_API_KEY', None) or request.session.get('gemini_api_key')
        
        if not api_key:
            return JsonResponse({'success': False, 'error': 'API Key not configured'})
            
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
            The patient has been diagnosed with {disease} but has allergies to: {allergies}.
            Please suggest 4-5 safe, natural home remedies for {disease} that do NOT contain these allergens.
            Focus on traditional cures like ginger stew, turmeric milk, herbal teas, etc.
            Return ONLY a JSON array of strings, e.g., ["Ginger Tea", "Steam Inhalation"].
            """
            
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json"
                )
            )
            
            remedies = json.loads(response.text)
            return JsonResponse({'success': True, 'remedies': remedies})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def set_api_key(request):
    if request.method == 'POST':
        api_key = request.POST.get('api_key')
        if api_key:
            request.session['gemini_api_key'] = api_key
    return redirect('chat')

def chat_view(request, chat_id=None):
    print("--- CHAT VIEW CALLED ---")
    # Initialize conversations storage if not present
    if 'conversations' not in request.session:
        request.session['conversations'] = {}
    
    # Migration: Move old chat_history to a new conversation if it exists
    if 'chat_history' in request.session and request.session['chat_history']:
        print("Migrating legacy chat_history")
        old_chat_id = str(uuid.uuid4())
        request.session['conversations'][old_chat_id] = {
            'id': old_chat_id,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'messages': request.session['chat_history'],
            'title': 'Previous Chat'
        }
        del request.session['chat_history']
        request.session.modified = True

    # Handle switching chats via URL parameter
    if chat_id:
        print(f"Switching to chat_id: {chat_id}")
        if chat_id in request.session['conversations']:
            request.session['current_chat_id'] = chat_id
        else:
            # Invalid ID, redirect to new chat
            print(f"Chat ID {chat_id} not found, redirecting to new chat")
            return redirect('chat')
    
    # Get current chat ID or create one if none exists
    current_chat_id = request.session.get('current_chat_id')
    print(f"Current chat ID in session: {current_chat_id}")
    
    if not current_chat_id or current_chat_id not in request.session['conversations']:
        print("Creating NEW chat session")
        current_chat_id = str(uuid.uuid4())
        request.session['current_chat_id'] = current_chat_id
        request.session['conversations'][current_chat_id] = {
            'id': current_chat_id,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'messages': [],
            'title': 'New Chat'
        }
        request.session.modified = True

    current_chat = request.session['conversations'][current_chat_id]
    print(f"Loaded chat {current_chat_id} with {len(current_chat['messages'])} messages")
    
    # Check settings first, then session
    api_key = getattr(settings, 'GEMINI_API_KEY', None) or request.session.get('gemini_api_key')
    
    if request.method == 'POST' and api_key:
        user_message = request.POST.get('message')
        if user_message:
            # Add user message to history
            current_chat['messages'].append({'role': 'user', 'content': user_message})
            
            # Update title if it's the first message
            if len(current_chat['messages']) == 1:
                # Simple title generation: first 30 chars of message
                current_chat['title'] = (user_message[:30] + '...') if len(user_message) > 30 else user_message
            
            request.session.modified = True
            
            # Check for greetings locally to avoid API calls and provide a warm welcome
            greetings = ['hi', 'hii', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
            if user_message.lower().strip() in greetings:
                warm_welcome = "Hello! It's good to hear from you. How are you feeling today? Please tell me about any symptoms you're experiencing."
                current_chat['messages'].append({'role': 'assistant', 'content': warm_welcome})
                request.session.modified = True
            else:
                # Process with Google Gemini
                try:
                    client = genai.Client(api_key=api_key)
                    
                    predictor = DiseasePredictor.get_instance()
                    all_symptoms = predictor.get_all_symptoms()
                    
                    # Construct the system prompt
                    system_prompt = f"""
                    You are a compassionate and helpful medical assistant acting as a doctor. 
                    Your goal is to understand how the patient is feeling and identify their symptoms.
                    
                    The ONLY symptoms you know about and can ask about are these: {all_symptoms}.
                    
                    Rules:
                    1. Be warm, empathetic, and polite. Start by acknowledging their feelings.
                    2. Ask questions to determine if the user has any of the symptoms in the list above.
                    3. Do NOT ask about symptoms that are not in the list.
                    4. If the user mentions a symptom that is not in the list, gently explain you only check for specific symptoms.
                    5. Map user descriptions to the exact symptom names in the list.
                    6. If the user says 'stop', 'enough', or you have gathered 3-5 strong symptoms, output a JSON block ONLY: 
                       {{"action": "predict", "symptoms": ["symptom1", "symptom2"]}}
                    7. If you are just chatting or asking questions, reply as a caring doctor.
                    8. Do NOT diagnose yourself. Wait for the prediction action.
                    """
                    
                    # Prepare contents for the new API
                    contents = []
                    for msg in current_chat['messages']:
                        role = 'user' if msg['role'] == 'user' else 'model'
                        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg['content'])]))
                    
                    # Generate response
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt
                        )
                    )
                    
                    bot_reply = response.text
                    
                    # Check for JSON action
                    if '{"action": "predict"' in bot_reply:
                        try:
                            # Extract JSON
                            start = bot_reply.find('{')
                            end = bot_reply.rfind('}') + 1
                            json_str = bot_reply[start:end]
                            data = json.loads(json_str)
                            
                            if data.get('action') == 'predict':
                                symptoms = data.get('symptoms', [])
                                predictions, error = predictor.predict(symptoms)
                                
                                if error:
                                    final_reply = f"I tried to predict but encountered an error: {error}"
                                else:
                                    # Second pass: Get remedies
                                    pred_str = ", ".join([f"{p['disease']} ({p['probability']}%)" for p in predictions])
                                    
                                    remedy_prompt = f"""
                                    The prediction model identified these diseases: {pred_str}.
                                    Please explain these to the user and provide 4-5 home remedies for the less severe ones.
                                    IMPORTANT: Ask the user if they have any allergies before suggesting specific ingredients.
                                    """
                                    
                                    # Append the bot's prediction response and our remedy prompt to contents
                                    contents.append(types.Content(role='model', parts=[types.Part.from_text(text=bot_reply)]))
                                    contents.append(types.Content(role='user', parts=[types.Part.from_text(text=remedy_prompt)]))
                                    
                                    remedy_response = client.models.generate_content(
                                        model="gemini-2.5-flash",
                                        contents=contents,
                                        config=types.GenerateContentConfig(
                                            system_instruction=system_prompt
                                        )
                                    )
                                    final_reply = remedy_response.text
                                    
                        except Exception as e:
                            final_reply = f"Error processing prediction: {str(e)}"
                    else:
                        final_reply = bot_reply

                    current_chat['messages'].append({'role': 'assistant', 'content': final_reply})
                    request.session.modified = True
                
                except Exception as e:
                    current_chat['messages'].append({'role': 'assistant', 'content': f"Error: {str(e)}"})
                    request.session.modified = True

    # Sort conversations by timestamp (newest first)
    conversations_list = sorted(request.session['conversations'].values(), key=lambda x: x['timestamp'], reverse=True)

    return render(request, 'prediction/chat.html', {
        'chat_history': current_chat['messages'],
        'conversations': conversations_list,
        'current_chat_id': current_chat_id,
        'api_key_set': bool(api_key)
    })

def new_chat_view(request):
    if 'current_chat_id' in request.session:
        del request.session['current_chat_id']
    return redirect('chat')

def delete_chat_view(request, chat_id=None):
    print("--- DELETE CHAT VIEW CALLED ---")
    
    # 1. Clean up legacy chat_history if it exists
    if 'chat_history' in request.session:
        print("Found legacy chat_history, deleting it.")
        del request.session['chat_history']

    # 2. Get conversations
    conversations = request.session.get('conversations', {})
    print(f"Current conversations keys: {list(conversations.keys())}")
    
    # 3. Determine target ID
    target_id = chat_id or request.session.get('current_chat_id')
    print(f"Target ID to delete: {target_id}")
    
    if target_id:
        # Remove from conversations dict
        if target_id in conversations:
            print(f"Deleting {target_id} from conversations")
            del conversations[target_id]
            request.session['conversations'] = conversations
            messages.success(request, "Chat deleted successfully.")
        else:
            print(f"ID {target_id} not found in conversations")
            messages.warning(request, "Chat not found or already deleted.")

        # Remove from current_chat_id if it matches
        if request.session.get('current_chat_id') == target_id:
            print("Clearing current_chat_id")
            del request.session['current_chat_id']

        # 4. Force save
        request.session.modified = True
        request.session.save()
        print("Session saved")
    else:
        print("No target_id found (no chat_id arg and no current_chat_id in session)")
        messages.error(request, "No active chat to delete.")

    return redirect('chat')
