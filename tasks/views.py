from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from tasks import models
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.mixins import UserIsOwnerMixins
from tasks.forms import TaskForm, TaskFilterForm, CommentForm
from django.http import HttpResponseRedirect

from tasks.models import Comment


class TaskListView(LoginRequiredMixin, ListView):
    model = models.Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'

    def get_queryset(self):

        queryset = models.Task.objects.filter(creator = self.request.user).all()
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)

        return queryset



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskFilterForm(self.request.GET)
        return context

class TaskDetailView(LoginRequiredMixin,DetailView):
    model = models.Task
    context_object_name = 'task'
    template_name = 'tasks/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.comment_to_task = self.get_object()
            comment.save()
            return redirect('tasks:task-detail', pk=comment.comment_to_task.pk)

        else:
            pass

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = models.Task
    template_name = 'tasks/task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskCompleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = 'done'
        task.save()
        return HttpResponseRedirect(reverse_lazy('tasks:task-list'))

    def get_object(self):
        task_id = self.kwargs.get('pk')
        return get_object_or_404(models.Task, pk=task_id)



class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixins, UpdateView):
    model = models.Task
    form_class = TaskForm
    template_name = 'tasks/task_update_form.html'
    success_url = reverse_lazy('tasks:task-list')


class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixins, DeleteView):
    model = models.Task
    success_url = reverse_lazy('tasks:task-list')
    template_name = 'tasks/task_delete_confirmation.html'


