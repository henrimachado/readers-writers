
import threading as th
from time import sleep
import random #para gerar valores aleatórios

mutex =  th.Semaphore() 
wrt = th.Semaphore() #semáforo para escrita
lista = [] #Lista de informações compartilhadas
itens = len(lista) #Contador de itens da lista
cont_leitores = 0 #Contador de leitores
sep = ("\n.........................................................................................\n")

def Leitor():
    global lista
    global itens
    global cont_leitores
    
    mutex.acquire() #Fechando o sinal
    cont_leitores += 1 #Adicionando um leitor à RC 
    
    if (cont_leitores == 1):
        wrt.acquire() #Fecha a região para escritores
    mutex.release() #Abre a região para outros leitores
    
    #Leitura dos dados
    
    id_leitor = th.current_thread().name #Captura o nome da Thread para identificação

    if (itens == 0):
        print("Solicitação de acesso por {}.\nSituação: Acesso negado! Não há informações a serem lidas".format(id_leitor))
        mutex.acquire()
        cont_leitores -= 1 #Leitor finaliza sua ação e decrementa o Contador
        if (cont_leitores == 0): #Verifica se ainda há leitores acessando a RC 
            wrt.release() #Caso não existam outros leitores acessando a RC, libera o acesso aos escritores
            print ("{}Operação finalizada. Acesso liberado.{}".format(sep, sep))
    
        mutex.release()
        
    else:
        print ("\n{} entrou...".format(id_leitor))
        for dado in lista:
            sleep(1)
            print ("{} está lendo...\nInformação lida: {}{}".format(id_leitor, dado, sep))
        
        mutex.acquire()
        cont_leitores -= 1 #Leitor finaliza sua ação e decrementa o Contador
        print ("{} saiu. A quantidade atual de leitores é de {}.\n".format(id_leitor, cont_leitores))
        
        if (cont_leitores == 0): #Verifica se ainda há leitores acessando a RC 
            wrt.release() #Caso não existam outros leitores acessando a RC, libera o acesso aos escritores
            print ("{}Operação finalizada. Acesso liberado.{}".format(sep ,sep))
        
        mutex.release()
    
def Escritor():
    global lista
    global itens
    while(itens < 10):
        wrt.acquire() #Fecha o sinal para escrita
        id_escritor = th.current_thread().name #Capturando a identificação do processo Escritor
        
        #Verifica se há espaços disponíveis para armazenamento
        if (itens == 10):
            print ("Solicitação de acesso por {}.\nSituação: Acesso negado. Capacidade máxima atingida!\n".format(id_escritor))
            wrt.release()
            break
        print ("\n{} entrou...\n".format(id_escritor))
        
        #Escrita dos dados
        print ("Quantidade de espaços disponíveis para escrita: {}".format(10 - itens))
        quant_dados =  input("Insira a quantidade de valores a serem escritos: ") #Usuário define quantos números serão inseridos na lista por processo escritor
        n = int(quant_dados)
        print (sep)
        while(n > 0):
            dado = (random.randint(-100, 100)) #adiciona números aleatórios à lista
            print ("O dado a ser inserido é: {}".format(dado))
            lista.append(dado)
            print ("Lista atual: {}{}".format(lista,sep))
            itens += 1 #Incrementa a contagem de itens na lista
            n -= 1
            if (itens == 10):
                print ('\nLista cheia. Revogando acesso para escritores{}'.format(sep))
                break
        wrt.release() #abre o sinal
        break #Para que permita a passagem a outros escritores
    
#Definindo as threads leitoras
l0 = th.Thread(target = Leitor, name = "Leitor 00")
l1 = th.Thread(target = Leitor, name = "Leitor 01")
l2 = th.Thread(target = Leitor, name = "Leitor 02")
l3 = th.Thread(target = Leitor, name = "Leitor 03")
l4 = th.Thread(target = Leitor, name = "Leitor 04")
l5 = th.Thread(target = Leitor, name = "Leitor 05")

#Definindo as threads Escritoras
e1 = th.Thread(target = Escritor, name = "Escritor 01")
e2 = th.Thread(target = Escritor, name = "Escritor 02")
e3 = th.Thread(target = Escritor, name = "Escritor 03")

#Iniciando o programa
print ("{}Dados na lista atualmente: {}{}".format(sep, lista, sep))

#Iniciando os processos
l0.start()
e1.start()
l1.start()
l2.start()
e2.start()
l3.start()
l4.start()
e3.start()
l5.start()

#Finalizando o processo e escrevendo a lista final
while(True):
    if (e3.is_alive() == False):
        print ("{}Dados finais: {}{}".format(sep, lista, sep))
        break


'''
Referências Bibliográficas:

TANENBAUM, A. S.; BOS, H. Sistemas operacionais modernos. 4a. ed. Rio De Janeiro (Rj):
Pearson Education do Brasil, 2016.
'''
