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
                    model="llama-3.1-8b-instant",
                )
                enhanced_prompt = chat_completion.choices[0].message.content
                st.success("✅ Skenario berhasil dipertajam oleh AI!")
                st.info(f"**Prompt Rahasia (Dikirim ke mesin gambar):** {enhanced_prompt}")
                
            except Exception as e:
                st.error(f"Gagal menghubungi server Groq: {e}")
                st.stop()
                
        with st.spinner("🎨 Hugging Face sedang melukis gambar (Tunggu 10-20 detik)..."):
            try:
                # 2. Hugging Face API (Teks ke Gambar - Stable Diffusion XL)
                API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
                headers = {"Authorization": f"Bearer {hf_key}"}
                payload = {"inputs": enhanced_prompt}
                
                response = requests.post(API_URL, headers=headers, json=payload)
                
                if response.status_code == 200:
                    image_bytes = response.content
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    st.balloons()
                    st.success("✅ Berhasil! Ini adalah frame pertama untuk video Anda.")
                    st.image(image, caption="Hasil Render Open Source")
                else:
                    st.error(f"Server Hugging Face sedang sibuk memuat model (Code: {response.status_code}). Silakan klik tombol Generate sekali lagi dalam beberapa detik.")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat merender: {e}")
