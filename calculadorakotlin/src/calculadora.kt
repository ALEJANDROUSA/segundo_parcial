open class Calculadora {

    // Operaciones básicas con Double 
    open fun sumar(a: Double, b: Double): Double = a + b
    open fun restar(a: Double, b: Double): Double = a - b
    open fun multiplicar(a: Double, b: Double): Double = a * b

    open fun dividir(a: Double, b: Double): Double {
        require(b != 0.0) { "Error: No se puede dividir entre cero" }
        return a / b
    }

    // Sobrecarga de métodos para Int 
    fun sumar(a: Int, b: Int): Int = a + b
    fun restar(a: Int, b: Int): Int = a - b
    fun multiplicar(a: Int, b: Int): Int = a * b

    fun dividir(a: Int, b: Int): Double {
        require(b != 0) { "Error: División por cero no permitida" }
        return a.toDouble() / b.toDouble()
    }
}
