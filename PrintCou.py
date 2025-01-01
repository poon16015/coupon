from escpos.printer import Usb
from PIL import Image
import os



# ฟังก์ชันพิมพ์คูปองทั้งหมด
def print_all_coupons(folder="Coupons"):
    try:
        # หาไฟล์คูปองทั้งหมดในโฟลเดอร์
        files = sorted([f for f in os.listdir(folder) if f.endswith('.png')])

        # เชื่อมต่อเครื่องพิมพ์ (ปรับ ID ให้ตรงกับเครื่องของคุณ)
        printer = Usb(idVendor=0x04b8, idProduct=0x0e27)

        # พิมพ์คูปองทีละไฟล์
        for file in files:
            coupon_file = os.path.join(folder, file)
            if os.path.exists(coupon_file):
                printer.image(coupon_file)
                printer.cut()  # ตัดกระดาษหลังพิมพ์แต่ละใบ
                print(f"พิมพ์คูปอง {file} สำเร็จ!")
            else:
                print(f"ไม่พบไฟล์ {file} ในโฟลเดอร์ {folder}!")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

# เรียกพิมพ์คูปองทั้งหมด
if __name__ == "__main__":
    print_all_coupons()
