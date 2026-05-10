import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests

# PAGE CONFIG
st.set_page_config(
    page_title="Stock Market Analyzer",
    page_icon="📈",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<style>
.main {
    background-color: #0E1117;
    color: white;
}

.stMetric {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 10px;
}

h1, h2, h3 {
    color: #00FFAA;
}
</style>
""", unsafe_allow_html=True)

# TITLE
st.title("📈 AI Stock Market Analyzer Dashboard")

# SIDEBAR
st.sidebar.header("Dashboard Controls")

ticker = st.sidebar.text_input("Stock Ticker", "AAPL")

start_date = st.sidebar.date_input(
    "Start Date",
    pd.to_datetime("2023-01-01")
)

end_date = st.sidebar.date_input(
    "End Date",
    pd.to_datetime("today")
)

# FETCH DATA
df = yf.download(ticker, start=start_date, end=end_date)

# INDICATORS
df["SMA20"] = df["Close"].rolling(20).mean()
df["EMA20"] = df["Close"].ewm(span=20).mean()

# RSI
delta = df["Close"].diff()

gain = (delta.where(delta > 0, 0)).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()

rs = gain / loss

df["RSI"] = 100 - (100 / (1 + rs))

# KPI SECTION
st.subheader("📊 Market Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Price",
    f"${round(df['Close'].iloc[-1], 2)}"
)

col2.metric(
    "Highest Price",
    f"${round(df['High'].max(), 2)}"
)

col3.metric(
    "Lowest Price",
    f"${round(df['Low'].min(), 2)}"
)

returns = (
    (df["Close"].iloc[-1] - df["Close"].iloc[0])
    / df["Close"].iloc[0]
) * 100

col4.metric(
    "Total Return",
    f"{round(returns,2)}%"
)

# CANDLESTICK CHART
st.subheader("📈 Candlestick Chart")

fig = go.Figure()

fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Market Data'
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["SMA20"],
        line=dict(color='orange'),
        name='SMA 20'
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["EMA20"],
        line=dict(color='cyan'),
        name='EMA 20'
    )
)

fig.update_layout(
    template="plotly_dark",
    height=700
)

st.plotly_chart(fig, use_container_width=True)

# RSI CHART
st.subheader("📉 RSI Indicator")

rsi_fig = go.Figure()

rsi_fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["RSI"],
        name="RSI"
    )
)

rsi_fig.update_layout(
    template="plotly_dark",
    height=400
)

st.plotly_chart(rsi_fig, use_container_width=True)

# AI PREDICTION
st.subheader("🤖 AI Stock Prediction")

if st.button("Predict Next Day Price"):

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json={
                "price": float(df["Close"].iloc[-1])
            }
        )

        prediction = response.json()["prediction"]

        st.success(
            f"Predicted Next Price: ${round(prediction, 2)}"
        )

    except:
        st.error("FastAPI server not running!")

# DOWNLOAD DATA
csv = df.to_csv().encode('utf-8')

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name=f"{ticker}_data.csv",
    mime='text/csv'
)

# RAW DATA
st.subheader("📄 Raw Data")

st.dataframe(df.tail(20))