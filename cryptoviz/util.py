import numpy as np
import pandas as pd
from binance.spot import Spot
import plotly.graph_objects as go
from plotly.offline import plot
from datetime import datetime, timedelta

# Replace with your actual Binance API key and secret
API_KEY = 'API_KEY'
SECRET_KEY = 'SECRET_KEY'


def data_extract(sym, start, end):
    client = Spot(api_key=API_KEY, api_secret=SECRET_KEY)

    start_ts = int(pd.to_datetime(start).timestamp() * 1000)
    end_ts = int(pd.to_datetime(end).timestamp() * 1000) if end else int(pd.Timestamp.now().timestamp() * 1000)

    all_data = []
    limit = 1000  # Binance max per call
    interval = 30 * 60 * 1000  # 30 minutes in ms

    while start_ts < end_ts:
        response = client.klines(symbol=sym, interval='30m', startTime=start_ts, endTime=end_ts, limit=limit)
        if not response:
            break
        all_data.extend(response)

        # Move to next batch
        last_ts = response[-1][0]
        start_ts = last_ts + interval

        if last_ts >= end_ts:
            break

    # Convert to DataFrame
    cryptocurrency = pd.DataFrame(all_data, columns=[
        'Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Close time', 'Quote asset volume', 'Number of trades',
        'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'
    ])
    cryptocurrency['Open time'] = pd.to_datetime(cryptocurrency['Open time'], unit='ms')
    cryptocurrency.set_index('Open time', inplace=True)

    return cryptocurrency.iloc[:, 3:4].astype(float).values, cryptocurrency.index


def plot_graph_with_forecast(crypto, predicted_price, real_price, dates, forecast):
    import plotly.graph_objects as go
    from datetime import timedelta

    # Forecast timestamps (30 minutes apart like real data)
    last_date = dates[-1].to_pydatetime() if isinstance(dates[-1], pd.Timestamp) else dates[-1]
    forecast_dates = [last_date + timedelta(minutes=30 * (i + 1)) for i in range(len(forecast))]

    fig = go.Figure()

    # Real and Predicted
    fig.add_trace(go.Scatter(
        x=dates[1:], y=real_price.flatten(),
        mode='lines', name='Real Price', line=dict(color='purple')
    ))

    fig.add_trace(go.Scatter(
        x=dates[1:], y=predicted_price.flatten(),
        mode='lines', name='Predicted Price', line=dict(color='orange')
    ))

    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast_dates, y=forecast.flatten(),
        mode='lines', name='Future Forecast',
        line=dict(color='green', dash='dash')
    ))

    # Set the x-axis range only to the relevant date area
    full_dates = list(dates[1:]) + forecast_dates
    fig.update_layout(
        title=f'{crypto.capitalize()} Price Prediction with Forecast',
        xaxis_title='Date',
        yaxis_title='Price (USDT)',
        hovermode='x unified',
        legend=dict(x=0.01, y=0.99),
        xaxis=dict(range=[full_dates[0], full_dates[-1]])
    )

    return fig.to_html(full_html=False)