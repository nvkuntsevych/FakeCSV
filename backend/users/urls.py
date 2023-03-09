from django.urls import path

from users.views import LoginUserView


urlpatterns = [
    path('login/', LoginUserView.as_view()),
]
