from datetime import datetime
from base64 import b64encode
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from ravendb import DocumentStore

from . import forms, models

store = DocumentStore('http://localhost:8080', 'dataset_store')
store.initialize()


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with store.open_session() as session:
            query = session.query(object_type=models.Dataset)
            datasets = list(query)
            images = {}

            for dataset in datasets:
                print(dataset.upload_date)
                dataset.upload_date = datetime.strptime(dataset.upload_date[:-3], "%Y-%m-%dT%H:%M:%S.%f")
                images[dataset.Id] = b64encode(session.advanced.attachments.get(dataset.Id, "image.png").data).decode()

            context['datasets'] = list(query)
            context['dataset_images'] = images
        return context


class UploadDatasetView(LoginRequiredMixin, FormView):
    template_name = 'datasets/upload-dataset.html'
    form_class = forms.UploadDatasetForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        files = request.FILES.getlist('uploaded_files')

        image = request.FILES['image']

        if form.is_valid():
            with store.open_session() as session:
                dataset = models.Dataset(
                    None,  # type: ignore
                    form.cleaned_data['name'],
                    form.cleaned_data['description'],
                    self.request.user.id,  # type: ignore
                    datetime.now()
                )

                session.store(dataset)

                session.advanced.attachments.store(
                    dataset,
                    'image.png',
                    image.read(),
                    image.content_type
                )

                for file in files:
                    session.advanced.attachments.store(
                        dataset,
                        file.name,
                        file.read(),
                        file.content_type
                    )

                session.save_changes()

        return self.form_valid(form)
