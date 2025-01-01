import serial

# ตั้งค่าพอร์ต COM11
printer = serial.Serial(
    port="COM11",       
    baudrate=9600,     
    bytesize=8,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

# ทดสอบส่งข้อมูลไปยังเครื่องพิมพ์
printer.write(b"Hello, Epson TM-T82X!\n")  # ข้อความ
printer.write(b"\x1d\x56\x42\x00")        # คำสั่งตัดกระดาษ (ESC/POS)

# ปิดการเชื่อมต่อ
printer.close()
