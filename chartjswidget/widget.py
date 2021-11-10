import importlib.resources
import json

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget


CHART_JS = 'chart-3.8.0.min.js'
PAGE_TEMPLATE = 'page.html'


class ChartJSWidget(QWebEngineView):
    """This is s a _thin_ wrapper around QWebEngineView that displays
    a web view containing a canvas rending a chart.js chart.

    ```python
    import random
    from chartjswidget import ChartJSWidget

    my_config = {
    'type': 'line',
    'options': {}
    }

    my_data = {
    'labels': ['January', 'February', 'March', 'April', 'May', 'June'],
    'datasets': [{
      'label': 'Random numbers',
      'backgroundColor': 'rgb(255, 99, 132)',
      'borderColor': 'rgb(255, 99, 132)',
      'data': [random.randrange(0, 45) for i in range(6)]
    }]
    }

    widget = ChartJSWidget(config=my_config, data=my_data)
    ```
    """
    def __init__(self, config:dict={}, data:dict={}, style:str='',
                 parent:QWidget=None) -> None:
        """Create a ChartJSWidget

        Keyword arguments:
        config (dict) -- The ChartJS config object.
        data (dict) -- The ChartJS data. Do not specify both config['data']
                       and a separate data parameter
        style (str) -- Raw CSS styles to include in the HTML document
        parent (object) -- Qt parent of this widget

        Returns:
        None
        """
        super().__init__(parent)
        self._style = style

        if (type(config) is not dict) or ('type' not in config):
            raise ValueError('config must be a dict containing "type" key.')
        self.config = config

        if data and 'data' in self.config:
            raise ValueError('do not supply both config["data"] and data')

        if data and ((type(data) is not dict) or ('datasets' not in data)):
            raise ValueError('data must be a dict containing "datasets" key.')
        self.data = data

        if data and 'data' not in self.config:
            self.config.update({'data': self.data})

        with importlib.resources.open_text(__package__, CHART_JS) as fh:
            self._chart_js = fh.read()
        with importlib.resources.open_text(__package__, PAGE_TEMPLATE) as fh:
            self._html = fh.read()

        self.redraw()


    def redraw(self):
        html = self._html.replace('CHART_JS_CODE', self._chart_js)
        html = html.replace('CHART_CONFIG', json.dumps(self.config))
        html = html.replace('PAGE_STYLE', self._style)
        self.setHtml(html)


    def update(self, config=False, data=True) -> None:
        """Update the chart by calling a Javascript function to set new data
        and/or config values, followed by a call to `.update()`.

        Keyword arguments:
        config (bool) -- Update `.config` (default False)
        data (bool) -- Update `.data` (default True)

        Returns:
        None
        """
        page = self.page()
        if config:
          new_config = json.dumps(self.config)
          page.runJavaScript(f'qChart.config = {new_config};')
        if data:
          new_data = json.dumps(self.data)
          page.runJavaScript(f'qChart.data = {new_data};')
        page.runJavaScript('qChart.update();')


