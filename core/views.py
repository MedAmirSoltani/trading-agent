# views.py

from django.shortcuts import render, redirect
import plotly.graph_objs as go
from plotly.offline import plot
from .models import Preferences

from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm,CustomUserChangeForm,PreferencesForm

def home(request):
    return render(request, 'home.html')
def how(request):
    return render(request, 'how.html')
def about(request):
    return render(request, 'about.html')



def dashboard(request):
 if Preferences.objects.filter(user=request.user).exists():
    # Dummy data for demonstration
    portfolio_returns_data = [0.05, 0.08, 0.1, 0.12, 0.15]
    asset_allocation_data = {'Stocks': 60, 'Bonds': 30, 'Cash': 10}
    market_trends_data = {'x': ['Jan', 'Feb', 'Mar'], 'y': [100, 150, 200]}
    
    # Line chart for portfolio returns over time
    portfolio_returns_chart = plot([go.Scatter(x=list(range(len(portfolio_returns_data))), y=portfolio_returns_data, mode='lines', name='Portfolio Returns')], output_type='div')

    # Pie chart for asset allocation
    asset_allocation_chart = plot([go.Pie(labels=list(asset_allocation_data.keys()), values=list(asset_allocation_data.values()))], output_type='div')

    # Bar chart for market trends
    market_trends_chart = plot([go.Bar(x=market_trends_data['x'], y=market_trends_data['y'])], output_type='div')

    return render(request, 'dashboard.html', {'portfolio_returns_chart': portfolio_returns_chart,
                                               'asset_allocation_chart': asset_allocation_chart,
                                               'market_trends_chart': market_trends_chart})
 else:
        # If preferences are not registered, redirect to the preferences page
        return redirect('preferences')

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







def market_insights(request):
    company_names = ['Company A', 'Company B', 'Company C']
    # Dummy data for demonstration
    market_indicators = ['GDP Growth', 'Unemployment Rate', 'Inflation Rate']
    news_sentiment = {'Positive': 0.6, 'Neutral': 0.3, 'Negative': 0.1}

    return render(request, 'market_insights.html', {'market_indicators': market_indicators,
                                                    'company_names': company_names,
                                                    
                                                    'news_sentiment': news_sentiment})




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




