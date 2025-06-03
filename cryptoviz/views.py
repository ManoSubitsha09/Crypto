import numpy as np
from sklearn.preprocessing import MinMaxScaler
from flask import render_template, request
from cryptoviz.util import data_extract, plot_graph_with_forecast
from cryptoviz import flaskapp, eth_model, btc_model, ltc_model, xrp_model


@flaskapp.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == "POST":
        crypto = request.form.get('crypto')
        start = request.form.get('start')
        end = request.form.get('end')

        # Map crypto to symbol and model
        crypto_mapping = {
            "bitcoin": ("BTCUSDT", btc_model),
            "ethereum": ("ETHUSDT", eth_model),
            "ripple": ("XRPUSDT", xrp_model),
            "litecoin": ("LTCUSDT", ltc_model)
        }

        if crypto not in crypto_mapping:
            return render_template("home.html", error="Cryptocurrency not available.")

        sym, model = crypto_mapping[crypto]

        try:
            # Get data and timestamps
            data, timestamps = data_extract(sym, start, end)
            if len(data) < 2:
                return render_template("home.html", error="Not enough data for the selected range.")

            # Scale data
            scaler = MinMaxScaler()
            data_scaled = scaler.fit_transform(data)

            # Real-time prediction on historical data
            X_test = data_scaled[:-1]
            y_test = data_scaled[1:]
            X_test_reshaped = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))
            predicted_real = model.predict(X_test_reshaped)
            predicted_real = scaler.inverse_transform(predicted_real)
            real_price = scaler.inverse_transform(y_test)

            # Future forecast (e.g., next 30 days)
            future_steps = 30
            last_input = data_scaled[-1].reshape(1, 1, data_scaled.shape[1])
            future_forecast = []

            for _ in range(future_steps):
                next_pred = model.predict(last_input)
                future_forecast.append(next_pred[0])
                last_input = np.reshape(next_pred, (1, 1, data_scaled.shape[1]))

            future_forecast = scaler.inverse_transform(np.array(future_forecast))

            # Generate plot with historical + future data
            plot_html = plot_graph_with_forecast(crypto, predicted_real, real_price, timestamps[1:], future_forecast)

            return render_template("predict.html", plot_html=plot_html)

        except Exception as e:
            return render_template("home.html", error=f"Error during prediction: {str(e)}")

    return render_template("home.html")


@flaskapp.route("/")
def home():
    return render_template("home.html")