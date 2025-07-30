from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView, CreateView, DetailView, TemplateView, DeleteView, View
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

from .models import (
    GreenPost, ContactMessage, Feedback,
    VolunteerRequest, Suggestion, ReportIssue,
    Event, VolunteerApplication
)
from .forms import (
    GreenPostForm, ContactForm, SignUpForm, FeedbackForm,
    VolunteerRequestForm, ReportIssueForm,
    EventForm, VolunteerApplicationForm
)


# ---------------------------
# Home & Posts
# ---------------------------
class HomeView(ListView):
    model = GreenPost
    template_name = 'greentech/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        qs = GreenPost.objects.all()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        visits = self.request.session.get('visits', 0) + 1
        self.request.session['visits'] = visits
        ctx.update({
            'visits': visits,
            'query': self.request.GET.get('q', ''),
        })
        return ctx


class AddPostView(LoginRequiredMixin, CreateView):
    model = GreenPost
    form_class = GreenPostForm
    template_name = 'greentech/add_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = GreenPost
    template_name = 'greentech/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Feedback form and list for this post
        context['feedback_form'] = FeedbackForm()
        context['feedbacks'] = Feedback.objects.filter(post=self.object).order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        """Handles feedback form submissions."""
        self.object = self.get_object()
        if not request.user.is_authenticated:
            messages.error(request, "You need to be logged in to submit feedback.")
            return redirect('login')

        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.post = self.object
            feedback.save()
            messages.success(request, "Thank you for your feedback!")
        else:
            messages.error(request, "There was a problem with your feedback.")

        return redirect('post_detail', pk=self.object.pk)


@method_decorator(staff_member_required, name='dispatch')
class AdminPostListView(ListView):
    model = GreenPost
    template_name = 'greentech/admin_post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']


@method_decorator(staff_member_required, name='dispatch')
class DeletePostView(DeleteView):
    model = GreenPost
    template_name = 'greentech/confirm_delete.html'
    success_url = reverse_lazy('admin_post_list')

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        messages.success(request, f"Deleted post “{post.title}”.")
        return super().delete(request, *args, **kwargs)


# ---------------------------
# Authentication
# ---------------------------
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'greentech/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


# ---------------------------
# Contact
# ---------------------------
class ContactView(LoginRequiredMixin, CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = 'greentech/contact.html'
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        messages.success(self.request, "Message sent successfully.")
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class ContactMessagesView(ListView):
    model = ContactMessage
    template_name = 'greentech/contact_messages.html'
    context_object_name = 'contact_messages'
    ordering = ['-created_at']


# ---------------------------
# About (Static Page)
# ---------------------------
class AboutView(TemplateView):
    template_name = 'greentech/about.html'


# ---------------------------
# Feedback
# ---------------------------
class FeedbackView(LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'greentech/feedback.html'
    success_url = reverse_lazy('feedback')

    def form_valid(self, form):
        fb = form.save(commit=False)
        fb.user = self.request.user
        fb.save()
        messages.success(self.request, "Feedback submitted.")
        return redirect(self.success_url)


# ---------------------------
# Volunteers
# ---------------------------
class VolunteerRequestView(LoginRequiredMixin, CreateView):
    model = VolunteerRequest
    form_class = VolunteerRequestForm
    template_name = 'greentech/volunteer.html'
    success_url = reverse_lazy('volunteer')

    def dispatch(self, request, *args, **kwargs):
        # Prevent multiple requests from the same user
        if hasattr(request.user, 'volunteer_request'):
            messages.info(request, "You have already submitted a volunteer request.")
            return redirect('event_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.name = self.request.user.get_full_name() or self.request.user.username
        form.instance.email = self.request.user.email
        messages.success(self.request, "Your volunteer request has been submitted successfully.")
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class VolunteerRequestsView(ListView):
    model = VolunteerRequest
    template_name = 'greentech/volunteer_requests.html'
    context_object_name = 'requests'
    ordering = ['-created_at']


@method_decorator(staff_member_required, name='dispatch')
class AcceptVolunteerView(View):
    def post(self, request, pk):
        vr = get_object_or_404(VolunteerRequest, pk=pk)
        vr.status = 'A'
        vr.save()
        messages.success(request, f"Accepted volunteer request from {vr.name}.")
        return redirect('volunteer_requests')

    def get(self, request, pk):
        return redirect('volunteer_requests')


@method_decorator(staff_member_required, name='dispatch')
class DenyVolunteerView(View):
    def post(self, request, pk):
        vr = get_object_or_404(VolunteerRequest, pk=pk)
        vr.status = 'D'
        vr.save()
        messages.warning(request, f"Denied volunteer request from {vr.name}.")
        return redirect('volunteer_requests')

    def get(self, request, pk):
        return redirect('volunteer_requests')


# # ---------------------------
# # Suggestions & Issues
# # ---------------------------
# class SuggestionView(CreateView):
#     model = Suggestion
#     form_class = SuggestionForm
#     template_name = 'greentech/suggestion.html'
#     success_url = reverse_lazy('suggestion')


class ReportIssueView(CreateView):
    model = ReportIssue
    form_class = ReportIssueForm
    template_name = 'greentech/report_issue.html'
    success_url = reverse_lazy('report_issue')


# ---------------------------
# Dashboard & Users
# ---------------------------
@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'greentech/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'total_posts': GreenPost.objects.count(),
            'total_contacts': ContactMessage.objects.count(),
            'total_feedbacks': Feedback.objects.count(),
            'total_volunteers': VolunteerRequest.objects.count(),
            'total_suggestions': Suggestion.objects.count(),
            'total_issues': ReportIssue.objects.count(),
            'total_events': Event.objects.count(),
            'total_users': User.objects.count(),
        })
        return ctx


@method_decorator(staff_member_required, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'greentech/user_list.html'
    context_object_name = 'users'
    ordering = ['username']


@method_decorator(staff_member_required, name='dispatch')
class DeleteUserView(DeleteView):
    model = User
    template_name = 'greentech/confirm_delete_user.html'
    success_url = reverse_lazy('user_list')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        username = user.username
        messages.success(request, f"Deleted user '{username}'.")
        return super().delete(request, *args, **kwargs)


class EventListView(ListView):
    model = Event
    template_name = 'greentech/event_list.html'
    context_object_name = 'events'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            user_applications = {
                app.event_id: app.status
                for app in VolunteerApplication.objects.filter(user=user)
            }
            context['user_applications'] = user_applications
        else:
            context['user_applications'] = {}
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'greentech/event_detail.html'
    context_object_name = 'event'


class AddEventView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'greentech/add_event.html'
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Event created successfully.")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff  # Only staff can create events


class VolunteerApplicationView(LoginRequiredMixin, CreateView):
    model = VolunteerApplication
    form_class = VolunteerApplicationForm
    template_name = 'greentech/apply_volunteer.html'
    success_url = reverse_lazy('event_list')

    def get_initial(self):
        initial = super().get_initial()
        event_id = self.request.GET.get("event")
        if event_id:
            event = get_object_or_404(Event, pk=event_id)
            initial['event'] = event
        return initial

    def dispatch(self, request, *args, **kwargs):
        # Check if the user has an approved volunteer request
        try:
            volunteer_req = request.user.volunteer_request
            if volunteer_req.status != 'A':
                messages.error(request, "Your volunteer request is not approved yet.")
                return redirect('event_list')
        except VolunteerRequest.DoesNotExist:
            messages.error(request, "You must submit a volunteer request before applying for an event.")
            return redirect('volunteer')  # Redirect to general volunteer request form
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.request.GET.get("event")
        if event_id:
            context['event'] = get_object_or_404(Event, pk=event_id)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.name = self.request.user.get_full_name() or self.request.user.username
        form.instance.email = self.request.user.email
        messages.success(self.request, "Application submitted successfully.")
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch')
class AcceptEventVolunteerView(View):
    def post(self, request, pk):
        app = VolunteerApplication.objects.get(pk=pk)
        app.status = 'A'
        app.save()
        messages.success(request, f"Accepted volunteer application from {app.name} for {app.event.title}.")
        return redirect('admin_event_list')


@method_decorator(staff_member_required, name='dispatch')
class DenyEventVolunteerView(View):
    def post(self, request, pk):
        app = VolunteerApplication.objects.get(pk=pk)
        app.status = 'D'
        app.save()
        messages.warning(request, f"Denied volunteer application from {app.name} for {app.event.title}.")
        return redirect('admin_event_list')

@method_decorator(staff_member_required, name='dispatch')
class FeedbackListView(ListView):
    model = Feedback
    template_name = 'greentech/feedback_list.html'
    context_object_name = 'feedbacks'
    ordering = ['-created_at']

@method_decorator(staff_member_required, name='dispatch')
class DeleteFeedbackView(DeleteView):
    model = Feedback
    template_name = 'greentech/confirm_delete_feedback.html'
    success_url = reverse_lazy('feedback_list')

    def delete(self, request, *args, **kwargs):
        feedback = self.get_object()
        messages.success(request, f"Feedback by {feedback.user.username} deleted.")
        return super().delete(request, *args, **kwargs)