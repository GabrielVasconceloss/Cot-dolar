import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import requests
import json
from datetime import datetime


class CotacaoDolarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cotação do Dólar em Tempo Real")

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.plot = self.fig.add_subplot(1, 1, 1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.atualizar_grafico()

    def obter_cotacao_dolar(self):
        # Substitua 'SUA_CHAVE_API' pela chave da sua conta no Alpha Vantage
        api_key = 'HA9PMO6Z4VVRCB54'
        url = f'https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=USD&to_symbol=BRL&interval=1min&apikey={api_key}'

        response = requests.get(url)
        dados = json.loads(response.text)

        if 'Time Series FX (1min)' in dados:
            # Obtém a última cotação
            ultima_cotacao = list(dados['Time Series FX (1min)'].values())[0]['1. open']
            return float(ultima_cotacao)
        else:
            return None

    def atualizar_grafico(self):
        cotacao = self.obter_cotacao_dolar()

        if cotacao is not None:
            agora = datetime.now().strftime('%H:%M:%S')
            self.plot.clear()
            self.plot.plot(agora, cotacao, marker='o', color='b')
            self.plot.set_title("Cotação do Dólar em Tempo Real")
            self.plot.set_xlabel("Hora")
            self.plot.set_ylabel("Cotação do Dólar (BRL)")
            self.canvas.draw()

        # Atualiza a cada 1 minuto (60000 milissegundos)
        self.root.after(60000, self.atualizar_grafico)


if __name__ == "__main__":
    root = tk.Tk()
    app = CotacaoDolarApp(root)
    root.mainloop()
