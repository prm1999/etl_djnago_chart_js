from django.urls import path
from . import views

app_name = 'lr_visual'

urlpatterns = [
    path('', views.home, name='home'),
    path('explorer/', views.drop_down, name='drop_down'),
    path('distribution/', views.pie_chart, name='pie_chart'),
    path('drill-down/', views.drill_down, name='drill_down'),
    path('defaulters/', views.hue_one, name='hue_one'),
    path('zone-analysis/', views.hue_two, name='hue_two'),
    path('hue-three/', views.hue_three, name='hue_three'),
]
