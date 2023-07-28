#!/path/to/python/interpreter

import requests
import json

data = {
    "document_type": "CC",
    "document": "1088016550",
    "password": "2102",
    "nit": "901656093",
    "company":"efbfc0ec1b05915d779bc314c7533650a863bb0fcd99fc14320ec426d6fa3cdbe573a4eb96f0744f5462933296f6b54dc402e109f27b8542dd4014a66863c451"
}
url = "https://reportes.pagosimple.com.co/back-api-simple/v1/local/api-simple/auth/login"
path_auth_json_file = "/home/raigoza/Documents/Temporales/Temporales_projects/SISTEMA-TIT/backend/auth.json"
try:
    response = requests.post(
        url,
        data= json.dumps(data),
        headers={"Content-Type": "application/json"}
        )
    with open(path_auth_json_file, "w+", encoding="utf-8") as file:
        json.dump(json.loads(response.content)["data"], file, indent=4)
except Exception as e:
    print(e)
