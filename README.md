# Segundo Parcial — Inteligencia Artificial y Paradigmas de Programación  

---

## 1️⃣ Perceptrón por Agentes  

### Resumen  
Este proyecto implementa un **perceptrón simple** que aprende a separar puntos 2D linealmente separables.  
Cada punto de entrenamiento se maneja como un **objeto autónomo**, y el modelo principal simula el proceso de aprendizaje ajustando los pesos y el sesgo.  
El sistema incluye una **interfaz gráfica interactiva** desarrollada con **Matplotlib**, la cual permite observar en tiempo real la evolución de la frontera de decisión y la precisión del modelo.

---

### Objetivo  
- Representar y entrenar un **perceptrón de dos entradas + bias**.  
- Visualizar cómo el modelo aprende mediante una **simulación gráfica en tiempo real**.  
- Evaluar la precisión final en un conjunto de prueba independiente.  

---

### Diseño del sistema  
**Componentes principales:**

- **`PuntoAgente`**  
  Representa un punto con coordenadas (x, y) y una etiqueta (+1 o -1).  
  Se usa tanto en el conjunto de entrenamiento como en el de prueba.  

- **`PerceptronModelo`**  
  Contiene toda la lógica del modelo:
  - Inicializa pesos y bias aleatoriamente.  
  - Genera puntos y una “línea real” que sirve como frontera verdadera.  
  - Aplica la **regla del perceptrón** para ajustar pesos.  
  - Evalúa precisión en datos de prueba.  

- **Visualización (CanvasGrid + Chart)**  
  Permite observar en la ventana de MESA la clasificación de los puntos en colores y la precisión durante el entrenamiento.  
  Incluye sliders para configurar los parámetros y botones para iniciar la simulación.

---

### Cómo ejecutar el código  
#### Requisitos previos  
1. Tener **Python 3.10 o superior** instalado.  
2. Instalar MESA y dependencias:  
   ```bash
   pip install mesa==2.1.1 numpy matplotlib
   ```
3. Colocar el archivo `ejercicio_perceptron.py` en una carpeta de trabajo.  

#### Ejecución con interfaz gráfica  
En la terminal, ejecutar:  
```bash
ejercicio_perceptron.py
```
Esto abrirá una ventana del servidor MESA en el navegador (normalmente en `http://127.0.0.1:8521/`) o una ventana emergente.  
Ahí podrás:  
- Ajustar la **tasa de aprendizaje** y **número de iteraciones** con los sliders.  
- Presionar **Run** para ver el entrenamiento paso a paso.  
- Observar cómo cambia la frontera de decisión y los colores de los puntos.  


### Resultados (modo headless de ejemplo)  
Se realizó una ejecución sin interfaz con:  
- 50 puntos de entrenamiento  
- 200 puntos de prueba  
- tasa de aprendizaje = 0.1  
- 50 iteraciones  

**Resultado obtenido:**  
- Precisión: **≈ 97.8%**  
- Convergencia rápida (~3 épocas)  
- Comportamiento estable y coherente con datos linealmente separables.  

---

### Ejemplo visual (simulación)  
<img width="1177" height="981" alt="image" src="https://github.com/user-attachments/assets/4028dc6d-6006-4272-bfa3-92d6d63b6504" />
<img width="1179" height="1009" alt="image" src="https://github.com/user-attachments/assets/89cf9de2-a041-494d-98ab-5d6a76998dd3" />

---

## 2️⃣ Calculadora Distribuida con Agentes  

### Resumen  
En este proyecto se desarrolla una **calculadora distribuida** donde cada operador aritmético (+, −, ×, ÷, ^) es gestionado por un **agente independiente** usando el framework **MESA**.  
Las expresiones son analizadas, convertidas a notación postfija (RPN) y luego evaluadas por los agentes mediante comunicación interna de tareas.

---

### Objetivo  
- Modelar el cálculo distribuido de expresiones aritméticas.  
- Implementar **comunicación entre agentes** mediante colas de tareas.  
- Respetar la **precedencia y asociatividad** de los operadores.  

---

### Diseño del sistema  

**Agentes implementados:**
- **`OperacionAgente`**  
  - Ejecuta una operación específica (por ejemplo suma o división).  
  - Cada agente mantiene una cola de tareas y devuelve resultados al modelo principal.  

- **`IOAgente`**  
  - Actúa como interfaz y coordinador general.  
  - Tokeniza la expresión, la convierte a RPN y delega operaciones a los agentes correspondientes.  
  - Evalúa los resultados y presenta la respuesta final al usuario.  

**Modelo principal (`ModeloCalculadora`)**
- Crea los agentes de operación y el agente IO.  
- Controla el flujo de ejecución paso a paso.  

---

### Cómo ejecutar el código  
#### Requisitos previos  
1. Tener **Python 3.10 o superior**.  
2. Instalar las dependencias:  
   ```bash
   pip install mesa==2.1.1 numpy
   ```
3. Colocar el archivo `ejercicio_calculadora_python.py` en la carpeta de trabajo.  

#### Ejecución  
En la terminal, ejecutar:  
```bash
python ejercicio_calculadora_python.py
```
El programa pedirá una expresión matemática (por ejemplo):  
```
(2 + 3) * 4 - 5 / 2
```
y mostrará el resultado final, procesando internamente las operaciones mediante los agentes.  

---

### Implementación (puntos clave)
- Expresiones soportadas: `+ - * / ^`  
- Manejo de errores:
  - División por cero → `ZeroDivisionError`  
  - Paréntesis mal balanceados → `ValueError`
- Evaluación controlada paso a paso (`model.step()`) para simular asincronía.  

---

### Ejemplo de ejecución  
```text
Calculadora distribuida basada en agentes (MESA)
Ejemplo: (2 + 3) * 4 - 5 / 2

Ingresa expresión: (2 + 3) * 4 - 5 / 2
Resultado: 17.5
```

---
### Ejemplo visual (simulación) 
<img width="1039" height="499" alt="image" src="https://github.com/user-attachments/assets/ffd7f26b-3446-46fa-973f-cdd8fb8bf5e6" />
---

## 3️⃣ Calculadora Científica (Kotlin)

### Resumen  
Proyecto desarrollado en **Kotlin** que implementa una calculadora científica con interfaz gráfica (**Swing**).  
Soporta operaciones básicas y funciones avanzadas (trigonometría, potencias, raíces, logaritmos, exponenciales, conversión de grados y radianes, etc.).  
---
### Diagrama UML
<img width="933" height="1165" alt="image" src="https://github.com/user-attachments/assets/45f11413-acd5-444e-b36b-6fa25f41779c" />
---

### Estructura de ficheros  
En la carpeta `src/` se encuentran los siguientes archivos:

```
calculadora.kt              → Clase base con operaciones aritméticas básicas  
calculadoracientifica.kt    → Clase derivada con funciones científicas  
calcular.kt                 → Interfaz gráfica en Swing (ventana, botones y pantalla)  
Main.kt                     → Punto de entrada del programa  
memoria.kt                  → Clase de manejo de memoria (M+, M-, MR, MC)  
solver.kt                   → Evaluador de expresiones (Shunting Yard → RPN)
```

---

### Cómo ejecutar el código  

#### Requisitos previos  
1. Tener instalado **IntelliJ IDEA** o el compilador **Kotlin CLI**.  
2. Crear un proyecto Kotlin y colocar los archivos dentro de la carpeta `src`.  

#### Ejecución desde IntelliJ  
1. Abrir el proyecto `calculadorakotlin`.  
2. Ir a `src/Main.kt`.  
3. Hacer clic en **Run** para ejecutar.  
4. Se abrirá la **interfaz gráfica de la calculadora**.  

#### Ejecución desde consola  
Compilar y ejecutar con:  
```bash
kotlinc src/*.kt -include-runtime -d CalculadoraCientifica.jar
java -jar CalculadoraCientifica.jar
```

---

### Ejemplo de uso  
- Expresión básica: `2 + 3 * 4 - 5` → `9`  
- Expresión científica: `sin(30) + log(100)` → `2.5`  
- División por cero: muestra mensaje de error controlado.  

---
### Ejemplo visual (simulación)
<img width="601" height="799" alt="image" src="https://github.com/user-attachments/assets/cb5ce1d8-8661-4b1b-9413-7c1257194c28" />
<img width="600" height="808" alt="image" src="https://github.com/user-attachments/assets/b0a6c330-47da-4de9-95e6-88133c20160d" />
<img width="595" height="802" alt="image" src="https://github.com/user-attachments/assets/342cb74b-3df4-4a55-bdab-46f55c6ae866" />



---
## Conclusiones  
- Los **agentes** son una poderosa abstracción para modelar sistemas distribuidos.  
- En el **perceptrón**, permiten observar de forma dinámica cómo el modelo aprende mediante interacción visual.  
- En la **calculadora distribuida**, los agentes ejemplifican la cooperación y comunicación para resolver tareas complejas.  
- En la **calculadora científica (Kotlin)**, se evidencia el uso correcto de los **principios POO** (herencia, encapsulamiento, polimorfismo).  
- En conjunto, los tres ejercicios integran los paradigmas de **agentes** y **objetos**, demostrando comprensión tanto teórica como práctica del curso.  

---

**Autor:** *Alejandro Poveda Sandoval*  

