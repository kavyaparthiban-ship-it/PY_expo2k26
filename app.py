import streamlit as st
import time
import requests
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="FARMIO", layout="wide")

# ---------------- 2FACTOR CONFIG ----------------
API_KEY = "215a66be-fcc4-11f0-a6b2-0200cd936042"
TEMPLATE = "FARMIO_OTP"

# ---------------- LANGUAGE DATA ----------------
languages = {
    "English": {"welcome": "Welcome to FARMIO", "farmer": "Farmer", "consumer": "Consumer"},
    "Tamil": {"welcome": "FARMIO-க்கு வரவேற்கிறோம்", "farmer": "விவசாயி", "consumer": "நுகர்வோர்"},
    "Malayalam": {"welcome": "FARMIOയിലേക്ക് സ്വാഗതം", "farmer": "കർഷകൻ", "consumer": "ഉപഭോക്താവ്"},
    "Telugu": {"welcome": "FARMIO కి స్వాగతం", "farmer": "రైతు", "consumer": "వినియోగదారు"},
    "Marathi": {"welcome": "FARMIO मध्ये आपले स्वागत आहे", "farmer": "शेतकरी", "consumer": "ग्राहक"},
    "Kannada": {"welcome": "FARMIO ಗೆ ಸ್ವಾಗತ", "farmer": "ರೈತ", "consumer": "ಗ್ರಾಹಕ"},
    "Bengali": {"welcome": "FARMIO তে আপনাকে স্বাগতম", "farmer": "কৃষক", "consumer": "ভোক্তা"},
    "Gujarati": {"welcome": "FARMIO માં આપનું સ્વાગત છે", "farmer": "કિસાન", "consumer": "ગ્રાહક"},
    "Assamese": {"welcome": "FARMIO ত আপোনাক স্বাগতম", "farmer": "কৃষক", "consumer": "গ্ৰাহক"},
    "Odia": {"welcome": "FARMIOରେ ଆପଣଙ୍କୁ ସ୍ବାଗତ", "farmer": "କୃଷକ", "consumer": "ଗ୍ରାହକ"},
    "Bhojpuri": {"welcome": "FARMIO में राउर स्वागत बा", "farmer": "किसान", "consumer": "ग्राहक"},
    "Hindi": {"welcome": "FARMIO में आपका स्वागत है", "farmer": "किसान", "consumer": "उपभोक्ता"},
    "Punjabi": {"welcome": "FARMIO ਵਿੱਚ ਤੁਹਾਡਾ ਸਵਾਗਤ ਹੈ", "farmer": "ਕਿਸਾਨ", "consumer": "ਗ੍ਰਾਹਕ"},
    "Urdu": {"welcome": "FARMIO میں خوش آمدید", "farmer": "کسان", "consumer": "صارف"},
}

native_names = {
    "English": "English",
    "Tamil": "தமிழ்",
    "Malayalam": "മലയാളം",
    "Telugu": "తెలుగు",
    "Marathi": "मराठी",
    "Kannada": "ಕನ್ನಡ",
    "Bengali": "বাংলা",
    "Gujarati": "ગુજરાતી",
    "Assamese": "অসমীয়া",
    "Odia": "ଓଡ଼ିଆ",
    "Bhojpuri": "भोजपुरी",
    "Hindi": "हिन्दी",
    "Punjabi": "ਪੰਜਾਬੀ",
    "Urdu": "اردو",
}

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "splash"
if "language" not in st.session_state:
    st.session_state.language = "English"

# ---------------- STYLE ----------------
st.markdown("""
<style>
body {
    background-color: #f0fff0;
    font-family: 'Segoe UI', sans-serif;
}
div.stButton > button:first-child {
    background-color: #2f7d32;
    color: white;
    height: 50px;
    width: 200px;
    border-radius: 10px;
    font-size: 18px;
    margin: 5px;
}
input[type="text"], input[type="password"], input[type="number"] {
    height: 40px;
    font-size: 16px;
    border-radius: 8px;
    border:1px solid #2f7d32;
    padding-left: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SPLASH SCREEN ----------------
if st.session_state.page == "splash":

    logo_file = os.path.join(
        os.path.dirname(__file__),
        "A_logo_for_WEXPO_2026.png"
    )

    # Show logo
    if os.path.exists(logo_file):
        st.image(logo_file, width=150)
    else:
        st.markdown(
            "<h3 style='text-align:center;color:red;'>Logo not found</h3>",
            unsafe_allow_html=True
        )

    # Title and tagline
    st.markdown("""
        <div style='text-align:center; padding:15px; border-radius:15px; background-color:#e0f8e0;'>
            <h1 style='color:#2f7d32'>FARMIO</h1>
            <p style='color:#2f7d32; font-size:16px;'>Connecting Farmers & Consumers</p>
        </div>
        """, unsafe_allow_html=True)

    time.sleep(2)
    st.session_state.page = "language"
    st.rerun()

# ---------------- LANGUAGE SELECTION ----------------
elif st.session_state.page == "language":
    st.markdown("<h2 style='text-align:center; color:#2f7d32'>Select Language</h2>", unsafe_allow_html=True)

    langs = list(native_names.keys())
    n_cols = 3
    for i in range(0, len(langs), n_cols):
        cols = st.columns(n_cols)
        for j, lang_key in enumerate(langs[i:i+n_cols]):
            if cols[j].button(native_names[lang_key]):
                st.session_state.language = lang_key
                st.session_state.page = "user_type"
                st.rerun()

# ---------------- USER TYPE ----------------
elif st.session_state.page == "user_type":
    text = languages[st.session_state.language]
    st.markdown(f"<h2 style='color:#2f7d32; text-align:center;'>{text['welcome']}</h2>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button(f"👨‍🌾 {text['farmer']}"):
            st.session_state.page = "farmer"
            st.rerun()
    with c2:
        if st.button(f"🛒 {text['consumer']}"):
            st.session_state.page = "consumer"
            st.rerun()

# ---------------- FARMER LOGIN ----------------
elif st.session_state.page == "farmer":
    st.markdown("<h2 style='color:#2f7d32;'>Farmer Login (OTP)</h2>", unsafe_allow_html=True)
    phone = st.text_input("Mobile Number (10 digits)")

    if st.button("Send OTP"):
        if phone.isdigit() and len(phone) == 10:
            url = f"https://2factor.in/API/V1/{API_KEY}/SMS/91{phone}/AUTOGEN/{TEMPLATE}"
            res = requests.get(url).json()
            if res["Status"] == "Success":
                st.session_state.session_id = res["Details"]
                st.session_state.otp_time = time.time()
                st.success("OTP sent 📲")
            else:
                st.error(f"Failed to send OTP: {res['Details']}")
        else:
            st.error("Enter valid 10-digit number")

    if "session_id" in st.session_state:
        user_otp = st.text_input("Enter OTP", type="password")
        elapsed = int(time.time() - st.session_state.otp_time)
        remaining = 120 - elapsed
        if remaining > 0:
            st.info(f"OTP valid for {remaining} seconds ⏱️")
        else:
            st.warning("OTP expired. Send again ⏱️")

        if st.button("Verify OTP"):
            verify_url = f"https://2factor.in/API/V1/{API_KEY}/SMS/VERIFY/{st.session_state.session_id}/{user_otp}"
            verify_res = requests.get(verify_url).json()
            if verify_res["Status"] == "Success":
                st.success("Farmer Logged In 🎉")
                st.session_state.farmer_logged_in = True
                if "farmer_verified" not in st.session_state:
                    st.session_state.farmer_verified = False
                st.session_state.page = "farmer_dashboard"
                st.rerun()
            else:
                st.error("❌ Invalid OTP or expired. Try again.")

# ---------------- FARMER DASHBOARD ----------------
elif st.session_state.page == "farmer_dashboard":
    st.markdown("<h2 style='color:#2f7d32;'>Farmer Dashboard</h2>", unsafe_allow_html=True)

    if st.session_state.farmer_verified:
        st.success("✅ Verified Farmer")
    else:
        st.warning("⚠️ Not Verified Yet")

    if st.button("💰 Sell Product"):
        if not st.session_state.farmer_verified:
            st.session_state.page = "farmer_live_verification"
            st.rerun()
        else:
            st.session_state.page = "farmer_product_upload"
            st.rerun()

# ---------------- FARMER LIVE VIDEO VERIFICATION ----------------
elif st.session_state.page == "farmer_live_verification":
    st.markdown("<h3 style='color:#2f7d32;'>Step 1: Live Video Verification</h3>", unsafe_allow_html=True)

    video_file = st.file_uploader("Upload Live Video (mp4/webm)", type=["mp4","webm"])
    if video_file is not None:
        save_path = f"uploads/verification_{int(time.time())}.mp4"
        os.makedirs("uploads", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(video_file.getbuffer())
        st.session_state.farmer_verified = True
        st.success("✅ Live Video Uploaded & Verified (Demo: auto-approved)")
        st.session_state.page = "farmer_product_upload"
        st.rerun()

# ---------------- FARMER PRODUCT UPLOAD ----------------
elif st.session_state.page == "farmer_product_upload":
    st.markdown("<h3 style='color:#2f7d32;'>Step 2: Upload Product</h3>", unsafe_allow_html=True)

    product_name = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=1)
    price = st.number_input("Price per unit")
    category = st.text_input("Category")
    product_media = st.file_uploader("Upload Live Photo/Video of Product", type=["jpg","png","mp4","webm"])

    if st.button("Upload Product"):
        if not product_name or not quantity or not price or not category or not product_media:
            st.error("Please fill all fields and upload media")
        else:
            os.makedirs("uploads", exist_ok=True)
            save_path = f"uploads/product_{int(time.time())}_{product_media.name}"
            with open(save_path, "wb") as f:
                f.write(product_media.getbuffer())
            st.success(f"✅ Product '{product_name}' Uploaded Successfully!")
            st.session_state.page = "farmer_dashboard"
            st.rerun()

# ---------------- CONSUMER LOGIN ----------------
elif st.session_state.page == "consumer":
    st.markdown("<h2 style='color:#2f7d32;'>Consumer Registration</h2>", unsafe_allow_html=True)

    phone = st.text_input("Mobile Number (10 digits)")
    email = st.text_input("Email (Optional)")

    if st.button("Send OTP"):
        if phone.isdigit() and len(phone) == 10:
            url = f"https://2factor.in/API/V1/{API_KEY}/SMS/91{phone}/AUTOGEN/{TEMPLATE}"
            res = requests.get(url).json()
            if res["Status"] == "Success":
                st.session_state.consumer_session_id = res["Details"]
                st.session_state.consumer_otp_time = time.time()
                st.success("OTP sent 📲")
            else:
                st.error(f"Failed to send OTP: {res['Details']}")
        else:
            st.error("Enter valid 10-digit number")

    if "consumer_session_id" in st.session_state:
        user_otp = st.text_input("Enter OTP", type="password")
        elapsed = int(time.time() - st.session_state.consumer_otp_time)
        remaining = 120 - elapsed
        if remaining > 0:
            st.info(f"OTP valid for {remaining} seconds ⏱️")
        else:
            st.warning("OTP expired. Send again ⏱️")

        if st.button("Verify OTP"):
            verify_url = f"https://2factor.in/API/V1/{API_KEY}/SMS/VERIFY/{st.session_state.consumer_session_id}/{user_otp}"
            verify_res = requests.get(verify_url).json()
            if verify_res["Status"] == "Success":
                if email:
                    st.success(f"Consumer Registered ✅\nPhone verified 📲\nEmail: {email}")
                else:
                    st.success("Consumer Registered ✅\nPhone verified 📲")
            else:
                st.error("❌ Invalid OTP or expired. Try again.")

