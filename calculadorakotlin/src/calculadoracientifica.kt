import kotlin.math.*

class CalculadoraCientifica : Calculadora() {

    //  Funciones trigonométricas en grados 
    fun senoGrados(angulo: Double): Double = sin(Math.toRadians(angulo))
    fun cosenoGrados(angulo: Double): Double = cos(Math.toRadians(angulo))
    fun tangenteGrados(angulo: Double): Double = tan(Math.toRadians(angulo))

    // Funciones trigonométricas en radianes 
    fun senoRadianes(radianes: Double): Double = sin(radianes)
    fun cosenoRadianes(radianes: Double): Double = cos(radianes)
    fun tangenteRadianes(radianes: Double): Double = tan(radianes)

    // Potencia 
    fun elevar(base: Double, exponente: Double): Double = base.pow(exponente)

    // Raíz cuadrada 
    fun raizCuadrada(valor: Double): Double {
        require(valor >= 0.0) { "No se puede calcular la raíz de un número negativo" }
        return sqrt(valor)
    }

    // Logaritmos 
    fun logBase10(valor: Double): Double {
        require(valor > 0.0) { "El logaritmo base 10 requiere un valor positivo" }
        return log10(valor)
    }

    fun logNatural(valor: Double): Double {
        require(valor > 0.0) { "El logaritmo natural requiere un valor positivo" }
        return ln(valor)
    }

    // Exponencial
    fun exponencial(valor: Double): Double = exp(valor)

    // Conversión de unidades 
    fun gradosARadianes(grados: Double): Double = Math.toRadians(grados)
    fun radianesAGrados(radianes: Double): Double = Math.toDegrees(radianes)
}
