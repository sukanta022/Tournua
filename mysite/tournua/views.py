from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import UserAccount, Tournament, Team, Match
from .forms import SignupForm
from django.views.decorators.cache import never_cache
from django.utils import timezone
import itertools

def signup_save(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})




def login_view(request):
    error = None
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if user exists
        user_obj = UserAccount.objects.filter(email=email, password=password).first()

        if user_obj:
            request.session["user_id"] = user_obj.id
            return redirect("dashboard")
        else:
            error = "Invalid email or password!"

    return render(request, "login.html", {"error": error})



@never_cache
def dashboard(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    try:
        user = UserAccount.objects.get(id=user_id)
        name = user.full_name.split(" ")[0]
    except UserAccount.DoesNotExist:
        return redirect("login")

    return render(request, "demo.html", {"name": name})


def logout_view(request):
    # Clear all session data
    request.session.flush()  # This removes all session data
    return redirect("home")



def create_tournament(request):
    if request.method == "POST":
        name = request.POST.get("tournament_name")
        description = request.POST.get("tournament_descriptions")
        trophy = request.FILES.get("trophy")  # you’ll need to update HTML to allow trophy upload
        t_type = request.POST.get("select_type")
        player_type = request.POST.get("player_type")
        format_choice = request.POST.get("format")
        groups = request.POST.get("select_group")
        teams_per_group = request.POST.get("team_num")

        # Save tournament
        tournament = Tournament.objects.create(
            name=name,
            description=description,
            trophy=trophy,
            tournament_type=t_type,
            player_type=player_type,
            format=format_choice,
            num_groups=groups,
            teams_per_group=teams_per_group,
        )

        # Save teams
        for i in range(1, 9):  # 8 teams
            team_name = request.POST.get(f"team{i}")
            team_logo = request.FILES.get(f"team{i}_logo")
            if team_name:  # only save if team entered
                Team.objects.create(
                    tournament=tournament,
                    name=team_name,
                    logo=team_logo
                )
        if format_choice.lower() == "league":
            num_matches = generate_league_fixtures(tournament)
            print(f"{num_matches} matches created for tournament '{tournament.name}'")

        return redirect("dashboard")  # redirect after success

    return render(request, "tournament_form.html")






def generate_league_fixtures(tournament):
    teams = list(tournament.teams.all())

    # Clear previous matches if any
    tournament.matches.all().delete()

    fixtures = []
    # Generate all possible pairs of teams
    for team1, team2 in itertools.combinations(teams, 2):
        # Each pair plays twice (home & away)
        fixtures.append(Match(tournament=tournament, team1=team1, team2=team2))
        fixtures.append(Match(tournament=tournament, team1=team2, team2=team1))

    # Bulk create all matches in DB
    Match.objects.bulk_create(fixtures)
    return f"{len(fixtures)} matches created for tournament '{tournament.name}'"

