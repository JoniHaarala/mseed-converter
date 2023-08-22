# mseed2ascii-converter v1.3.0

## Convert miniSEED time series data to ASCII

Convert miniSEED formatted time series data to ASCII text.  The output
includes a simple header followed by using ObsPy package.

### Documentation
Here you have a simplify documentation of how to use program

- importing obspy library

`from obspy import read`

- Read .mseed file

`st = read(ruta_archivo_mseed)`

- Get metadata data

`metadatos = st[0].stats`

- Write file information in a .txt file
```
  with open(ruta_archivo_txt, 'w') as archivo_txt:
  archivo_txt.write(f"Fecha de la medición: {fecha_medicion}\n")

  #metadata
  archivo_txt.write("\nMetadatos:\n")
  for clave, valor in metadatos.items():
    archivo_txt.write(f"{clave}: {valor}\n")

  #results
  archivo_txt.write("Resultados:\n")
  for resultado in resultados:
    archivo_txt.write(f"{resultado}\n")
```
### Tecnologies
- [Python](https://www.python.org/)
- [ObsPy](https://docs.obspy.org/index.html "ObsPy")

### Licensing

Apache license version 2.0. See included LICENSE file for details.

Copyright (c) 2023 Jonatan Haarala
