from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import boto3
import psycopg2
from datetime import datetime
import os
from mangum import Mangum

app = FastAPI()

# Configuración
BUCKET = "user-10293847-ueia-so"
DB_HOST = "taller-db.cd4o0osm03ry.us-east-2.rds.amazonaws.com"
DB_USER = "postgres"
DB_PASS = "ValePostgres"
DB_NAME = "postgres"

s3 = boto3.client("s3")

def get_db():
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        dbname=DB_NAME
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS imagenes (
            id SERIAL PRIMARY KEY,
            usuario VARCHAR(100),
            ruta_s3 VARCHAR(500),
            fecha_creacion TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.on_event("startup")
def startup():
    init_db()

@app.post("/upload")
async def upload_image(usuario: str, file: UploadFile = File(...)):
    # Validar formato
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=415, detail="Solo se aceptan PNG o JPG")
    
    # Subir a S3
    s3_key = f"{usuario}/{file.filename}"
    s3.upload_fileobj(file.file, BUCKET, s3_key)
    
    # Guardar en RDS
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO imagenes (usuario, ruta_s3, fecha_creacion) VALUES (%s, %s, %s)",
        (usuario, s3_key, datetime.now())
    )
    conn.commit()
    cur.close()
    conn.close()
    
    return {"mensaje": "Imagen subida correctamente", "ruta": s3_key}

@app.get("/imagen")
def get_image(usuario: str, nombre: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT ruta_s3, fecha_creacion FROM imagenes WHERE usuario=%s AND ruta_s3=%s",
        (usuario, f"{usuario}/{nombre}")
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Usuario o imagen no encontrada")
    
    # Generar URL prefirmada
    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": row[0]},
        ExpiresIn=3600
    )
    
    return {"url": url, "fecha_creacion": row[1]}

handler = Mangum(app)
