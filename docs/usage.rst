========
Usage
========

To use django-reversion-extras in a project::

    # views.py
    from django.views import generic
    from reversion_extras.views import DetailVersionListView, UpdateVersionListView

    from .models import FooModel
    from .forms import FooModelForm


    # it works just like django.views.generic.DetailView from django
    class FooModelUpdateViewWithVersionList(UpdateVersionListView):
        model = FooModel
        version_paginate_by = 20
        success_url = reverse_lazy('foomodel_list')


    # it works just like django.views.generic.UpdateView from django
    class FooModelDetailViewWithVersionList(UpdateVersionListView):
        model = FooModel
        version_paginate_by = 20
        form_class = FooModelForm
        success_url = reverse_lazy('foomodel_list')


    class FooModelListView(generic.ListView):
        model = FooModel


    # models.py
    from django.db import models
    import reversion

    class FooModel(models.Model):

        content = models.TextField()

    reversion.register(FooModel)


    # urls.py
    from django.conf.urls import include, url

    from .views import (
        FooModelListView,
        FooModelUpdateViewWithVersionList,
        FooModelDetailViewWithVersionList
    )

    urlpatterns = [
        url(r'^$', FooModelListView.as_view(), name='foomodel_list'),
        url(r'^update_with_versions/(?P<pk>\d+)/$', FooModelUpdateViewWithVersionList.as_view(), name='foomodel_update'),
        url(r'^detail_with_versions/(?P<pk>\d+)/$', FooModelDetailViewWithVersionList.as_view(), name='foomodel_detail')
    ]


