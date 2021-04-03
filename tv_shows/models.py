from django.db import models
import re, datetime

class ShowManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['title']) < 2 or postData['title'] == None:
            errors["title"] = "Show title should be at least 2 characters"
        if len(postData['network']) < 2 or postData['network'] == None:
            errors["network"] = "Network name should be at least 2 characters"
        if len(postData['description']) != 0:
            if len(postData['description']) < 10:
                errors["description"] = "Description is optional: should be at least 10 characters"
        # print(postData['release'])
        # print(errors)        
        try:
            datetime.datetime.strptime(postData['release'], '%Y-%m-%d')
        except ValueError:
            errors['release'] = "Please enter a valid date"
        return errors
        
# =====================FROM SOLUTION ==============================
class ShowManagerSol(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['title']) < 2:
            errors['title'] = 'Title field should be at least 2 characters'
        if len(form['network']) < 3:
            errors['network'] = 'Network field should be at least 3 characters'
        if form['description'] != '' and len(form['description']) < 10:
            errors['description'] = 'Description should be at least 10 characters'
        if datetime.strptime(form['release_date'], '%Y-%m-%d') > datetime.now():
            errors['release_date'] = 'Release Date should be in the past'
        return errors
#=================================================================================

class Network(models.Model):
    name = models.CharField(max_length=255)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Show(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    release_date = models.DateTimeField()
    network = models.ForeignKey(Network, related_name='shows', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()

