import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import filedialog
from PIL import Image, ImageTk
import qrcode
import io

# Variable global para guardar el último QR generado
ultimo_qr = None

def generar_qr():
    global ultimo_qr
    url = entrada.get()
    if not url:
        estado.config(text="⚠️ Por favor, ingresá un link.")
        return

    opcion = combo_tamano.get()
    tamanos = {
        "Pequeño (100x100)": 100,
        "Mediano (200x200)": 200,
        "Grande (300x300)": 300,
        "Muy Grande (400x400)": 400
    }
    tamano = tamanos.get(opcion, 200)

    qr = qrcode.make(url)
    ultimo_qr = qr

    bio = io.BytesIO()
    qr.save(bio, format="PNG")
    bio.seek(0)
    img = Image.open(bio)
    img = img.resize((tamano, tamano))
    img_tk = ImageTk.PhotoImage(img)

    qr_imagen.config(image=img_tk)
    qr_imagen.image = img_tk
    estado.config(text="✅ Código QR generado.")

def guardar_qr():
    global ultimo_qr
    if not ultimo_qr:
        estado.config(text="⚠️ Primero generá un QR.")
        return

    archivo = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("Imagen PNG", "*.png")],
        title="Guardar QR como..."
    )

    if archivo:
        ultimo_qr.save(archivo)
        estado.config(text=f"💾 Guardado en:\n{archivo}")

# Tema: podés probar otros como "solar", "darkly", "superhero", "cyborg", etc.
app = tb.Window(themename="darkly")
app.title("🔲 Generador de QR Moderno")
app.geometry("900x650")
app.resizable(False, False)

# Título principal
tb.Label(app, text="🔗 Ingresá un link para generar tu QR", font=("Segoe UI", 18, "bold")).pack(pady=20)

# Entrada de texto
entrada = tb.Entry(app, font=("Segoe UI", 12), width=60)
entrada.pack(pady=10)

# Selector de tamaño
tb.Label(app, text="📏 Elegí tamaño del QR", font=("Segoe UI", 14)).pack(pady=(20, 5))
combo_tamano = tb.Combobox(app, values=[
    "Pequeño (100x100)",
    "Mediano (200x200)",
    "Grande (300x300)",
    "Muy Grande (400x400)"
], font=("Segoe UI", 12), state="readonly", width=30, bootstyle=PRIMARY)
combo_tamano.current(2)
combo_tamano.pack()

# Botones
botones_frame = tb.Frame(app)
botones_frame.pack(pady=30)

tb.Button(botones_frame, text="🎯 Generar QR", command=generar_qr, bootstyle=SUCCESS, width=20).grid(row=0, column=0, padx=10)
tb.Button(botones_frame, text="💾 Guardar QR", command=guardar_qr, bootstyle=INFO, width=20).grid(row=0, column=1, padx=10)

# Imagen del QR
qr_imagen = tb.Label(app)
qr_imagen.pack(pady=20)

# Estado
estado = tb.Label(app, text="", font=("Segoe UI", 11), anchor=CENTER)
estado.pack(pady=10)

app.mainloop()
