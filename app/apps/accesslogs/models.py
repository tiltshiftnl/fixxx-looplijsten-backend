from django.db import models


class LogEntry(models.Model):
    """
    A request log entry
    """
    # Request user information can be null for anonymous requests
    request_user_email = models.CharField(max_length=255, null=True, editable=False)
    request_user_id = models.CharField(max_length=255, null=True, editable=False)

    # The other fields can never be null
    request_uri = models.CharField(max_length=255, null=False, editable=False)
    request_meta = models.TextField(null=False, editable=False)
    request_method = models.CharField(max_length=7, null=False, editable=False)
    response_status_code = models.CharField(max_length=3, null=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, editable=False)

    def save(self, *args, **kwargs):
        """
        A log entry can only be added once, and should not be editable
        """
        is_new = self.pk is None

        if is_new:
            # Only safe if this is a newly created object
            super().save(*args, **kwargs)
        else:
            # Don't save if this object is already created, and is being edited
            raise Exception("It's not allowed to edit or update log entries")

    def __str__(self):
        return self.request_uri
