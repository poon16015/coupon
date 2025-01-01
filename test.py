from escpos.printer import Usb
from PIL import Image

# เชื่อมต่อกับเครื่องพิมพ์ผ่าน USB
# ตัวอย่าง: idVendor=0x04b8 (Epson), idProduct=0x0e15 (ขึ้นอยู่กับรุ่น)
try:
    printer = Usb(0x04b8, 0x0e15)  # แก้ไขค่า idVendor และ idProduct ให้ตรงกับเครื่องพิมพ์ของคุณ
except Exception as e:
    print(f"ไม่สามารถเชื่อมต่อเครื่องพิมพ์ได้: {e}")
    exit()

# ข้อความบนใบเสร็จ
printer.text("ร้าน ABC\n")
printer.text("หมายเลขคูปอง: 123456\n")
printer.text("รับส่วนลด 20% สำหรับการซื้อครั้งถัดไป\n")
printer.text("วันหมดอายุ: 31 ธันวาคม 2024\n\n")

# พิมพ์บาร์โค้ด
printer.barcode("123456", "CODE128", width=2, height=100, pos='CENTER')

# เพิ่มบรรทัดว่าง
printer.text("\n\n")

# ปิดการเชื่อมต่อเครื่องพิมพ์
printer.cut()
