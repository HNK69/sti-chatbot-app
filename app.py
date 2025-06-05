import streamlit as st
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model

# Load trained CNN model
@st.cache_resource
def load_sti_model():
    return load_model("sti_image_model.h5")

model = load_sti_model()
classes = ["Herpes", "Gonorrhea", "Syphilis", "Normal"]

# Image preprocessing
def preprocess_image(img):
    img = img.resize((224, 224))  # Adjust to your model's input size
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Symptom-based diagnosis scoring
def diagnose_by_symptoms(symptoms):
    scores = {"Herpes": 0, "Gonorrhea": 0, "Syphilis": 0}
    
    if symptoms.get('genital_sores'):
        scores["Herpes"] += 2
    if symptoms.get('pain'):
        scores["Herpes"] += 1
        scores["Gonorrhea"] += 1
    if symptoms.get('itching'):
        scores["Herpes"] += 1
    if symptoms.get('painful_urination'):
        scores["Gonorrhea"] += 2
    if symptoms.get('discharge'):
        scores["Gonorrhea"] += 2
    if symptoms.get('rash'):
        scores["Syphilis"] += 2
    if symptoms.get('fever'):
        scores["Syphilis"] += 1
    if symptoms.get('swollen_glands'):
        scores["Syphilis"] += 1

    top_disease = max(scores, key=scores.get)
    return top_disease if scores[top_disease] >= 2 else "Uncertain"

# UI
st.set_page_config(page_title="STI Diagnosis Chatbot", page_icon="🧠")
st.title("🧠 STI Diagnosis App")
st.markdown("Provide symptoms and upload an image for a more accurate prediction.")

consent = st.checkbox("I agree this is not a substitute for professional medical advice.")
if not consent:
    st.warning("Please agree to the disclaimer to proceed.")
    st.stop()

# Upload Image
st.subheader("📸 Upload Image (optional)")
uploaded_image = st.file_uploader("Upload an image (jpg/jpeg/png)", type=["jpg", "jpeg", "png"])

image_diagnosis = "No image uploaded"
if uploaded_image:
    img = Image.open(uploaded_image)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    preprocessed = preprocess_image(img)
    prediction = model.predict(preprocessed)[0]
    image_diagnosis = classes[np.argmax(prediction)]
    st.markdown(f"**📷 Image-based Diagnosis:** `{image_diagnosis}`")

# Symptom inputs
st.subheader("🩺 Symptom Checklist")
symptoms = {
    "genital_sores": st.checkbox("Genital sores"),
    "pain": st.checkbox("Pain in genital area"),
    "itching": st.checkbox("Itching"),
    "painful_urination": st.checkbox("Painful urination"),
    "discharge": st.checkbox("Unusual discharge"),
    "rash": st.checkbox("Skin rash"),
    "fever": st.checkbox("Fever"),
    "swollen_glands": st.checkbox("Swollen glands")
}

if st.button("🔍 Diagnose"):
    symptom_diagnosis = diagnose_by_symptoms(symptoms)
    
    st.markdown("### 🧾 Combined Diagnosis")

    # Priority to Image diagnosis if it's confident
    if image_diagnosis != "No image uploaded" and image_diagnosis != "Normal":
        st.success(f"🔬 **Likely condition (image-based):** {image_diagnosis}")
    elif symptom_diagnosis != "Uncertain":
        st.success(f"📋 **Likely condition (symptom-based):** {symptom_diagnosis}")
    else:
        st.warning("🤷 Unable to determine condition confidently. Please consult a doctor.")

    st.markdown("**Disclaimer:** This app does not replace clinical consultation.")
