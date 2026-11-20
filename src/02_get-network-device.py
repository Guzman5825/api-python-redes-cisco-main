
import requests

api_url = "http://localhost:58000/api/v1/network-device"

headers = {
    "X-Auth-Token": "NC-3-b3f0b4159b62498385bd-nbi"
}

# Solicitar los dispositivos a la API
resp = requests.get(api_url, headers=headers)

print("Request status:", resp.status_code)

# Verificar que la solicitud haya sido exitosa
if resp.status_code == 200:

    response_json = resp.json()

    networkDevices = response_json.get("response", [])

    print("\n========== DISPOSITIVOS DE RED ==========\n")

    for networkDevice in networkDevices:

        print(
            networkDevice.get("hostname", "Sin hostname"),
            "\t",
            networkDevice.get("platformId", "Sin plataforma"),
            "\t",
            networkDevice.get("managementIpAddress", "Sin IP")
        )

else:
    print("Error al consultar la API:")
    print(resp.text)
