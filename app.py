import streamlit as st
import requests
import base64
import random

# --- 1. OTURUM YÖNETİMİ ---
if 'kalan_hak' not in st.session_state:
    st.session_state.kalan_hak = 2
if 'is_pro' not in st.session_state:
    st.session_state.is_pro = False

# --- 2. HIZ OPTİMİZASYONLU AI MOTORU ---
@st.cache_data(ttl=3600)
def generate_free_commercial_image(prompt: str, style: str, size: str, quality: str):
    try:
        # Kalite çarpanları
        q_factor = {"1K (Standart)": 0.8, "2K (Yüksek)": 1.2, "4K (Ultra)": 1.8}
        factor = q_factor[quality]
        
        size_meta = {
            "Dikey Shorts (9:16)": {"w": int(720*factor), "h": int(1280*factor)},
            "Yatay Video (16:9)": {"w": int(1280*factor), "h": int(720*factor)},
            "Kare Post (1:1)": {"w": int(1024*factor), "h": int(1024*factor)}
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
        response = requests.get(url, headers=headers, timeout=45) 
        
        if response.status_code == 200 and len(response.content) > 10000:
            return response.content
        return None
    except:
        return None

# --- 3. ARAYÜZ TASARIMI ---
st.set_page_config(page_title="AI Görsel Stüdyo", page_icon="⚡", layout="wide")

st.sidebar.title("⚡ Hesap Bilgileri")

# Pro Aktivasyon Alanı
if not st.session_state.is_pro:
    st.sidebar.write(f"Bugünkü Kalan Hakkınız: **{st.session_state.kalan_hak}**")
    pro_kod = st.sidebar.text_input("Pro Şifre:", type="password")
    if st.sidebar.button("Pro'ya Geç"):
        if pro_kod == "1854aaaehgx": # Belirlenen şifre
            st.session_state.is_pro = True
            st.rerun()
        else:
            st.sidebar.error("Geçersiz şifre!")
else:
    st.sidebar.success("✅ Pro Sürüm Aktif! Sınırsız kullanım.")

st.sidebar.markdown("---")
st.sidebar.info("Sınırsız üretim için:")
st.sidebar.markdown("[👉 Sınırsız Erişim Satın Al](https://shopier.com/MAGAZA_LINKIN_BURAYA)")

st.title("⚡ Profesyonel AI Görsel Stüdyosu")
col1, col2 = st.columns([1, 1])

with col1:
    user_prompt = st.text_input("Görseli tarif et:", placeholder="Örn: A futuristic city...")
    selected_size = st.selectbox("Boyut", ["Dikey Shorts (9:16)", "Yatay Video (16:9)", "Kare Post (1:1)"])
    selected_style = st.selectbox("Tarz", ["Sinematik / Fotoğraf", "3D Animasyon / Pixar", "Siberpunk / Neon", "Sihirli Fantastik"])
    selected_quality = st.select_slider("Kalite", options=["1K (Standart)", "2K (Yüksek)", "4K (Ultra)"])

with col2:
    if st.button("✨ Görseli Tasarla", use_container_width=True):
        if not user_prompt.strip():
            st.warning("Lütfen bir açıklama yazın!")
        elif st.session_state.is_pro or st.session_state.kalan_hak > 0:
            with st.spinner("Yapay zeka işleniyor..."):
                img_bytes = generate_free_commercial_image(user_prompt, selected_style, selected_size, selected_quality)
                if img_bytes:
                    if not st.session_state.is_pro:
                        st.session_state.kalan_hak -= 1
                    st.success(f"Başarılı! {'Pro moddasın.' if st.session_state.is_pro else f'Kalan hakkın: {st.session_state.kalan_hak}'}")
                    b64 = base64.b64encode(img_bytes).decode()
                    st.markdown(f'<img src="data:image/png;base64,{b64}" style="width:100%; border-radius:10px;">', unsafe_allow_html=True)
                    st.download_button("📥 İndir", img_bytes, "ai_image.png", use_container_width=True)
                else:
                    st.error("Üretim sırasında hata oluştu.")
        else:
            st.error("Günlük ücretsiz hakkın bitti!")
            st.markdown("[👉 Sınırsız Erişim Satın Al](https://shopier.com/MAGAZA_LINKIN_BURAYA)")
            
