import streamlit as st
import requests
import io
import time
from PIL import Image
from groq import Groq

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Mesin Master AI", page_icon="🎬", layout="centered")

# --- SISTEM MEMORI (SESSION STATE) ---
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None
if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = None
if "enhanced_prompt" not in st.session_state:
    st.session_state.enhanced_prompt = ""
if "generated_video" not in st.session_state:
    st.session_state.generated_video = None

st.title("🎬 Mesin Generator Visual AI")
st.write("Prototipe mesin video mandiri tanpa API berbayar.")
st.divider()

# --- SETUP API KEYS ---
try:
    groq_key = st.secrets["GROQ_API_KEY"]
    hf_key = st.secrets["HF_API_KEY"] # Diaktifkan kembali untuk mesin Video
    client = Groq(api_key=groq_key)
except Exception as e:
    st.error("⚠️ Kunci API tidak ditemukan. Pastikan GROQ_API_KEY dan HF_API_KEY ada di Secrets.")
    st.stop()

# --- TAHAP 1: TEKS KE GAMBAR ---
st.subheader("1. Buat Frame Pertama")
story_prompt = st.text_area(
    "Ketik skenario adegan (Bahasa Indonesia):", 
    placeholder="Contoh: Seekor kucing oren 3D memakai kacamata hitam...", 
    height=100
)

if st.button("🎨 Generate Visual", use_container_width=True):
    if not story_prompt:
        st.warning("⚠️ Ide cerita tidak boleh kosong.")
    else:
        # Reset video jika membuat gambar baru
        st.session_state.generated_video = None 
        
        with st.spinner("🤖 Groq sedang meracik prompt profesional..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are an expert prompt engineer for AI image generators. Convert the user's idea into a highly detailed, descriptive image prompt in English. Focus on cinematic lighting, style, and 3D render qualities. Return ONLY the English prompt text."},
                        {"role": "user", "content": story_prompt}
                    ],
                    model="openai/gpt-oss-120b",
                )
                st.session_state.enhanced_prompt = chat_completion.choices[0].message.content
                st.success("✅ Skenario berhasil dipertajam!")
            except Exception as e:
                st.error(f"Gagal menghubungi server Groq: {e}")
                st.stop()
                
        with st.spinner("🖼️ Mesin gambar sedang melukis (Tunggu sebentar)..."):
            try:
                API_URL_IMG = "https://image.pollinations.ai/prompt/"
                response = requests.get(
                    API_URL_IMG + st.session_state.enhanced_prompt, 
                    params={"width": 1024, "height": 1024, "nologo": "true", "seed": 42}
                )
                if response.status_code == 200:
                    st.session_state.image_bytes = response.content
                    st.session_state.generated_image = Image.open(io.BytesIO(st.session_state.image_bytes))
                    st.balloons()
                else:
                    st.error(f"Mesin gambar sibuk (Code: {response.status_code}).")
            except Exception as e:
                st.error(f"Terjadi kesalahan merender gambar: {e}")

# --- TAHAP 2: GAMBAR KE VIDEO ---
if st.session_state.generated_image:
    st.image(st.session_state.generated_image, caption="Frame Awal", use_container_width=True)
    
    st.download_button(
        label="💾 1. Unduh Gambar Ini Dulu", 
        data=st.session_state.image_bytes, 
        file_name="frame_kucing.png", 
        mime="image/png", 
        use_container_width=True
    )
    
    st.divider()
    st.subheader("🎥 2. Mesin Penggerak Video")
    st.info("💡 Menggunakan server mirror komunitas yang stabil (Stable Video Diffusion).")
    
    # Menanamkan mesin mirror komunitas yang lebih tahan banting
    import streamlit.components.v1 as components
    components.iframe("https://mediasynthesismuseum-stable-video-diffusion.hf.space", height=850, scrolling=True)
    
    st.divider()
    st.write("Jika tampilan di atas terpotong atau mesin sedang sibuk, klik jalur alternatif ini:")
    st.link_button("🚀 Buka Mesin Video di Tab Baru", "https://huggingface.co/spaces/mediasynthesismuseum/stable-video-diffusion", use_container_width=True)
