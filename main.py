from obspy import read

# Ruta del archivo .mseed y archivo de salida .txt
ruta_archivo_mseed_ejex = "SB.121..DP1.2022-12-30T13.59.19.ms"
ruta_archivo_mseed_ejey = "SB.121..DP2.2022-12-30T13.59.19.ms"
ruta_archivo_mseed_ejez = "SB.121..DPZ.2022-12-30T13.59.19.ms"

newName = ruta_archivo_mseed_ejex.split(".")
archivo_resultado = '{}.{}..{}.txt'.format(newName[0], newName[1], newName[4])

# Read the .mseed files
stx = read(ruta_archivo_mseed_ejex)
sty = read(ruta_archivo_mseed_ejey)
stz = read(ruta_archivo_mseed_ejez)

# Create an empty array for each coordinate
resultsX = []
resultsY = []
resultsZ = []

# Travel each Stream trace
for trace in stx:
    # Get the trace values
    # Append the value in the results array
    trace_values = trace.data
    resultsX.extend(trace_values)

for trace in sty:
    trace_values = trace.data
    resultsY.extend(trace_values)

for trace in stz:
    trace_values = trace.data
    resultsZ.extend(trace_values)

# get .mseed metadata
metadata = stx[0].stats
# Write the new information in an ascii type file
with (open(archivo_resultado, 'w') as archivo_txt):
    # metadata
    for clave, valor in metadata.items():
        archivo_txt.write(f"{clave.capitalize()}: {valor}\n")
    archivo_txt.write('Channels: 3\n')

    # results
    for i in range(len(resultsX)):
        linea = [
            f"{resultsX[i]}\t", f"{resultsY[i]}\t",
            f"{resultsZ[i]}\n"
        ]
        archivo_txt.write(''.join(linea))

    print("finished successfully")
