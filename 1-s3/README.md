## B-5 ¿Qué cambia al manejar múltiples archivos?

Con un solo archivo, `aws s3 cp` trabaja de archivo a archivo:
- Le indicas exactamente qué archivo subir y a qué ruta llega.
- AWS transfiere solo ese objeto.

Con múltiples archivos cambian tres cosas:

1. **Apuntas a carpetas, no a archivos.** En lugar de un archivo como origen,
   le das una carpeta local, y como destino una "carpeta" dentro del bucket.

2. **Necesitas la bandera `--recursive`.** Sin ella, AWS CLI no entra a la
   carpeta y no sube nada. Con `--recursive` recorre todos los archivos
   dentro y los sube uno por uno automáticamente.

3. **Se conserva la estructura de subcarpetas.** Si tienes `varios/uno.txt`
   y `varios/dos.txt`, en S3 quedan como `s3://bucket/varios/uno.txt` y
   `s3://bucket/varios/dos.txt`. La jerarquía se mantiene.

