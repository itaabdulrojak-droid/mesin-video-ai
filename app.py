import streamlit as st
import requests
import io
from PIL import Image
from groq import Groq

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Mesin Master AI", page_icon="🎬", layout="centered")

# --- SISTEM MEMORI (SESSION STATE) ---
# Menyimpan gambar dan prompt agar tidak hilang saat layar ponsel dimuat ulang
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None
if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = None
if "enhanced_prompt" not in st.session_state:
    st.session_state.enhanced_prompt = ""

st.title("🎬 Mesin Generator Visual AI")
st.write("Prototipe mesin video mandiri tanpa API berbayar.")
st.divider()

# --- SETUP API KEYS ---
try:
    groq_key = st.secrets["GROQ_API_KEY"]
    # hf_key = st.secrets["HF_API_KEY"] # (Dinonaktifkan sementara)
    client = Groq(api_key=groq_key)
except Exception as e:
    st.error("⚠️ Kunci API Groq tidak ditemukan di Secrets.")
    st.stop()

# --- ANTARMUKA TAHAP 1: TEKS KE GAMBAR ---
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
        with st.spinner("🤖 Groq sedang meracik prompt profesional..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert prompt engineer for AI image generators. Convert the user's idea into a highly detailed, descriptive image prompt in English. Focus on cinematic lighting, style, and 3D render qualities. Return ONLY the English prompt text."
                        },
                        {
                            "role": "user",
                            "content": story_prompt,
                        }
                    ],
                    model="openai/gpt-oss-120b",
                )
                st.session_state.enhanced_prompt = chat_completion.choices[0].message.content
                st.success("✅ Skenario berhasil dipertajam!")
                
                with st.expander("Lihat Prompt Rahasia"):
                    st.write(st.session_state.enhanced_prompt)
                    
            except Exception as e:
                st.error(f"Gagal menghubungi server Groq: {e}")
                st.stop()
                
        with st.spinner("🖼️ Mesin gambar sedang melukis (Tunggu sebentar)..."):
            try:
                API_URL = "https://image.pollinations.ai/prompt/"
                response = requests.get(
                    API_URL + st.session_state.enhanced_prompt, 
                    params={"width": 1024, "height": 1024, "nologo": "true", "seed": 42}
                )
                
                if response.status_code == 200:
                    st.session_state.image_bytes = response.content
                    st.session_state.generated_image = Image.open(io.BytesIO(st.session_state.image_bytes))
                    st.balloons()
                else:
                    st.error(f"Mesin gambar alternatif sibuk (Code: {response.status_code}). Coba lagi.")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat merender: {e}")

# --- MENAMPILKAN HASIL & TOMBOL LANJUTAN ---
if st.session_state.generated_image:
    st.image(st.session_state.generated_image, caption="Frame Animasi 3D", use_container_width=True)
    
    # Kolom untuk menata tombol agar rapi di layar ponsel
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="💾 Unduh Gambar",
            data=st.session_state.image_bytes,
            file_name="frame_pertama.png",
            mime="image/png",
            use_container_width=True
        )
        
    with col2:
        if st.button("🎥 Jadikan Video", type="primary", use_container_width=True):
            st.info("Mesin Image-to-Video sedang disiapkan. Kita akan menyambungkan API animasi di tahap selanjutnya!")
