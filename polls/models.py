import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin

# each model is represented by a class that subclasses django.db.models.Model.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    end_date = models.DateTimeField("due date")
    is_due = models.BooleanField(default=False)
    # for this object's representation
    def __str__(self):
        return self.question_text
    # sort the column header for was_published_recently in admin page
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    # self is for instance method; This allows the method to access the instance's attributes and other methods
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    def is_due(self):
        now = timezone.now()
        if now <= self.end_date:
            self.is_due = True


class Choice(models.Model):
    # to change default related manager name 'choice_set', define 'related_name'
    # question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    is_most_voted = models.BooleanField(default=False)
    def __str__(self):
        return self.choice_text
    @classmethod
    def most_voted(cls, question_id):
        # access the Question's primary key directly via the question_id attribute of the Choice model. This attribute is automatically created by Django for the ForeignKey field
        choices = cls.objects.filter(question_id=question_id)
        if not choices.exists():
            return None
        # the hyphen (-) before a field name in the order_by method indicates descending order
        most_voted_choice = choices.order_by('-votes').first()

        choices.update(is_most_voted=False)
        most_voted_choice.is_most_voted = True
        most_voted_choice.save()



