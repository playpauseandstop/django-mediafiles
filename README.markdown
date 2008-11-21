Introduction
============

``django-mediafiles`` is Django reusable application to manage media files in
your Django project. Now ``django-mediafiles`` supports:

 * Directories creating, editing (chmod, chown, rename), deleting
 * Files creating, uploading, editing (chmod, chown), deleting
 * Recycle bin
 * Thumbnail creation for images
 * Text files editing in browser

Basic installation
==================

 1. Install ``django-mediafiles`` via:

        # python setup.py install

 or add ``mediafiles`` directory to your ``PYTHONPATH``.

 1. Add ``mediafiles`` to your project ``INSTALLED_APPS`` and set up serving
 of ``mediafiles`` media directory.

 1. Add ``(r'^mediafiles/', include('mediafiles.urls'))`` to your project
 URLConf.

 1. That's all :) Now login into Django admin CRUD and click on **Media
 Files** (or localized value) link.

More
====

See ``docs/`` directory for more information about ``django-mediafiles``
