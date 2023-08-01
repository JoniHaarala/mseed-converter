from obspy import read, UTCDateTime

# Ruta del archivo .mseed y archivo de salida .txt
ruta_archivo_mseed = "route/file.ms"
ruta_archivo_txt = "route/result.txt"

# Leer el archivo .mseed
st = read(ruta_archivo_mseed)
# print(st)
# print(st[0].stats)
# print(st[0].data)
data = st[0].data

# Obtener la fecha de la medición
fecha_medicion = st[0].stats.starttime

# Crear una lista para almacenar los resultados
resultados = []

# Recorrer cada traza en el Stream
for traza in st:
  # Obtener los valores de la traza
  valores_traza = traza.data
  # Agregar los valores a la lista de resultados
  resultados.extend(valores_traza)

# Obtener los metadatos del archivo .mseed
metadatos = st[0].stats

# Escribir la información en el archivo .txt
with open(ruta_archivo_txt, 'w') as archivo_txt:
  archivo_txt.write(f"Fecha de la medición: {fecha_medicion}\n")
  #metadatos
  archivo_txt.write("\nMetadatos:\n")
  for clave, valor in metadatos.items():
    archivo_txt.write(f"{clave}: {valor}\n")
  #resultados
  archivo_txt.write("Resultados:\n")
  for resultado in resultados:
    archivo_txt.write(f"{resultado/1000}\n")

print("finished")
