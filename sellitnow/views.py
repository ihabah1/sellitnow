from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to SellItNow!</h1>")
from django.shortcuts import render



@method_decorator(login_required, name='dispatch')
class LobbyView(View):
    """Lobby view that shows all available rooms"""
    def get(self, request):
        rooms = Room.objects.all()  # Fetch all rooms
        return render(request, 'app/lobby.html', {'rooms': rooms})


def create_room(request):
    return render(request, "app/create_room.html")

def join_room(request, room_name):  # Accept room_name as argument
    return render(request, "app/join_room.html", {"room_name": room_name})
