from flask import Flask, render_template, request
import yfinance as yf
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/roe', methods=['POST'])
def roe():
    symbol = request.form['symbol']
    ticker = yf.Ticker(symbol)
    roe = ticker.info['returnOnEquity']

    # 株価データの取得とチャート作成
    history = ticker.history(period='1y')
    plt.plot(history.index, history['Close'])
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Price Chart for ' + symbol)
    plt.grid(True)

    # チャートを画像に変換
    chart_img = BytesIO()
    plt.savefig(chart_img, format='png')
    chart_img.seek(0)
    chart_base64 = base64.b64encode(chart_img.getvalue()).decode('utf-8')

    return render_template('roe.html', symbol=symbol, roe=roe, chart_base64=chart_base64)

if __name__ == '__main__':
    app.run(debug=True)
