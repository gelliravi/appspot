Django-powered sites
=======================
Note these `Django <http://www.djangoproject.com/>`_ apps are still work in progress, with limited doc and support.

Athaliana-history
------------------------------
`Athaliana-history <http://biocon.berkeley.edu/athaliana>`_ is a site to
interactively browse the results of the positional history of `A. thaliana`
genes from `Freeling lab <http://microscopy.berkeley.edu/~freeling/>`_, UC Berkeley.
The *positional history* refers to whether a gene can be found in its syntenic
locations in a few outgroup species with increasing phylogenetic distance to
`A. thaliana` (`A. lyrata`, papaya, poplar, grape). The pipeline to run the
positional history is accessible `here
<https://github.com/tanghaibao/positional-history>`_.

Server configuration
---------------------
Modify apache conf to include lines similar to the following::

    WSGIScriptAlias /athaliana /youraddress/django.wsgi
    <Directory "/home/bao/public_html/bao/apache">
        Order allow,deny
        Allow from all
    </Directory>

    Alias /static "youraddress/static"
    <Directory "/home/bao/public_html/bao/static">
        Order allow,deny
        Allow from all
    </Directory>

