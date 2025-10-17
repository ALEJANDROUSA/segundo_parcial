import javax.swing.SwingUtilities
import kotlin.math.abs

// Función que ejecuta pruebas automáticas en consola
fun ejecutarPruebasConsola() {
    val calculadora = CalculadoraCientifica()

    val pruebas = listOf(
        "2 + 3 * 4 - 5" to 9.0,
        "(2 + 3) * (4 - 1) / 5 + 2^3" to 11.0,
        "3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3" to 3.0001220703125,
        "sin(30)" to 0.5,
        "log(100)" to 2.0,
        "ln(e)" to 1.0,
        "sqrt(9)" to 3.0
    )

    var todoCorrecto = true

    println("Iniciando pruebas automáticas de la CalculadoraCientifica...\n")

    for ((expresion, esperado) in pruebas) {
        try {
            val resultado = ExpressionEvaluator.evaluate(expresion, calculadora, true)
            println("Expresión: $expresion = $resultado (Esperado: $esperado)")
            if (!resultado.isFinite() || abs(resultado - esperado) > 1e-9) {
                println(" Falló\n"); todoCorrecto = false
            } else {
                println(" Correcto\n")
            }
        } catch (e: Exception) {
            println("⚠️  Error evaluando '$expresion': ${e.message}\n")
            todoCorrecto = false
        }
    }

    // Verificación de error esperado (división por cero)
    try {
        ExpressionEvaluator.evaluate("1 / 0", calculadora, true)
        println("⚠️  '1 / 0' no lanzó excepción (❌ Falló)")
        todoCorrecto = false
    } catch (e: Exception) {
        println(" '1 / 0' lanzó excepción correctamente -> OK")
    }

    println(
        if (todoCorrecto)
            "\n Todas las pruebas fueron exitosas."
        else
            "\n Algunas pruebas no pasaron correctamente."
    )
}

// Función principal del programa
fun main(args: Array<String>) {
    if ("--test" in args) {
        ejecutarPruebasConsola()
    } else {
        SwingUtilities.invokeLater {
            CalculatorUI() // Inicia la interfaz gráfica
        }
    }
}
