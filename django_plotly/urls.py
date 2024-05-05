# trading_agent/urls.py
from django.urls import path, include  # make sure include is imported
from django.urls import path
from django.contrib.auth.views import LogoutView
from core.views import loading,chat_interface,sector_details,company_details,download_csv,sentiment_analysis,topic_detail,add_topic,add_from_csv,forum,dashboard,portfolio_analysis,trading_strategies,market_insights,company_portfolio,home,about,how,register,user_login,profile,preferences,update_preferences,allcourses
urlpatterns = [
    path('', include('pwa.urls')),  # Add this line
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
    path('forum/', forum, name='forum'),
    path('topic/<int:topic_id>/', topic_detail, name='topic_detail'),
    path('add_topic/', add_topic, name='add_topic'),
    path('add_from_csv/', add_from_csv, name='add_from_csv'),
    path('sentiment_analysis/', sentiment_analysis, name='sentiment_analysis'),
    path('download_csv/', download_csv, name='download_csv'),
     path('loading/', loading, name='loading'),
    path('sector_details/<str:sector_name>/', sector_details, name='sector_details'),
    path('company_details/<str:company_name>/', company_details, name='company_details'),
    path('chat/', chat_interface, name='chat'),

    path('', user_login, name='login'),
    path('company_portfolio/<str:company_name>/', company_portfolio, name='company_portfolio'),
]
