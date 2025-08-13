from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    chart_data = None
    error = None

    if request.method == "POST":
        symbols_input = request.form.get("symbols")
        symbols = [s.strip().upper() for s in symbols_input.split(",") if s.strip()]

        if not symbols:
            error = "Please enter at least one stock symbol"
        else:
            chart_data = {"dates": None, "datasets": []}
            try:
                for symbol in symbols:
                    stock = yf.Ticker(symbol)
                    history = stock.history(period="7d")
                    if not history.empty:
                        dates = history.index.strftime("%Y-%m-%d").tolist()
                        prices = history["Close"].round(2).tolist()
                        if chart_data["dates"] is None:
                            chart_data["dates"] = dates
                        zipped = list(zip(dates, prices))
                        chart_data["datasets"].append({"label": symbol, "data": zipped})
                    else:
                        error = f"No data found for {symbol}"
            except Exception as e:
                error = str(e)

    return render_template("index.html", chart_data=chart_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)