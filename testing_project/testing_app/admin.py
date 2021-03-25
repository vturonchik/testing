# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from models import Question, Answer, Topic


class QuestionInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(QuestionInlineFormSet, self).clean()
        fidelity_check_list = []
        for form in self.forms:
            fidelity = form.cleaned_data.get('fidelity')
            if fidelity is not None:
                fidelity_check_list.append(fidelity)
        if not any(fidelity for fidelity in fidelity_check_list):
            raise ValidationError('There must be at least one correct answer.')
        elif all(fidelity for fidelity in fidelity_check_list):
            raise ValidationError('All answers can\'t be correct.')


class AnswerInstanceInline(admin.TabularInline):
    model = Answer
    formset = QuestionInlineFormSet


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'topic')
    list_filter = ('topic',)
    inlines = [AnswerInstanceInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'fidelity')
    list_filter = ('question',)
    fields = ['question', ('answer', 'fidelity')]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass
