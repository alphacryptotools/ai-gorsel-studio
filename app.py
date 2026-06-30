import streamlit as st
import requests
import base64
import random

# --- 1. OTURUM YÖNETİMİ (LIMIT KONTROLÜ) ---
if 'kalan_hak' not in st.session_state:
    st.session_state.kalan_hak = 2

# --- 2. AI MOTORU ---
def generate_free_commercial_image(prompt: str, style: str, size: str):
    try:
        size_meta = {
            "Dikey Shorts (9:16)": {"w": 720, "h": 1280},
            "Yatay Video (16:9)": {"w": 1280, "h": 720},
            "Kare Post (1:1)": {"w": 1024, "h": 1024}
        }
        w = size_meta[size]["w"]
        h = size_meta[size]["h"]

        styles = {
            "Sinematik / Fotoğraf": "hyperrealistic photography, 8k resolution, dramatic lighting",
            "3D Animasyon / Pixar": "cute 3D animation style, vibrant pastel colors, soft studio lighting",
            "Siberpunk / Neon": "cyberpunk concept art, neon glow, cinematic dark atmosphere",
            "Sihirli Fantastik": "enchanted fantasy illustration, award-winning concept art"
        }

        final_prompt = f"{prompt.strip()}, {styles[style]}, high quality, sharp focus"
        seed = random.randint(1, 999999)
        url = f"https://image.pollinations.ai/p/{requests.utils.quote(final_prompt)}?width={w}&height={h}&seed={seed}&model=flux&enhance=false"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200 and len(response.content) > 10000:
            return response.content
        return None
    except:
        return None

# --- 3. ARAYÜZ TASARIMI ---
st.set_page_config(page_title="Hızlı Görsel Stüdyosu", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    h1 { background: linear-gradient(135deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
    .panel-box { background-color: #161b22; padding: 25px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 15px; }
    .stButton>button { background: linear-gradient(135deg, #00f2fe, #4facfe) !important; color: #0d1117 !important; font-weight: bold !important; border-radius: 10px !important; }
    </style>
""", unsafe_allow_html=True)

# Yan menüde limit bilgisi
st.sidebar.title("⚡ Hesap Bilgileri")
st.sidebar.write(f"Bugünkü Kalan Hakkınız: **{st.session_state.kalan_hak}**")
st.sidebar.markdown("---")
st.sidebar.info("Sınırsız üretim için lisansınızı alın:")
st.sidebar.markdown("[👉 Sınırsız Erişim Satın Al](https://shopier.com/MAGAZA_LINKIN_BURAYA)")

st.markdown("<h1>⚡ Hızlı Yapay Zeka Görsel Stüdyosu</h1>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
    user_prompt = st.text_input("Ne çizilsin?", placeholder="Örn: A cute neon cat in space...")
    selected_size = st.selectbox("Resim Boyutu", ["Dikey Shorts (9:16)", "Yatay Video (16:9)", "Kare Post (1:1)"])
    selected_style = st.selectbox("Sanat Tarzı", ["Sinematik / Fotoğraf", "3D Animasyon / Pixar", "Siberpunk / Neon", "Sihirli Fantastik"])
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='panel-box' style='min-height: 400px;'>", unsafe_allow_html=True)
    if st.button("✨ Görseli Tasarla", use_container_width=True):
        if not user_prompt.strip():
            st.error("Lütfen bir açıklama yazın!")
        elif st.session_state.kalan_hak > 0:
            with st.spinner("🤖 Yapay zeka fırçasını oynatıyor..."):
                img_bytes = generate_free_commercial_image(user_prompt, selected_style, selected_size)
                if img_bytes:
                    st.session_state.kalan_hak -= 1 # Hakkı düşür
                    st.success(f"Görsel üretildi! Kalan hakkınız: {st.session_state.kalan_hak}")
                    b64 = base64.b64encode(img_bytes).decode()
                    st.markdown(f'<img src="data:image/png;base64,{b64}" style="width:100%; border-radius:10px;">', unsafe_allow_html=True)
                    st.download_button("📥 İndir", img_bytes, "ai_studio.png", use_container_width=True)
                else:
                    st.error("Bir sorun oluştu, tekrar deneyin.")
        else:
            st.error("Günlük ücretsiz hakkınız doldu!")
            st.markdown("[👉 Sınırsız Erişim Satın Almak İçin Tıkla](https://shopier.com/MAGAZA_LINKIN_BURAYA)")
    st.markdown("</div>", unsafe_allow_html=True)
