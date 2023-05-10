from django.db import models


class Statuses(models.TextChoices):
    Unchecked = 'U'
    Checked = 'C'
    Friends = 'F'
