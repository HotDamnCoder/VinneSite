from django.db import models
from .elements import Element as ele


class Element(models.Model):
    number = models.IntegerField()
    symbol = models.CharField(max_length=3)
    est_name = models.TextField()
    name = models.TextField()
    group = models.IntegerField()
    period = models.IntegerField()
    block = models.CharField(max_length=3)
    protons = models.IntegerField()
    neutrons = models.IntegerField()
    electrons = models.IntegerField()
    mass = models.FloatField()
    eleneg = models.FloatField()
    tboil = models.FloatField()
    tmelt = models.FloatField()
    density = models.FloatField()
    oxistates = models.TextField()
    atmrad = models.FloatField()

    def add_info(self, element: ele):
        self.number = element.number
        self.symbol = element.symbol
        self.name = element.name
        self.group = element.group
        self.period = element.period
        self.block = element.block
        self.protons = element.protons
        self.neutrons = element.neutrons
        self.electrons = element.electrons
        self.mass = element.mass
        self.eleneg = element.eleneg
        self.tboil = element.tboil
        self.tmelt = element.tmelt
        self.density = element.density
        self.oxistates = element.oxistates
        self.atmrad = element.atmrad
