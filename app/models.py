import shortuuid
from django.db import models

class Noeud(models.Model):
    id = models.CharField(primary_key=True, max_length=22, default=shortuuid.uuid)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Lampe(models.Model):
    id = models.CharField(primary_key=True, max_length=22, default=shortuuid.uuid)
    name = models.CharField(max_length=100)
    puissance = models.IntegerField() 
    noeud = models.ForeignKey(Noeud, on_delete=models.CASCADE, related_name='lampes')

    def __str__(self):
        return f"{self.name} - {self.puissance}W - {self.noeud.name}"

class Planification(models.Model):
    id = models.CharField(primary_key=True, max_length=22, default=shortuuid.uuid)
    lampe = models.ForeignKey(Lampe, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    

    def __str__(self):
        return f"{self.lampe.name} - {self.lampe.noeud.name}"
