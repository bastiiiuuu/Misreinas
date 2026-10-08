"""Dibuja los envases genéricos del prototipo; no son fotos ni marcas reales.

Ejecutar con el Python del proyecto. Solo requiere Pillow, ya utilizado por Django.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

DESTINO = Path(__file__).resolve().parents[1] / "inicio/static/inicio/img/productos"
DESTINO.mkdir(parents=True, exist_ok=True)
NAVY = "#10243a"


def font(size):
    try:
        return ImageFont.truetype("C:/Windows/Fonts/seguisb.ttf", size)
    except OSError:
        return ImageFont.load_default(size=size)


def ilustracion(tipo):
    image = Image.new("RGB", (560, 420), "#f2f4f5")
    d = ImageDraw.Draw(image)
    d.ellipse((100, 333, 460, 365), fill="#dce1e5")

    def label(box, color, title, subtitle="MIS REINAS"):
        d.rounded_rectangle(box, radius=12, fill=color)
        x = (box[0] + box[2]) / 2
        d.text((x, box[1] + 13), title, font=font(25), fill="white", anchor="mt")
        d.text((x, box[3] - 14), subtitle, font=font(12), fill="white", anchor="mb")

    if tipo == "pan":
        d.ellipse((110, 127, 450, 340), fill="#bc772f", outline="#a66729", width=4)
        d.ellipse((110, 110, 450, 310), fill="#e7b15e")
        for x in (200, 280, 360):
            d.line((x - 20, 145, x + 10, 220), fill="#fff0c6", width=15)
    elif tipo == "leche":
        d.polygon([(195, 105), (230, 60), (335, 60), (365, 105), (365, 345), (195, 345)], fill="#fafcff", outline="#a3b6c9", width=4)
        d.polygon([(195, 105), (230, 60), (335, 60), (310, 105)], fill="#8bb7dc")
        d.line((195, 105, 365, 105), fill="#a3b6c9", width=4)
        label((196, 180, 364, 310), "#377bb3", "LECHE", "ENTERA · 1 L")
    elif tipo in {"arroz", "mascotas"}:
        color = "#efe1bb" if tipo == "arroz" else "#b97c4e"
        d.polygon([(192, 65), (365, 65), (350, 110), (375, 340), (185, 340), (207, 110)], fill=color, outline="#c3b18d", width=4)
        label((197, 139, 362, 243), "#35785c" if tipo == "arroz" else NAVY, "ARROZ" if tipo == "arroz" else "MASCOTAS", "1 KG")
        if tipo == "arroz":
            for x, y in [(230, 278), (266, 293), (299, 274), (330, 299)]:
                d.ellipse((x, y, x + 20, y + 9), fill="white")
        else:
            d.ellipse((257, 285, 305, 322), fill="#efce9d")
            for x, y in [(242, 268), (268, 258), (296, 265), (315, 282)]:
                d.ellipse((x, y, x + 19, y + 20), fill="#efce9d")
    elif tipo == "fideos":
        d.rounded_rectangle((184, 65, 375, 343), radius=18, fill="#ba4a3d")
        d.rounded_rectangle((212, 165, 348, 301), radius=14, fill="#f2d69b")
        for x in range(225, 340, 15):
            d.line((x, 175, x, 286), fill="#e1b359", width=8)
        label((188, 77, 371, 155), "#ba4a3d", "FIDEOS", "400 G")
    elif tipo == "agua":
        d.rounded_rectangle((181, 122, 378, 344), radius=35, fill="#a8d8e8", outline="#5794b3", width=4)
        d.rounded_rectangle((250, 76, 310, 134), radius=12, fill="#a8d8e8", outline="#5794b3", width=4)
        d.rounded_rectangle((245, 64, 315, 85), radius=7, fill="#3377a4")
        d.rounded_rectangle((210, 136, 345, 173), radius=14, outline="#5794b3", width=8)
        label((184, 208, 375, 302), "#3377a4", "AGUA", "PURIFICADA · 6 L")
    elif tipo == "helado":
        d.polygon([(211, 220), (349, 220), (280, 355)], fill="#dca15c", outline="#ba7c3d", width=4)
        for y in (240, 262, 284):
            d.line((228, y, 330, y + 12), fill="#ba7c3d", width=3)
        d.ellipse((204, 153, 355, 253), fill="#a26c50")
        d.ellipse((208, 110, 350, 220), fill="#f0b6c5")
        d.ellipse((240, 65, 324, 147), fill="#fff0d2")
    elif tipo == "chocolate":
        d.rounded_rectangle((177, 75, 384, 345), radius=14, fill="#75452c")
        for x in (194, 253, 312):
            for y in (92, 147):
                d.rounded_rectangle((x, y, x + 52, y + 46), radius=5, fill="#996340", outline="#593522", width=2)
        label((177, 220, 384, 345), "#b13e42", "CHOCOLATE", "100 G")
    elif tipo == "bebida":
        d.polygon([(247, 72), (314, 72), (314, 121), (343, 161), (354, 192), (354, 338), (208, 338), (208, 192), (217, 161), (247, 121)], fill="#694439", outline="#3c3131", width=4)
        d.rounded_rectangle((241, 54, 320, 79), radius=5, fill="#bb4947")
        label((208, 195, 354, 291), "#bb4947", "COLA", "1,5 L")
    elif tipo == "huevos":
        d.rounded_rectangle((112, 213, 450, 345), radius=20, fill="#b8a382", outline="#958567", width=4)
        for x, y in [(140, 160), (239, 160), (338, 160), (140, 210), (239, 210), (338, 210)]:
            d.ellipse((x, y, x + 78, y + 110), fill="#f2dbc1", outline="#d2ba9b", width=3)
        label((112, 295, 450, 351), "#847358", "HUEVOS", "PACK DE 6")

    d.text((280, 389), "ILUSTRACIÓN · DEMOSTRACIÓN", fill="#667887", font=font(13), anchor="mm")
    image.save(DESTINO / f"{tipo}.png", optimize=True)


if __name__ == "__main__":
    for producto in ("pan", "leche", "arroz", "fideos", "mascotas", "agua", "helado", "chocolate", "bebida", "huevos"):
        ilustracion(producto)
    print("10 ilustraciones generadas en", DESTINO)
