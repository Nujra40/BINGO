from django.urls import path
from . import views

app_name = 'game'
urlpatterns = [
    path('start/<str:me>/<str:oppo>', views.start, name='start'),
    path('processGameState/', views.processGameState, name='processGameState'),
    path('refGame/<str:me>/<str:oppo>', views.refGame, name="refGame")
]