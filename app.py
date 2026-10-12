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
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("💾 Unduh Gambar", data=st.session_state.image_bytes, file_name="frame.png", mime="image/png", use_container_width=True)
        
    with col2:
        if st.button("🎥 Jadikan Video", type="primary", use_container_width=True):
            with st.spinner("⏳ Menghidupkan gambar... (Bisa memakan waktu 1-3 menit)"):
                try:
                    # Mengirim gambar ke model Stable Video Diffusion di Hugging Face
                    API_URL_VID = "https://api-inference.huggingface.co/models/stabilityai/stable-video-diffusion-img2vid-xt"
                    headers = {"Authorization": f"Bearer {hf_key}"}
                    
                    response_vid = requests.post(API_URL_VID, headers=headers, data=st.session_state.image_bytes)
                    
                    if response_vid.status_code == 200:
                        st.session_state.generated_video = response_vid.content
                        st.success("✅ Video berhasil dianimasikan!")
                    elif response_vid.status_code == 503:
                        # Server gratis HF sering tertidur, kode 503 berarti server sedang "bangun"
                        st.warning("Mesin video sedang dipanaskan (Loading Model). Silakan tunggu 30 detik dan klik tombol 'Jadikan Video' lagi.")
                    else:
                        st.error(f"Gagal membuat video. Code: {response_vid.status_code}. Pesan: {response_vid.text}")
                except Exception as e:
                    st.error(f"Terjadi kesalahan koneksi video: {e}")

# --- MENAMPILKAN HASIL VIDEO ---
if st.session_state.generated_video:
    st.divider()
    st.subheader("🎬 Hasil Render Video AI")
    st.video(st.session_state.generated_video)
    st.download_button(
        label="💾 Unduh Video (MP4)",
        data=st.session_state.generated_video,
        file_name="animasi_ai.mp4",
        mime="video/mp4",
        use_container_width=True
    )
