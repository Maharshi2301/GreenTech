from django.db import models
from django.contrib.auth.models import User

class GreenPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # New field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(GreenPost, on_delete=models.CASCADE, related_name="feedbacks", null=True)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.post.title}"

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class VolunteerApplication(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('D', 'Denied'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="applications", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # <-- New
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    motivation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return f"{self.name} - {self.event.title} ({self.get_status_display()})"

class VolunteerRequest(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('D', 'Denied'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='volunteer_request', null=True)
    name             = models.CharField(max_length=100)
    email            = models.EmailField()
    phone_number     = models.CharField("Phone #", max_length=20)
    area_of_interest = models.CharField(max_length=200)
    availability     = models.CharField(
                          max_length=200,
                          help_text="e.g. weekends, weekdays, evenings"
                      )
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='P',
        help_text="Admin can Accept or Deny"
    )

    class Meta:
        verbose_name = "Community Request"
        verbose_name_plural = "Community Requests"

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

class Suggestion(models.Model):
    title = models.CharField(max_length=100)
    suggestion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ReportIssue(models.Model):
    name = models.CharField(max_length=100)
    issue = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
