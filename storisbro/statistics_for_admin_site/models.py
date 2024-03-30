from django.db import models


class Statistics(models.Model):
    registered_users = models.IntegerField(default=0)
    registered_users_owner = models.IntegerField(default=0)
    registered_users_client = models.IntegerField(default=0)
    unique_visits = models.IntegerField(default=0)
    refills = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    admin_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    creative_uploads = models.IntegerField(default=0)
    community_uploads = models.IntegerField(default=0)
    story_views = models.IntegerField(default=0)
