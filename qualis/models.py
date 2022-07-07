from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

class Import(models.Model):
    fs = FileSystemStorage(location='/media/files/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    import_date = models.DateTimeField(null=False)
    file = models.FileField(storage=fs, null=True, blank=True)



class Journals(models.Model):
    issn = models.CharField(max_length=9, null=False, blank=False, unique=True)
    journal = models.CharField(max_length=300, null=False, blank=False)
    qualis = models.CharField(max_length=2, blank=True, null=True)
    import_data = models.ForeignKey(Import, on_delete=models.CASCADE, null=True)

    def __str__(self):
        journal_describe = self.issn+'-'+self.journal
        return journal_describe

    class Meta:
        db_table = 'journals'