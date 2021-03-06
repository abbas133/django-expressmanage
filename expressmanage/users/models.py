from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from author.decorators import with_author


@with_author
class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    role = CharField(_("Role of User"), blank=True, max_length=20)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
