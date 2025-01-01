from PIL import Image, ImageDraw, ImageFont
from escpos.printer import Usb
import barcode
from barcode.writer import ImageWriter
import os

# สร้างโฟลเดอร์สำหรับบาร์โค้ดและคูปอง หากยังไม่มีอยู่
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
def generate_coupon(number, width_cm, height_cm, dpi=300):
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
    barcode_image.thumbnail((width_px - 40, height_px // 2))  # ปรับขนาดบาร์โค้ดให้พอดี
    image.paste(barcode_image, (20, height_px // 2))

    # บันทึกคูปองในโฟลเดอร์ Coupons
    image_path = f'Coupons/coupon_{number}.png'
    image.save(image_path)
    return image_path

# ฟังก์ชันพิมพ์คูปอง
def print_coupon(number):
    # กำหนดค่าการเชื่อมต่อ USB กับเครื่องพิมพ์ Epson TM-T82X
    printer = Usb(idVendor=0x04B8, idProduct=0x0E27, timeout=0)

    # เริ่มต้นการพิมพ์
    try:
        # พิมพ์หัวข้อ
        printer.set(align="center", font="a", width=2, height=2)
        printer.text("ร้าน ABC\n")
        printer.text("-------------------------------\n")
        
        # พิมพ์รายละเอียด
        printer.set(align="left", font="a", width=1, height=1)
        printer.text(f"หมายเลขคูปอง: {number}\n")
        printer.text("รับส่วนลด 20% สำหรับการซื้อครั้งถัดไป\n")
        printer.text("วันหมดอายุ: 31 ธันวาคม 2024\n")
        printer.text("-------------------------------\n")
        
        # พิมพ์บาร์โค้ด
        printer.barcode(str(number), 'CODE128', function_type='B')

        # ตัดกระดาษ
        printer.cut()

        print(f"พิมพ์คูปองหมายเลข {number} สำเร็จ!")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการพิมพ์: {e}")

# สร้างและพิมพ์คูปองตั้งแต่หมายเลข 1-10
for i in range(1, 11):
    print(f"กำลังสร้างคูปองหมายเลข {i}...")
    generate_coupon(i, 8, 15)  # ขนาด 8 ซม. x 15 ซม.
    print_coupon(i)
