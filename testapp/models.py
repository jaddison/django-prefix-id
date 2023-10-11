from django.db import models

from prefix_id.field import PrefixIDField


class MyModel(models.Model):
    id = PrefixIDField(prefix="test_model", primary_key=True)
    id_no_prefix = PrefixIDField()
    id_no_prefix_blank = PrefixIDField(blank=True)
    id_no_prefix_none = PrefixIDField(null=True)
