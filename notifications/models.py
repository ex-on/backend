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
  # 4: Activity level notifications
  link_id = models.IntegerField(null=True)

  class Meta:
    managed = True
    db_table = 'notification'

class UserNotiReception(models.Model):
  user = models.ForeignKey('users.User', on_delete=models.CASCADE)

  exercise_attendance = models.BooleanField(default=True)
  daily_exercise_complete = models.BooleanField(default=True)
  weekly_exercise_protein = models.BooleanField(default=True)
  hot_post = models.BooleanField(default=True)
  hot_qna = models.BooleanField(default=True)
  qna_best_answer = models.BooleanField(default=True)
  qna_selected_answer = models.BooleanField(default=True)
  activity_level_up = models.BooleanField(default=True)

  post_comment = models.BooleanField(default=True)
  post_reply = models.BooleanField(default=True)

  qna_answer = models.BooleanField(default=True)
  qna_comment = models.BooleanField(default=True)
  qna_reply = models.BooleanField(default=True)

  general = models.BooleanField(default=True)

  class Meta:
    managed = True
    db_table = 'user_noti_reception'