from django.db import models

class Noeud(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Lampe(models.Model):
    name = models.CharField(max_length=100)
    puissance = models.IntegerField()  # Assuming this is the power of the lamp
    noeud = models.ForeignKey(Noeud, on_delete=models.CASCADE, related_name='lampes')

    def __str__(self):
        return f"{self.name} - {self.puissance}W"
