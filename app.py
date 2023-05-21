from flask import Flask, render_template, request
import yfinance as yf
import mplfinance as mpf
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

    # 株価データの取得
    history = ticker.history(period='1y')

    # キャンドルチャートを描画
    fig, ax = mpf.plot(history, type='candle', mav=(5, 10), volume=True, returnfig=True)
    
    # チャートを画像に変換
    chart_img = BytesIO()
    fig.savefig(chart_img, format='png')
    chart_img.seek(0)
    chart_base64 = base64.b64encode(chart_img.getvalue()).decode('utf-8')
    
    return render_template('roe.html', symbol=symbol, roe=roe, chart_base64=chart_base64)

if __name__ == '__main__':
    app.run(debug=True)
