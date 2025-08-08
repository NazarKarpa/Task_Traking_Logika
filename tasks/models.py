from django.db import models
from django.contrib.auth.models import User
from django.db.models import ManyToManyField


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progres', 'In Progress'),
        ('done', 'Done')
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    title = models.CharField(max_length=256)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'tasks')
    members = models.ManyToManyField(User, blank=True, related_name='assigned_tasks')

    def __str__(self):
        return f'Title: {self.title}'

class Comment(models.Model):
    text = models.TextField()
    comment_to_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    media = models.FileField(upload_to='comments_media/', blank=True, null=True)


    def __str__(self):
        return f'comment: {self.comment_to_task}'


    def get_absolute_url(self):
        return self.comment_to_task.get_absolute_url()


class Project(models.Model):
    pass
