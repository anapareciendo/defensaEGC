"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from principal.models import *
from principal.views import busca_votaciones

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
        
#    def test_poll(self):
#        """
#        Test that the Poll is correctly created and saved in DB
#        """
#        ca = Ca.objects.create(id=1312, name="Josemita")
#        census = Census.objects.create(id=1222, title="Jos", postalCode=11510, ca=ca)
#        poll = Poll.objects.create(id=1312, title="Prueba", description="Votacion de prueba", startDate="2017-01-13", endDate="2018-01-10",census=census, participantes=0, votos=0)
#        self.assertEqual(poll.id, 1312)
        
    def test_busca_votaciones(self):
       
        bv = busca_votaciones()
        
        res = 1
        if(len(bv) == 0):
            res=0
            
        self.assertEqual(res,1)
        
