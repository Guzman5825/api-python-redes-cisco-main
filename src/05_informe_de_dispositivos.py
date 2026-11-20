import requests
import csv
import json

# ========================================== CONFIGURACION

BASE_URL = "http://localhost:58000/api/v1"

USUARIO = "admin"
PASSWORD = "admin"

ARCHIVO_CSV = "topologia.csv"

# ========================================== AUTENTICACION

def obtener_token():

    url = f"{BASE_URL}/ticket"

    datos = {
        "username": USUARIO,
        "password": PASSWORD
    }

    respuesta = requests.post(url, json=datos)
    respuesta.raise_for_status()

    token = respuesta.json()["response"]["serviceTicket"]

    print("[OK] Autenticacion correcta")

    return token


# ========================================== CONSULTAR API

def consultar_api(endpoint, headers):

    url = f"{BASE_URL}/{endpoint}"

    respuesta = requests.get(url, headers=headers)
    respuesta.raise_for_status()

    return respuesta.json()


# ========================================== EXTRAER LISTAS

def obtener_lista(datos):

    if isinstance(datos, list):
        return datos

    if isinstance(datos, dict):

        for clave in (  "response", "data", "items","hosts","networkDevices", "device"  ):

            valor = datos.get(clave)

            if isinstance(valor, list):
                return valor

        if isinstance(datos.get("response"), dict):
            return obtener_lista(datos["response"])

    return []


# ========================================== OBTENER CAMPO

def obtener_campo(datos, *nombres):

    for nombre in nombres:

        valor = datos.get(nombre)

        if valor is not None and valor != "":
            return valor

    return ""


# ========================================== GENERAR CSV

def generar_csv(hosts, dispositivos):

    with open(
        ARCHIVO_CSV,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:

        escritor = csv.writer(
            archivo,
            delimiter=";"
        )

        columnas = [ "Dispositivo","Nombre", "IP","Conectado a", "Interfaz"]

        # ========================================== CREAR RELACION IP -> NOMBRE

        mapa_dispositivos = {}

        for dispositivo in dispositivos:

            ip = obtener_campo(
                dispositivo,
                "managementIpAddress",
                "ipAddress",
                "ip"
            )

            nombre = obtener_campo(
                dispositivo,
                "hostname",
                "name",
                "hostName"
            )

            if ip and nombre:
                mapa_dispositivos[ip] = nombre

        # ========================================== DISPOSITIVOS O PC
        escritor.writerow(["DISPOSITIVOS O PC"])
        escritor.writerow(columnas)

        for host in hosts:

            nombre = obtener_campo(
                host,
                "hostName",
                "name",
                "hostname"
            )

            ip = obtener_campo(
                host,
                "hostIp",
                "ipAddress",
                "ip"
            )

            tipo = obtener_campo(
                host,
                "hostType",
                "type",
                "subType"
            )

            conectado = obtener_campo(
                host,
                "connectedNetworkDeviceIpAddress",
                "connectedNetworkDevice",
                "connectedDevice"
            )

            interfaz = obtener_campo(
                host,
                "connectedInterfaceName",
                "connectedInterface"
            )

            conectado = mapa_dispositivos.get(
                conectado,
                conectado
            )

            escritor.writerow([
                tipo or "Host",
                nombre,
                ip,
                conectado,
                interfaz
            ])

        # ========================================== ROUTER O SWITCH 
        escritor.writerow([])
        escritor.writerow(["ROUTER O SWITCH"])
        escritor.writerow(columnas)

        for dispositivo in dispositivos:

            nombre = obtener_campo(
                dispositivo,
                "hostname",
                "name",
                "hostName"
            )

            ip = obtener_campo(
                dispositivo,
                "managementIpAddress",
                "ipAddress",
                "ip"
            )

            tipo = obtener_campo(
                dispositivo,
                "type",
                "deviceType",
                "platformId"
            )

            escritor.writerow([
                tipo or "Network Device",
                nombre,
                ip,
                "",
                ""
            ])

    print("\n[OK] Archivo generado:", ARCHIVO_CSV)
    print("[OK] Total de hosts:", len(hosts))
    print("[OK] Total de routers y switches:", len(dispositivos))


# ========================================== PROGRAMA PRINCIPAL 

def main():

    try:

        # Obtener token
        token = obtener_token()

        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": token
        }

        # Consultar hosts
        print("\n[INFO] Consultando hosts...")

        hosts_json = consultar_api(
            "host",
            headers
        )

        # Consultar routers y switches
        print("[INFO] Consultando routers y switches...")

        dispositivos_json = consultar_api(
            "network-device",
            headers
        )

        # Consultar topologia fisica
        print("[INFO] Consultando topologia fisica...")

        topologia = consultar_api(
            "topology/physical-topology",
            headers
        )

        # Extraer listas
        hosts = obtener_lista(hosts_json)
        dispositivos = obtener_lista(
            dispositivos_json
        )

        # Guardar topologia JSON
        with open(
            "topologia_json.json",
            "w",
            encoding="utf-8"
        ) as archivo:
            json.dump(
                topologia,
                archivo,
                indent=4,
                ensure_ascii=False
            )
        # Generar CSV
        generar_csv(
            hosts,
            dispositivos
        )
    except requests.exceptions.RequestException as error:
        print("\n[ERROR] Problema de conexion con Packet Tracer:")
        print(error)
    except (KeyError, ValueError) as error:
        print("\n[ERROR] Problema al interpretar la respuesta:")
        print(error)


if __name__ == "__main__":
    main()
