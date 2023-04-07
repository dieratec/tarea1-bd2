from django import forms


class UploadDatasetForm(forms.Form):
    name = forms.CharField(
        error_messages={'required': 'Por favor, agregue nombre del dataset'},
        label="Nombre"
    )
    description = forms.CharField(
        widget=forms.Textarea,
        error_messages={'required': 'Por favor, agregue descripción del dataset'},
        label="Descripción"
    )
    image = forms.ImageField(
        error_messages={'required': 'Por favor, agregue una imagen del dataset'},
        label="Imagen"
    )
    uploaded_files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        label="Archivos"
    )
    name.widget.attrs.update({'class': 'input'})
    description.widget.attrs.update({'class': 'textarea'})
    image.widget.attrs.update({'class': 'file-input'})
    uploaded_files.widget.attrs.update({'class': 'file-input'})
