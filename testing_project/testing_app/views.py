# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

from models import Question, Topic, Answer


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "testing_app/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class TopicListView(generic.ListView):
    model = Topic
    context_object_name = 'topics'
    queryset = Topic.objects.all()
    template_name = 'testing_app/index.html'


class TestDetailView(generic.DetailView):
    model = Question
    context_object_name = 'questions'
    template_name = 'testing_app/question.html'
    questions_count = 0

    def __init__(self, **kwargs):
        super(TestDetailView, self).__init__(**kwargs)
        self.question_id = 1

    @classmethod
    def update_question_counter(cls, queryset_length):
        cls.questions_count = queryset_length

    def get_queryset(self):
        queryset = Question.objects.filter(topic_id=self.kwargs['topic_id'])
        if TestDetailView.questions_count == 0:
            TestDetailView.update_question_counter(len(queryset))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TestDetailView, self).get_context_data(**kwargs)
        context['next_pk'] = str(int(self.kwargs['pk']) + 1)
        context['topic_id'] = self.kwargs['topic_id']
        return context

    def _redirect_to_next_question(self, request, *args, **kwargs):
        self.object = self.get_object(self.get_queryset())
        context = self.get_context_data(**kwargs)
        context['object'] = self.object
        return redirect('test-details', *args, **kwargs)

    @staticmethod
    def _redirect_to_results(request, *args, **kwargs):
        return redirect('results')

    def _collect_user_response(self, request):
        user_answers = request.POST.getlist('choice')
        self._validate_user_answers(user_answers, request.session)

    def _validate_user_answers(self, user_answers, session):
        current_question_id_correct_answers = [
            answer.id for answer in Answer.objects.filter(question_id=self.question_id, fidelity=True)
        ]
        self.question_id += 1
        for user_answer in user_answers:
            if int(user_answer) not in current_question_id_correct_answers:
                if 'incorrect' in session:
                    session['incorrect'] += 1
                else:
                    session['incorrect'] = 1
                return
        if 'correct' in session:
            session['correct'] += 1
        else:
            session['correct'] = 1

    def post(self, request, *args, **kwargs):
        if int(self.kwargs['pk']) <= TestDetailView.questions_count:
            self._collect_user_response(request)
            return self._redirect_to_next_question(request, *args, **kwargs)
        else:
            request.session['questions_count'] = TestDetailView.questions_count
            return self._redirect_to_results(request, *args, **kwargs)


class ResultsTemplateView(generic.TemplateView):
    template_name = 'testing_app/results.html'

    def get(self, request, *args, **kwargs):
        correct_answers = request.session['correct']
        incorrect_answers = request.session['incorrect']
        context = self.get_context_data(**kwargs)
        context['correct'] = correct_answers
        context['incorrect'] = incorrect_answers
        context['accuracy'] = (correct_answers * 100) / request.session['questions_count']
        self._clean_session(request)
        return self.render_to_response(context)

    @staticmethod
    def _clean_session(request):
        request.session['correct'] = 0
        request.session['incorrect'] = 0
        request.session['questions_count'] = 0
