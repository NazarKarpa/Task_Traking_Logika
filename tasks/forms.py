from django import forms
from tasks.models import Task, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'media']
        widgets = {
            'media': forms.FileInput()
        }


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'members']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['due_date'].widget.attrs['class'] += ' my-custom=datepicker'



class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', 'Всі'),
        ('todo', 'To Do'),
        ('in_progres', 'In Progress'),
        ('done', 'Done')
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label='Статус')

    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'form-control'})


