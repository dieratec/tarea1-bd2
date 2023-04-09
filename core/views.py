from datetime import datetime
from base64 import b64encode

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from .forms import RegistrationForm
from . import models

from ravendb import DocumentStore
from pymongo import MongoClient

from datasetman import models as dataset_models

store = DocumentStore('http://localhost:8080', 'dataset_store')
store.initialize()

client = MongoClient('localhost', 27017)


class SignUpView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserDetailView(DetailView):

    model = models.User
    template_name = 'users/user-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        collection = client.followers_db
        follower_list = collection.followers.find_one({'belongs_to': self.request.user.pk})

        with store.open_session() as session:
            query = session.query(object_type=dataset_models.Dataset).where_equals("user_id", kwargs['object'].pk)

            datasets = list(query)
            images = {}

            for dataset in datasets:
                dataset.upload_date = datetime.strptime(dataset.upload_date[:-3], "%Y-%m-%dT%H:%M:%S.%f")  # type: ignore
                images[dataset.Id] = b64encode(session.advanced.attachments.get(dataset.Id, "image.png").data).decode()  # type: ignore

            context['datasets'] = list(query)
            context['dataset_images'] = images

        if (follower_list):
            context['following'] = kwargs['object'].pk in follower_list['following']
        return context


def follow_user(request, user_id):
    collection = client.followers_db

    follower_list = collection.followers.find_one({'belongs_to': request.user.pk})

    if (follower_list):
        follower_list['following'].append(user_id)

        collection.followers.update_one({'belongs_to': request.user.pk}, {"$set": follower_list}, upsert=False)
    else:
        following = {
            'belongs_to': request.user.pk,
            'following': [user_id]
        }

        collection.followers.insert_one(following)

    return redirect('user-details', user_id)


def unfollow_user(request, user_id):
    collection = client.followers_db

    follower_list = collection.followers.find_one({'belongs_to': request.user.pk})

    if (follower_list):
        if user_id in follower_list['following']:
            follower_list['following'].remove(user_id)

        collection.followers.update_one({'belongs_to': request.user.pk}, {"$set": follower_list}, upsert=False)

    return redirect('user-details', user_id)
