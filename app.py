import streamlit as st
import requests
import base64
import random

# --- 1. SINIRSIZ VE ÜCRETSİZ AI MOTORU ---
def generate_free_commercial_image(prompt: str, style: str, size: str):
    """
    Sıfır maliyetli, token istemeyen ve ticari satışa uygun
    kesintisiz yapay zeka resim motoru.
    """
    try:
        # Ölçü ayarları
        size_meta = {
            "Dikey Shorts (9:16)": {"w": 720, "h": 1280},
            "Yatay Video (16:9)": {"w": 1280, "h": 720},
            "Kare Post (1:1)": {"w": 1024, "h": 1024}
        }
        w = size_meta[size]["w"]
        h = size_meta[size]["h"]

        # Profesyonel Stil Filtreleri
        styles = {
            "Sinematik / Fotoğraf": "hyperrealistic photography, 8k resolution, highly detailed, dramatic lighting, cinematic masterpiece",
            "3D Animasyon / Pixar": "cute 3D animation style, vibrant pastel colors, soft studio lighting, ultra detailed character",
            "Siberpunk / Neon": "cyberpunk concept art, neon glow, cinematic dark atmosphere, high contrast digital painting",
            "Sihirli Fantastik": "enchanted fantasy illustration, award-winning concept art, beautiful scenery, masterfully crafted"
        }

        # Arka planda promptu zenginleştirme ve engelleri aşmak için rastgele sayı ekleme
        final_prompt = f"{prompt.strip()}, {styles[style]}, high quality, sharp focus"
        seed = random.randint(1, 999999)
        
        # Sınırsız ve stabil açık kaynak havuzu
        url = f"https://image.pollinations.ai/p/{requests.utils.quote(final_prompt)}?width={w}&height={h}&seed={seed}&model=flux&enhance=false"
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200 and len(response.content) > 10000:
            return response.content
        return None
    except:
        return None

# --- 2. GÖZ ALICI PREMİUM SİTE TASARIMI ---
st.set_page_config(page_title="Hızlı Görsel Stüdyosu", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    h1 {
        background: linear-gradient(135deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        text-align: center;
    }
    .panel-box {
        background-color: #161b22;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #30363d;
        margin-bottom: 15px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe, #4facfe) !important;
        color: #0d1117 !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border-radius: 10px !important;
        padding: 12px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚡ Hızlı Yapay Zeka Görsel Stüdyosu</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8b949e;'>Sıfır maliyetle, anında ve sınırsız profesyonel görseller üretin.</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
    st.subheader("📝 1. Hayalindeki Sahne")
    user_prompt = st.text_input("Ne çizilsin? (İngilizce yazmanız önerilir)", placeholder="Örn: A cute neon cat in space...")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='panel-box'>", unsafe_allow_html=True)
    st.subheader("📐 2. Boyut ve Stil Seçimi")
    selected_size = st.selectbox("Resim Boyutu", ["Dikey Shorts (9:16)", "Yatay Video (16:9)", "Kare Post (1:1)"])
    selected_style = st.selectbox("Sanat Tarzı", ["Sinematik / Fotoğraf", "3D Animasyon / Pixar", "Siberpunk / Neon", "Sihirli Fantastik"])
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='panel-box' style='text-align: center; min-height: 400px;'>", unsafe_allow_html=True)
    st.subheader("🖼️ Çıktı Ekranı")
    st.markdown("---")
    
    if st.button("✨ Görseli Tasarla", use_container_width=True):
        if not user_prompt.strip():
            st.error("Lütfen bir açıklama yazın!")
        else:
            with st.spinner("🤖 Yapay zeka fırçasını oynatıyor..."):
                img_bytes = generate_free_commercial_image(user_prompt, selected_style, selected_size)
                
            if img_bytes:
                st.success("Görsel başarıyla üretildi!")
                b64 = base64.b64encode(img_bytes).decode()
                
                # Ekranda şık durması için boyutlandırma
                disp_width = "260px" if "9:16" in selected_size else "100%"
                st.markdown(f'<img src="data:image/png;base64,{b64}" style="width:{disp_width}; border-radius:10px; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.download_button(
                    label="📥 Resmi Bilgisayara İndir",
                    data=img_bytes,
                    file_name="ai_studio_output.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                st.error("Üretim sırasında bir sorun oluştu. Lütfen butona tekrar basmayı deneyin.")
    st.markdown("</div>", unsafe_allow_html=True)