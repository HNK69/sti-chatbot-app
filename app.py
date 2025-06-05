import streamlit as st
from PIL import Image

# Page settings
st.set_page_config(page_title="STI Diagnosis Chatbot", page_icon="🧠", layout="centered")

st.title("🧠 STI Diagnosis Chatbot")
st.markdown("This tool offers basic guidance for Sexually Transmitted Infections (STIs) based on your symptoms and optional image upload. Not a substitute for professional medical advice.")

# Consent checkbox
consent = st.checkbox("I understand this is not medical advice and agree to proceed.")

if consent:

    # Image upload section
    st.subheader("📸 Upload an Image (Optional)")
    uploaded_image = st.file_uploader("Upload a photo of the affected area", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.info("Image received. (Model-based prediction feature coming soon)")

    # Symptom checklist
    st.subheader("🩺 Symptoms Checklist")

    symptoms_input = {
        "genital_sores": st.checkbox("Do you have genital sores?"),
        "pain": st.checkbox("Are you experiencing pain in the genital area?"),
        "itching": st.checkbox("Is there itching in the genital area?"),
        "painful_urination": st.checkbox("Do you feel pain during urination?"),
        "discharge": st.checkbox("Do you notice any unusual discharge?"),
        "rash": st.checkbox("Do you have a rash?"),
        "fever": st.checkbox("Are you experiencing fever?"),
        "swollen_glands": st.checkbox("Do you have swollen glands?")
    }

    def sti_diagnosis(symptoms):
        if symptoms.get('genital_sores') and symptoms.get('pain') and symptoms.get('itching'):
            return {
                "Diagnosis": "Herpes Simplex Virus (HSV)",
                "Prevention": "Use protection during sex; avoid contact during outbreaks.",
                "Advice": "Consult a dermatologist or healthcare provider for antiviral treatment."
            }
        elif symptoms.get('painful_urination') and symptoms.get('discharge'):
            return {
                "Diagnosis": "Gonorrhea",
                "Prevention": "Practice safe sex; get regular STI screenings.",
                "Advice": "See a doctor immediately for antibiotic treatment."
            }
        elif symptoms.get('rash') and symptoms.get('fever') and symptoms.get('swollen_glands'):
            return {
                "Diagnosis": "Syphilis",
                "Prevention": "Avoid risky sexual behavior; use condoms.",
                "Advice": "Early treatment with penicillin is essential."
            }
        else:
            return {
                "Diagnosis": "Uncertain",
                "Prevention": "Practice safe sex; get regular health check-ups.",
                "Advice": "Consult a healthcare professional for a proper diagnosis."
            }

    if st.button("Get Diagnosis"):
        with st.spinner("Analyzing your symptoms..."):
            result = sti_diagnosis(symptoms_input)
            st.success("Diagnosis Completed")
            st.markdown(f"### 🧾 Possible Diagnosis: **{result['Diagnosis']}**")
            st.markdown(f"**🛡 Prevention Tips:** {result['Prevention']}")
            st.markdown(f"**📌 Advice:** {result['Advice']}")
else:
    st.warning("You must agree to the terms above to use this tool.")
