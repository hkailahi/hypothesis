# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2019 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

from __future__ import absolute_import, division, print_function

from django.conf.urls import include, url
from django.contrib import admin

patterns, namespace, name = admin.site.urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'toys.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r"^admin/", include((patterns, name), namespace=namespace))
]
