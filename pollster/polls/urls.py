# polls/urls.py

from django.urls import path
from . import views


app_name = 'polls'  # Set an application namespace

urlpatterns = [
    path('', views.index, name='index'),
   
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    path('external-data/', views.external_data_view, name='external-data'),
]
