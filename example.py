import json
import random
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QComboBox, QDialog, QPushButton, QVBoxLayout

from chartjswidget import ChartJSWidget


class App(QApplication):
    def __init__(self):
        super().__init__()
        self.n_datasets = 2

        my_config = {
        'type': 'bar',
        'options': {}
        }

        my_data = {
        'labels': ['January', 'February', 'March', 'April', 'May', 'June'],
        'datasets': self._random_datasets()
        }

        self.w = QDialog()
        self.w.setWindowTitle("ChartJSWidget Example")
        layout = QVBoxLayout(self.w)

        self.chart = ChartJSWidget(config=my_config, data=my_data)
        self.chart.resize(1024, 768)
        self.chart.setContextMenuPolicy(Qt.NoContextMenu)
        layout.addWidget(self.chart)

        dropbox = QComboBox()
        dropbox.addItem('bar')
        #dropbox.addItem('bubble')
        dropbox.addItem('doughnut')
        dropbox.addItem('line')
        dropbox.addItem('polarArea')
        dropbox.addItem('radar')
        #dropbox.addItem('scatter')
        layout.addWidget(dropbox)
        dropbox.currentTextChanged.connect(self.reconfigure)

        button = QPushButton("Randomize Data")
        button.clicked.connect(self.randomize)
        layout.addWidget(button)

        self.w.show()

    def _random_color(self):
        color = ','.join([str(random.randrange(0,256)) for _ in range(3)])
        return f'rgb({color})'

    def _random_datasets(self):
        res = []
        # yes, the results look terrible
        for i in range(self.n_datasets):
            res.append({
                'label': f'Rando Set {i}',
                'backgroundColor': self._random_color(),
                'borderColor': self._random_color(),
                'data': [random.randrange(-100, 100) for i in range(6)]
                })
        return res

    def randomize(self):
        self.chart.data['datasets'] = self._random_datasets()
        self.chart.update()

    def reconfigure(self, type_):
        self.chart.config['type'] = type_
        self.chart.redraw()



if __name__ == "__main__":
    app = App()
    sys.exit(app.exec())

