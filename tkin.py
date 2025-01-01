import tkinter as tk
from tkinter import messagebox
import serial # type: ignore
from PIL import Image, ImageDraw, ImageFont
import barcode # type: ignore
from barcode.writer import ImageWriter # type: ignore
import os

file_path_txt = "C:/Users/poony/Desktop/aaa/coupon_template.txt"

# ฟังก์ชันสร้างบาร์โค้ด
def generate_barcode(number):
    EAN = barcode.get_barcode_class('code128')
    ean = EAN(str(number), writer=ImageWriter())
    filename = f'barcodes/barcode_{number}'
    ean.save(filename)
    return f'{filename}.png'

# ฟังก์ชันสร้างคูปอง
def generate_coupon(number, prefix, width_cm, height_cm, dpi=300):
    full_number = f"{prefix}{number}"
    width_px = int(width_cm * dpi / 2.54)
    height_px = int(height_cm * dpi / 2.54)
    image = Image.new('RGB', (width_px, height_px), color='white')
    draw = ImageDraw.Draw(image)

    barcode_image = Image.open(generate_barcode(full_number))
    barcode_image.thumbnail((width_px - 40, height_px // 2))
    image.paste(barcode_image, (20, height_px // 2))

    image_path = f'Coupons/coupon_{full_number}.png'
    image.save(image_path)
    return image_path

# # ฟังก์ชันพิมพ์คูปองด้วย PySerial
# def print_coupon(serial_port, baud_rate, number, prefix):
#     full_number = f"{prefix}{number}"
#     try:
#         # เปิดการเชื่อมต่อ Serial
#         with serial.Serial(port=serial_port, baudrate=baud_rate, timeout=1) as printer:
#             # พิมพ์หัวข้อ
#             printer.write(b"\x1B\x61\x01")  # ตั้งค่าการจัดกลาง
#             printer.write(b"ABC\n".encode('utf-8'))
#             printer.write(b"-------------------------------\n".encode('utf-8'))

#             # พิมพ์รายละเอียดคูปอง
#             printer.write(b"\x1B\x61\x00")  # ตั้งค่าการจัดซ้าย
#             printer.write(f"หมายเลขคูปอง: {full_number}\n".encode('utf-8'))
#             printer.write("รับส่วนลด 20% สำหรับการซื้อครั้งถัดไป\n".encode('utf-8'))
#             printer.write("วันหมดอายุ: 31 ธันวาคม 2024\n".encode('utf-8'))
#             printer.write(b"-------------------------------\n")

#             # พิมพ์บาร์โค้ด
#             printer.write(b"\x1D\x6B\x04")  # คำสั่ง ESC/POS พิมพ์บาร์โค้ด (Code128)
#             printer.write(full_number.encode('utf-8') + b"\x00")

#             # ตัดกระดาษ
#             printer.write(b"\x1D\x56\x42\x00")  # คำสั่ง ESC/POS ตัดกระดาษแบบเต็ม

#         print(f"พิมพ์คูปองหมายเลข {full_number} สำเร็จ!")
#     except Exception as e:
#         print(f"เกิดข้อผิดพลาดในการพิมพ์: {e}")


# ฟังก์ชันพิมพ์บาร์โค้ดด้วย PySerial
# def print_barcode(serial_port, baud_rate, number, prefix):
#     full_number = f"{prefix}{number}"
#     try:
#         with open('C:/Users/poony/Desktop/aaa/coupon_template.txt','r',encoding='utf-8') as file :
#             line1 = file.readlines(1).strip()
#             line2 = file.readlines(2).strip()


#         # เปิดการเชื่อมต่อ Serial
#         with serial.Serial(port=serial_port, baudrate=baud_rate, timeout=1) as printer:
#             # พิมพ์บาร์โค้ด

            
#             printer.write(b"\x1B\x61\x01") # ตั้งค่าการจัดกลาง 
          
#             printer.write(f"{line1}\n".encode('utf-8')) # อ่านจาก txt บันทัด 1
#             printer.write(f"{line2}\n".encode('utf-8')) # อ่านจาก txt บันทัด 2

#             printer.write(b"\x1D\x6B\x04") # คำสั่ง ESC/POS พิมพ์บาร์โค้ด (Code128) 
#             printer.write(full_number.encode('utf-8') + b"\x00") 
#             printer.write(f"{full_number}\n".encode('utf-8'))

#             # ตัดกระดาษ
#             printer.write(b"\x1D\x56\x42\x00")  # คำสั่ง ESC/POS ตัดกระดาษแบบเต็ม

#         print(f"พิมพ์บาร์โค้ดหมายเลข {full_number} สำเร็จ!")
#     except Exception as e:
#         print(f"เกิดข้อผิดพลาดในการพิมพ์: {e}")


def print_barcode(serial_port, baud_rate, file_path_txt, prefix):
    try:
        # อ่านข้อมูลจากไฟล์
        with open(file_path_txt, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        # แทนที่ placeholder ด้วยค่าจริง
        full_number = f"{prefix}{lines[1].strip()}"
        lines[1] = lines[1].replace("<number>", full_number)
        lines[2] = lines[2].replace("<barcode>", full_number)

        # เปิดการเชื่อมต่อ Serial
        with serial.Serial(port=serial_port, baudrate=baud_rate, timeout=1) as printer:
            # ตั้งค่าการจัดกลาง
            printer.write(b"\x1B\x61\x01")
            
            # พิมพ์ข้อความแต่ละบรรทัด
            for line in lines:
                printer.write(f"{line.strip()}\n".encode('utf-8'))

            # พิมพ์หมายเลขบาร์โค้ด
            printer.write(f"{full_number}\n".encode('utf-8'))

            # พิมพ์บาร์โค้ด (Code128)
            printer.write(b"\x1D\x6B\x04")
            printer.write(full_number.encode('utf-8') + b"\x00")
            
          

            # ตัดกระดาษ
            printer.write(b"\x1D\x56\x42\x00")  # คำสั่ง ESC/POS ตัดกระดาษแบบเต็ม

        print(f"พิมพ์คูปองพร้อมบาร์โค้ดหมายเลข {full_number} สำเร็จ!")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการพิมพ์: {e}")


# ฟังก์ชันสำหรับกรอกข้อมูลจาก GUI
def generate_and_print():
    try:
        start_num = int(entry_start.get())
        end_num = int(entry_end.get())
        prefix = entry_prefix.get()

        if start_num > end_num:
            messagebox.showerror("Error", "หมายเลขเริ่มต้นต้องน้อยกว่าหมายเลขสิ้นสุด")
            return

        serial_port = "COM11"  # ระบุพอร์ต Serial ที่เครื่องพิมพ์เชื่อมต่อ
        baud_rate = 9600      # ค่า Baud rate ของเครื่องพิมพ์

        for i in range(start_num, end_num + 1):
            generate_coupon(i, prefix, 8, 9)  # ขนาด 8 x 9 ซม
            print_barcode(serial_port, baud_rate, i, prefix)

        messagebox.showinfo("สำเร็จ", "พิมพ์คูปองทั้งหมดเสร็จสิ้น")
    
    except ValueError:
        messagebox.showerror("Error", "กรุณากรอกหมายเลขให้ถูกต้อง")

# สร้างหน้าต่าง GUI
root = tk.Tk()
root.title("เครื่องมือพิมพ์คูปอง")

# เลย์เอาต์ของ GUI
label_prefix = tk.Label(root, text="ตัวอักษรนำหน้า:")
label_prefix.grid(row=0, column=0, padx=10, pady=10)
entry_prefix = tk.Entry(root)
entry_prefix.grid(row=0, column=1, padx=10, pady=10)

label_start = tk.Label(root, text="หมายเลขเริ่มต้น:")
label_start.grid(row=1, column=0, padx=10, pady=10)
entry_start = tk.Entry(root)
entry_start.grid(row=1, column=1, padx=10, pady=10)

label_end = tk.Label(root, text="หมายเลขสิ้นสุด:")
label_end.grid(row=2, column=0, padx=10, pady=10)
entry_end = tk.Entry(root)
entry_end.grid(row=2, column=1, padx=10, pady=10)



button_generate = tk.Button(root, text="พิมพ์คูปอง", command=generate_and_print)
button_generate.grid(row=3, column=0, columnspan=2, pady=20)

# รัน GUI
root.mainloop()
