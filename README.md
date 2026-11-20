# API Python – Redes Cisco (Packet Tracer)

Conjunto de scripts en Python que consumen la API REST de **Cisco Packet Tracer** (`http://localhost:58000/api/v1`) para autenticarse, consultar dispositivos y hosts de la red, y generar un informe de la topología.

Los scripts `01` a `04` son los suministrados por la cátedra. El script `05` es el desarrollado por el grupo.

## Requisitos

- Python 3.8 o superior
- Cisco Packet Tracer abierto, con la API habilitada y escuchando en `localhost:58000`
- Bibliotecas listadas en `requirements.txt`:

```bash
pip install -r requirements.txt
```

> **Importante:** no se sube al repositorio la carpeta del entorno virtual (`cisco`, `.venv`, `venv`, etc.) ni archivos con usuarios o contraseñas (`.env`). El `.gitignore` ya los excluye.

## Descripción de los scripts

### Scripts de la cátedra

| Script | Descripción |
|--------|-------------|
| `01_get-ticket.py` | Se autentica contra la API (`POST /ticket`) con usuario y contraseña, e imprime el estado de la solicitud y el **service ticket** que devuelve el servidor. Ese ticket es el que se usa como `X-Auth-Token` en las demás consultas. |
| `02_get-network-device.py` | Consulta `GET /network-device` usando un token y muestra el listado de **dispositivos de red** (routers y switches) con todos sus datos. Tiene comentada una línea para imprimir solo hostname, plataforma e IP de administración. |
| `03_get-host.py` | Consulta `GET /host` y muestra, por cada **host** (PC, servidores, etc.), su nombre, IP, MAC y la interfaz a la que está conectado. |
| `04_tabulate.py` | Script completo: obtiene el ticket, consulta los dispositivos de red y los hosts, y los muestra en **tablas ordenadas** en consola usando la biblioteca `tabulate`. Dispositivos: hostname, número de serie y versión de software. Hosts: hostname, tipo e IP. |

> Nota: los scripts `02` y `03` traen un token fijo en el código. Los tokens vencen, por lo que hay que ejecutar primero `01_get-ticket.py` y reemplazar el valor de `X-Auth-Token` por el ticket nuevo. Los scripts `01` y `04` usan credenciales distintas entre sí; deben coincidir con las configuradas en Packet Tracer.

### Script propio del grupo

| Script | Descripción |
|--------|-------------|
| `05_informe_de_dispositivos.py` | Genera un **informe de la topología** en dos archivos. Funciona así: <br>1. Se autentica y obtiene el ticket. <br>2. Consulta los hosts (`/host`), los routers y switches (`/network-device`) y la topología física (`/topology/physical-topology`). <br>3. Guarda la topología completa en `topologia_json.json`. <br>4. Genera `topologia.csv` (separador `;`, codificación UTF-8 con BOM para abrir bien en Excel) con dos secciones: **DISPOSITIVOS O PC** (tipo, nombre, IP, dispositivo al que están conectados e interfaz) y **ROUTER O SWITCH** (tipo, nombre e IP). <br>El script traduce la IP del dispositivo al que está conectado cada host por su nombre, para que el informe sea legible. Además maneja errores de conexión con Packet Tracer y de formato en las respuestas. |

**Archivos que genera:**

- `topologia.csv`: tabla de hosts y dispositivos de red.
- `topologia_json.json`: respuesta cruda de la topología física.

## Orden de uso sugerido

```bash
python 01_get-ticket.py                # 1. Verificar autenticación y obtener ticket
python 02_get-network-device.py        # 2. Listar routers y switches
python 03_get-host.py                  # 3. Listar hosts
python 04_tabulate.py                  # 4. Ver todo en tablas
python 05_informe_de_dispositivos.py   # 5. Generar informe (CSV + JSON)
```

## Autores

Grupo NN – Redes de Computadoras (3643)

*(Completar con los nombres de los integrantes.)*
