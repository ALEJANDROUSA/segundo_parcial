import java.awt.*
import javax.swing.*
import kotlin.system.exitProcess

class CalculatorUI {
    private val calc = CalculadoraCientifica()
    private val mem = Memoria()
    private val frame = JFrame("NeoCalc - Calculadora Científica")
    private val display = JTextField()
    private var lastAnswer: Double? = null
    private var degreesMode = true

    init {
        createUI()
    }

    private fun createUI() {
        
        UIManager.put("Panel.background", Color(32, 33, 36))
        UIManager.put("Button.background", Color(48, 49, 52))
        UIManager.put("Button.foreground", Color.WHITE)
        UIManager.put("TextField.background", Color(24, 25, 28))
        UIManager.put("TextField.foreground", Color.WHITE)
        UIManager.put("Label.foreground", Color(200, 200, 200))
        UIManager.put("OptionPane.background", Color(32, 33, 36))
        UIManager.put("OptionPane.messageForeground", Color.WHITE)
        UIManager.put("OptionPane.foreground", Color.WHITE)

        frame.defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        frame.layout = BorderLayout(8, 8)
        frame.background = Color(32, 33, 36)

        // display superior
        display.font = Font("Consolas", Font.PLAIN, 22)
        display.horizontalAlignment = JTextField.RIGHT
        display.margin = Insets(10, 10, 10, 10)
        frame.add(display, BorderLayout.NORTH)

        // panel central con BoxLayout vertical
        val centerPanel = JPanel()
        centerPanel.layout = BoxLayout(centerPanel, BoxLayout.Y_AXIS)
        centerPanel.background = Color(32, 33, 36)

        centerPanel.add(makeRow("7", "8", "9", "/", "sqrt"))
        centerPanel.add(makeRow("4", "5", "6", "*", "^"))
        centerPanel.add(makeRow("1", "2", "3", "-", "("))
        centerPanel.add(makeRow("0", ".", "ANS", "+", ")"))
        centerPanel.add(makeRow("sin", "cos", "tan", "log", "ln"))
        centerPanel.add(makeRow("exp", "pi", "e", "M+", "M-"))
        centerPanel.add(makeRow("MR", "MC", "CLR", "BACK", "MODE"))

        frame.add(centerPanel, BorderLayout.CENTER)

        // barra inferior
        val bottom = JPanel(FlowLayout(FlowLayout.CENTER, 10, 10))
        bottom.background = Color(32, 33, 36)
        val evalBtn = JButton("Calcular")
        val exitBtn = JButton("Salir")
        val statusLabel = JLabel("Modo: °")
        statusLabel.foreground = Color(170, 170, 170)

        evalBtn.addActionListener { evaluateExpression(statusLabel) }
        exitBtn.addActionListener { exitProcess(0) }

        bottom.add(evalBtn)
        bottom.add(statusLabel)
        bottom.add(exitBtn)
        frame.add(bottom, BorderLayout.SOUTH)

        frame.pack()
        frame.setSize(420, 550)
        frame.setLocationRelativeTo(null)
        frame.isVisible = true
    }

    private fun makeRow(vararg labels: String): JPanel {
        val row = JPanel(FlowLayout(FlowLayout.CENTER, 10, 10))
        row.background = Color(32, 33, 36)
        for (text in labels) {
            val btn = JButton(text)
            btn.font = Font("Segoe UI", Font.BOLD, 15)
            btn.preferredSize = Dimension(65, 40)
            btn.addActionListener { onButton(text) }
            row.add(btn)
        }
        return row
    }

    private fun onButton(label: String) {
        when (label) {
            "CLR" -> display.text = ""
            "BACK" -> if (display.text.isNotEmpty()) display.text = display.text.dropLast(1)
            "M+" -> memoryAdd()
            "M-" -> memorySubtract()
            "MR" -> display.text += mem.recall().toString()
            "MC" -> { mem.clear(); JOptionPane.showMessageDialog(frame, "Memoria borrada") }
            "ANS" -> display.text += (lastAnswer?.toString() ?: "")
            "pi" -> display.text += "pi"
            "e" -> display.text += "e"
            "MODE" -> toggleMode()
            "sqrt","sin","cos","tan","log","ln","exp" -> display.text += "$label("
            else -> display.text += label
        }
    }

    private fun toggleMode() {
        degreesMode = !degreesMode
        val mode = if (degreesMode) "°" else "rad"
        JOptionPane.showMessageDialog(frame, "Modo cambiado a $mode")
    }

    private fun evaluateExpression(statusLabel: JLabel) {
        val expr = display.text.trim()
        if (expr.isEmpty()) return
        try {
            val result = ExpressionEvaluator.evaluate(expr, calc, degreesMode)
            lastAnswer = result
            statusLabel.text = "= $result"
            display.text = result.toString()
        } catch (ex: Exception) {
            JOptionPane.showMessageDialog(frame, "Error: ${ex.message}", "Error", JOptionPane.ERROR_MESSAGE)
        }
    }

    private fun memoryAdd() {
        val expr = display.text.trim()
        if (expr.isEmpty()) {
            JOptionPane.showMessageDialog(frame, "Ingresa expresión para M+")
            return
        }
        try {
            val v = ExpressionEvaluator.evaluate(expr, calc, degreesMode)
            mem.mPlus(v)
            JOptionPane.showMessageDialog(frame, "Guardado en memoria: ${mem.recall()}")
        } catch (ex: Exception) {
            JOptionPane.showMessageDialog(frame, "Error: ${ex.message}")
        }
    }

    private fun memorySubtract() {
        val expr = display.text.trim()
        if (expr.isEmpty()) {
            JOptionPane.showMessageDialog(frame, "Ingresa expresión para M-")
            return
        }
        try {
            val v = ExpressionEvaluator.evaluate(expr, calc, degreesMode)
            mem.mMinus(v)
            JOptionPane.showMessageDialog(frame, "Memoria actual: ${mem.recall()}")
        } catch (ex: Exception) {
            JOptionPane.showMessageDialog(frame, "Error: ${ex.message}")
        }
    }
}