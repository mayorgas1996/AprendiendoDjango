from django import forms
from django.core import validators

class FormArticle(forms.Form):
    title = forms.CharField(
        label = 'Titulo',
        max_length = 40,
        widget = forms.TextInput(
            attrs={
                'placeholder':'Mete el titulo',
                'class':'titulo_form_article'
            }
        ),
        validators=[
            validators.MinLengthValidator(4, "El titulo es demasiado corto"),
            validators.RegexValidator('^[A-Za-z0-9]*$', "El titulo está mal formado", "invalid_title")
        ]
    )
    content = forms.CharField(
        label = 'Contenido',
        widget= forms.Textarea(),
        validators=[
            validators.MaxLengthValidator(50,'Te has pasado de contenido')
        ]
    )

    content.widget.attrs.update({
        'placeholder':'Mete el contenido',
        'class':"contenido_form_article",
        'id':'contenido_form'
    })

    public_options = [
        (0, "No"),
        (1, "Si")
    ]

    public = forms.TypedChoiceField(
        label = "¿Publicado?",
        choices = public_options
    )
