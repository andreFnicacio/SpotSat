import requests


BASE_URL = "http://localhost:8000/api"


tiff_file_path = "FAA_UTM18N_NAD83.tif"


def test_classification():
    url = f"{BASE_URL}/classification/"
    files = {'file': open(tiff_file_path, 'rb')}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        print("Classificação realizada com sucesso!")
        print("Resposta:", response.json())
    else:
        print(f"Falha na classificação! Código de status: {response.status_code}")
        print("Resposta:", response.text)


def test_metrics():
    url = f"{BASE_URL}/metrics/"
    response = requests.get(url)
    if response.status_code == 200:
        print("Métricas obtidas com sucesso!")
        print("Resposta:", response.json())
    else:
        print(f"Falha ao obter métricas! Código de status: {response.status_code}")
        print("Resposta:", response.text)


def test_consultation(id_raster):
    url = f"{BASE_URL}/consultation/?idRaster={id_raster}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Consulta realizada com sucesso!")
        print("Resposta:", response.json())
    else:
        print(f"Falha na consulta! Código de status: {response.status_code}")
        print("Resposta:", response.text)


if __name__ == "__main__":
    print("Testando classificação...")
    test_classification()
    
    print("\nTestando métricas...")
    test_metrics()
    
    
    id_raster_exemplo = "957066bc-bb9e-4c34-8690-e2290c787dce"
    
    print("\nTestando consulta...")
    test_consultation(id_raster_exemplo)
