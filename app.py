import streamlit as st
import time
import random
import os
from twilio.rest import Client

# ---------------- TWILIO CONFIG (SECURE) ----------------
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")

if not TWILIO_SID or not TWILIO_AUTH or not TWILIO_PHONE:
    st.error("Twilio credentials not set. Please check environment variables.")
    st.stop()

client = Client(TWILIO_SID, TWILIO_AUTH)

# ---------------- CONFIG ----------------
st.set_page_config(page_title="FARMIO", layout="centered")

# ---------------- LANGUAGE DATA ----------------
languages = {
    "English": {"welcome": "Welcome to FARMIO", "farmer": "Farmer", "consumer": "Consumer"},
    "Tamil": {"welcome": "FARMIO-க்கு வரவேற்கிறோம்", "farmer": "விவசாயி", "consumer": "நுகர்வோர்"},
    "Hindi": {"welcome": "FARMIO में आपका स्वागत है", "farmer": "किसान", "consumer": "उपभोक्ता"},
    "Telugu": {"welcome": "FARMIO కి స్వాగతం", "farmer": "రైతు", "consumer": "వినియోగదారు"},
}

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "splash"

if "language" not in st.session_state:
    st.session_state.language = "English"

# ---------------- SPLASH SCREEN ----------------
if st.session_state.page == "splash":
    logo_file = "A_logo_for_WEXPO_2026.png"

    if os.path.exists(logo_file):
        st.image(logo_file, width=220)
    else:
        st.image("https://via.placeholder.com/220.png?text=FARMIO")

    st.markdown("<h2 style='color:green; text-align:center;'>FARMIO</h2>", unsafe_allow_html=True)
    st.caption("Initializing setup...")
    time.sleep(2)

    st.session_state.page = "language"
    st.rerun()

# ---------------- LANGUAGE SELECTION ----------------
elif st.session_state.page == "language":
    st.title("Select Your Language")
    lang = st.selectbox("Choose Language", list(languages.keys()))
    if st.button("Continue"):
        st.session_state.language = lang
        st.session_state.page = "user_type"
        st.rerun()

# ---------------- USER TYPE ----------------
elif st.session_state.page == "user_type":
    text = languages[st.session_state.language]
    st.title(text["welcome"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button(text["farmer"]):
            st.session_state.page = "farmer"
            st.rerun()

    with col2:
        if st.button(text["consumer"]):
            st.session_state.page = "consumer"
            st.rerun()

# ---------------- FARMER LOGIN (OTP) ----------------
elif st.session_state.page == "farmer":
    st.title("Farmer Login")

    phone = st.text_input("Enter Mobile Number (10 digits)")

    if st.button("Send OTP"):
        if phone and phone.isdigit() and len(phone) == 10:
            otp = random.randint(1000, 9999)

            st.session_state.generated_otp = str(otp)
            st.session_state.otp_time = time.time()

            try:
                client.messages.create(
                    body=f"Your FARMIO OTP is {otp}",
                    from_=TWILIO_PHONE,
                    to=f"+91{phone}"
                )
                st.success("OTP sent successfully 📲")
            except Exception as e:
                st.error("Failed to send OTP")
                st.code(str(e))
        else:
            st.error("Enter a valid 10-digit mobile number")

    user_otp = st.text_input("Enter OTP", type="password")

    if st.button("Verify OTP"):
        if "generated_otp" not in st.session_state:
            st.error("Please request OTP first")
        elif time.time() - st.session_state.otp_time > 120:
            st.error("OTP expired ⏱️ Please resend")
        elif user_otp == st.session_state.generated_otp:
            st.success("OTP Verified 🎉 Farmer Logged In")
        else:
            st.error("Invalid OTP ❌")

# ---------------- CONSUMER REGISTRATION ----------------
elif st.session_state.page == "consumer":
    st.title("Consumer Registration")

    phone = st.text_input("Enter Mobile Number")
    email = st.text_input("Enter Email")

    if st.button("Submit"):
        if phone and email:
            st.success("Details Submitted Successfully ✅")
        else:
            st.error("Please fill all fields")




