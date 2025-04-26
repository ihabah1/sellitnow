from django.contrib import admin
from django.urls import path, include
from app.views import (
    HomeView,
    LobbyView,
    play_ping_pong,
    play_tetris,
    submit_score,
    user_dashboard,
    update_points
)

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('admin/', admin.site.urls),

    # Profile page
    path('profile/', user_dashboard, name='profile'),


    # Game lobby & play
    path('lobby/', LobbyView.as_view(), name='lobby'),
    path('play/ping-pong/', play_ping_pong, name='play_ping_pong'),
    path('play/tetris/', play_tetris, name='play_tetris'),
    path('submit-score/', submit_score, name='submit_score'),
    path("api/update-points/", update_points, name="update_points"),
    # Auth
    path('accounts/', include('allauth.urls')),
]
