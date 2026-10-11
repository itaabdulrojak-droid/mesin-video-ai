import streamlit as st
import time

# Konfigurasi Halaman
st.set_page_config(page_title="AI Video Engine", page_icon="🎬", layout="centered")

st.title("🎬 Mesin Generator Video AI")
st.write("Ubah karakter statis menjadi adegan video animasi 3D.")

st.divider()

# Bagian 1: Input Karakter
st.subheader("1. Referensi Karakter")
uploaded_image = st.file_uploader("Upload foto karakter (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_image:
    st.image(uploaded_image, caption="Karakter Siap Digunakan", width=250)

# Bagian 2: Input Prompt Cerita
st.subheader("2. Skenario Adegan")
story_prompt = st.text_area(
    "Deskripsikan adegan video:", 
    placeholder="Contoh: Kurir paket berbaju oranye berlari panik mengejar mobil van yang meluncur turun. Kamera dinamis, gaya animasi Pixar 3D...", 
    height=150
)

# Pengaturan Tambahan (Opsional untuk nanti)
with st.expander("Pengaturan Lanjutan"):
    st.selectbox("Rasio Aspek", ["16:9 (YouTube)", "9:16 (Shorts/TikTok)"])
    st.slider("Durasi (detik)", min_value=5, max_value=15, value=5)

st.divider()

# Bagian 3: Tombol Eksekusi
if st.button("Generate Video 🚀", use_container_width=True):
    if not uploaded_image:
        st.warning("⚠️ Mohon upload foto referensi karakter terlebih dahulu.")
    elif not story_prompt:
        st.warning("⚠️ Deskripsi skenario tidak boleh kosong.")
    else:
        st.info("Memproses permintaan... Menghubungi server AI.")
        
        # --- BLOK SIMULASI LOADING ---
        # Di sinilah nanti kita akan menaruh kode koneksi ke API asli
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            time.sleep(0.03) # Simulasi waktu tunggu
            progress_bar.progress(i + 1)
            if i == 30:
                status_text.text("Menganalisis gambar karakter...")
            elif i == 60:
                status_text.text("Merender pergerakan adegan 3D...")
        
        status_text.empty()
        progress_bar.empty()
        
        st.success("✅ Video berhasil di-generate! (Ini masih simulasi UI)")
        
        # Nanti kita gunakan st.video(url_dari_api) untuk menampilkan hasilnya
        st.info("Video player akan muncul di sini setelah API terhubung.")
