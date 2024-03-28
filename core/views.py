# views.py

from django.shortcuts import render, redirect
import plotly.graph_objs as go
from plotly.offline import plot
from .models import Preferences
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm,CustomUserChangeForm,PreferencesForm
from django.http import JsonResponse
import matplotlib.pyplot as plt
import yfinance as yf
def home(request):
    # Fetch real-time data from Yahoo Finance for a specific stock (e.g., S&P 500)
    stock_data = yf.download('^GSPC', period='1d', interval='1m')

    # Perform ARIMA prediction
    # Example: ARIMA model with p=5, d=1, and q=0
    model = ARIMA(stock_data['Close'], order=(5, 1, 0))
    fitted_model = model.fit()
    forecast_steps = 15  # 180 steps correspond to 3 hours (60 minutes/hour * 3 hours)
    forecast = fitted_model.forecast(steps=forecast_steps)

    # Create a candlestick trace
    trace = go.Candlestick(
        x=stock_data.index,
        open=stock_data['Open'],
        high=stock_data['High'],
        low=stock_data['Low'],
        close=stock_data['Close'],
        name='World Stock Price'
    )

    # Generate future timestamps for the forecast
    last_timestamp = stock_data.index[-1]
    future_timestamps = pd.date_range(start=last_timestamp, periods=forecast_steps+1, closed='right', freq='T')[1:]

    # Add ARIMA forecast as a scatter plot
    forecast_trace = go.Scatter(
        x=future_timestamps,
        y=forecast,
        mode='lines',
        name='Forecast',
        line=dict(color='blue', width=2)
    )

    # Define layout with rangeslider
    layout = go.Layout(
        title='Real-Time World Stock Price Plot with Forecast',
        xaxis=dict(title='Time', rangeslider=dict(visible=True)),  # Add rangeslider
        yaxis=dict(title='Price')
    )

    # Create Plotly figure
    fig = go.Figure(data=[trace, forecast_trace], layout=layout)
    plot_div = fig.to_html(full_html=False)

    return render(request, 'home.html', {'plot_div': plot_div})


def how(request):
    return render(request, 'how.html')
def about(request):
    return render(request, 'about.html')

from django.shortcuts import render
import pandas as pd
import plotly.graph_objs as go


from statsmodels.tsa.arima.model import ARIMA

def dashboard(request):
    # Load CSV data
    df = pd.read_csv('C:/Users/solta/OneDrive/Bureau/project/trading-agent/data/TUNINDEX_pi_ds_esprit.csv')

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Fit an ARIMA model
    model = ARIMA(df['Close'], order=(5, 1, 0))
    model_fit = model.fit()

    # Forecast future prices
    forecast = model_fit.forecast(steps=10)

    # Create Plotly trace for the candlestick chart
    trace_candlestick = go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Historical Price',
        increasing=dict(line=dict(color='green')),  # Color for increasing candles
        decreasing=dict(line=dict(color='red'))     # Color for decreasing candles
    )

    # Add forecasted prices to the trace
    forecast_dates = pd.date_range(start=df['Date'].iloc[-1], periods=5)[1:]
    trace_forecast = go.Scatter(
        x=forecast_dates,
        y=forecast,
        mode='lines',
        name='Forecasted Price',
        line=dict(color='blue'),  # Change color for forecasted prices
        hoverinfo='x+y',
        showlegend=True
    )

    # Define layout for the main plot
    layout = go.Layout(
        title='Tunindex Price Chart with Forecast',
        xaxis=dict(title='Date', tickformat='%d-%m-%Y'),
        yaxis=dict(title='Price', tickformat=',.0f'),
        hovermode='closest',
        showlegend=True,
        font=dict(family='Arial, sans-serif', size=12, color='black'),
        margin=dict(l=80, r=50, t=80, b=50)
    )

    # Create Plotly figure
    fig = go.Figure(data=[trace_candlestick, trace_forecast], layout=layout)

    # Add date range selector
    fig.update_layout(xaxis_rangeslider_visible=True)

    # Convert Plotly figure to JSON
    plotly_chart = fig.to_json()

    return render(request, 'dashboard.html', {'plotly_chart': plotly_chart})









import pandas as pd
from django.shortcuts import render
import plotly.graph_objs as go
from statsmodels.tsa.arima.model import ARIMA
from django.core.paginator import Paginator

def market_insights(request):
    # Load CSV data
    df = pd.read_csv('C:/Users/solta/OneDrive/Bureau/project/trading-agent/data/all_data2.csv')

    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Keep only the rows with the highest price for each date
    df = df.loc[df.groupby('Date')['Price'].idxmax()]

    # Fit an ARIMA model
    model = ARIMA(df['Price'], order=(5, 1, 0))
    model_fit = model.fit()

    # Forecast future prices
    forecast = model_fit.forecast(steps=10)

    # Create Plotly trace for the line chart
    trace = go.Scatter(x=df['Date'],
                       y=df['Price'],
                       mode='lines',  # Display only points
                       name='Highest Price',
                       hoverinfo='x+y+text',
                       text=df.apply(lambda row: f"Date: {row['Date']}<br>Price: {row['Price']}<br>Open: {row['Open']}<br>High: {row['High']}<br>Low: {row['Low']}", axis=1))

    # Add forecasted prices to the trace
    forecast_dates = pd.date_range(start=df['Date'].iloc[-1], periods=5)[1:]
    trace_forecast = go.Scatter(x=forecast_dates,
                                y=forecast,
                                mode='lines',
                                name='Forecasted Price',
                                line=dict(color='green'),  # Change color for forecasted prices
                                hoverinfo='x+y',
                                showlegend=True)

    # Define layout for the main plot
    layout = go.Layout(title='Stock Market Price Chart with Forecast',
                       xaxis=dict(title='Date', tickformat='%d-%m-%Y'),
                       yaxis=dict(title='Price', tickformat=',.0f'),
                       hovermode='closest',
                       showlegend=True,
                       font=dict(family='Arial, sans-serif', size=12, color='black'),
                       margin=dict(l=80, r=50, t=80, b=50))

    # Create Plotly figure
    fig = go.Figure(data=[trace, trace_forecast], layout=layout)

    # Add date range selector
    fig.update_layout(xaxis_rangeslider_visible=True)

    # Convert Plotly figure to JSON
    plotly_chart = fig.to_json()
    df1 = pd.read_csv('C:/Users/solta/OneDrive/Bureau/project/trading-agent/data/all_data2.csv')
    df1['Date'] = pd.to_datetime(df1['Date'])

    # Get the latest data for each company
    df_latest = df1.groupby('value').apply(lambda x: x.nlargest(1, 'Date')).reset_index(drop=True)

    # Prepare data for the table
    table_data = df_latest[['value', 'Open', 'Price', 'Change','Sector']]


    # Convert the current page object to a list of dictionaries
    table_data_list = table_data.to_dict(orient='records')

    # Sentiment analysis data (dummy data for now)
    news_sentiment = {'Positive': 0.6, 'Neutral': 0.3, 'Negative': 0.1}

    return render(request, 'market_insights.html', {'plotly_chart': plotly_chart, 'news_sentiment': news_sentiment, 'table_data': table_data_list})











def company_details(request, company_name):
    # Load CSV data
    df = pd.read_csv('C:/Users/solta/OneDrive/Bureau/project/trading-agent/data/all_data2.csv')

    # Filter data for the specified company
    df_company = df[df['value'] == company_name]

    # Convert Date column to datetime
    df_company['Date'] = pd.to_datetime(df_company['Date'])

    # Fit an ARIMA model
    model = ARIMA(df_company['Price'], order=(5, 1, 0))
    model_fit = model.fit()

    # Forecast future prices
    forecast = model_fit.forecast(steps=10)

    # Additional information about the company
    company_info = {
        'name': company_name,
        'latest_price': df_company['Price'].iloc[-1],
        'open_price': df_company['Open'].iloc[-1],
        'high_price': df_company['High'].max(),
        'low_price': df_company['Low'].min(),
        'sector': df_company['Sector'].iloc[0]  # Assuming the sector is constant for the company
    }

    # Create Plotly trace for the line chart
    trace = go.Scatter(x=df_company['Date'],
                       y=df_company['Price'],
                       mode='lines',  # Display only points
                       name='Price',
                       hoverinfo='x+y+text',
                       text=df_company.apply(lambda row: f"Date: {row['Date']}<br>Price: {row['Price']}<br>Open: {row['Open']}<br>High: {row['High']}<br>Low: {row['Low']}", axis=1))

    # Add forecasted prices to the trace
    forecast_dates = pd.date_range(start=df_company['Date'].iloc[-1], periods=5)[1:]
    trace_forecast = go.Scatter(x=forecast_dates,
                                y=forecast,
                                mode='lines',
                                name='Forecasted Price',
                                line=dict(color='green'),  # Change color for forecasted prices
                                hoverinfo='x+y',
                                showlegend=True)

    # Define layout for the main plot
    layout = go.Layout(title=f'Stock Market Price Chart for {company_name} with Forecast',
                       xaxis=dict(title='Date', tickformat='%d-%m-%Y'),
                       yaxis=dict(title='Price', tickformat=',.0f'),
                       hovermode='closest',
                       showlegend=True,
                       font=dict(family='Arial, sans-serif', size=12, color='black'),
                       margin=dict(l=80, r=50, t=80, b=50))

    # Create Plotly figure
    fig = go.Figure(data=[trace, trace_forecast], layout=layout)

    # Add date range selector
    fig.update_layout(xaxis_rangeslider_visible=True)

    # Convert Plotly figure to JSON
    plotly_chart = fig.to_json()

    # Pass data to the template for rendering
    return render(request, 'company_details.html', {'plotly_chart': plotly_chart, 'company_info': company_info})








def sector_details(request, sector_name):
    # Load CSV data
    df = pd.read_csv('C:/Users/solta/OneDrive/Bureau/project/trading-agent/data/all_data2.csv')

    # Filter data for the specified sector
    df_sector = df[df['Sector'] == sector_name]

    # Convert Date column to datetime
    df_sector['Date'] = pd.to_datetime(df_sector['Date'])

    # Fit an ARIMA model
    model = ARIMA(df_sector['Price'], order=(5, 1, 0))
    model_fit = model.fit()

    # Forecast future prices
    forecast = model_fit.forecast(steps=10)

    # Additional information about the sector
    sector_info = {
        'name': sector_name,
        'average_price': df_sector['Price'].mean(),
        'highest_price': df_sector['Price'].max(),
        'lowest_price': df_sector['Price'].min(),
        'total_companies': df_sector['value'].nunique()
    }

    # Create Plotly trace for the line chart
    trace = go.Scatter(x=df_sector['Date'],
                       y=df_sector['Price'],
                       mode='lines',  # Display only points
                       name='Price',
                       hoverinfo='x+y+text',
                       text=df_sector.apply(lambda row: f"Date: {row['Date']}<br>Price: {row['Price']}<br>Open: {row['Open']}<br>High: {row['High']}<br>Low: {row['Low']}", axis=1))

    # Add forecasted prices to the trace
    forecast_dates = pd.date_range(start=df_sector['Date'].iloc[-1], periods=5)[1:]
    trace_forecast = go.Scatter(x=forecast_dates,
                                y=forecast,
                                mode='lines',
                                name='Forecasted Price',
                                line=dict(color='green'),  # Change color for forecasted prices
                                hoverinfo='x+y',
                                showlegend=True)

    # Define layout for the main plot
    layout = go.Layout(title=f'Stock Market Price Chart for {sector_name} with Forecast',
                       xaxis=dict(title='Date', tickformat='%d-%m-%Y'),
                       yaxis=dict(title='Price', tickformat=',.0f'),
                       hovermode='closest',
                       showlegend=True,
                       font=dict(family='Arial, sans-serif', size=12, color='black'),
                       margin=dict(l=80, r=50, t=80, b=50))

    # Create Plotly figure
    fig = go.Figure(data=[trace, trace_forecast], layout=layout)

    # Add date range selector
    fig.update_layout(xaxis_rangeslider_visible=True)

    # Convert Plotly figure to JSON
    plotly_chart = fig.to_json()

    # Pass data to the template for rendering
    return render(request, 'sector_details.html', {'plotly_chart': plotly_chart, 'sector_info': sector_info})










def portfolio_analysis(request):    
    # Dummy data for demonstration
    portfolio_metrics = {'Cumulative Returns': 0.25, 'Volatility': 0.15, 'Sharpe Ratio': 1.5, 'Max Drawdown': 0.1}
    benchmark_performance = {'Cumulative Returns': 0.20, 'Volatility': 0.12, 'Sharpe Ratio': 1.3, 'Max Drawdown': 0.12}

    return render(request, 'portfolio_analysis.html', {'portfolio_metrics': portfolio_metrics,
                                                        'benchmark_performance': benchmark_performance})







from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def trading_strategies(request):
    # Dummy data for demonstration (trading strategies)
    trading_strategies_info = [
    {'Name': 'Introduction to Trading', 'Objective': 'Getting started with trading fundamentals', 'Image': '/static/images/intro.jpg', 'Description': "Trading is the art of buying and selling financial assets, such as stocks, bonds, currencies, and commodities, with the aim of making a profit. It involves analyzing market data, identifying opportunities, and executing trades based on various strategies like the ones mentioned above. Whether you're a seasoned investor or a novice trader, understanding these strategies can help you navigate the complex world of financial markets more effectively. Happy trading!"},
    {'Name': 'Momentum Strategy', 'Objective': 'Maximizing returns', 'Image': '/static/images/mom.jpg', 'Description': "Imagine you're at a sports event, witnessing a team on an impressive winning streak. Momentum traders operate much like enthusiastic fans cheering for the team with consistent victories. They rely on the principle that assets exhibiting recent positive price movements are likely to continue rising, while those with negative movements are expected to keep falling. This strategy is grounded in the idea that markets tend to follow trends, and once a trend is established, it's likely to persist for a certain period. Momentum traders use technical indicators like Relative Strength Index (RSI) or Moving Average Convergence Divergence (MACD) to identify assets with strong momentum. For instance, if a stock has been steadily climbing in price over the past few weeks, a momentum trader might buy it, expecting the upward trend to continue. However, it's essential for momentum traders to exercise caution, as momentum can quickly shift, leading to abrupt reversals in price direction."},
    {'Name': 'Mean Reversion Strategy', 'Objective': 'Minimizing volatility', 'Image': '/static/images/mr.jpg', 'Description': "Picture a rubber band being stretched to its limit; eventually, it snaps back to its original position. Mean reversion traders operate on a similar principle, believing that asset prices tend to move back towards their historical average over time. When an asset's price strays too far from its mean, these traders see it as an opportunity to buy low or sell high. The strategy is based on the assumption that markets often exhibit short-term fluctuations around a long-term equilibrium or average price. For example, if a stock's price has dropped significantly below its long-term average, a mean reversion trader might buy it, anticipating a return to its average price. However, it's crucial for mean reversion traders to carefully assess whether the price deviation from the mean is a temporary anomaly or a sign of a fundamental change in the asset's value."},
    {'Name': 'Trend Following Strategy', 'Objective': 'Identifying and riding trends', 'Image': '/static/images/tf.jpg', 'Description': "Imagine riding a wave at the beach; you catch the wave's momentum and ride it until it begins to lose strength. Trend following traders operate similarly, aiming to profit from sustained price movements in a particular direction. They identify trends using technical analysis tools like moving averages or trendlines. When they spot an upward trend, they buy assets with the expectation that prices will continue to rise. Conversely, during a downtrend, they sell assets, anticipating further declines. Trend following strategies are based on the belief that markets exhibit momentum, and once a trend is established, it's likely to continue for a significant period. However, it's essential for trend followers to be mindful of potential reversals and to implement risk management measures to protect against adverse market movements."},
    {'Name': 'Arbitrage Strategy', 'Objective': 'Exploiting price inefficiencies', 'Image': '/static/images/ar.jpg', 'Description': "Imagine finding the same product selling for different prices in two different stores; you buy it from the cheaper store and sell it at the higher-priced one, pocketing the price difference as profit. Arbitrageurs exploit price discrepancies between different markets or assets to make risk-free profits. This strategy relies on the principle of the law of one price, which states that identical goods should have the same price when expressed in a common currency. For example, if a stock is trading at $50 on one exchange and $52 on another, an arbitrageur might buy it on the cheaper exchange and simultaneously sell it on the more expensive one, profiting from the price difference. However, arbitrage opportunities are typically short-lived and require swift execution to capitalize on price disparities before they disappear."},
    {'Name': 'Contrarian Strategy', 'Objective': 'Capitalizing on market reversals', 'Image': '/static/images/cs.jpg', 'Description': "Envision swimming against the current in a river; while others are being carried downstream, you're moving in the opposite direction. Contrarian traders go against prevailing market sentiment, buying when others are selling and selling when others are buying. They believe that markets often overreact to news or events, creating opportunities to profit from sentiment shifts. Contrarian strategies are based on the premise that market sentiment tends to be cyclical, swinging between optimism and pessimism. For instance, if a stock's price plunges due to negative news, a contrarian trader might see it as an opportunity to buy low, expecting the price to rebound as market sentiment improves. However, contrarian trading requires a contrarian mindset and the ability to withstand periods of short-term market volatility."},
    {'Name': 'Breakout Strategy', 'Objective': 'Capitalizing on price breakouts', 'Image': '/static/images/bs.jpg', 'Description': "Imagine a dam bursting; once the barrier is broken, water rushes through with force. Breakout traders aim to capitalize on significant price movements that occur when an asset breaches support or resistance levels. They wait for a breakout, where the price moves above resistance or below support, signaling a potential trend continuation. Breakout strategies are based on the premise that price movements tend to accelerate following a breakout, as traders rush to capitalize on the new trend. For example, if a stock's price breaks above a key resistance level, breakout traders might buy it, anticipating further upward movement. However, breakout trading carries inherent risks, including false breakouts and whipsaw movements, requiring traders to implement strict risk management measures."},
    {'Name': 'Swing Trading Strategy', 'Objective': 'Profiting from short- to medium-term price swings', 'Image': '/static/images/sw.jpg', 'Description': "Picture a pendulum swinging back and forth; swing traders aim to profit from the market's natural ebb and flow. They identify short- to medium-term price swings within a larger trend and capitalize on them. Swing traders typically hold positions for a few days to several weeks, buying at swing lows and selling at swing highs. Swing trading strategies are based on the premise that markets often exhibit periodic fluctuations within a broader trend, providing opportunities for short-term profits. For instance, if a stock's price experiences a short-term dip within an overall uptrend, a swing trader might buy it, expecting the price to bounce back as the trend resumes. However, swing trading requires discipline and patience, as traders must wait for opportune entry and exit points to maximize profitability."},
    ]


    # Fetch user preferences (assuming one-to-one relationship between CustomUser and Preferences)
    user_preferences = None
    if request.user.is_authenticated:
        user_preferences = Preferences.objects.filter(user=request.user).first()

    # Analyze user preferences and recommend the best course
    recommended_courses = recommend_course(user_preferences)

    # Filter out the recommended courses
    recommended_strategies = []
    for course in recommended_courses:
        recommended_strategies += [strategy for strategy in trading_strategies_info if strategy['Name'] == course]

    # Paginate the courses
    paginator = Paginator(recommended_strategies, 1)  # Show 5 courses per page
    page = request.GET.get('page')
    try:
        recommended_strategies = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        recommended_strategies = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        recommended_strategies = paginator.page(paginator.num_pages)

    return render(request, 'trading_strategies.html', {'trading_strategies_info': recommended_strategies, 'recommended_course': recommended_courses})

def recommend_course(preferences):
    if not preferences:
        return ['Introduction to Trading']  # Default recommendation if preferences are not available

    # Analyze user preferences and recommend the best courses based on their preferences
    risk_tolerance = preferences.risk_tolerance
    investment_horizon = preferences.investment_horizon
    investment_objective = preferences.investment_objective
    knowledge_experience = preferences.knowledge_experience

    recommended_strategies = []

    if risk_tolerance == 'high':
        if investment_horizon == 'long_term':
            recommended_strategies.append('Mean Reversion Strategy')
            recommended_strategies.append('Trend Following Strategy')
        if investment_horizon == 'medium_term':
            recommended_strategies.append('Trend Following Strategy')
            recommended_strategies.append('Swing Trading Strategy')
        recommended_strategies.append('Momentum Strategy')
        recommended_strategies.append('Arbitrage Strategy')

    elif risk_tolerance == 'medium':
        if investment_objective == 'capital_preservation':
            recommended_strategies.append('Mean Reversion Strategy')
            recommended_strategies.append('Swing Trading Strategy')
        if investment_objective == 'income_generation':
            recommended_strategies.append('Trend Following Strategy')
            recommended_strategies.append('Arbitrage Strategy')
        recommended_strategies.append('Momentum Strategy')
        recommended_strategies.append('Breakout Strategy')

    else:  # Low risk tolerance
        if knowledge_experience == 'advanced':
            recommended_strategies.append('Mean Reversion Strategy')
            recommended_strategies.append('Breakout Strategy')
        else:
            recommended_strategies.append('Momentum Strategy')
            recommended_strategies.append('Introduction to Trading')

    return recommended_strategies



def allcourses(request):
    # Dummy data for demonstration (trading strategies)
    trading_strategies_info = [
    {'Name': 'Introduction to Trading', 'Objective': 'Getting started with trading fundamentals', 'Image': '/static/images/intro.jpg', 'Description': "Trading is the art of buying and selling financial assets, such as stocks, bonds, currencies, and commodities, with the aim of making a profit. It involves analyzing market data, identifying opportunities, and executing trades based on various strategies like the ones mentioned above. Whether you're a seasoned investor or a novice trader, understanding these strategies can help you navigate the complex world of financial markets more effectively. Happy trading!"},

    {'Name': 'Momentum Strategy', 'Objective': 'Maximizing returns', 'Image': '/static/images/mom.jpg', 'Description': "Imagine you're at a sports event, witnessing a team on an impressive winning streak. Momentum traders operate much like enthusiastic fans cheering for the team with consistent victories. They rely on the principle that assets exhibiting recent positive price movements are likely to continue rising, while those with negative movements are expected to keep falling. This strategy is grounded in the idea that markets tend to follow trends, and once a trend is established, it's likely to persist for a certain period. Momentum traders use technical indicators like Relative Strength Index (RSI) or Moving Average Convergence Divergence (MACD) to identify assets with strong momentum. For instance, if a stock has been steadily climbing in price over the past few weeks, a momentum trader might buy it, expecting the upward trend to continue. However, it's essential for momentum traders to exercise caution, as momentum can quickly shift, leading to abrupt reversals in price direction."},
    {'Name': 'Mean Reversion Strategy', 'Objective': 'Minimizing volatility', 'Image': '/static/images/mr.jpg', 'Description': "Picture a rubber band being stretched to its limit; eventually, it snaps back to its original position. Mean reversion traders operate on a similar principle, believing that asset prices tend to move back towards their historical average over time. When an asset's price strays too far from its mean, these traders see it as an opportunity to buy low or sell high. The strategy is based on the assumption that markets often exhibit short-term fluctuations around a long-term equilibrium or average price. For example, if a stock's price has dropped significantly below its long-term average, a mean reversion trader might buy it, anticipating a return to its average price. However, it's crucial for mean reversion traders to carefully assess whether the price deviation from the mean is a temporary anomaly or a sign of a fundamental change in the asset's value."},
    {'Name': 'Trend Following Strategy', 'Objective': 'Identifying and riding trends', 'Image': '/static/images/tf.jpg', 'Description': "Imagine riding a wave at the beach; you catch the wave's momentum and ride it until it begins to lose strength. Trend following traders operate similarly, aiming to profit from sustained price movements in a particular direction. They identify trends using technical analysis tools like moving averages or trendlines. When they spot an upward trend, they buy assets with the expectation that prices will continue to rise. Conversely, during a downtrend, they sell assets, anticipating further declines. Trend following strategies are based on the belief that markets exhibit momentum, and once a trend is established, it's likely to continue for a significant period. However, it's essential for trend followers to be mindful of potential reversals and to implement risk management measures to protect against adverse market movements."},
    {'Name': 'Arbitrage Strategy', 'Objective': 'Exploiting price inefficiencies', 'Image': '/static/images/ar.jpg', 'Description': "Imagine finding the same product selling for different prices in two different stores; you buy it from the cheaper store and sell it at the higher-priced one, pocketing the price difference as profit. Arbitrageurs exploit price discrepancies between different markets or assets to make risk-free profits. This strategy relies on the principle of the law of one price, which states that identical goods should have the same price when expressed in a common currency. For example, if a stock is trading at $50 on one exchange and $52 on another, an arbitrageur might buy it on the cheaper exchange and simultaneously sell it on the more expensive one, profiting from the price difference. However, arbitrage opportunities are typically short-lived and require swift execution to capitalize on price disparities before they disappear."},
    {'Name': 'Contrarian Strategy', 'Objective': 'Capitalizing on market reversals', 'Image': '/static/images/cs.jpg', 'Description': "Envision swimming against the current in a river; while others are being carried downstream, you're moving in the opposite direction. Contrarian traders go against prevailing market sentiment, buying when others are selling and selling when others are buying. They believe that markets often overreact to news or events, creating opportunities to profit from sentiment shifts. Contrarian strategies are based on the premise that market sentiment tends to be cyclical, swinging between optimism and pessimism. For instance, if a stock's price plunges due to negative news, a contrarian trader might see it as an opportunity to buy low, expecting the price to rebound as market sentiment improves. However, contrarian trading requires a contrarian mindset and the ability to withstand periods of short-term market volatility."},
    {'Name': 'Breakout Strategy', 'Objective': 'Capitalizing on price breakouts', 'Image': '/static/images/bs.jpg', 'Description': "Imagine a dam bursting; once the barrier is broken, water rushes through with force. Breakout traders aim to capitalize on significant price movements that occur when an asset breaches support or resistance levels. They wait for a breakout, where the price moves above resistance or below support, signaling a potential trend continuation. Breakout strategies are based on the premise that price movements tend to accelerate following a breakout, as traders rush to capitalize on the new trend. For example, if a stock's price breaks above a key resistance level, breakout traders might buy it, anticipating further upward movement. However, breakout trading carries inherent risks, including false breakouts and whipsaw movements, requiring traders to implement strict risk management measures."},
    {'Name': 'Swing Trading Strategy', 'Objective': 'Profiting from short- to medium-term price swings', 'Image': '/static/images/sw.jpg', 'Description': "Picture a pendulum swinging back and forth; swing traders aim to profit from the market's natural ebb and flow. They identify short- to medium-term price swings within a larger trend and capitalize on them. Swing traders typically hold positions for a few days to several weeks, buying at swing lows and selling at swing highs. Swing trading strategies are based on the premise that markets often exhibit periodic fluctuations within a broader trend, providing opportunities for short-term profits. For instance, if a stock's price experiences a short-term dip within an overall uptrend, a swing trader might buy it, expecting the price to bounce back as the trend resumes. However, swing trading requires discipline and patience, as traders must wait for opportune entry and exit points to maximize profitability."}
]

    # Paginate the courses
    paginator = Paginator(trading_strategies_info, 1)  # Show 1 strategy per page
    page = request.GET.get('page')
    try:
        trading_strategies_info = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        trading_strategies_info = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        trading_strategies_info = paginator.page(paginator.num_pages)

    return render(request, 'allcourses.html', {'trading_strategies_info': trading_strategies_info})















def company_portfolio(request, company_name):
    portfolio_returns_data = [0.05, 0.08, 0.1, 0.12, 0.15]
    asset_allocation_data = {'Stocks': 60, 'Bonds': 30, 'Cash': 10}
    market_trends_data = {'x': ['Jan', 'Feb', 'Mar'], 'y': [100, 150, 200]}
    # Dummy data for demonstration
    # Replace this with actual data retrieval logic for the selected company
    portfolio_returns_chart = plot([go.Scatter(x=list(range(len(portfolio_returns_data))), y=portfolio_returns_data, mode='lines', name='Portfolio Returns')], output_type='div')

    company_portfolio_data = {
        'Company A': {'Cumulative Returns': 0.25, 'Volatility': 0.15, 'Sharpe Ratio': 1.5, 'Max Drawdown': 0.1},
        'Company B': {'Cumulative Returns': 0.30, 'Volatility': 0.12, 'Sharpe Ratio': 1.6, 'Max Drawdown': 0.08},
        'Company C': {'Cumulative Returns': 0.20, 'Volatility': 0.18, 'Sharpe Ratio': 1.3, 'Max Drawdown': 0.12}
    }

    company_portfolio_metrics = company_portfolio_data.get(company_name, {})
    
    return render(request, 'company_portfolio.html', {'company_name': company_name,
                                                      'company_portfolio_metrics': company_portfolio_metrics,
                                                      'portfolio_returns_chart': portfolio_returns_chart})










# views.py


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # Return an 'invalid login' error message
                pass
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect back to the profile page after saving
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})



def preferences(request):
    if request.method == 'POST':
        form = PreferencesForm(request.POST)
        if form.is_valid():
            preferences = form.save(commit=False)
            preferences.user = request.user
            preferences.save()
            
            # Assign preferences to the user and save the user instance
            request.user.preferences = preferences
            request.user.save()
            
            return redirect('dashboard')  # Redirect to dashboard or any other page
    else:
        form = PreferencesForm()
    return render(request, 'preferences.html', {'form': form})

def update_preferences(request):
    try:
        preferences = Preferences.objects.get(user=request.user)
    except Preferences.DoesNotExist:
        return redirect('preferences')  # Redirect to create preferences if they don't exist

    if request.method == 'POST':
        form = PreferencesForm(request.POST, instance=preferences)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to dashboard or any other page
    else:
        form = PreferencesForm(instance=preferences)

    return render(request, 'update_preferences.html', {'form': form})


from django.shortcuts import render, redirect
from .models import ForumTopic, ForumComment
from .forms import ForumTopicForm, ForumCommentForm
import csv
from .forms import CsvUploadForm
def forum(request):
    topics = ForumTopic.objects.all()

    # Paginate the topics
    paginator = Paginator(topics, 5)  
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'forum.html', {'page_obj': page_obj})



def topic_detail(request, topic_id):
    topic = ForumTopic.objects.get(id=topic_id)
    comments = topic.forumcomment_set.all()
    if request.method == 'POST':
        form = ForumCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.topic = topic
            comment.save()
            return redirect('topic_detail', topic_id=topic_id)
    else:
        form = ForumCommentForm()
    return render(request, 'topic_detail.html', {'topic': topic, 'comments': comments, 'form': form})

def add_topic(request):
    if request.method == 'POST':
        topic_form = ForumTopicForm(request.POST)
        post_form = ForumCommentForm(request.POST)
        if topic_form.is_valid() and post_form.is_valid():
            topic = topic_form.save(commit=False)
            topic.user = request.user
            topic.save()
            post = post_form.save(commit=False)
            post.topic = topic
            post.user = request.user
            post.save()
            return redirect('forum')
    else:
        topic_form = ForumTopicForm()
        post_form = ForumCommentForm()
    return render(request, 'add_topic.html', {'topic_form': topic_form, 'post_form': post_form})

from django.db import IntegrityError

def add_from_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if csv_file.name.endswith('.csv'):
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                # Create or get the topic
                topic_name = row['Topic']
                try:
                    topic = ForumTopic.objects.create(topic=topic_name, user=request.user)
                except IntegrityError:  # Handle IntegrityError if user_id is not provided
                    topic = ForumTopic.objects.create(topic=topic_name)

                # Create the comment and associate it with the topic
                comment_text = row['Comment']
                comment = ForumComment(topic=topic, user=request.user, comment=comment_text)
                comment.save()

            return redirect('forum')  # Redirect to forum page after adding posts
    else:
        # If not a POST request or no CSV file provided, render the form
        form = CsvUploadForm()
    return render(request, 'add_from_csv.html', {'form': form})

from django.http import HttpResponse
from textblob import TextBlob
def sentiment_analysis(request):
    # Retrieve comments from the database
    comments = ForumComment.objects.all()

    # Perform sentiment analysis and store results
    data = []
    for comment in comments:
        sentiment_score = TextBlob(comment.comment).sentiment.polarity

        data.append({
            'Date': comment.created_at,
            'Name': comment.user.username,
            'Topic': comment.topic,
            'Comment': comment.comment,
            'Sentiment_Score': sentiment_score
        })

         # Paginate the data
    paginator = Paginator(data, 5) 
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'sentiment_analysis.html', {'page_obj': page_obj})

def download_csv(request):
    # Retrieve data for the CSV file (similar to what you did in the sentiment_analysis view)
    comments = ForumComment.objects.all()
    data = []

    for comment in comments:
        sentiment_score = TextBlob(comment.comment).sentiment.polarity
        # Add the comment data to the list
        data.append({
            'Date': comment.created_at,
            'Name': comment.user.username,
            'Topic': comment.topic.topic,
            'Comment': comment.comment,
            'Sentiment_Score': sentiment_score,
        })

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sentiment_analysis.csv"'

    # Write data to the CSV file
    writer = csv.DictWriter(response, fieldnames=['Date', 'Name', 'Topic', 'Comment', 'Sentiment_Score'])
    writer.writeheader()
    for row in data:
        writer.writerow(row)

    return response