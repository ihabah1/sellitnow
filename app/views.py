from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import GameScore, Game

# -------------------------------
# User Dashboard
# -------------------------------
@login_required
def user_dashboard(request):
    total_points = GameScore.total_score_for_user(request.user)
    recent_scores = GameScore.objects.filter(user=request.user).order_by('-played_at')[:5]
    return render(request, 'account/dashboard.html', {
        'total_points': total_points,
        'game_scores': recent_scores
    })


# -------------------------------
# Game Lobby (Choose Game)
# -------------------------------
class LobbyView(LoginRequiredMixin, View):  # LoginRequiredMixin ensures login requirement for class-based views
    def get(self, request):
        games = Game.objects.all()
        return render(request, 'app/lobby.html', {'games': games})


# -------------------------------
# Save Score (POST)
# -------------------------------
@login_required
def submit_score(request):
    if request.method == "POST":
        game_name = request.POST.get("game_name")
        score = int(request.POST.get("score", 0))
        # Create or update GameScore for user
        GameScore.objects.create(user=request.user, game_name=game_name, score=score)
        messages.success(request, "Your score has been saved!")
        return redirect('user_dashboard')  # Assuming you want to redirect to the user dashboard after submitting score
    return redirect('lobby')


# -------------------------------
# Play Game Views
# -------------------------------
@login_required
def play_ping_pong(request):
    return render(request, 'games/ping_pong.html')


@login_required
def play_tetris(request):
    return render(request, 'games/tetris.html')


# -------------------------------
# Home Page
# -------------------------------
class HomeView(View):
    def get(self, request):
        return render(request, 'app/index.html')
