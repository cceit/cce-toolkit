from django.db import models
from django import forms
from django.utils.safestring import mark_safe

"""Based on Spectrum Colorpicker
http://bgrins.github.io/spectrum/
"""


class SpectrumColorPickerWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        rendered = super(SpectrumColorPickerWidget, self).render(name, value, attrs)
        return rendered + mark_safe(u'''<link href="//cdnjs.cloudflare.com/ajax/libs/spectrum/1.8.0/spectrum.min.css" type="text/css" media="all" rel="stylesheet"><script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/spectrum/1.8.0/spectrum.min.js"></script><script type="text/javascript">
                            $(document).ready(function()
                            {
                            $('#id_%s').spectrum({
                                showInput: true,
                                showAlpha: true,
                                preferredFormat: "rgb",
                                allowEmpty: true,
                            });
                            });
                    </script>''' % name)


class SpectrumColorPickerField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 100
        super(SpectrumColorPickerField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = SpectrumColorPickerWidget
        return super(SpectrumColorPickerField, self).formfield(**kwargs)