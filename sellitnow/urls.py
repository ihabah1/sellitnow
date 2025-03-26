from django.contrib import admin
from django.urls import path, include
from app.views import (
    HomeView,
    LobbyView,
    ProductCreateView,
    AdminDashboardView,
    create_room,
    join_room,
)

urlpatterns = [
    path('', HomeView.as_view(), name='index'),  # Default home page
    path('admin/', admin.site.urls),  # Django admin panel
    path('lobby/', LobbyView.as_view(), name='lobby'),  # Lobby view for products
    path('add-product/', ProductCreateView.as_view(), name='add_product'),  # Product creation page
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),  # Admin dashboard
    
    # Room URLs
    path('create-room/', create_room, name='create_room'),
    path("join-room/<str:room_name>/", join_room, name="join_room"),  # Accepts a room name


    # Authentication URLs
    path('accounts/', include('allauth.urls')),  # Django Allauth for authentication
]
