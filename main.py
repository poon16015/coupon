from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import os


# สร้างโฟลเดอร์สำหรับบาร์โค้ดและคูปอง
if not os.path.exists('barcodes'):
    os.makedirs('barcodes')
if not os.path.exists('Coupons'):
    os.makedirs('Coupons')

# ฟังก์ชันสร้างบาร์โค้ด
def generate_barcode(number):
    EAN = barcode.get_barcode_class('code128')
    ean = EAN(str(number), writer=ImageWriter())
    filename = f'barcodes/barcode_{number}'
    ean.save(filename)
    return f'{filename}.png'

# ฟังก์ชันสร้างคูปอง
def generate_coupon_image(number, width_cm, height_cm, dpi=203):
    # แปลงเซนติเมตรเป็นพิกเซล
    width_px = int(width_cm * dpi / 2.54)
    height_px = int(height_cm * dpi / 2.54)

    # สร้างภาพคูปอง
    image = Image.new('RGB', (width_px, height_px), color='white')
    draw = ImageDraw.Draw(image)

    # โหลดฟอนต์ (ใช้ฟอนต์ Arial หรือฟอนต์เริ่มต้น)
    try:
        font_title = ImageFont.truetype("arial.ttf", 24)  # ฟอนต์สำหรับชื่อร้านค้า
        font_text = ImageFont.truetype("arial.ttf", 18)   # ฟอนต์สำหรับข้อความทั่วไป
    except IOError:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()

    # เพิ่มชื่อร้านค้า
    draw.text((20, 20), "ร้าน ABC", fill='black', font=font_title)

    # เพิ่มรายละเอียดคูปอง
    draw.text((20, 60), f"หมายเลขคูปอง: {number}", fill='black', font=font_text)
    draw.text((20, 90), "รับส่วนลด 20% สำหรับการซื้อครั้งถัดไป", fill='black', font=font_text)
    draw.text((20, 120), "วันหมดอายุ: 31 ธันวาคม 2024", fill='black', font=font_text)

    # เพิ่มบาร์โค้ด
    barcode_image = Image.open(generate_barcode(number))
    
    # ปรับขนาดบาร์โค้ดให้กว้างไม่เกินคูปอง
    max_width = width_px - 40
    barcode_image.thumbnail((max_width, height_px // 4))  # ลดความสูงให้เหมาะสม (1/4 ของความสูง)

    # คำนวณตำแหน่งกึ่งกลาง
    barcode_x = (width_px - barcode_image.width) // 2
    barcode_y = (height_px - barcode_image.height) // 2

    # วางบาร์โค้ดที่กึ่งกลาง
    image.paste(barcode_image, (barcode_x, barcode_y))

    return image

# ฟังก์ชันสร้างและบันทึกคูปอง
def create_and_save_coupons(start_number, end_number, width_cm, height_cm):
    for number in range(start_number, end_number + 1):
        coupon_image = generate_coupon_image(number, width_cm, height_cm)
        filename = f'Coupons/coupon_{number}.png'
        coupon_image.save(filename)
        print(f"บันทึกคูปอง {filename} สำเร็จ!")

# สร้างคูปองหมายเลข 1-10
create_and_save_coupons(1, 10, 8, 15)  # กว้าง 8 ซม. สูง 15 ซม.

print("สร้างคูปองทั้งหมดสำเร็จ!")
