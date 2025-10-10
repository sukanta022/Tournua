from django.shortcuts import render, redirect, get_object_or_404
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

    user = UserAccount.objects.get(id=user_id)
    name = user.full_name.split(" ")[0]

    # Tournaments user created
    own_tournaments = Tournament.objects.filter(user=user)

    # Tournaments user joined (excluding own)
    joined_tournaments = Tournament.objects.filter(participants=user).exclude(user=user)

    tournaments = own_tournaments | joined_tournaments
    tournaments = tournaments.order_by('-created_at')

    return render(request, "demo.html", {
        "name": name,
        "tournaments": tournaments,
        "user": user
    })

def join_tournament(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    user = UserAccount.objects.get(id=user_id)
    error = None

    if request.method == "POST":
        code = request.POST.get("tournament_code").strip().upper()
        try:
            tournament = Tournament.objects.get(code=code)

            if tournament.user == user:
                error = "You cannot join your own tournament."
            elif tournament.participants.filter(id=user.id).exists():
                error = "You already joined this tournament."
            else:
                tournament.participants.add(user)
                return redirect("dashboard")  # success

        except Tournament.DoesNotExist:
            error = "Invalid tournament code."

    # **Fetch created tournaments + joined tournaments**
    created_tournaments = Tournament.objects.filter(user=user).order_by('-created_at')
    joined_tournaments = Tournament.objects.filter(participants=user).exclude(user=user).order_by('-created_at')

    # Combine into one list (optional: keep separate in template)
    tournaments = list(created_tournaments) + list(joined_tournaments)

    return render(request, "demo.html", {
        "error": error,
        "tournaments": tournaments,
        "user": user,
        "name": user.full_name.split(" ")[0]
    })


def logout_view(request):
    # Clear all session data
    request.session.flush()  # This removes all session data
    return redirect("home")



def create_tournament(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        user = UserAccount.objects.get(id=user_id)
        name = request.POST.get("tournament_name")
        description = request.POST.get("tournament_descriptions")
        trophy = request.POST.get("trophy")  # you’ll need to update HTML to allow trophy upload
        t_type = request.POST.get("select_type")
        player_type = request.POST.get("player_type")
        format_choice = request.POST.get("format")
        groups = request.POST.get("select_group")
        teams_per_group = request.POST.get("team_num")

        # Save tournament
        tournament = Tournament.objects.create(
            user=user,
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



def tournament_view(request, tournament_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    user = get_object_or_404(UserAccount, id=user_id)
    tournament = get_object_or_404(Tournament, id=tournament_id)
    matches = Match.objects.filter(tournament=tournament).select_related('team1', 'team2').order_by('created_at')

    # Check if current user is the creator
    is_creator = tournament.user == user

    context = {
        'tournament': tournament,
        'matches': matches,
        'user': user,
        'is_creator': is_creator
    }
    return render(request, 'view.html', context)




# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Match

def update_match_score(request):
    if request.method == "POST":
        match_id = request.POST.get("match_id")
        team1_score = request.POST.get("team1_score")
        team2_score = request.POST.get("team2_score")

        # Validate input
        try:
            team1_score = int(team1_score)
            team2_score = int(team2_score)
        except (ValueError, TypeError):
            messages.error(request, "Please enter valid integer scores.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Get the match
        match = get_object_or_404(Match, id=match_id)

        # Update scores and mark as played
        match.team1_score = team1_score
        match.team2_score = team2_score
        match.played = True
        match.save()

        messages.success(request, f"Scores updated for {match.team1.name} vs {match.team2.name}")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # If someone tries GET request
    return redirect('/')


from django.shortcuts import render, get_object_or_404
from .models import Tournament, Match, Team

def leaderboard(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    matches = Match.objects.filter(tournament=tournament, played=True)
    teams = Team.objects.filter(tournament=tournament)  # all teams in tournament

    # Initialize standings for all teams
    standings = {}
    for team in teams:
        standings[team.id] = {
            "team": team,
            "MP": 0,
            "W": 0,
            "D": 0,
            "L": 0,
            "GS": 0,
            "GC": 0,
            "Pts": 0,
            "played": False  # track if played at least one match
        }

    # Update stats for played matches
    for match in matches:
        t1 = match.team1
        t2 = match.team2
        s1 = match.team1_score
        s2 = match.team2_score

        standings[t1.id]["MP"] += 1
        standings[t2.id]["MP"] += 1
        standings[t1.id]["GS"] += s1
        standings[t1.id]["GC"] += s2
        standings[t2.id]["GS"] += s2
        standings[t2.id]["GC"] += s1

        standings[t1.id]["played"] = True
        standings[t2.id]["played"] = True

        if s1 > s2:
            standings[t1.id]["W"] += 1
            standings[t2.id]["L"] += 1
            standings[t1.id]["Pts"] += 3
        elif s1 < s2:
            standings[t2.id]["W"] += 1
            standings[t1.id]["L"] += 1
            standings[t2.id]["Pts"] += 3
        else:
            standings[t1.id]["D"] += 1
            standings[t2.id]["D"] += 1
            standings[t1.id]["Pts"] += 1
            standings[t2.id]["Pts"] += 1

    # Convert to list
    leaderboard = list(standings.values())

    # Sort: first played teams by Pts->GD->GS, then unplayed teams at the bottom
    played_teams = [t for t in leaderboard if t["played"]]
    unplayed_teams = [t for t in leaderboard if not t["played"]]

    # Sort played teams
    played_teams.sort(key=lambda x: (x["Pts"], x["GS"] - x["GC"], x["GS"]), reverse=True)

    # Combine: played first, unplayed at bottom
    leaderboard = played_teams + unplayed_teams

    # Assign position and format values
    for i, row in enumerate(leaderboard, start=1):
        row["P"] = i
        # For unplayed teams, set all numeric stats to "-"
        if not row["played"]:
            for key in ["MP", "W", "D", "L", "GS", "GC", "Pts"]:
                row[key] = "-"

    return render(request, "leaderboard.html", {
        "tournament": tournament,
        "leaderboard": leaderboard
    })


from django.utils import timezone
def update_match_date(request):
    if request.method == "POST":
        match_id = request.POST.get("match_id")
        match_date = request.POST.get("match_date")

        if not match_date:
            messages.error(request, "Please select a valid date and time.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        match = get_object_or_404(Match, id=match_id)

        try:
            # Convert string to datetime
            from datetime import datetime
            match.match_date = datetime.strptime(match_date, "%Y-%m-%dT%H:%M")
            match.save()
            messages.success(request, f"Match date updated for {match.team1.name} vs {match.team2.name}")
        except ValueError:
            messages.error(request, "Invalid date format. Please try again.")

        return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect('/')









