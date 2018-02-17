import requests
from Facturas import Factura
import shutil
from os.path import join,  basename

url = "http://192.168.15.15:5000/upload"
xml_path = 'C:/Users/SICAD/Dropbox/Generador de PDF/Huiini/errores/DA47D3EB-7595-401C-8E07-EF8109D4F7DD.xml'

#xml_path = 'C:/Users/SICAD/Dropbox/Araceli/2017/JUNIO/EGRESOS/DE820CD4-2F37-4751-9D38-0FD6947CB287.xml'
files = {'files': open(xml_path , 'rb')}
r = requests.post (url, files=files)
f = Factura(xml_path)
print(f.UUID)
# print(r.content)
# print(r.text)
xml_name = basename(f.xml_path)
url_get = "http://192.168.15.15:5000/download"
if r.text == "ya":
        
    r = requests.get(url_get, params={'uuid': f.UUID, 'xml_name': xml_name, 'folio': 55}, stream=True)
    if r.status_code == 200:
        with open(join('C:/Users/SICAD/Dropbox/Generador de PDF/Huiini/errores', f.UUID+'.pdf'),'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        print("valio")