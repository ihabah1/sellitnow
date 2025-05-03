from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

from .models import GameScore, Game

# -------------------------------
# User Dashboard
# -------------------------------
@login_required
def user_dashboard(request):
    game_scores = GameScore.objects.filter(user=request.user).order_by('-played_at')
    total_points = game_scores.aggregate(Sum('score'))['score__sum'] or 0
    return render(request, 'app/profile.html', {
        'game_scores': game_scores,
        'total_points': total_points
    })

# -------------------------------
# Game Lobby
# -------------------------------
class LobbyView(LoginRequiredMixin, View):
    def get(self, request):
        games = Game.objects.all()
        return render(request, 'app/lobby.html', {'games': games})

# -------------------------------
# Submit Score (Legacy POST)
# -------------------------------
@login_required
def submit_score(request):
    if request.method == "POST":
        game_name = request.POST.get("game_name")
        score = int(request.POST.get("score", 0))
        game, _ = Game.objects.get_or_create(name=game_name)
        GameScore.objects.create(user=request.user, game=game, score=score)
        messages.success(request, "Your score has been saved!")
        return redirect('user_dashboard')
    return redirect('lobby')

# -------------------------------
# Game Views
# -------------------------------
@login_required
def play_ping_pong(request):
    return render(request, 'games/ping_pong.html')

@login_required
def play_galaxy_shooter(request):
    return render(request, 'games/galaxy_shooter.html')

# -------------------------------
# API Endpoint: Update Points
# -------------------------------
@csrf_exempt
@login_required
def update_points(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            points = int(data.get("points", 0))
            user = request.user

            game, _ = Game.objects.get_or_create(name="Ping Pong", defaults={"max_score": 3})
            GameScore.objects.create(user=user, game=game, score=points)

            total = GameScore.objects.filter(user=user).aggregate(Sum('score'))['score__sum'] or 0
            return JsonResponse({"success": True, "total_score": total})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)

# -------------------------------
# Home Page
# -------------------------------
class HomeView(View):
    def get(self, request):
        return render(request, 'app/index.html')
