# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
from datetime import datetime
from datetime import timedelta
import json
import random
import requests
import time
from logSave import logSave

STOCK_MAXIMO = 1000
LOG = logSave("LogMinorista.txt")

class ActionQueComprar(Action):

     def name(self) -> Text:
         return "action_que_comprar"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        LOG.save("El bot decide que comprar segun el stock actual de sus productos. Se rellenara el stock de aquellos productos que no tienen el stock al maximo y pueden ser comprados en el mayorista con el cual se esta interactuando.")
        mayorista = tracker.get_slot("mayorista")
        message = "quiero comprar "
        with open ("Productos.json", 'r+') as p_minorista:
            minorista = json.load(p_minorista)
            i = 0
            while i < len(minorista["productos"]):
                if minorista["productos"][i]["stock"] < STOCK_MAXIMO and minorista["productos"][i]["proveedor"] == mayorista:
                    solicitado = STOCK_MAXIMO - minorista["productos"][i]["stock"]
                    producto = minorista["productos"][i]["nombre"]
                    message = message + f"{solicitado} bultos de {producto} "
                    LOG.save(f"  + {solicitado} bultos de {producto}")
                    minorista["productos"][i]["stock"] += solicitado
                i += 1
            #Aumento el stock de los productos
            p_minorista.seek(0)
            json.dump(minorista, p_minorista, indent=4)
        dispatcher.utter_message(text=message)
        return[]

class ActionElegirHacer(Action):

     def name(self) -> Text:
         return "action_elegir_que_hacer"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        LOG.save("El bot minorista decide que hacer a continuacion:")

        if tracker.get_slot("usuario") != None:
            loggeado = True
        else:
            loggeado = False
        

        stock = tracker.get_slot("stock")
        print("stock: ")
        print(stock)
        historial = tracker.get_slot("historial")
        print("historial: ")
        print(historial)
        horarios = tracker.get_slot("horarios")
        print("horarios: ")
        print(horarios)
        precios = tracker.get_slot("precios")
        print("precios: ")
        print(precios)
        mayorista = tracker.get_slot("mayorista")
        print("-----------")

        if loggeado == False and (stock == True or historial == True):
            LOG.save("- No esta loggeado, por lo que decide loggearse")
            dispatcher.utter_message(text="quiero iniciar sesion en mi cuenta")
            if mayorista == None:
                mayorista = next(tracker.get_latest_entity_values("mayorista"), None)
                return[SlotSet("usuario", "Monarca"), SlotSet("mayorista", mayorista)]
            else:
                return[SlotSet("usuario", "Monarca")]
        else:
            if stock == True:
                LOG.save("- Ya se ha loggeado previamente, por lo que decide realizar una compra a pedido del usuario")
                dispatcher.utter_message(text="me gustaria realizar un pedido")
                return[SlotSet("stock", False)]
            elif precios == True:
                LOG.save("- EL bor decide consultar por los precios del mayorista, a pedido del usuario")
                dispatcher.utter_message(text="necesito saber el precio de sus productos")
                return[SlotSet("precios", False)]
            elif historial == True:
                LOG.save("- El bot decide ver el historial de compras a pedido del usuario")
                dispatcher.utter_message(text="quiero ver mi historial de commpras")
                return[SlotSet("historial", False)]
            elif horarios == True:
                LOG.save("- El bot decide consultar por los horarios de atencion al cliente a pedido del usuario")
                dispatcher.utter_message(text="quiero saber cuales son los horarios de atencion al cliente")
                return[SlotSet("horarios", False)]
            else:
                LOG.save("- Se termina la interaccion con el mayorista")
                dispatcher.utter_message(text="Eso seria todo, muchas gracias")

        return []
    
class ActionConsultarStock(Action):

    def name(self) -> Text:
        return "action_stock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        LOG.save("El usuario solicito revisar el stock de los productos.")
        with open('Productos.json', 'r') as contenido:
            productos = json.load(contenido)
            dispatcher.utter_message(text= "Este es el catalogo actualizado de nuestros productos:\n")
            for producto in productos["productos"]:
                dispatcher.utter_message(text = "| \t Producto: " + producto["nombre"] + "\n")
                dispatcher.utter_message(text = "| \t Precio individual: " + str(producto["individual"]) + " \n")
                dispatcher.utter_message(text = "| \t Precio bulto: " + str(producto["preciobulto"]) + " \n")
                dispatcher.utter_message(text = "| \t Stock: "+ str(producto["stock"]) +" \n")
                dispatcher.utter_message(text = "--------------------------------------\n")
        return []


class ActionConnect(Action):

    def name(self) -> Text:
        return "action_connect"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        LOG.save("Usuario solicito interactuar con un mayorista.")

        stock = False
        horarios = False
        historial = False
        precios = False
        mayorista = 'None'

        for entity in tracker.latest_message['entities']:
            if entity["value"] == 'stock':
                stock = True
            elif entity["value"] == 'historial':
                historial = True
            elif entity["value"] == 'horarios':
                horarios = True
            elif entity["value"] == 'precios':
                precios = True
            elif entity["entity"] == 'mayorista':
                mayorista = entity["value"]

        if stock == True:
            with open ("Productos.json", 'r') as p_minorista:
                minorista = json.load(p_minorista)
                i = 0
                break_f = False
                Jaguar_f = False
                Arcor_f = False
                Limpisima_f = False
                while i < len(minorista["productos"]) and break_f == False:
                    if minorista["productos"][i]["stock"] < STOCK_MAXIMO:
                        break_f = True
                        if minorista["productos"][i]["proveedor"] == "Jaguar":
                            Jaguar_f = True
                        elif minorista["productos"][i]["proveedor"] == "Arcor":
                            Arcor_f = True
                        elif minorista["productos"][i]["proveedor"] == "Limpisima":
                            Limpisima_f = True
                    i += 1
                if Jaguar_f == False and Arcor_f == False and Limpisima_f == False:
                    dispatcher.utter_message(text = "El stock de todos los productos esta al valor maximo")
                    LOG.save("- Solicitud de rellenar stock rechazada: El stock de cada producto esta a su valor maximo")
                    return[]
                if Jaguar_f == True:
                    dispatcher.utter_message(text = "conectandose con el bot Mayorista Jaguar...")
                    LOG.save("- Solicitud aceptada de rellenar stock aceptada: Productos del proveedor Jaguar estan por debajo del valor maximo de stock. Conectando con bot Mayorista")
                elif Arcor_f == True:
                    dispatcher.utter_message(text = "conectandose con el bot Mayorista Arcor...")
                    LOG.save("- Solicitud aceptada de rellenar stock aceptada: Productos del proveedor Arcor estan por debajo del valor maximo de stock. Conectando con bot Mayorista")
                elif Limpisima_f == True:
                    dispatcher.utter_message(text = "conectandose con el bot Mayorista Limpisima...")
                    LOG.save("- Solicitud aceptada de rellenar stock aceptada: Productos del proveedor Limpisima estan por debajo del valor maximo de stock. Conectando con bot Mayorista")
                return [SlotSet("stock", stock), SlotSet("historial", historial), SlotSet("horarios", horarios), SlotSet("precios", precios)]
        elif historial == True or horarios == True or precios == True:
            if mayorista != 'None':
                    LOG.save(f"- Conectando con bot Mayorista Jaguar")
                    message = f"conectandose con el bot Mayorista Jaguar..."
                    dispatcher.utter_message(text = message)
                    return [SlotSet("stock", stock), SlotSet("historial", historial), SlotSet("horarios", horarios), SlotSet("precios", precios)]
            else:
                LOG.save(f"- Se rechazo la solicitud debido a que no se especifico a que mayorista desea conectarse")
                dispatcher.utter_message(text= "No se a quien debo consultarle eso")
        else:
            LOG.save(f"- Se rechazo la solicitud debido a que no se especifico la razon por la cual se debe interactuar con el bot mayorista")
            dispatcher.utter_message(text= "No tengo ganas de socializar sin necesidad ahora mismo")    



            
class ActionLog(Action):

    def name(self) -> Text:
        return "action_log"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text = LOG.show())
        return []



class ActionLog(Action):

    def name(self) -> Text:
        return "action_testear"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        LOG.save("Se ejecuto la accion de testeo y se desconto 500 de stock a cada producto.")
        with open('Productos.json', 'r+') as contenido:
            productos = json.load(contenido)
            for p in productos["productos"]:
                if p["stock"] >= 500:
                    p["stock"] -= 500
            contenido.seek(0)
            json.dump(productos, contenido, indent=4)
            contenido.truncate()

        dispatcher.utter_message(text= "Se redujo 500 de stock a los productos")

        return[]







# -------------------------------------- ACCIONES NO USADAS -------------------------------------

class ActionRealizarPedido(Action):
    def name(self) -> Text:
        return "action_realizar_pedido"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user = tracker.get_slot('usuario')
        usermessage = tracker.latest_message['text']
        produc = tracker.latest_message['entities']
        #Consigue las cantidades de cada uno de los productos que se desea comprar
        unidad = [int(s) for s in usermessage.split() if s.isdigit()]
        print(unidad)
        print(produc)
        carrito = []
        i = 0
        while i < len(produc):
            y = {
                "producto": produc[i]["value"],
                "unidades": unidad[i],
                "precio_unidad": 0
            }
            carrito.append(y)
            i += 1

        compra_aceptada = True
        #Revisa si hay stock de los productos a comprar
        with open("Productos.json", 'r+') as p:
            datos_prod = json.load(p)
            z = 0
            while z < len(carrito):
                j = 0
                while j < len(datos_prod["productos"]) and carrito[z]["producto"] != datos_prod["productos"][j]["nombre"]:
                    j = j+1
                if j < len(datos_prod["productos"]) and carrito[z]["producto"] == datos_prod["productos"][j]["nombre"]:

                    if datos_prod["productos"][j]["stock"] == carrito[z]["unidades"]:
                        print("Problema stock")
                        produc = carrito[z]["producto"]
                        compra_aceptada = False
                        message = f"No hay suficientes unidades de {produc} para efectuar la compra"
                        dispatcher.utter_message(text=message)
                    else:
                        carrito[z]["precio_unidad"] = datos_prod["productos"][j]["individual"]
                else:
                    no_vende = carrito[z]["producto"]
                    message = f"El elemento {no_vende} que desea comprar no se encuentre en nuestro catalogo"
                    dispatcher.utter_message(text=message)
                    compra_aceptada = False

                z += 1
                    
            #Si hay stock de los productos, se guarda la compra en la cuenta y se pasa al metodo de pago 
        if compra_aceptada:
            print(f"compra:{compra_aceptada}")
            npedido = random.randint(1000, 9999)
            date = datetime.today() + timedelta(days = random.randint(1, 20))
            date = date.strftime("%d/%m/%Y")
            total = 0
            for elemento in carrito:
                total += (elemento["precio_unidad"] * elemento["unidades"])

            #Se reduce el stock de los productos
            with open("Productos.json", 'r+') as p:
                datos_prod = json.load(p)
                for elemento in carrito:
                    j = 0
                    while elemento["producto"] != datos_prod["productos"][j]["nombre"]:
                        j = j+1
                    if datos_prod["productos"][j]["stock"] <= elemento["unidades"]:
                        datos_prod["productos"][j]["stock"] = 0
                    elif datos_prod["productos"][j]["stock"] > elemento["unidades"]:
                        datos_prod["productos"][j]["stock"] -= elemento["unidades"]
                p.seek(0)
                json.dump(datos_prod, p, indent=4)

            message = f"El numero de pedido es {npedido}. Su pedido llegara el {date}\nEL total a pagar es {total} + envio.\nPor favor ingrese al siguiente link y coloque sus datos para completar el pago: https://www.completarpedido.com\nGracias por comprar con nosotros!"
            dispatcher.utter_message(text=message)
        return[]

class ActionInteraccionMayorista(Action):
    def name(self) -> Text:
        return "action_mayorista"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        def send_mesagge(msg, sender, port):

            # direccion del localhost en el que se encuentra el servidor de rasa
            url = 'http://localhost:'+str(port)+'/webhooks/rest/webhook'

            #objeto json que se enviara al servidor de rasa
            data = {"sender": sender, "message": msg} 

            #envio mediante post el objeto json al servidor de rasa
            x = requests.post(url, json=data) 
            #obtengo la respuesta del servidor de rasa
            rta = x.json() 

            
            if x.status_code == 200: 
                #si el status es 200, entonces contesto bien
                #retorno el texto de la respuesta
                return rta.pop(0)['text'] 
            else: 
                #si el status no es 200 hubo un error
                #imprimo el error por pantalla
                print(x.raw) 
                return None 

        """
            INSTANCIO EL BOT 1
        """
        #puerto del bot 1
        p1 = 5006
        #nombre que le voy a dar al bot 1
        s1 = 'Minorista'


        """
            INSTANCIO EL BOT 2
        """
        #puerto del bot 2
        p2 = 5005
        #nombre que le voy a dar al bot 2
        s2 = 'Mayorista' 


        #insatncio 'message' que es el primer mensaje que le voy a enviar al bot
        message = 'Hola'
        print(s1 + ': ' + message)
        last_message_minorista = ""
        while last_message_minorista != "Eso seria todo, muchas gracias": 
            #ciclo infinitamente para que los bots se comuniquen
            #llamo a la funcion send_mesagge y le paso el mensaje, el nombre del bot que envia el mensaje y el puerto del bot al que le voy a enviar el mensaje 
            message = send_mesagge(message, s1, p2)
            print(s2 + ': ' + message)
            #llamo a la funcion send_mesagge y le paso el mensaje, el nombre del bot que envia el mensaje y el puerto del bot al que le voy a enviar el mensaje
            message = send_mesagge(message, s2, p1) 
            last_message_minorista = message
            print(s1 + ': ' + message)
        
        dispatcher.utter_message(text= "Interaccion terminada")
        return[]

# ---------------------------------------------------------------------------------------------------------------