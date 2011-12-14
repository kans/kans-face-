import datetime

from django.db import models

import settings

class DebugDateTimeField(models.DateTimeField):
  """Set DEBUG_TIME to the time you want to use for auto_now and
  auto_now_add fields when creating debug data"""

  def pre_save(self, model_instance, add):
    """ignore changes when we are migrating or if we explicitly told it not to log them
    NOTE:  failing when making a new model in a migration is intentional!
    Consider when that data came into existance, and use that date!"""

    if settings.IS_MIGRATING or (hasattr(model_instance, "skip_auto_now") and model_instance.skip_auto_now):
      return getattr(model_instance, self.attname)
    elif self.auto_now or (self.auto_now_add and add):
      value = datetime.datetime.utcnow()
      setattr(model_instance, self.attname, value)
      return value
    else:
      return super(DebugDateTimeField, self).pre_save(model_instance, add)

class BaseModel(models.Model):
  """A base class for things that need to track creation and updated times."""

  updated_on = DebugDateTimeField(auto_now=True)
  created_on = DebugDateTimeField(auto_now_add=True)

  id = models.AutoField(primary_key=True)

  class Meta:
    abstract = True
