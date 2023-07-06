from flask import Flask, render_template, request, redirect, url_for
import quotes

app = Flask(__name__)


@app.route('/')
def index():
  quote = quotes.get_daily_quote()
  return render_template('index.html', quote_of_the_day=quote)

@app.route('/generate_random_message', methods=["POST"])
def generate_random_message():
  quote = quotes.get_random_quote()
  return render_template("generation.html", quote=quote)


@app.route('/generate_prompted_message', methods=["POST"])
def generate_prompted_message():
  prompt = request.form["prompt_textbox"]
  quote = quotes.get_prompted_quote(prompt)
  return render_template("generation.html", quote=quote)


@app.route('/home', methods=["POST"])
def home():
  return redirect(url_for('index'))


@app.route('/meet', methods=["POST"])
def meet():
  return render_template("meet.html")


@app.route('/saved', methods=["POST"])
def saved():
  return render_template("saved.html")


if __name__ == "__main__":
  quotes.start_quote_generation()
  app.run(host='0.0.0.0', port=777)