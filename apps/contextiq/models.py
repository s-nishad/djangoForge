# apps/rag/models.py
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import BaseModel 

User = get_user_model()


class ParsingStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    MANUAL = "manual", "Manual Entry"


class Document(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='documents/%Y/%m/%d/', null=True, blank=True)
    parse_content = models.TextField(blank=True, null=True)
    parse_content_status = models.CharField(
        max_length=20,
        choices=ParsingStatus.choices,
        default=ParsingStatus.PENDING
    )

    def save(self, *args, **kwargs):
        # Automatically set title from file name if not provided
        if not self.title and self.file:
            self.title = self.file.name.split('/')[-1]
        elif self.parse_content and not self.title:
            self.title = self.parse_content[:20] + "..."
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or f"Document #{self.id}"
