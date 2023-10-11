from django.core import exceptions
from django.db import models
from django.utils.translation import gettext_lazy as _

from prefix_id.base62 import generate_base62_id


class PrefixIDField(models.CharField):
    default_error_messages = {
        "invalid_type": _("The value must be text."),
        "invalid_prefix": _("“%(value)s” requires the prefix “%(prefix)s”."),
    }
    description = _("Collision-resistant universal identifier")

    def __init__(self, *args, prefix: str = None, **kwargs):
        self.prefix = prefix or None
        prefix_length = len(self.prefix or "")

        # 'max_length' is the sum of prefix length + 1 char for the
        # underscore separator + 22 (the max_length of a base62 encoded UUID).
        kwargs["max_length"] = (prefix_length + 1 if prefix_length else 0) + 22
        kwargs.setdefault("editable", False)
        kwargs.setdefault("unique", True)

        super().__init__(*args, **kwargs)

    def get_default(self):
        # Overriding this method is needed to get a field-level attribute
        # (ie. 'prefix') available to the default value generation.
        encoded_value = generate_base62_id()

        if self.prefix and isinstance(self.prefix, str):
            return f"{self.prefix}_{encoded_value}"

        return encoded_value

    def deconstruct(self):
        # Overriding this method needed to ensure that migrations are
        # successfully generated. The return value of this method is
        # used to calculate differences between current model state and
        # new: in this case, we need to ensure that 'prefix' is added.
        name, path, args, kwargs = super().deconstruct()
        kwargs["prefix"] = self.prefix
        return name, path, args, kwargs

    def validate(self, value, model_instance):
        if self.null and value is None:
            pass
        elif not isinstance(value, str):
            raise exceptions.ValidationError(
                self.error_messages["invalid_type"],
                code="invalid_type",
            )
        else:
            parts = value.rsplit("_", 1)

            incorrect_or_missing_prefix = self.prefix and (len(parts) == 1 or parts[0] != self.prefix)
            unwanted_prefix_present = not self.prefix and len(parts) > 1
            disallowed_empty_str_present = not self.blank and len(value) == 0

            if incorrect_or_missing_prefix or unwanted_prefix_present or disallowed_empty_str_present:
                raise exceptions.ValidationError(
                    self.error_messages["invalid_prefix"],
                    code="invalid_prefix",
                    params={"value": value, "prefix": self.prefix},
                )

        return super().validate(value, model_instance)
