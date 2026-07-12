import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

# 1. ตั้งค่าหน้าเว็บแบบ Premium Layout
st.set_page_config(page_title="TWI Analyzer - พี่โจ รีเจนตามงบ", page_icon="🚀", layout="centered")

st.markdown("""
<style>
    div.stButton > button:first-child {
        background-color: #ff0050 !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        padding: 12px !important;
        box-shadow: 0px 4px 15px rgba(255, 0, 80, 0.3);
    }
    .stNumberInput, .stTextInput {
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 TWI Analyzer v4.2 (ระบบ Groq สายฟรีร้อยเปอร์เซ็นต์)")
st.caption("⚡ สมองกลวิเคราะห์สินค้าวิน & พิมพ์เขียวคอนเทนต์ | สไตล์ พี่โจ รีเจนตามงบ")
st.markdown("---")

# 2. เชื่อมต่อระบบหลังบ้าน Groq
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("🔑 ไม่พบรหัสกุญแจในระบบ Secrets กรุณาใส่รหัส GROQ_API_KEY ก่อนครับพี่โจ")

# 3. จัดกลุ่มกล่องข้อมูลการตลาด
with st.container(border=True):
    st.markdown("### 📦 ข้อมูลการตลาดและผลตอบแทน")
    col1, col2 = st.columns(2)
    with col1:
        price = st.number_input("💵 ราคาสินค้าปัจจุบัน (บาท)", min_value=0, value=290, step=1)
    with col2:
        commission = st.number_input("💰 ค่าคอมมิชชันที่ได้รับ (%)", min_value=0, max_value=100, value=15, step=1)
    promo = st.text_input("🎁 โปรโมชั่นที่จัดตอนนี้", value="ส่งฟรี")

st.markdown("---")

# ฟังก์ชันแปลงรูปภาพเป็น Base64 ส่งให้ Groq อ่าน
def encode_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# 4. ส่วนอัปโหลดรูปภาพ
st.subheader("📸 อัปโหลดรูปภาพสถิติ")
uploaded_file = st.file_uploader("เลือกรูปภาพแดชบอร์ด 7 วันย้อนหลัง", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="รูปภาพแดชบอร์ดที่อัปโหลดเข้าสู่ระบบ", use_container_width=True)
    
    if st.button("🚀 เริ่มสแกนและวิเคราะห์ผลด่วน"):
        with st.spinner("🧙‍♂️ เลขาจีกำลังส่งข้อมูลให้ระบบ Groq ถอดรหัสภาพสักครู่ครับ..."):
            try:
                # แปลงภาพ
                base64_image = encode_image_to_base64(image)
                
                prompt = f"""
                คุณคือผู้เชี่ยวชาญด้าน TikTok Affiliate Marketing และเป็นสมองกลของช่อง "พี่โจ รีเจนตามงบ"
                กรุณาสแกนรูปภาพแดชบอร์ด TikTok Shop 7 วันนี้ เพื่ออ่านค่า Orders, CTR, จำนวนครีเอเตอร์, และการเพิ่มลงรถเข็น
                พร้อมคำนวณคะแนนรวม TWI (เต็ม 100) โดยแบ่งสัดส่วน: แดชบอร์ด 70 คะแนน, ราคาไม่เกิน 290 บาท 15 คะแนน, ค่าคอมฯ 15% ขึ้นไป 15 คะแนน
                
                ข้อมูลสินค้าเพิ่มเติม: ราคา {price} บาท, ค่าคอม {commission}%, โปรโมชั่น {promo}

                กรุณาสรุปผลลัพธ์เป็นภาษาไทย โดยแบ่งเนื้อหาออกเป็น 3 ส่วนเพื่อนำไปใส่ในระบบ Tab ดังนี้:
                
                [PART_1]
                เขียนคะแนนสรุปตัวเลขดิบเพียวๆ บรรทัดแรก เช่น คะแนน: 88
                และระบุช่วงกลุ่มผลการตัดสินใจจาก 4 ช่วงนี้ให้ชัดเจน:
                - ช่วง 85 - 100 คะแนน: [🏆 สินค้าโคตรวิน ทุบยอดขายด่วน!]
                - ช่วง 65 - 84 คะแนน: [⭐️ กระแสดี น่าบิ้วด์ตามงบ]
                - ช่วง 40 - 64 คะแนน: [⏳ เหนื่อยผลักดัน ต้องปั้นด้วยคอนเทนต์]
                - ช่วง ต่ำกว่า 40 คะแนน: [❌ ข้ามไปก่อน อย่าหาทำเสียเวลา]
                พร้อมวิเคราะห์ความคุ้มค่าลึกซึ้งในมุมมองราคา {price} บาท และค่าคอม {commission}% ว่าคุ้มค่าแรงไหม
                
                [PART_2]
                ### 🎬 พิมพ์เขียวคอนเทนต์และแผนงานทำคลิป
                - **🎬 จำนวนคลิปที่ต้องทำอย่างน้อย**: ระบุจำนวนคลิปตามเกณฑ์ช่วงคะแนน
                - **🎯 มุมมองการทำคอนเทนต์ (Content Angles)**: แจกแจงมุมมองการเล่าเรื่องของแต่ละคลิปให้ฉีกกัน
                - **🔥 ประโยคเปิดคลิปหยุดนิ้ว (3-Second Hooks)**: คิดประโยคเปิดคลิปที่กระชากใจตรงกับมุมมองและราคาสินค้า
                - **🛒 ประโยค CTA ปิดการขาย**: คิดประโยคปิดท้ายคลิปที่กระตุ้นให้คนดูจิ้มตะกร้าเหลืองทันที
                
                [PART_3]
                ### 📈 รายงานตัวเลขสถิติจากแดชบอร์ด
                - ระบุค่าตัวเลข Orders, CTR, จำนวนครีเอเตอร์, รถเข็น ที่คุณอ่านได้จริงจากภาพแดชบอร์ด
                """
                
                # สั่งงานผ่านโมเดลสายตาอันทรงพลังของ Llama 3.2
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}",
                                    },
                                },
                            ],
                        }
                    ],
                    model="llama-3.2-11b-vision-preview",
                )
                
                raw_text = chat_completion.choices[0].message.content
                
                # แยกข้อมูลลงแท็บ
                parts = raw_text.split("[PART_")
                part1 = parts[1].replace("1]", "") if len(parts) > 1 else raw_text
                part2 = parts[2].replace("2]", "") if len(parts) > 2 else "ไม่มีข้อมูลพิมพ์เขียว"
                part3 = parts[3].replace("3]", "") if len(parts) > 3 else "ไม่มีข้อมูลสถิติ"
                
                st.success("✨ เนรมิตข้อมูลสำเร็จแล้วครับพี่โจ!")
                
                tab1, tab2, tab3 = st.tabs(["📊 ผลการประเมิน TWI", "🎬 แผนงานทำคอนเทนต์", "📈 ตัวเลขสถิติจริง"])
                
                with tab1:
                    with st.container(border=True):
                        st.markdown(part1)
                with tab2:
                    with st.container(border=True):
                        st.markdown(part2)
                with tab3:
                    with st.container(border=True):
                        st.markdown(part3)
                
            except Exception as e:
                st.error(f"❌ เกิดข้อผิดพลาดหลังบ้าน: {str(e)}")
