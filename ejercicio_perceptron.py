import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


try:
    import mesa
    _Base = mesa.Model
except Exception:
    class _Base:
        def __init__(self):
            pass

# entidades 
class SamplePoint:
    """punto etiquetado en 2D"""
    def __init__(self, idx, xy, label):
        self.idx = idx
        self.xy = np.array(xy, dtype=float)
        self.label = int(label)  # -1 o 1

class AgentPerceptron(_Base):
    """Perceptrón simple que mantiene datos de entrenamiento/prueba."""
    def __init__(self, n_train=100, n_test=200, lr=0.1):
        super().__init__()
        self.n_train = int(n_train)
        self.n_test = int(n_test)
        self.lr = float(lr)
        self.weights = np.random.uniform(-1, 1, 2)
        self.bias = np.random.uniform(-0.5, 0.5)
        self.iter_count = 0
        self._define_ground_truth()
        self._make_datasets()

    def _define_ground_truth(self):
        a, b = np.random.uniform(-1, 1, 2)
        c = np.random.uniform(-0.5, 0.5)
        if abs(a) < 1e-6 and abs(b) < 1e-6:
            a = 1.0
        self.ground_line = (a, b, c)

    def reset(self):
        self._define_ground_truth()
        self.weights = np.random.uniform(-1, 1, 2)
        self.bias = np.random.uniform(-0.5, 0.5)
        self.iter_count = 0
        self._make_datasets()

    def _make_datasets(self):
        self.train = []
        self.test = []
        a, b, c = self.ground_line

        def lab(p):
            return 1 if (a * p[0] + b * p[1] + c) >= 0 else -1

        for i in range(self.n_train):
            x, y = np.random.uniform(-1, 1, 2)
            self.train.append(SamplePoint(i, (x, y), lab((x, y))))

        for i in range(self.n_train, self.n_train + self.n_test):
            x, y = np.random.uniform(-1, 1, 2)
            self.test.append(SamplePoint(i, (x, y), lab((x, y))))

    def infer(self, x):
        x = np.array(x, dtype=float)
        v = np.dot(self.weights, x) + self.bias
        return 1 if v >= 0 else -1

    def single_epoch(self):
        mistakes = 0
        for pt in self.train:
            x = pt.xy
            y = pt.label
            yhat = self.infer(x)
            if yhat != y:
                # regla perceptrón
                self.weights += self.lr * y * x
                self.bias += self.lr * y
                mistakes += 1
        self.iter_count += 1
        return mistakes

    def fit(self, epochs, callback=None, notify_every=1):
        epochs = int(epochs)
        for e in range(epochs):
            m = self.single_epoch()
            if callback and ((e + 1) % notify_every == 0 or e == epochs - 1):
                callback(self, self.iter_count)
            if m == 0:
                if callback:
                    callback(self, self.iter_count)
                break

    def score(self):
        if not self.test:
            return 0.0
        ok = sum(1 for pt in self.test if self.infer(pt.xy) == pt.label)
        return ok / len(self.test) * 100.0

# interfaz y visualización 
def build_interface(per_model):
    fig, ax = plt.subplots(figsize=(8, 7))
    plt.subplots_adjust(right=0.78, left=0.08, bottom=0.12)

    # estética alternativa: fondo claro con cuadrícula y tipografía distinta
    ax.set_facecolor('#fbfcff')
    ax.grid(True, linestyle=':', linewidth=0.6, alpha=0.7)

    title = ax.set_title('perceptrón — clasificación lineal', fontsize=14, fontweight='semibold')

    # valores x para trazar líneas
    xspan = np.array([-1.25, 1.25])

    # scatter inicial (colores y marcador distinto)
    def initial_points():
        pts = np.array([p.xy for p in per_model.train])
        labs = np.array([p.label for p in per_model.train])
        colors = []
        for p, l in zip(pts, labs):
            correct = (per_model.infer(p) == l)
            colors.append('#1f77b4' if correct else '#ff7f0e')  # azul / naranja
        sc = ax.scatter(pts[:, 0], pts[:, 1], s=50, c=colors,
                        marker='D', edgecolors='white', linewidths=0.6, alpha=0.95)
        return sc

    scatter = initial_points()

    # separador verdadero (estilo punteado fino)
    a, b, c = per_model.ground_line
    if abs(b) > 1e-6:
        y_true = -(a * xspan + c) / b
        true_line, = ax.plot(xspan, y_true, linestyle=(0, (3, 5)), linewidth=1.2, label='separador real')
    else:
        x0 = -c / a
        true_line, = ax.plot([x0, x0], [-1.25, 1.25], linestyle=(0, (3, 5)), linewidth=1.2, label='separador real')

    # frontera de decisión (más gruesa, color sólido)
    decision_line, = ax.plot([], [], linewidth=2.6, solid_capstyle='round', label='frontera actual')

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.legend(loc='upper left', framealpha=0.9)

    # estado y precisión (cajas con fondo semitransparente)
    status_box = ax.text(-1.05, 1.05, f'iter: {per_model.iter_count}', fontsize=9,
                         bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'))

    acc_box = ax.text(0.2, 1.05, '', fontsize=9, bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'))

    # controles: sliders verticales a la derecha y botones abajo a la derecha
    ax_lr = plt.axes([0.82, 0.15, 0.03, 0.6])   # barra vertical
    ax_iter = plt.axes([0.88, 0.15, 0.03, 0.6])  # barra vertical

    s_lr = Slider(ax_lr, 'tasa', 0.001, 1.0, valinit=per_model.lr, orientation='vertical', valstep=0.001)
    s_iter = Slider(ax_iter, 'iter', 1, 1000, valinit=100, orientation='vertical', valstep=1)

    ax_btn_train = plt.axes([0.70, 0.03, 0.12, 0.06])
    ax_btn_reset = plt.axes([0.84, 0.03, 0.12, 0.06])
    btn_train = Button(ax_btn_train, 'entrenar', hovercolor='#d3e6ff')
    btn_reset = Button(ax_btn_reset, 'reiniciar', hovercolor='#ffd9cc')

    def refresh_display(model_obj, iteration=None):
        pts = np.array([p.xy for p in model_obj.train])
        labs = np.array([p.label for p in model_obj.train])
        new_colors = []
        for p, l in zip(pts, labs):
            new_colors.append('#1f77b4' if model_obj.infer(p) == l else '#ff7f0e')

        scatter.set_offsets(pts)
        scatter.set_color(new_colors)

        w = model_obj.weights
        b = model_obj.bias
        # dibujar frontera actual (w0 x + w1 y + b = 0)
        if abs(w[1]) > 1e-6:
            y_dec = -(w[0] * xspan + b) / w[1]
            decision_line.set_data(xspan, y_dec)
        else:
            if abs(w[0]) > 1e-6:
                x0 = -b / w[0]
                decision_line.set_data([x0, x0], [-1.25, 1.25])
            else:
                decision_line.set_data([], [])

        status_box.set_text(
            f'iter: {model_obj.iter_count}\npesos: [{model_obj.weights[0]:.3f}, {model_obj.weights[1]:.3f}]  b: {model_obj.bias:.3f}'
        )

        fig.canvas.draw_idle()
        plt.pause(0.001)

    def on_train(evt):
        per_model.lr = s_lr.val
        epochs = int(s_iter.val)
        btn_train.label.set_text('corriendo...')
        btn_train.ax.figure.canvas.draw()
        per_model.fit(epochs, callback=refresh_display, notify_every=1)
        pct = per_model.score()
        acc_box.set_text(f'precisión (test): {pct:.2f}%')
        btn_train.label.set_text('entrenar')
        btn_train.ax.figure.canvas.draw()

    def on_reset(evt):
        per_model.reset()
        # reconstruir scatter colors y actualizar líneas
        refresh_display(per_model)
        acc_box.set_text('')

    btn_train.on_clicked(on_train)
    btn_reset.on_clicked(on_reset)

    # primera actualización y mostrar
    refresh_display(per_model)
    plt.show()

# prueba headless (verificación funcional)
def quick_check():
    m = AgentPerceptron(n_train=50, n_test=200, lr=0.1)
    print('inicio -> pesos:', m.weights, 'bias:', m.bias)
    m.fit(epochs=50)
    print(f'precision headless: {m.score():.2f}%')

if __name__ == '__main__':
    quick_check()
    m = AgentPerceptron(n_train=200, n_test=400, lr=0.1)
    build_interface(m)
