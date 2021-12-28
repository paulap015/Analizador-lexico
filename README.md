# Analizador lexico 
## pseudocodigo a lenguaje PHP 

### Pseudocodigo solución 2 
Algoritmo  
entero suma(entero _operando1, entero _operando2){  
	retornar _operando1 + _operando2  
}  
entero resta(entero _operando1, entero _operando2){  
	retornar _operando1 - _operando2  
}  
principal (){  
	entero _opcion=1  
	entero _operando1=5  
	entero _operando2=4  
	segun(_opcion){  
	caso 1:  
		_response = suma(_operando1,_operando2)  
		imprimir("el resultado de la suma es: ", _response)  
		break  
	caso 2:  
		_response = resta(_operando1,_operando2)  
		imprimir("el resultado de la resta es: ", _response)  
		break  
	defecto:  
		imprimir("Opción no válida")  
	}  
}  
FinAlgoritmo  

- solucion 2 es un poco más corta y sencilla de entender  
