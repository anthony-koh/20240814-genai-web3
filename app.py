import google.generativeai as genai
from flask import Flask,render_template,request,logging,jsonify
import os
import textblob
import requests

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
    
@app.route("/financial_news", methods=["GET", "POST"])
def financial_news():
    news_articles = fetch_financial_news()
    return render_template('financial_news.html', news_articles=news_articles)

if __name__ == "__main__":
    app.run()
