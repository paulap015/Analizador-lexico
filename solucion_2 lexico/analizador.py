tipos_reservados = ['entero','char','booleano','caracter']
diccionario={}

def analizador(diccionario,codigo,archivo):
    for linea in codigo:
        if linea == ' ':
            continue
        linea = dar_espacio(linea)
        operacion = es_funcion(linea)
        linea_list = linea.split()
        if len(operacion) != 0: # es funcion 
            if operacion[1]==True:#funcion que retorna tipo 
                for tipo in tipos_reservados:
                    if linea.find(tipo)!=-1:
                        linea = linea.replace(tipo,'function ',1)
            else:#funcion void 
                linea = 'function '+linea
            
            linea =traducir_palabra(linea)
            escribir(archivo,linea)
            continue
        operacion = es_palabra_reservada(linea_list[0]) # tomar la primera palabra de 
        linea = traducir_palabra(linea) #traduce lo que se puede traducir
        linea = asignar_variable(linea)
        if (operacion[0]==True and operacion[1]==True) or len(operacion)==1 : # es una asignacion
            linea = linea +';'
        escribir(archivo, linea)
def asignar_variable(linea):
    pos_ini = linea.find('(')
    pos_fin= linea.find(')')
    punto = linea.find(';')
    coma=linea.find(',')
    igualdad = linea.find('=')
    linea_aux=linea[igualdad+1:].strip() #obtener la parte derecha de la igualdad
    if pos_ini !=-1 and pos_fin !=1 : # es una sentencia de control
        if linea_aux.isnumeric()==False and linea_aux.find('"')==-1: #es una variable op = op2
            linea = linea[:pos_ini+1]+"$"+linea[pos_ini+2:]
        else:
            linea = linea +';'
        if punto !=-1:
            linea = linea.replace(';','; $')
        if coma!=-1:
            linea=linea.replace(',',', $')
            linea = linea.replace('$ ','$')
    
    if (igualdad !=-1 ):#hay una asig 
        linea_aux=linea[igualdad+1:].strip() #obtener la parte derecha de la igualdad
        if pos_ini==-1 or (igualdad < pos_ini) :
            if linea_aux.isnumeric()==False and linea_aux.find('"')==-1 and pos_ini==-1 and linea_aux.find("[")==-1:
                linea_aux="$"+linea_aux
            linea = linea[0:igualdad+1]+linea_aux
            linea_aux=linea[:igualdad]
            if (linea_aux.find('$') == -1):
                linea = "$"+linea
    if linea.find('return')!=-1:
        linea_aux=linea.split()
        for palabra in linea_aux:
            if diccionario.get(palabra) is None:
                linea=linea.replace(palabra,'$'+palabra)
        linea +=';'
    return linea
def es_palabra_reservada(palabra):
    respuesta=[]
    if palabra in diccionario.keys():
        respuesta.append(True)
    if palabra in diccionario.keys() and palabra in tipos_reservados:
        respuesta.append(True)
    else:
        respuesta.append(False)
    return respuesta
def escribir(archivo,linea):
    linea=linea.replace("$ ","$")
    archivo.write(linea+'\n')
def traducir_palabra(linea):
    linea_list = linea.split()
    for palabra in linea_list:
        if palabra in diccionario.keys():
            linea = linea.replace(palabra,diccionario.get(palabra))
    return linea
def es_funcion(linea):
    suma = 0
    lista_linea=linea.split()
    respuesta=[]
    for i in ['(',')','{']:
        suma = suma+linea.count(i)
    # tiene un tipo de dato o sea retorna algo o es una funcion void
    if (lista_linea[0] in tipos_reservados or lista_linea[0]not in diccionario) and suma ==3:
        respuesta.append(True)
        respuesta.append(lista_linea[0] in tipos_reservados)
    return respuesta
def dar_espacio(linea):
    for simbolo in ['(',')','[',']',',','{','}']:
        linea = linea.replace(simbolo," "+simbolo+" ")     
    return linea 
def manejo_archivos(archivo_):
    with open(archivo_) as file:
        file_info = file.readlines()
        file_info = list(map(lambda x: x.strip(), file_info))
    return file_info     
def generar_dictionary(file_info):
    dictionary_info = {}
    for i in file_info:
        key_value = i.split(' ')
        dictionary_info[key_value[0]] = key_value[1]
    return dictionary_info

if __name__ == '__main__':
    diccionario = generar_dictionary(manejo_archivos("tbl_lexica.txt"))
    codigo = manejo_archivos("codigo.txt")
    archivo = open('transformacionPHP.php', 'w')
    analizador(diccionario, codigo,archivo)
    
