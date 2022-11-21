from django.db import models


class UserCreation(models.Model):
    """Class for user creation"""
    user_name = models.CharField(max_length=15)

    def __str__(self):
        return self.user_name


class Articles(models.Model):
    article_name = models.CharField(max_length=3, null=True)

    def __str__(self):
        return self.article_name


class CreateVocabulary(models.Model):
    """Class for data creation"""
    name = models.ForeignKey(UserCreation, on_delete=models.CASCADE)
    article = models.ManyToManyField(Articles)
    word_de = models.CharField(max_length=30)
    word_en = models.CharField(max_length=30)
    sentence = models.CharField(max_length=100)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sentence
