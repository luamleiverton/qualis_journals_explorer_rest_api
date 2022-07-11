from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage



class Journals(models.Model):
    issn = models.CharField(max_length=9, null=False, blank=False, unique=True)
    journal = models.CharField(max_length=300, null=False, blank=False)
    qualis = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        journal_describe = self.issn+'-'+self.journal
        return journal_describe

    class Meta:
        db_table = 'journals'