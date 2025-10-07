from django.db import models
import random
import string


class UserAccount(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # will store hashed password

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class Tournament(models.Model):
    code = models.CharField(max_length=8, unique=True, editable=False)
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

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_code():
        """Generate a unique 6-character alphanumeric code."""
        from .models import Tournament  # avoid circular import
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not Tournament.objects.filter(code=code).exists():
                return code


class Team(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="teams")
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="team_logos/", blank=True, null=True)

    def __str__(self):
        return self.name