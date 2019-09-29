# Adventure Writer
 ![Image](https://raw.githubusercontent.com/srbill1996/Adventure-Writter/master/preview.png)


Adventure writter te permite crear tus propias aventuras conversacionaes facil y rapidamente.

    -Sencillo.
    -Lenguaje de programación propio facil y rapido.
    -Muchas posibilidades.

Que es una aventura conversacional?, según wikipedia.
> La aventura conversacional es un género de videojuegos, más común de ordenadores que de consola o arcades, en el que la descripción de la situación en la que se encuentra el jugador proviene principalmente de un texto. A su vez, el jugador debe teclear la acción a realizar. El juego interpreta la entrada -normalmente- en lenguaje natural, lo cual provoca una nueva situación y así sucesivamente. A veces existen gráficos en estos juegos, que sin embargo son tan sólo situacionales o que ofrecen ayuda complementaria en algunos casos, al estilo de las ilustraciones de un libro. El género de las aventuras gráficas surgió como evolución de las videoaventuras y las aventuras conversacionales, dejando estas últimas 'pasadas de moda' en Occidente. En Japón siguen estando muy presentes en la forma de novelas visuales, un género que se puede considerar sucesor de las aventuras conversacionales, aunque con características propias.


# 📑 Creando tu propia aventura

**Introducción**
Adventure Writter te permite crear tus propias aventuras conversacionales de una manera facil y rapida a traves de un formato de programación sencillo que podrás guardar y ejecutar con el interprete.

La interfaz básica de una aventura conversacional consta de una pantalla donde se irá imprimiento la historia y una medio para que el usuario escriba, usando sus propias palabras lo que quiera realizar y esté disponible dentro del contexto.


# Los Escenarios
Una habitación, un parque, un patio, un jardín, hasta el mismisimo infierno son lugares donde nuestro jugador podría pisar durante el desarrollo de una historia, por ello, el motor cuenta con un sistema de escenarios facil y practico, donde cada lugar, constara de un archivo el cual tendrá los principios basicos para su uso.

La estructura por defecto de un escenario es la siguiente.

    #LOAD{}         - Acciones que se van a ejecutar cuando se cargue el escenario.
    #LOADA_AGAIN{}  - Acciones que se van a ejecutar cuando se cargue otra vez el escenario.
    !<nombre>{}     - Acción que será reconocida por el programa. (ex: Mirar el techo).
        El nombre puede contener variaciones para la misma acción por ejemplo, Mirar el techo | Mirar arriba {}.
    ¡<nombre>{}     - Acción que se podrá ejecutar una sola vez. (ex: Quemar papel).

Las acciones para cada tipo, estarán presente entre las llaves/brackets {}.

Los ya mencionados escenarios, se irán ejecutando y contectando entre sí para dar lugar al desarrollo de una historia.
Esta se compondrá de varios archivos de texto plano con la extensión '.adventure' ubicados dentro de directorio especifico, donde uno será el inicial y que dará pie a la aventura.

**Aventura de ejemplo:**

> habitacion1.adventure
```
//Instrucción de inicialización
#LOAD{
    Hola esta es una habitación.
}
#LOAD_AGAIN{
    Hola otra vez! Vuelves al mismo lugar!
}
//Acción
!Abrir puerta | pasar por la puerta | entrar{
    &LOAD habitación2
}
//Otra acción
¡toser {
    De pronto, toses.
}
```
> habitacion2.adventure
```
//Instrucción de inicialización
#LOAD{
    Esta es una habitacion nueva!
}
#LOAD_AGAIN{
    Vuelves a esta habitación.
}
//Acción
!volver{
    &LOAD habitación1
}
//Otra acción
¡toser {
    De pronto, toses.
}
```


#Instrucciones

Dijimos que los bloques en una aventura, contienen las instrucciones a ejecutar
```
{
    Hola este es un texto que se va a imprimir.
    :variable = algo
    ?variable is algo
        hacer esto
    ?else
        si no, esto
    Blablabla
}
```

**📝 IMPRESION DE TEXTO**

El elemento principal de una aventura conversacional es el texto.
Colocar un texto en pantalla es realmente simple, tan simple como solo escribir!.

**💡CREACIÓN Y MANEJO DE VARIABLES**

Las aventuras son algo mas alla que simplemente imprimir texto, es poder interactuar con el entorno, cambiar las cosas, los eventos en el transcurso, para ello contamos con herramientas que nos permiten manejar esas capacidades.
Las variables son un elemento que nos permite almacenar algo, lo que sea y cambiarlo cuando queramos.
```
   Formato de una variable:
    :<nombre_variable> = <valor: string, booleano, lo que sea>
```
Para crear una variable colocamos en una linea nueva el signo ':' seguido del nombre simbolico que queremos para ella y luego el signo '=' indicando el valor que contendrá.
ejemplo: 
```
:perro = 'Firulais'
:manzana.color = verde

```
Como verán, la segunda variable consta de un '.' de por medio, esto sirve para de una manera logica asignarle un atributo a lo que representa esta variable, en este caso, una manzana, cuyo color, es el verde.

> **Tipos de valores que puede contener una variable:**
*-Un valor crudo, como puede ser una palabra sin comillas. ej: cerrado, roto
-Una lista. ej: [llave1, llave2]


**El jugador quiere abrir una puerta:**

El escenario es el siguiente, el jugador tiene en frente una puerta y puede ejecutar una acción para abrirla, las puertas pueden estár abiertas o cerradas, por eso sería conveniente definir una puerta y su estado actual.
```
:puerta.estado = cerrada
```
En este caso el estado de la puerta es cerrada, indicando que esta está cerrada.(podría haber puerto en vez de False, falso, o , cerrado, cambiando hasta el nombre como mas desee)
Una vez que el usuario haya abierto la puerta.
```
:puerta.estado = abierta
```
El estado abierto de la puerta pasará a abierta.

Un ejemplo practico.
```
#LOAD{
    Bienvenido! En frente tuyo ves una puerta.
    :puerta.estado = cerrada
}
!abrir puerta {
    Te decides a abrir la puerta.
    :puerta.estado = abierta
}
```
Genial! Tenemos la capacidad de almacenar propiedades de objetos, estados, nombres, lo que se nos ocurra, pero, de que serviría esto si no podemos comprobar condiciones?

**💡OPERADORES CONDICIONALES**

***Operador if y la importancia de la identización***

Pongamos otro escenario, donde el jugador puede ejecutar una acción, que rompa una ventana, como bien sabemos, una ventana se puede romper una sola vez, de lo contrario no sonaria muy consistente para la experiencia poder volver a romper algo que ya se rompió previamente.

Formato de condicional:
```
?<nombre_variable> is|not is <valor_comparar>
```

Decidimos que una ventana está sana
```
:ventana.estado = sana
```

Si el jugador ejecuta la acción para romperla, sería logico verificar primero si la ventana está sana, por que si estuviese rota, no tendría mucho sentido romper algo que ya está roto.
Para ello, recurriremos al operador condicional '?' que sigue la siguiente estructura.
```
?<condicion>
    Instrucciones que se van a ejecutar si la condicion es verdadera

```
La condición, si es verdadera ejecutara el codigo que prosigue las siguientes lineas, en caso contrario, lo ignorara y seguira con lo que esté por debajo.
En nuestro caso sería algo así.
```
!romper ventana {
    ?ventana is sana
        Una linda e integra ventana, decides pegarle una patada! Paff!
        :ventana.estado = rota
    ?ventana is rota
        La ventana está destruida, no puedes seguir rompiendola.
}
```
Notese los niveles de tabulado, que permitiran a las operaciones discriminar lo que tiene que hacer y no.

**Operaciones condicionales:**
```
?valor1 is 'algo' //compriueba si valor1 es igual a 'algo'
?valor1 is not 'algo' //comprueba si no lo es
?valor1 not is 'algo' //lo mismo
```



**Operador Else:**

En caso de que queramos obviar el hecho de que ya está rota sin tener que comprobarlo, podemos verificar solo si la ventana está sana, y en el caso contrario, usar el operador '?else' para ejecutar lo correspondiente en caso de que lo anterior no se cumpla.
```
!romper ventana {
    ?ventana is sana
        Una linda e integra ventana, decides pegarle una patada! Paff!
        :ventana.estado = rota
    ?else
        La ventana está destruida, no puedes seguir rompiendola.
}
```





