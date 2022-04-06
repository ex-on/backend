from django.db import models

# Create your models here.
class Notification(models.Model):
  user = models.ForeignKey('users.User', on_delete=models.CASCADE)
  title = models.CharField(max_length=30)
  body = models.CharField(max_length=50)
  created_at = models.DateTimeField(auto_now_add=True)
  read = models.BooleanField(default=False)
  type = models.IntegerField()
  # 0: General notifications
  # 1: Exercise notifications
  # 2: Post notifications
  # 3: Q&A notifications
  link_id = models.IntegerField(null=True)

  class Meta:
    managed = True
    db_table = 'notification'
