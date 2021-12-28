<?php
function suma ( $_operando1 , $_operando2){
return $_operando1+$_operando2; 
}
function resta ( $_operando1 , $_operando2){
return $_operando1-$_operando2; 
}
function principal(){
$_opcion=1;
$_operando1=5;
$_operando2=4;
switch( $_opcion ){
case  1:
$_response=suma($_operando1,$_operando2) ;
echo'el resultado de la suma es: ',$_response  ;
break;
case  2:
$_response=resta($_operando1,$_operando2) ;
echo'el resultado de la resta es: ',$_response  ;
break;
default:
echo'Opción no válida'  ;
}
}
?>
