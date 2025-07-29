from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    HomeView, AddPostView, PostDetailView,
    AdminPostListView, DeletePostView,
    SignUpView, ContactView, ContactMessagesView,
    AboutView, FeedbackView, FeedbackListView, DeleteFeedbackView,
    VolunteerRequestView, VolunteerRequestsView,
    AcceptVolunteerView, DenyVolunteerView,
    ReportIssueView, DashboardView, UserListView, DeleteUserView,
    EventListView, EventDetailView, AddEventView, VolunteerApplicationView,
    AcceptEventVolunteerView, DenyEventVolunteerView
)

urlpatterns = [
    # Home & Posts
    path('', HomeView.as_view(), name='home'),
    path('add-post/', AddPostView.as_view(), name='add_post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('manage-posts/', AdminPostListView.as_view(), name='admin_post_list'),
    path('manage-post/<int:pk>/delete/', DeletePostView.as_view(), name='delete_post'),

    # Authentication
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='greentech/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # Contact
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact-messages/', ContactMessagesView.as_view(), name='contact_messages'),

    # About
    path('about/', AboutView.as_view(), name='about'),

    # Feedback
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('manage-feedbacks/', FeedbackListView.as_view(), name='feedback_list'),
    path('manage-feedbacks/<int:pk>/delete/', DeleteFeedbackView.as_view(), name='delete_feedback'),

    # Volunteers
    path('volunteer/', VolunteerRequestView.as_view(), name='volunteer'),
    path('volunteer-requests/', VolunteerRequestsView.as_view(), name='volunteer_requests'),
    path('volunteer-requests/<int:pk>/accept/', AcceptVolunteerView.as_view(), name='accept_volunteer'),
    path('volunteer-requests/<int:pk>/deny/', DenyVolunteerView.as_view(), name='deny_volunteer'),

    # Suggestions & Issues
    # path('suggestion/', SuggestionView.as_view(), name='suggestion'),
    path('report-issue/', ReportIssueView.as_view(), name='report_issue'),

    # Dashboard & Users
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),

    # Event
    path('events/', EventListView.as_view(), name='event_list'),
    path('events/add/', AddEventView.as_view(), name='add_event'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('events/apply/', VolunteerApplicationView.as_view(), name='apply_volunteer'),
    path('admin-events/', EventListView.as_view(template_name='greentech/admin_event_list.html'),
         name='admin_event_list'),
    path('admin-events/<int:pk>/accept/', AcceptEventVolunteerView.as_view(), name='accept_event_volunteer'),
    path('admin-events/<int:pk>/deny/', DenyEventVolunteerView.as_view(), name='deny_event_volunteer'),
]
