
import streamlit as st
import qrcode
from io import BytesIO

st.set_page_config(
    page_title="QR Studio | QR Generator",
    page_icon="🔳",
    layout="centered"
)

# Professional styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f3ff, #ffffff);
}
h1 {
    color: #4f46e5;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: #64748b;
    font-size: 17px;
}
div.stButton > button {
    background: #4f46e5;
    color: white;
    border-radius: 10px;
    border: none;
    width: 100%;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🔳 QR Studio")
st.markdown(
    '<p class="subtitle">Create beautiful custom QR codes in seconds.</p>',
    unsafe_allow_html=True
)

st.divider()

st.subheader("1. Enter your content")

data = st.text_area(
    "Website URL or text",
    placeholder="https://www.google.com",
    height=100
)

st.subheader("2. Customize your design")

col1, col2 = st.columns(2)

with col1:
    qr_color = st.color_picker(
        "QR pattern color",
        "#4F46E5"
    )

with col2:
    bg_color = st.color_picker(
        "Background color",
        "#FFFFFF"
    )

st.info("Tip: Choose a dark pattern color and a light background for easier scanning.")

if st.button("✨ Generate QR Code"):
    if not data.strip():
        st.warning("Please enter some text or a URL.")
    else:
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4
            )

            qr.add_data(data.strip())
            qr.make(fit=True)

            img = qr.make_image(
                fill_color=qr_color,
                back_color=bg_color
            )

            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_bytes = buffer.getvalue()

            st.session_state["qr_bytes"] = qr_bytes
            st.session_state["qr_data"] = data.strip()

        except Exception as e:
            st.error(f"Could not generate QR code: {e}")

if "qr_bytes" in st.session_state:
    st.divider()
    st.subheader("3. Your QR Code")

    st.image(
        st.session_state["qr_bytes"],
        caption="Your custom QR code",
        width=280
    )

    st.download_button(
        label="⬇️ Download QR Code (PNG)",
        data=st.session_state["qr_bytes"],
        file_name="custom_qr.png",
        mime="image/png",
        use_container_width=True
    )

    st.success("Your QR code is ready!")
    
st.divider()

st.caption("QR Studio • Built with Python 3.13")