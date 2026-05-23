import boto3
import os

BUCKET = "user-10293847-ueia-so" 
s3 = boto3.client("s3")

# ── SUBIR UN ARCHIVO ──────────────────────────────────────────
def subir(ruta_local, nombre_en_s3=None):
    nombre = nombre_en_s3 or os.path.basename(ruta_local)
    s3.upload_file(ruta_local, BUCKET, nombre)
    print(f"✅ Subido: {nombre}")

# ── VERIFICAR QUE EXISTE EN S3 ────────────────────────────────
def verificar(nombre_en_s3):
    respuesta = s3.head_object(Bucket=BUCKET, Key=nombre_en_s3)
    print(f"📋 Verificado: {nombre_en_s3} | Tamaño: {respuesta['ContentLength']} bytes")

# ── DESCARGAR UN ARCHIVO ──────────────────────────────────────
def descargar(nombre_en_s3, carpeta_destino="./descargas_boto3"):
    os.makedirs(carpeta_destino, exist_ok=True)
    destino = f"{carpeta_destino}/{nombre_en_s3}"
    s3.download_file(BUCKET, nombre_en_s3, destino)
    print(f"⬇️  Descargado en: {destino}")

# ── PRUEBA CON 3 ARCHIVOS ─────────────────────────────────────
archivos = ["texto1.txt", "texto2.txt", "texto3.txt"]

# Crear los 3 archivos localmente
for nombre in archivos:
    with open(nombre, "w") as f:
        f.write(f"Contenido de {nombre}\n")

print("=== SUBIENDO 3 ARCHIVOS ===")
for nombre in archivos:
    subir(nombre)
    verificar(nombre)

print("\n=== DESCARGANDO 3 ARCHIVOS ===")
for nombre in archivos:
    descargar(nombre)

print("\n✅ Prueba completa")
