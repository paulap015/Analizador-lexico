"""
* +--------------------------------------------------------------------------------------+
* | DESCRIPCION: Analizador léxico de pseudocodigo a lenguaje PHP |
* | ESTUDIANTE: Julian Santiago Martinez Trullo  – juliansmartinez@unicauca.edu.co |
* | ESTUDIANTE: Paula Peña Constain – ppena@unicauca.edu.co |
* | FECHA: 2021/12/14 |
* +--------------------------------------------------------------------------------------+
"""

"""
* +--------------------------------------------------------------------------------------+
*  LIBRERIAS UTILIZADAS |
* +--------------------------------------------------------------------------------------+
"""

import re


#definiciones globales 
var_reservados = ['entero', 'caracter',
                      'flotante', 'cadena', 'booleano', 'real']
delimitador = [',', '|', ';']
condicionales = [ '&', '||','and','|']

def analizador_lexico(url_tabla_lexica, url_pseudocodigo):
    # Abrir la tabla léxica
    with open(url_tabla_lexica, 'r') as file:
        file_info = file.readlines()
        file_info = list(map(lambda x: x.strip(), file_info))
        dictionary_info = generar_dictionary(file_info)
        
    # abrir pseudocodigo leerlo y crear un archivo .php para la traducción 
    with open(url_pseudocodigo, 'r') as psudo:
        ps_info = psudo.readlines()
        ps_info = list(map(lambda x: x.strip(), ps_info))
        archivo = open('transformacionPHP.php', 'w') # abre el archivo si no lo encuentra lo crea
        var = ""
        var_condicion = "$"
        cadena = ''
        var_funcion=''
        for linea in ps_info: # recorrer las lineas del psudocodigo es una lista
            if linea != '': # si no esta vacia haga 

                es_condicional = False
                es_ciclo = False
                es_funcion =False
                
                
               # linea = linea.replace("("," (")
                if linea.find('imprimir')!=-1:
                    
                    archivo.write(imprimir(linea))
                    continue
                if linea.count(" ") != 0:  # tiene mas de una palabra
                    # Tratando la cadena
                    linea = linea.split(" ")  # Línea pasa a ser una lista
                    linea = linea[0] + " " + "".join(linea[1:-1]) + " " + linea[-1] # omitir espacios internos en la linea
                    linea = linea.replace(';', "; ")# Esto sólo lo hace cuando es ciclo para
                    

                    if linea.split()[0] in var_reservados: # la primera palabra es un tipo de dato ¿?
                        if linea.find("(") != -1: #es funcion
                            linea ="function "+ linea.replace(linea.split()[0], "")
                            
                            es_funcion=True
                        for deli in delimitador:
                            if linea.find(deli) != -1:# encuentra un delimitador separando variables
                                linea = linea.replace(deli, " "+dictionary_info.get(deli)+" ")
                        for var_bool in ['verdadero','falso']: 
                            if linea.find(var_bool)!=-1: # es un booleano traducirlo de una vez 
                                linea = linea.replace(var_bool, " "+dictionary_info.get(var_bool)+" ")
                    
                    linea = linea.split(" ") # lista definitiva de expresiones
                    cantidad_palabras = len(linea)-1 #cuenta las palabras de la linea
                     
                    if linea[0] == 'si': # ver si es un condicional o un ciclo
                        es_condicional = True
                    if linea[0] == 'para' or linea[0] == 'mientras':
                        es_ciclo = True
                    
                    if es_funcion ==False:
                        
                        for palabra in linea: # recorrer cada palabra de la linea 
                            
                            if dictionary_info.get(palabra) != None:  # ¿la palabra esta en la tabla lexica? si 
                                if palabra in var_reservados: # es una inicializacion de variable ? 
                                    primera_palabra = linea[0]
                                    linea = "".join(linea[1:]) #uniendo desde la posicion 2 hasta lo ultimo no toma el tipo de dato
                                    linea = linea.replace(',', ' ,')# espacio cuando son varias definiciones de mismo tipo 
                                    
                                    if primera_palabra !='booleano': #no tratar las variables si son booleanas
                                        linea = generar_variables(linea) #tratar variables
                                    linea = linea.replace(' ', '')
                                    aux = re.split(',', linea)# separa por varios delimitadores -> separar por comas
                                    for i in range(len(aux)):# recorrer cada expresion almacenada en auxiliar
                                        #print("aux en i ", aux[i])
                                        archivo.write(dictionary_info.get(palabra)+aux[i]) #escribe el tipo($) y la variable 
                                        if(i < (len(aux))-1):
                                            archivo.write(' \n') # para cada elemento
                                    archivo.write('') #ultimo elemento
                                    break
                                else:# Están en la tabla léxica pero NO son una definición de variable ( mientras)
                                    cantidad_palabras -= 1 #se escribio una palabra
                                    archivo.write(dictionary_info.get(palabra))
                            else:
                                #la palabra no esta en la tabla lexica 
                                

                                if es_ciclo:  # Realiza la lógica para cada palabra que entra
                                    var += "$"
                                    cantidad_palabras -= 1
                                    for i in palabra:# recorre cada caracter en palabra
                                        if dictionary_info.get(i) != None: 
                                            var += dictionary_info.get(i) # si está traduzcalo 
                                        else:
                                            var += i # sino concatenelo 

                                    if cantidad_palabras == 0: # ya no hay mas palabras por recorrer
                                        var = var.replace(';', ' ;')#Le damos un espacio al valor o variable de la operación relacional
                                        var = generar_variables(var)
                                        var = var.replace(" ;",";")#Le quitamos el espacio que le dimos para envíar a la función 
                                        archivo.write(var) # escribirlo 
                                        var = "" # se inicializa nuevamente la variable 
                                if es_condicional:
                                    cantidad_palabras -= 1
                                    var_condicion += palabra
                                    
                                    for cond in condicionales:
                                        if var_condicion.find(cond) != -1: # encuentra un conector de condicion adicional
                                            var_condicion = var_condicion.replace(
                                                cond, " "+dictionary_info.get(cond)+" $")
                                    if cantidad_palabras == 0: # notiene mas palabras la linea
                                        var_condicion = generar_variables(var_condicion) 
                                        archivo.write(var_condicion)
                                        var_condicion = "$"

                                if es_condicional == False and es_ciclo == False:
                                    
                                    
                                    if linea[0]!="caso":
                                        var_funcion+= ''
                                        cantidad_palabras -= 1
                                        for i in palabra:# recorre cada caracter en palabra
                                            if dictionary_info.get(i) != None: 
                                                var_funcion += dictionary_info.get(i) # si está traduzcalo 
                                            else:
                                                var_funcion += i # sino concatenelo
                                        if cantidad_palabras == 0: # ya no hay mas palabras por recorrer
                                            
                                            var_funcion=generar_variables(var_funcion)
                                            archivo.write(" $"+var_funcion)
                                            var_funcion=''
                                    else:
                                        palabra=palabra.replace(" ","")
                                        archivo.write(' '+palabra)
                                # No están en nuestra TablaLexica
                    else:
                        #es funcion   
                        linea = "".join(linea)
                
                        linea = linea.replace('(',' ( $')
                        linea = linea.replace(',',' , $')
                        linea = linea.replace('function','function ')
                        #linea = generar_variables_funcion(linea)
                        
                        archivo.write(linea)
                       
                    # Cuando termine la línea haga salto de línea
                    archivo.write("\n")
                else:  # solo tiene una linea
                    
                    if dictionary_info.get(linea) != None:
                        archivo.write(dictionary_info.get(linea))
                    else:
                        if linea.find("(") != -1 and linea.find('=')==-1: #es funcion
                            archivo.write("function "+ linea)
                        else:
                           
                            linea='$'+linea+';'
                            linea = generar_variables_funcion(linea)    
                            
                            
                            if linea.find('verdadero')!=-1 or linea.find('falso')!= -1:
                                linea = linea.replace(var_bool, dictionary_info.get(var_bool))
                                    
                            else:
                                pass
                            # linea = generar_variables(linea)
                            archivo.write(linea)
                            
                    archivo.write("\n")
def imprimir(linea):
    linea = linea.replace('imprimir','echo')
    aux =generar_variables_funcion("".join(linea[7:-2]))
    aux= aux.replace(';','')
    linea = "".join(linea[0:7])+aux+" );"
    linea=linea.replace("$ ","$")
    linea += '\n'
    linea= linea.replace('(','')
    linea= linea.replace(')','')
    return linea

def generar_variables_funcion(linea):
    valor = ""
    linea += ' '
    
    for i in range(len(linea)):
        if linea[i] in ['<', '>', '==', '<=', '>=', '!=','(',',']: 
            for j in range(i+1, len(linea)):
                
                if linea[j] != ' ':
                    valor += linea[j]
                else:
                    if valor.isdigit() == False : #Sólo entran variables      
                        # Después de la posición cero hasta la posición i+1 (después del operacion relacional) se asigna a la variable
                        # el valor de '$'+ el valor de la variable involucrada en la sentencia y por último, concatenamos lo que queda faltando de la cadena
                        # desde la posición i + 1 (después del operacion relacional) hasta el tamaño de la cadena que conforma la variable      
                        linea = linea[:i+1] + '$' + valor + linea[i+1 + len(valor):]
                        
                    valor = ""
                    break
    linea = linea.replace(";","")
    linea+=';'
    return linea

# genera las variables en una linea si tiene algun signo de operacion relacional 
def generar_variables(linea):
    valor = ""
    linea += ' '
    
    for i in range(len(linea)):
        if linea[i] in ['<', '>', '==', '<=', '>=', '!=', '=','+','-']:
            
            for j in range(i+1, len(linea)):
                if linea[j] != ' ':
                    valor += linea[j]
                else:
                    valor= valor.replace(';','')
                    if valor.isdigit() == False and valor[0] != "'" and valor[0] !='"': #Sólo entran variables      
                        # Después de la posición cero hasta la posición i+1 (después del operacion relacional) se asigna a la variable
                        # el valor de '$'+ el valor de la variable involucrada en la sentencia y por último, concatenamos lo que queda faltando de la cadena
                        # desde la posición i + 1 (después del operacion relacional) hasta el tamaño de la cadena que conforma la variable      
                        linea = linea[:i+1] + '$' + valor + linea[i+1 + len(valor):]
                    valor = ""
                    break
    
    return linea

#genera el diccionario con clave(palabra pseudocodigo) = valor ( definicion en php)
def generar_dictionary(file_info):
    dictionary_info = {}
    for i in file_info:
        key_value = i.split(' ')
        dictionary_info[key_value[0]] = key_value[1]
    return dictionary_info

"""
* +--------------------------------------------------------------------------------------+
* | FUNCION PRINCIPAL - le envia los archivos al analizador lexico
* +--------------------------------------------------------------------------------------+
"""
if __name__ =='__main__':
    analizador_lexico("tablaLexica2.txt", "pseudocodigo.txt")
