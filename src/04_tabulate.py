
# Módulos que se usarán
import requests
import json
from tabulate import *

baseUri = "http://localhost:58000/api/v1"

# Llamada al API para obtener el ticket
headers = {"Content-Type": "application/json"}
data = json.dumps({"username": "admin", "password": "admin"})

resp = requests.post(baseUri + "/ticket", data=data, headers=headers)

print("Status de Solicitud:")
print(resp.status_code)

result = resp.json()

ticket = result["response"]["serviceTicket"]

print("\nEl Service Ticket es:")
print(ticket)


# Llamada al API para recibir los dispositivos de red
headers = {"X-Auth-Token": ticket}

resp = requests.get(baseUri + "/network-device", headers=headers)

result = resp.json()

print("\nDispositivos de Red:")

host_list = []
i = 0

for item in result["response"]:
    i += 1

    hostname = item.get("hostname", "No disponible")
    serial = item.get("serialNumber", "No disponible")
    software = item.get("softwareVersion", "No disponible")

    host_list.append([i, hostname, serial, software])

print(tabulate(
    host_list,
    headers=["N°", "Hostname", "Serial Number", "Software Version"],
    tablefmt="rst"
))


# Llamada al API para recibir los hosts
headers = {"X-Auth-Token": ticket}

resp = requests.get(baseUri + "/host", headers=headers)

result = resp.json()

print("\nHosts de la Red:")

host_list = []
i = 0

for item in result["response"]:
    i += 1

    hostname = item.get("hostName", "No disponible")
    tipo = item.get("hostType", "No disponible")
    ip = item.get("hostIp", "No disponible")

    host_list.append([i, hostname, tipo, ip])

print(tabulate(
    host_list,
    headers=["N°", "Hostname", "Tipo", "IP"],
    tablefmt="rst"
))
