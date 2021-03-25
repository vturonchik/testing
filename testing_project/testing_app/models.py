# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Topic(models.Model):
    title = models.CharField('Topic', max_length=20, help_text='Enter a topic')

    def __str__(self):
        return self.title.encode('utf-8')


class Question(models.Model):
    question = models.TextField('Question text', max_length=200, help_text='Enter a question')
    topic = models.ForeignKey(Topic, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.question.encode('utf-8')


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer = models.CharField('Answer', max_length=50, help_text='Enter an answer')
    fidelity = models.BooleanField()

    def __str__(self):
        return self.answer.encode('utf-8')
