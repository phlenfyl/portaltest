import sys

from django import VERSION

from django.db import models
from django.utils.text import capfirst
from django.core import exceptions

from multiselectfield.forms.fields import MultiSelectFormField, MinChoicesValidator, MaxChoicesValidator
from multiselectfield.utils import get_max_length
from multiselectfield.validators import MaxValueMultiFieldValidator

if sys.version_info < (3,):
    string_type = unicode # noqa: F821
else:
  string_type = str

class MSFList(list):

  def __init__(self, choices, *args, **kwargs):
    self.choices = choices
    super(MSFList, self).__init__(*args, **kwargs)

  def __str__(msgl):
    msg_list = [msgl.choices.get(int(i)) if i.isdigit() else msgl.choices.get(i) for i in msgl]
    return u', '.join([string_type(s) for s in msg_list])

  if sys.version_info < (3,):
    def __unicode__(self, msgl):
      return self.__str__(msgl)


class MyMultiSelectField(models.CharField):
    """ Choice values can not contain commas. """

    def __init__(self, *args, **kwargs):
        self.min_choices = kwargs.pop('min_choices', None)
        self.max_choices = kwargs.pop('max_choices', None)
        super(MyMultiSelectField, self).__init__(*args, **kwargs)
        self.max_length = get_max_length(self.choices, self.max_length)
        self.validators[0] = MaxValueMultiFieldValidator(self.max_length)
        if self.min_choices is not None:
            self.validators.append(MinChoicesValidator(self.min_choices))
        if self.max_choices is not None:
            self.validators.append(MaxChoicesValidator(self.max_choices))
    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def get_choices_selected(self, arr_choices):
        choices_selected = []

        # Handle list of strings or a single string
        if isinstance(arr_choices[0][1], (list, tuple)):
            for choice_group_selected in arr_choices:
                for choice_selected in choice_group_selected[1]:
                    choices_selected.append(string_type(choice_selected[0]))
        
        elif isinstance(arr_choices, (list, str)):
            if isinstance(arr_choices, str):
                try:
                    arr_choices = arr_choices.split(',')  # split comma-separated string
                except:
                    arr_choices = arr_choices
            try:
                choices_selected = [string_type(choice.strip()) for choice in arr_choices]
            except:
                choices_selected = [string_type(choice) for choice in arr_choices]


        return choices_selected
        # Handle list of lists (already handled in original code)

    def value_to_string(self, obj):
        try:
            value = self._get_val_from_obj(obj)
        except AttributeError:
            value = super(MyMultiSelectField, self).value_from_object(obj)
        return self.get_prep_value(value)

    def validate(self, value, model_instance):
        arr_choices = self.get_choices_selected(self.get_choices_default())
        for opt_select in value:
            if (opt_select not in arr_choices):
                if VERSION >= (1, 6):
                    raise exceptions.ValidationError(self.error_messages['invalid_choice'] % {"value": value})
                else:
                    raise exceptions.ValidationError(self.error_messages['invalid_choice'] % value)

    def get_default(self):
        default = super(MyMultiSelectField, self).get_default()
        if isinstance(default, int):
            default = string_type(default)
        return default

    def formfield(self, **kwargs):
        defaults = {'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text,
                    'choices': self.choices,
                    'max_length': self.max_length,
                    'max_choices': self.max_choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def get_prep_value(self, value):
        return '' if value is None else ";".join(map(str, value))

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared and not isinstance(value, string_type):
            value = self.get_prep_value(value)
        return value

    def to_python(self, value):
        choices = dict(self.choices)

        if value:
            if isinstance(value, list):
                return value
            elif isinstance(value, string_type):
                value_list = map(lambda x: x.strip(), value.split(';'))
                return MSFList(choices, value_list)
            elif isinstance(value, (set, dict)):
                return MSFList(choices, list(value))
        return MSFList(choices, [])

    if VERSION < (2, ):
        def from_db_value(self, value, expression, connection, context):
            if value is None:
                return value
            return self.to_python(value)
    else:
        def from_db_value(self, value, expression, connection):
            if value is None:
                return value
            return self.to_python(value)

    def contribute_to_class(self, cls, name):
        super(MyMultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            def get_list(obj):
                fieldname = name
                choicedict = dict(self.choices)
                display = []
                if getattr(obj, fieldname):
                    for value in getattr(obj, fieldname):
                        item_display = choicedict.get(value, None)
                        if item_display is None:
                            try:
                                item_display = choicedict.get(int(value), value)
                            except (ValueError, TypeError):
                                item_display = value
                        display.append(string_type(item_display))
                return display

            def get_display(obj):
                return ", ".join(get_list(obj))
            get_display.short_description = self.verbose_name

            setattr(cls, 'get_%s_list' % self.name, get_list)
            setattr(cls, 'get_%s_display' % self.name, get_display)


if VERSION < (1, 8):
    MyMultiSelectField = add_metaclass(models.SubfieldBase)(MyMultiSelectField)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^management\.customselect.multiselect\.MyMultiSelectField'])
except ImportError:
    pass
