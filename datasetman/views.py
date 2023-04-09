import zipfile
import json

from datetime import datetime
from base64 import b64encode

from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from ravendb import DocumentStore
from pymongo import MongoClient

from . import forms, models

from core import models as core_models

store = DocumentStore('http://localhost:8080', 'dataset_store')
store.initialize()

client = MongoClient('localhost', 27017)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        collection = client.followers_db

        follower_list = collection.followers.find_one({'belongs_to': self.request.user.pk})

        with store.open_session() as session:
            query = session.query(object_type=models.Dataset)

            if (self.request.GET.get('user_id')):
                query = query.where_equals("user_id", self.request.GET.get('user_id'))

            if (self.request.GET.get('username')):
                users = core_models.User.objects.all().filter(username__startswith=self.request.GET.get('username'))
                user_ids = [user.pk for user in users]
                query = query.where_in("user_id", user_ids)

            if (self.request.GET.get('following')):
                if (follower_list):
                    query = query.where_in("user_id", follower_list['following'])

            datasets = list(query)
            images = {}

            for dataset in datasets:
                dataset.upload_date = datetime.strptime(dataset.upload_date[:-3], "%Y-%m-%dT%H:%M:%S.%f")  # type: ignore
                images[dataset.Id] = b64encode(session.advanced.attachments.get(dataset.Id, "image.png").data).decode()  # type: ignore

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


class DatasetDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'datasets/detail-dataset.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dataset_id = kwargs['dataset_id']

        with store.open_session() as session:
            dataset: models.Dataset = session.load(f"datasets/{dataset_id}")  # type: ignore
            dataset.upload_date = datetime.strptime(dataset.upload_date[:-3], "%Y-%m-%dT%H:%M:%S.%f")  # type: ignore
            image = b64encode(session.advanced.attachments.get(dataset.Id, "image.png").data).decode()  # type: ignore
            context['dataset'] = dataset
            context['dataset_image'] = image

            context['comments'] = []
            comments = models.Comment.nodes.filter(dataset_id=dataset_id)
            for comment in comments:
                context['comments'].append(comment)

            if (self.request.user.pk == dataset.user_id):
                context['download_list'] = core_models.Download.objects.all().filter(dataset_id=dataset.Id)

        return context


@login_required
def download_dataset(request, dataset_id):
    response = HttpResponse(content_type='application/zip')
    zip_filename = f"{dataset_id}"

    with store.open_session() as session:
        dataset: models.Dataset = session.load(f"datasets/{dataset_id}")  # type: ignore
        uploaded_by = core_models.User.objects.get(pk=dataset.user_id)
        dataset_attachments_details = session.advanced.attachments.get_names(dataset)

        zip_file = zipfile.ZipFile(response, 'x')  # type: ignore

        for attachment_detail in dataset_attachments_details:
            attachment = session.advanced.attachments.get(dataset.Id, attachment_detail.name)
            zip_file.writestr(attachment_detail.name, attachment.data)  # type: ignore

        dataset_details = {
            'user': {
                'username': uploaded_by.username,
                'first_name': uploaded_by.first_name,
                'last_name': uploaded_by.last_name,
                'birthdate': uploaded_by.birthdate,
                'user_id': uploaded_by.pk,
                'email': uploaded_by.email,
            },
            'name': dataset.name,
            'description': dataset.description,
            'upload_time': dataset.upload_date,
            'dataset_id': dataset.Id
        }

        zip_file.writestr("details.json", str.encode(json.dumps(dataset_details, sort_keys=True, indent=4)))

        zip_file.close()

        download_reference = core_models.Download()
        download_reference.download_by = request.user
        download_reference.dataset_download = dataset_details
        download_reference.dataset_id = dataset.Id
        download_reference.save()

    response['Content-Disposition'] = f"attachment; filename={zip_filename}.zip"

    return response


@login_required
def clone_dataset(request, dataset_id):

    with store.open_session() as session:
        dataset: models.Dataset = session.load(f"datasets/{dataset_id}")  # type: ignore
        dataset_attachments_details = session.advanced.attachments.get_names(dataset)

        cloned_dataset = models.Dataset(
                    None,  # type: ignore
                    request.POST.get('new_name'),
                    dataset.description,
                    dataset.user_id,  # type: ignore
                    datetime.now()
                )

        session.store(cloned_dataset)

        for attachment_detail in dataset_attachments_details:
            attachment = session.advanced.attachments.get(dataset.Id, attachment_detail.name)
            session.advanced.attachments.store(
                    cloned_dataset,
                    attachment_detail.name,
                    attachment.data,
                    attachment_detail.content_type
                )

        session.save_changes()

    return redirect('home')


@login_required
def comment_dataset(request, dataset_id):

    if (len(request.POST.get("content")) > 0):
        comment = models.Comment(
            content=request.POST.get("content"),
            user_id=request.user.pk,
            dataset_id=dataset_id,
        )
        comment.save()

    return redirect('detail-dataset', dataset_id)


@login_required
def reply_comment(request, comment_id):

    comment = models.Comment.nodes.get(uid=comment_id)

    if (len(request.POST.get("content")) > 0):
        reply = models.Reply(
            content=request.POST.get("content"),
            user_id=request.user.pk,
        ).save()

        reply.parent_comment.connect(comment)
        reply.save()

    return redirect('detail-dataset', comment.dataset_id)
