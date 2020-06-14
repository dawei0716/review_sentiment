from django.urls import path
from . import views 

app_name = 'analyze_app'
urlpatterns = [
    path('', views.analyze,  name ='analyze_app'),
    path('analyze/', views.analyze_review, name='request_analysis'),
    path('results/', views.view_results, name='results'),
    path('about/', views.about_page, name='about'),
]