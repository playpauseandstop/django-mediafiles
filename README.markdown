Introduction
============

``django-mediafiles`` is Django reusable application to manage media files in
your Django project. Now ``django-mediafiles`` supports:

 * Directories creating +, editing (chmod, chown, rename +), deleting +
 * Files creating, uploading +, editing (chmod, chown), deleting +
 * Recycle bin
 * Thumbnail creation for images
 * Text files editing in browser

**NOTE**: Possibilities that supported current version of
``django-mediafiles`` labeled by **+**.

Requirements
============

 * Pygments 1.0 or later needed for source code highlight

        http://pygments.org/
        http://pypi.python.org/packages/source/P/Pygments/Pygments-1.0.tar.gz
        easy_install Pygments
        hg clone http://dev.pocoo.org/hg/pygments-main pygments

Basic installation
==================

 1. Install ``django-mediafiles`` via:

        # python setup.py install (Not worked yet :( )

 or add ``mediafiles`` directory to your ``PYTHONPATH``.

 1. Add ``mediafiles`` to your project ``INSTALLED_APPS`` and set up serving
 of ``mediafiles`` media directory.

 1. Add ``(r'^mediafiles/', include('mediafiles.urls'))`` to your project
 URLConf.

 1. That's all :) Now login into Django admin CRUD and click on **Media
 Files** (or localized value) link. (Not worked yet, go to mediafiles url
 to get access to it)

More
====

;)
