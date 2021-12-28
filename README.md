# Analizador lexico 
## pseudocodigo a lenguaje PHP 

### prueba pseudocodigo 
Algoritmo
entero suma(entero op1 , entero op2){
retornar op1 + op2
}
principal ( ){
entero op = 1
entero opcion = op
entero op = suma(op1,op2)
op=2
char var = [1,2,3]
para(x=0;x<10;x++){
segun(op){
caso 1:
\_response = suma(\_operando1,\_operando2)
imprimir("el resultado de la suma es: ", \_response)
FinAlgoritmo

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
