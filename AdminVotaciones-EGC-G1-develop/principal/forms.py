from models import Poll, Question, Option
from django.forms import ModelForm


class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['title','description','startDate','endDate', 'census']

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description', 'optional', 'multiple']

class OptionForm(ModelForm):
    class Meta:
        model = Option
        fields = ['description']
        