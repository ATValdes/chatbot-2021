import requests
import time
import re

textReceive = ""

def send_message(msg, sender, port, reciever):

    # direccion del localhost en el que se encuentra el servidor de rasa
    url = 'http://localhost:'+str(port)+'/webhooks/rest/webhook'

    #objeto json que se enviara al servidor de rasa
    data = {"sender": sender, "message": str(msg)} 

    #envio mediante post el objeto json al servidor de rasa
    x = requests.post(url, json=data) 
    #obtengo la respuesta del servidor de rasa
    rta = x.json() 

    
    if x.status_code == 200: 
        #si el status es 200, entonces contesto bien
        #retorno el texto de la respuesta
        for chat in rta: #esto es por si se recibe mas de un mensaje
            if 'text' in chat: #verifica si existe el campo text, ya que podemos recibir una imagen
                textReceive=chat['text'] #obtiene la respuesat del bot si es un mensaje
                print(reciever + ': ' + textReceive) #imprime la respuesta del bot
            if 'image' in chat: #verifica si existe el campo text, ya que podemos recibir una imagen
                imageReceive=chat['image'] #obtiene la respuesat del bot si es una imagen
                print(reciever + ': ' + imageReceive) #imprime la imagen que envio del bot
        return(textReceive)
    else: 
        #si el status no es 200 hubo un error
        #imprimo el error por pantalla
        print(x.raw) 
        return None 
    
"""
    INSTANCIO EL BOT MINORISTA
"""
#puerto del bot Minorista con el que interactuara el usuario
p1 = 5006

#Nombre del bot Minorista
s1 = "Monarca"

#Nombre del miembro del staff que interactuara con el bot Minorista
user = "Usuario"

#puerto de Jaguar
p2 = 5005

#puerto de Arcor
p3 = 5007

#puerto de Limpisima
p4 = 5008


textReceive = 'Mensaje Respuesta'

while True:

    message= input('¿Mensaje?: ')
    if message == "/stop": #si el menasje es '/stop' se sale del programa. Como en 'rasa shell'
        break

    message=send_message(message, user, p1, s1) #envio el mesnaje al bot y recibo la respuesta

    if message == "conectandose con el bot Mayorista Jaguar..." or message == "conectandose con el bot Mayorista Arcor..." or message == "conectandose con el bot Mayorista Limpisima...":
        
        m = {'Jaguar': p2, 'Arcor': p3, 'Limpisima': p4}
        #Consigo el nombre del mayorista
        name = re.search('Mayorista (.*)...', message).group(1)
        #Consigo el puerto del mayorista
        pm = m.get(name)

        #instancio 'message' que es el primer mensaje que le voy a enviar al bot
        message = 'Hola'
        print(s1 + ': ' + message)
        while message != "Eso seria todo, muchas gracias": 
            time.sleep(1)
            #ciclo infinitamente para que los bots se comuniquen
            #llamo a la funcion send_mesagge y le paso el mensaje, el nombre del bot que envia el mensaje y el puerto del bot al que le voy a enviar el mensaje 
            message = send_message(message, s1, pm, name)
            time.sleep(1)
            #llamo a la funcion send_mesagge y le paso el mensaje, el nombre del bot que envia el mensaje y el puerto del bot al que le voy a enviar el mensaje
            message = send_message(message, user, p1, s1) 