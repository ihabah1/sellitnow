from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product, Room  # Added Room model import
from .forms import ProductForm, RoomForm  # Added RoomForm import
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Import this!
from .models import Room





@login_required
def create_room(request):
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        
        if not room_name:
            messages.error(request, "Room name is required.")
            return redirect("create_room")

        # Check if room already exists
        if Room.objects.filter(name=room_name).exists():
            messages.error(request, "Room name already taken. Try another.")
            return redirect("create_room")

        # Save new room
        room = Room.objects.create(name=room_name, created_by=request.user)
        messages.success(request, f"Room '{room.name}' created successfully!")
        return redirect("lobby")  # Redirect to lobby after success

    return render(request, "app/create_room.html")

@login_required
def join_room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    return render(request, "app/room.html", {"room": room})

def get(self, request):
    rooms = Room.objects.all()
    print("Rooms:", rooms)  # Debugging: Check if rooms are passed
    return render(request, 'app/lobby.html', {'rooms': rooms})


@method_decorator(login_required, name='dispatch')
class LobbyView(View):
    """Lobby view that shows all available rooms"""
    def get(self, request):
        rooms = Room.objects.all()  # Ensure this retrieves all rooms
        return render(request, 'app/lobby.html', {'rooms': rooms})

class HomeView(View):
    """ Default homepage view """
    def get(self, request):
        return render(request, 'app/index.html')


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
