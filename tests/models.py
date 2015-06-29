from django.db import models
import reversion


class FooModel(models.Model):
    content = models.CharField(
        blank=True
    )


reversion.register(FooModel)
