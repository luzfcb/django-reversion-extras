# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import reversion
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import InvalidPage, Paginator
from django.db.models.query import QuerySet
from django.http import Http404
from django.utils import six
from django.utils.translation import ugettext as _
from django.views import generic
from reversion.models import Version

__all__ = (
    'MultipleVersionObjectMixin',
    'DetailVersionListView',
    'UpdateVersionListView'
)


class MultipleVersionObjectMixin(object):
    """
    A mixin for views manipulating multiple django-reversion Versions of object.
    """
    version_allow_empty = True
    version_queryset = None
    version_model = Version
    version_paginate_by = None
    version_paginate_orphans = 0
    version_context_object_name = None
    version_paginator_class = Paginator
    version_page_kwarg = 'versionpage'
    version_ordering = '-revision__date_created'
    version_object_list = None

    def get_version_queryset(self):
        """
        Return the list of version items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.version_queryset is not None:
            queryset = self.version_queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.version_model is not None:
            queryset = reversion.get_for_object(self.get_object())
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a Version QuerySet. Define "
                "%(cls)s.version_model, %(cls)s.version_queryset, or override "
                "%(cls)s.get_version_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        ordering = self.get_version_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

    def get_version_ordering(self):
        """
        Return the field or fields to use for ordering the version queryset.
        """
        return self.version_ordering

    def paginate_version_queryset(self, queryset, page_size):
        """
        Paginate the version queryset, if needed.
        """
        paginator = self.get_version_paginator(
            queryset, page_size, orphans=self.get_version_paginate_orphans(),
            allow_empty_first_page=self.get_version_allow_empty())
        page_kwarg = self.version_page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_("Page is not 'last', nor can it be converted to an int."))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': str(e)
            })

    def get_version_paginate_by(self, queryset):
        """
        Get the number of version items to paginate by, or ``None`` for no pagination.
        """
        return self.version_paginate_by

    def get_version_paginator(self, queryset, per_page, orphans=0,
                              allow_empty_first_page=True, **kwargs):
        """
        Return an instance of the version paginator for this view.
        """
        return self.version_paginator_class(
            queryset, per_page, orphans=orphans,
            allow_empty_first_page=allow_empty_first_page, **kwargs)

    def get_version_paginate_orphans(self):
        """
        Returns the maximum number of orphans extend the last page by when
        paginating.
        """
        return self.version_paginate_orphans

    def get_version_allow_empty(self):
        """
        Returns ``True`` if the view should display empty version lists, and ``False``
        if a 404 should be raised instead.
        """
        return self.version_allow_empty

    def get_version_context_object_name(self):
        """
        Get the name of the version item to be used in the context.
        """
        if self.version_context_object_name:
            return self.version_context_object_name
        elif hasattr(self, 'model'):
            return '%s_versions_list' % self.model._meta.model_name
        else:
            return None

    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        version_queryset = kwargs.pop('version_object_list', self.version_object_list)
        version_page_size = self.get_version_paginate_by(version_queryset)
        version_context_object_name = self.get_version_context_object_name()
        if version_page_size:
            version_paginator, version_page, version_queryset, version_is_paginated = self.paginate_version_queryset(
                version_queryset, version_page_size)
            context = {
                'version_paginator': version_paginator,
                'version_page_obj': version_page,
                'version_is_paginated': version_is_paginated,
                'object_versions_list': version_queryset
            }
        else:
            context = {
                'version_paginator': None,
                'version_page_obj': None,
                'version_is_paginated': False,
                'object_versions_list': version_queryset
            }
        if version_context_object_name is not None:
            context[version_context_object_name] = version_queryset
        context.update(kwargs)
        return super(MultipleVersionObjectMixin, self).get_context_data(**context)

    def get(self, request, *args, **kwargs):
        self.version_object_list = self.get_version_queryset()
        version_allow_empty = self.get_version_allow_empty()

        if not version_allow_empty:
            # When pagination is enabled and object_versions_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if (self.get_version_paginate_by(self.version_object_list) is not None and hasattr(self.version_object_list, 'exists')):  # noqa
                is_empty = not self.version_object_list.exists()
            else:
                is_empty = len(self.version_object_list) == 0
            if is_empty:
                raise Http404(
                    _("Empty Version list and '%(class_name)s.version_allow_empty' is False.")
                    % {'class_name': self.__class__.__name__})

        return super(MultipleVersionObjectMixin, self).get(self, request, *args, **kwargs)


class DetailVersionListView(MultipleVersionObjectMixin, generic.DetailView):
    """
    Render some list of django-reversion Versions of object, set by `self.model` or
    `self.queryset`. `self.queryset` can actually be any iterable of items, not just a queryset.
    """
    template_name_suffix = '_version_list'


class UpdateVersionListView(MultipleVersionObjectMixin, generic.UpdateView):
    """
    Render some list of versions of object, set by `self.model` or `self.queryset`.
    `self.queryset` can actually be any iterable of items, not just a queryset.
    """
    template_name_suffix = '_form_version_list'


class ReversionView(generic.FormView):
    pass
