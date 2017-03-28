from django.db import models
from django import forms
from django.utils.safestring import mark_safe

"""Based on Spectrum Colorpicker
http://bgrins.github.io/spectrum/
"""


class SpectrumColorPickerWidget(forms.TextInput):
    class Media:
        css = {'all': ('//cdnjs.cloudflare.com/ajax/libs/spectrum/1.8.0/spectrum.min.css',)}
        js = ('//cdnjs.cloudflare.com/ajax/libs/spectrum/1.8.0/spectrum.min.js',)

    def render(self, name, value, attrs=None):
        rendered = super(SpectrumColorPickerWidget, self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
                        $(function() {
                            $('#id_%s').spectrum({
                                showInput: true,
                                showAlpha: true,
                                preferredFormat: "hex",
                                allowEmpty:true,
                            });
                        });
                    </script>''' % name)


class SpectrumColorPickerField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(SpectrumColorPickerField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = SpectrumColorPickerWidget
        return super(SpectrumColorPickerField, self).formfield(**kwargs)