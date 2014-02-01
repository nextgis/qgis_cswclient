Working with metadata catalogs in QGIS
**************************************

CSW (Catalogue Service for Web) is an OGC (Open Geospatial Consortium)
specification, that defines common interfaces to discover, browse, and query
metadata about data, services, and other potential resources.

MetaSearch plugin for QGIS provides userfriendly interface for this services.

We want to thanks Linfiniti Consulting for sponsoring development.

Installation notes
==================

MetaSearch is designed for QGIS 2.0 and higher. There are no dependencies, all
necessary files are included in package.

You can obtain sources from our GitHub repository:

::
git clone https://github.com/geopython/MetaSearch.git


How does it work
================

After plugin installation and startup by clicking button


main window with two tabs will appear


The "Servers" tab is used for managing the list of available servers. Plugin
shipped with small list of servers, you can add them by pressing "Add default
servers" button. Also you can add new server, edit or delete existing with
"New", "Edit" and "Delete" buttons respectively.

Besides this it is possible to save server list in file with "Save" button and
load them from file with "Load" button. Before saving or loading you can select
only necessary servers. This is useful when you need to share settings between
several computers.

"Server info" will display available information about server in the text area.
Button «Metadata» has same purpose, but displayed information in separate
window as XML document.

In the "Search" tab you can set up search parameters and view results.

First of all it is necessary to enter search keyword (or comma separated list
of keywords) and boundaries to search within. By defaults used canvas bounding
box, if necessary you can enter values in fields. "From map canvas" and "Set
global" buttons allow to set up canvas bbox and global bbox in one click.

Results are displayed in list. It is possible to sort them by clicking on
column title. When record is selected "Abstract" field is filled, and if
available displayed URL. Also "Metadata" button becomes active. Pressing on
this button will display record metadata. When "Show XML" is clicked appears a
window with server response in XML format.

You can navigate through search results with "First", "Last", "Next" and "Prev"
buttons.

If record has type "downloadableData" and there is a link in their metadata,
button "Open URL" will be enabled. Pressing this button will cause opening link
in the default browser.

If record has type "liveData" and there is a link in their metadata, "Add to
WMS list" button will be enabled. When this button is pressed plugin tried to
verify is this is a valid WMS server or not. On success you will be asked for
name for this server and it will be added to the QGIS WMS servers list. Later
you can connect for this server as usual.

Note. Now very simple test used for check WMS URL's validity. So in some cases
this test will return wrong results and server will not be added to the QGIS
WMS list. In this case you can copy URL and add it manually.

Contacts
========

If you want report a bug or want make suggestion --- use our bugtracker
http://github.com/geopython/MetaSearch/issues
