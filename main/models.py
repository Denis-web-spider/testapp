from django.db import models

class Tests(models.Model):

    test_name = models.CharField(max_length=100)
    test_text = models.TextField(default='')

    def __str__(self):
        return self.test_name

class Questions(models.Model):

    question_text = models.CharField(max_length=255)
    test = models.ForeignKey(Tests, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

class Answers(models.Model):

    answer_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text
