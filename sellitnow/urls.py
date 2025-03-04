from django.contrib import admin
from django.urls import path, include
from app.views import HomeView, LobbyView, ProductCreateView, AdminDashboardView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),  # Default home page
    path('admin/', admin.site.urls),  # Django admin panel
    path('lobby/', LobbyView.as_view(), name='lobby'),  # Lobby view for products
    path('add-product/', ProductCreateView.as_view(), name='add_product'),  # Product creation page
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),  # Admin dashboard
    
    # Authentication URLs
    path('accounts/', include('allauth.urls')),  # Django Allauth for authentication
]
