=================
django-mediafiles
=================

1. Introduction_
2. Requirements_
3. `Basic installation`_
4. More_

Introduction
------------

``django-mediafiles`` is Django_ reusable application to manage media files in
your Django project. Now ``django-mediafiles`` supports:

- Directories creating +, editing (chmod, chown, rename +), deleting +
- Files creating, uploading +, editing (chmod, chown), deleting +
- Recycle bin
- Thumbnail creation for images
- Text files editing in browser +

**NOTE**: Possibilities that supported current version of ``django-mediafiles``
labeled by **+**.

.. _Django: http://www.djangoproject.com/

Requirements
------------

- `django.contrib.auth`_ and `django.contrib.humanize`_ must be added to your
  project's ``INSTALLED_APPS`` setting;
- `django.contrib.auth.middleware.AuthMiddleware`_ must exists in your project's
  ``MIDDLEWARE_CLASSES`` setting;
- Pygments_ >= 1.0 needed for source code highlight.

.. _`django.contrib.auth`: http://docs.djangoproject.com/en/dev/topics/auth/
.. _`django.contrib.humanize`: http://docs.djangoproject.com/en/dev/ref/contrib/humanize/
.. _`django.contrib.auth.middleware.AuthMiddleware`: http://docs.djangoproject.com/en/dev/ref/middleware/#module-django.contrib.auth.middleware
.. _Pygments: http://www.pygments.org/

Basic installation
------------------

1. Install ``django-mediafiles`` via::

    # python setup.py install

   or add ``mediafiles`` directory to your ``PYTHONPATH``.

2. Add ``mediafiles`` to your project ``INSTALLED_APPS`` and set up serving
   of ``mediafiles`` media directory.

3. Add ``(r'^mediafiles/', include('mediafiles.urls'))`` to your project
   URLConf.

4. That's all :) Now login into Django admin CRUD and click on **Media
   Files** (or localized value) link. (Not worked yet, go to mediafiles url
   to get access to it).

More
----

Check ``django-mediafiles`` Screenshots_ @ Google Code.

.. _Screenshots: http://code.google.com/p/django-mediafiles/wiki/Screenshots
