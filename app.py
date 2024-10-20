import google.generativeai as genai
from flask import Flask,render_template,request
import os
import textblob

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

if __name__ == "__main__":
    app.run()
