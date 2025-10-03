from django.db import models



class UserAccount(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # will store hashed password

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class Tournament(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    trophy = models.ImageField(upload_to="trophies/", blank=True, null=True)
    tournament_type = models.CharField(max_length=50, choices=[("online", "Online"), ("offline", "Offline")])
    player_type = models.CharField(max_length=50, choices=[("single", "Single"), ("team", "Team")])
    format = models.CharField(max_length=50, choices=[("Knockout", "Knockout"), ("League", "League")])
    num_groups = models.IntegerField(default=2)
    teams_per_group = models.IntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="teams")
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="team_logos/", blank=True, null=True)

    def __str__(self):
        return self.name