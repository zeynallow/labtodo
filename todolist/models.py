from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class TodoList(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title


class TodoListShare(models.Model):
    task = models.ForeignKey(TodoList,on_delete=models.CASCADE, related_name='tasks',db_index=True)
    shared_user = models.ForeignKey(User,on_delete=models.CASCADE)
    share_type = models.IntegerField()

    def __str__(self):
        return self.task


class Comment(models.Model):
    task = models.ForeignKey(TodoList,on_delete=models.CASCADE, related_name='comments')
    handle = models.TextField()
    comment = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
