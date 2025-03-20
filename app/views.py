from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product
from .forms import ProductForm

class HomeView(View):
    """ Default homepage view """
    def get(self, request):
        return render(request, 'app/index.html')

@method_decorator(login_required, name='dispatch')
class LobbyView(View):
    """ Lobby view that shows all listed products """
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'app/lobby.html', {'products': products})

class ProductCreateView(LoginRequiredMixin, View):
    """ View to create a new product listing """
    login_url = 'account_login'  # Redirects users to login if not authenticated

    def get(self, request):
        form = ProductForm()
        return render(request, 'app/add_product.html', {'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('lobby')
        return render(request, 'app/add_product.html', {'form': form})

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    """ Admin dashboard view """
    login_url = 'account_login'

    def test_func(self):
        return self.request.user.is_staff  # Only allow staff users

    def get(self, request):
        if not self.request.user.is_staff:
            return redirect('lobby')  # Redirect non-admin users
        products = Product.objects.all()
        return render(request, 'app/admin_dashboard.html', {'products': products})