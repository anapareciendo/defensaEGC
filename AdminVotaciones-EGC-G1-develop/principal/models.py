from django.db import models
from django.template.defaultfilters import default

class Ca(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    class Meta:
        db_table = 'ca'
    def __unicode__(self):
        return self.name

class Census(models.Model):
    id = models.IntegerField(unique=True, primary_key=True, null=False)
    title = models.CharField(max_length=100, null=False)
    postalCode = models.IntegerField(null=True, blank=True, db_column='postalCode')
    ca = models.ForeignKey(Ca)
    class Meta:
        db_table = 'census'
    def __unicode__(self):
        return self.title
    
class Poll(models.Model):
    id = models.IntegerField(unique=True, primary_key=True, null=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=500, null=False)
    startDate = models.DateField(null=False, db_column='startDate')
    endDate = models.DateField(null=False, db_column='endDate') 
    census = models.ForeignKey(Census)
    participantes = models.IntegerField(null=False, default=0, db_column='participantes_admitidos')
    votos = models.IntegerField(null=False, default=0, db_column='votos_actuales')
    class Meta:
        db_table = 'poll'
    def __unicode__(self):
        return self.title

class Question(models.Model):
    id = models.IntegerField(unique=True, null=False, primary_key=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=True)
    optional = models.BooleanField()
    multiple = models.BooleanField()
    poll = models.ForeignKey(Poll)
    class Meta:
        db_table = 'question'
    def __unicode__(self):
        return self.title

class Option(models.Model):
    id = models.IntegerField(unique=True, null=False, primary_key=True)
    description = models.CharField(max_length=500, null=False, blank=True)
    question = models.ForeignKey(Question)
    class Meta:
        db_table = 'question_option'
    def __unicode__(self):
        return self.description

class UserAccount(models.Model):
    id = models.IntegerField(unique=True, null=False, primary_key=True)
    username = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=50, null=False)
    email= models.CharField(max_length=100, null=False)
    role = models.IntegerField(unique=True, null=False, primary_key=True, db_column='role_id')

    class Meta:
        db_table = 'user_account'
    def __unicode__(self):
        return self.username

class User(models.Model):
    id = models.IntegerField(unique=True, null=False, primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    ca = models.ForeignKey(Ca)
    useraccount = models.ForeignKey(UserAccount, db_column='user_account_id')
    
    class Meta:
        db_table = 'user'
    def __unicode__(self):
        return self.name

class UserPerCensus(models.Model):
    id = models.IntegerField(unique=True, null=False, primary_key=True)
    census = models.ForeignKey(Census)
    useraccount = models.ForeignKey(UserAccount, db_column='user_account_id')

    class Meta:
        db_table = 'user_account_per_census'
    def __unicode__(self):
        return self.id
