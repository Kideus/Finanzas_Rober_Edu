import requests as req
import re
import time
import datetime as dt
import os

#las variables que vamos a usar
base_product = "C40.PA"
date1 = "1483225200"
date2 = "1512082800"
crumb = "0yWZfKFh160"
crumb = "0"
freq = "1d"
evnt="history"
galleta = "galleta"
main_path = os.path.dirname(os.path.realpath('__file__')) + "\\"
files_path = main_path + "csv files\\"
i=0

#Las direcciones que estamos usando
url_test = "https://google.es"
yahoo_url_finance = "https://finance.yahoo.com/quote/"+base_product

#Funciones
def get_galleta(request):
	#sacamos la galleta
	galleta_valor = request.cookies.get_dict()["B"]
	galleta = request.cookies.get_dict()
	return galleta

def get_crumb(request):
	#sacamos la mierda esta que necesita yahoo llamada crumb
	crumb = re.findall('CrumbStore":{"crumb":"(.*?)"}',request.text)[0]
	return crumb

def download_data(symbol,start_date,end_date,frequency,event,crumb,cookie, dw_path):
	#Esto es el proceso de descarga
	yahoo_url_download = "https://query1.finance.yahoo.com/v7/finance/download/"+symbol+"?period1="+start_date+"&period2="+end_date+"&interval="+frequency+"&events="+event+ "&crumb="+crumb
	#print ("Accessing file")
	response = req.get(yahoo_url_download, cookies=cookie)
	full_path = dw_path + symbol + ".csv"
	#print("Start download")
	text_file = open(full_path, "w")
	#print response.text
	text_file.write(response.text)
	text_file.close
	print (full_path)
	#print("End download")

def date_converter(year,month,day):
	date = dt.date(year,month,day)
	date_unix = str(int(time.mktime(date.timetuple())))
	return date_unix

def get_start_date(text):
	
	yr = int(re.findall("start_date:.*?-.*?-(....)", text)[0])
	mnth = int(re.findall("start_date:.*?-(.*?)-....",text)[0])
	dy = int(re.findall("start_date:(.*?)-.*?-....", text)[0])
		
	dict_date = {"year" : yr, "month":mnth,"day":dy}
	
	return dict_date

def get_end_date(text):
	
	yr = int(re.findall("end_date:.*?-.*?-(....)", text)[0])
	mnth = int(re.findall("end_date:.*?-(.*?)-....",text)[0])
	dy = int(re.findall("end_date:(.*?)-.*?-....", text)[0])
		
	dict_date = {"year" : yr, "month":mnth,"day":dy}
	
	return dict_date

def get_frequency(text):
	fq = re.findall("frequency:(.*?)\n", text)[0]
	return fq

def get_event(text):
	event =	re.findall("event:(.*?)\n", text)[0]
	return event
	
#hacer la conversion de fechas.
#hacer que se trague los datos de un fichero (productos, fechas(txt separados mejor) y luego ya ver lo del weekly y el monthly)
#definicion de atributos desde fichero
"""A partir de aqui es el codigo imperativo"""	

#Leemos los parametros del fichero y adaptamos las fechas a Unix
print "Reading parameters"
parameters = open(main_path+"parameters.txt", "r")
parameters_text = parameters.read()
start_date = get_start_date(parameters_text)
end_date = get_end_date(parameters_text)
unix_start_date = date_converter(start_date["year"],start_date["month"],start_date["day"])
unix_end_date = date_converter(end_date["year"],end_date["month"],end_date["day"])
freq = get_frequency(parameters_text)
evnt =get_event(parameters_text)

#Sacamos el listado de productos
print "Getting products list"
products=list()
products_file=open(main_path+"products.txt", "r")

for product in products_file:
	products.append(product.rstrip())

#Sacamos la request de la url.
print ("Accessing web")
resp = req.get(yahoo_url_finance)

#Descargamos los datos.
print("Start download")
for product in products:
	download_data(product,unix_start_date,unix_end_date,freq,evnt,get_crumb(resp),get_galleta(resp),files_path)
print("End download")
