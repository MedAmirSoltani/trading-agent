# trading_agent/urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from core.views import dashboard,portfolio_analysis,trading_strategies,market_insights,company_portfolio,home,about,how,register,user_login,profile,preferences,update_preferences,allcourses
urlpatterns = [
    path('home/', home, name='home'),
    path('preferences/', preferences, name='preferences'),
    path('update_preferences/', update_preferences, name='update_preferences'),
    path('about/', about, name='about'),
    path('how/', how, name='how'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('portfolio-analysis/', portfolio_analysis, name='portfolio_analysis'),
    path('trading-strategies/', trading_strategies, name='trading_strategies'),
    path('market-insights/', market_insights, name='market_insights'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
        path('allcourses/', allcourses, name='allcourses'),

    path('', user_login, name='login'),
    path('company_portfolio/<str:company_name>/', company_portfolio, name='company_portfolio'),
]
