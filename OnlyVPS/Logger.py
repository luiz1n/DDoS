from colorama import init, Fore, Style

init()

estilo = Style.BRIGHT
verde = Fore.GREEN
vermelho = Fore.RED
amarelo = Fore.YELLOW
magenta = Fore.MAGENTA

def Sucesso(msg):
    print(f'{verde}{estilo}{msg}')

def Error(msg):
    print(f'{vermelho}{estilo}{msg}')

def Aviso(msg):
    print(f'{amarelo}{estilo}{msg}')

def Personalize(color,style, msg):
    print(f'{color}{style}{msg}')
