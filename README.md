generic-static-host
===================

This is a quick-and-dirty attempt to formalize the configuration of the host I
use to serve "generic" static sites, which are just sites that don't need
anything more than nginx and python and php.

As of this writing, that host is provided by Digital Ocean, and its operating
system is Ubuntu 12.04 LTS.

Look in `nginx/sites-available` to see which sites this host serves.

bootstrapping
-------------

Run `fab -H <hostname or ip> bootstrap` to set up a new host. Then, make sure
to `fab deploy` each of the sites listed in `nginx/sites-available` from their
own repos.
