from django.forms import CheckboxSelectMultiple
from django.utils.html import format_html

class HorizontalCheckboxSelectMultiple(CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        for i, choice in enumerate(self.choices):
            checkbox = format_html(
                '<label class="inline-flex items-center mr-3"><input type="checkbox" name="{}" value="{}" {} class="form-checkbox h-5 w-5 text-indigo-600"><span class="ml-2 text-sm text-gray-700">{}</span></label>',
                name, choice[0], 'checked' if choice[0] in value else '', choice[1]
            )
            output.append(checkbox)

        return format_html('<div class="flex flex-wrap">{}</div>', '\n'.join(output))
