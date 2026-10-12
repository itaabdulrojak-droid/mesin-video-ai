import streamlit as st
import requests
import io
from PIL import Image
from groq import Groq

# Konfigurasi Halaman
st.set_page_config(page_title="Mesin Master AI", page_icon="🎬", layout="centered")

st.title("🎬 Mesin Generator Visual AI")
st.write("Menggunakan otak Groq (Llama 3) & mesin gambar Hugging Face (Stable Diffusion) tanpa biaya.")
st.divider()

# --- SETUP API KEYS ---
try:
    groq_key = st.secrets["GROQ_API_KEY"]
    hf_key = st.secrets["HF_API_KEY"]
    client = Groq(api_key=groq_key)
except Exception as e:
    st.error("⚠️ Kunci API tidak ditemukan. Pastikan sudah disimpan di Secrets.")
    st.stop()

# --- ANTARMUKA ---
st.subheader("Skenario Adegan")
story_prompt = st.text_area(
    "Ketik ide cerita Anda (bisa bahasa Indonesia):", 
    placeholder="Contoh: Seekor kucing oren 3D memakai kacamata hitam sedang berjalan santai di kota cyberpunk...", 
    height=100
)

if st.button("Generate Visual 🚀", use_container_width=True):
    if not story_prompt:
        st.warning("⚠️ Ide cerita tidak boleh kosong.")
    else:
        with st.spinner("🤖 Groq sedang meracik prompt profesional..."):
            try:
                # 1. Groq API (Menerjemahkan ide jadi prompt ahli)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert prompt engineer for AI image generators. Convert the user's idea into a highly detailed, descriptive image prompt in English. Focus on cinematic lighting, style, and 3D render qualities (like Pixar/Unreal Engine). Return ONLY the English prompt text, nothing else."
                        },
                        {
                            "role": "user",
                            "content": story_prompt,
                        }
                    ],
                    model="openai/gpt-oss-120b",
                )
                enhanced_prompt = chat_completion.choices[0].message.content
                st.success("✅ Skenario berhasil dipertajam oleh AI!")
                st.info(f"**Prompt Rahasia (Dikirim ke mesin gambar):** {enhanced_prompt}")
                
            except Exception as e:
                st.error(f"Gagal menghubungi server Groq: {e}")
                st.stop()
                
        with st.spinner("🎨 Hugging Face sedang melukis gambar (Tunggu 10-20 detik)..."):
            try:
                            # 2. Mesin Gambar Alternatif (Pollinations AI - Bebas API Key)
            try:
                # Menggunakan requests.get untuk mengambil gambar secara langsung
                API_URL = "https://image.pollinations.ai/prompt/"
                # Kita kirim prompt dari Groq dan minta ukuran persegi resolusi tinggi
                response = requests.get(
                    API_URL + enhanced_prompt, 
                    params={"width": 1024, "height": 1024, "nologo": "true", "seed": 42}
                )
                
                if response.status_code == 200:
                    image_bytes = response.content
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    st.balloons()
                    st.success("✅ Berhasil! Ini adalah frame pertama untuk video Anda.")
                    st.image(image, caption="Hasil Render AI Alternatif")
                else:
                    st.error(f"Mesin gambar alternatif sibuk (Code: {response.status_code}). Coba lagi.")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat merender: {e}")
