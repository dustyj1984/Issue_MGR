from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy
from accounts.models import Role, Team, CustomUser
from .models import Issue, Status, Priority

class BoardView(LoginRequiredMixin, ListView):
    template_name = 'issues/board.html'
    model = Issue

    def populate_issue_list(self, name, status, reporter, context):
        context[name] = Issue.objects.filter(
            status=status,
        ).filter(
            reporter=reporter
        ).order_by(
            "created_on"
        ).reverse()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        to_do_status = Status.objects.get(name='To Do')
        in_p_status = Status.objects.get(name='In Progress')
        done_status = Status.objects.get(name='Done')
        
        team = self.request.user.team
        role = Role.objects.get(name='Product Owner')
        product_owner = CustomUser.objects.filter(
            role=role).get(team=team)
        self.populate_issue_list('to_do_issues', to_do_status, product_owner, context)
        self.populate_issue_list('in_p_issues', in_p_status, product_owner, context)
        self.populate_issue_list('done_list', done_status, product_owner, context)
        return context

       

class IssueDetailView(LoginRequiredMixin, DetailView):
    template_name = 'issues/detail.html'
    model = Issue


class IssueCreateView(LoginRequiredMixin, CreateView):
    template_name = 'issues/new.html'
    model = Issue
    fields = ['summary', 'description', 'priority','status', 'assignee']

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)

class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'issues/edit.html'
    model = Issue
    fields = ['summary', 'description', 'priority', 'status', 'assignee']
    
    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)

class IssueDeleteView(DeleteView):
    template_name = 'issues/delete.html'
    model = Issue
    success_url = reverse_lazy('board')

# Create your views here.
