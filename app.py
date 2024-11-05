import google.generativeai as genai
from flask import Flask,render_template,request,logging,jsonify
import os
import textblob
import requests
import yfinance as yf

api = "AIzaSyBCBD5Hj0toGJHEuJheSIQNim86amy5Jmw"
genai.configure(api_key=api)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/ai_agent", methods=["GET","POST"])
def ai_agent():
    return(render_template("ai_agent.html"))

@app.route("/ai_agent_reply", methods=["GET","POST"])
def ai_agent_reply():
    q = request.form.get("q")
    r = model.generate_content(q)
    return(render_template("ai_agent_reply.html",r=r.text))

@app.route("/prediction", methods=["GET","POST"])
def prediction():
    return(render_template("index.html"))

@app.route("/joke", methods=["GET","POST"])
def joke():
    return(render_template("joke.html"))

@app.route("/paynow", methods=["GET","POST"])
def paynow():
    return(render_template("paynow.html"))

@app.route("/sentiment_analysis", methods=["GET","POST"])
def sentiment_analysis():
    return(render_template("sentiment_analysis.html"))

@app.route("/sentiment_analysis_reply", methods=["GET","POST"])
def sentiment_analysis_reply():
    q = request.form.get("q")
    r = textblob.TextBlob(q).sentiment
    return(render_template("sentiment_analysis_reply.html",r=r))

def fetch_financial_news():
    api_key = "76cac055c5ec487cb5f01affdd1bd27f"
    url = f"https://newsapi.org/v2/everything?q=finance&language=en&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data.get('articles', [])
    else:
        logging.error("Failed to fetch financial news")
        return []

MAGNIFICENT_7_SYMBOLS = ["AAPL", "MSFT", "NVDA", "TSLA", "GOOGL", "AMZN", "META"]

def get_stock_data(symbols):
    stock_data = {}
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")  # Get today's data
        if not data.empty:
            last_quote = data.iloc[-1]
            stock_data[symbol] = {
                "price": round(last_quote["Close"], 2),
                "change": round(last_quote["Close"] - last_quote["Open"], 2),
                "percent_change": round((last_quote["Close"] - last_quote["Open"]) / last_quote["Open"] * 100, 2)
            }
    return stock_data

@app.route("/financial_news", methods=["GET", "POST"])
def financial_news():
    news_articles = fetch_financial_news()
    stock_data = get_stock_data(MAGNIFICENT_7_SYMBOLS)
    return render_template('financial_news.html', stock_data = stock_data, news_articles=news_articles)

@app.route("/get_stock_data", methods=["GET"])
def get_stock_data_route():
    stock_data = get_stock_data(MAGNIFICENT_7_SYMBOLS)
    return jsonify(stock_data)

if __name__ == "__main__":
    app.run()
