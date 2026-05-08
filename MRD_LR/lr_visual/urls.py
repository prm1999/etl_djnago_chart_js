from django.urls import path

from . import views
from .views import home

app_name = 'lr_visual'

urlpatterns = [
    path("", views.home, name="home"),
    path("drop_down/", views.drop_down, name="drop_down"),  # drop down url
    path("pie_chart/", views.pie_chart, name="pie_chart"),  # pie chart url
    path("drill_down/", views.drill_down, name="drill_down"),# drill down url
    path("hue_one/", views.hue_one, name="hue_one"),# drill down url
    path("hue_two/", views.hue_two, name="hue_two"),  # drill down url

]
