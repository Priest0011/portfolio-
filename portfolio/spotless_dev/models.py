from django.db import models

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web Design'),
        ('app', 'App Development'),
        ('ecom', 'E-Commerce'),
        ('uiux', 'UI/UX Design'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    technologies = models.CharField(max_length=255, help_text="Comma-separated tech stack (e.g. Django, React, Firebase)")
    image = models.ImageField(upload_to='portfolio/')
    project_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_technologies_list(self):
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]

    def __str__(self):
        return self.title

class Skill(models.Model):
    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(help_text="Enter a value from 1 to 100")

    def __str__(self):
        return self.name
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
    
class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, default="Spotless")
    image = models.ImageField(upload_to='blog/')
    content = models.TextField()
    summary = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class About(models.Model):
    image = models.ImageField(upload_to='about/')