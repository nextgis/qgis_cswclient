MetaSearch Catalogue Client
===========================

Introduction
------------

MetaSearch is a QGIS plugin to interact with metadata catalogue services.
The OGC Catalogue Service (CSW) standard is initially supported.
Additional catalogue types are planned for future development.

MetaSearch provides an easy and intuitive approach and user-friendly interface
to searching metadata catalogues within QGIS.

Installation
------------

MetaSearch is designed for QGIS 2.0 and higher.  All dependencies are
included within MetaSearch.

Install MetaSearch from the QGIS plugin manager, or manually from
http://plugins.qgis.org/plugins/MetaSearch.

.. note:: for developers, please see the Developers section for specific
          instructions on on installing MetaSearch.

Working with Metadata Catalogues in QGIS
----------------------------------------

CSW (Catalogue Service for the Web)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CSW (Catalogue Service for the Web) is an OGC (Open Geospatial Consortium)
specification, that defines common interfaces to discover, browse, and query
metadata about data, services, and other potential resources.

Startup
^^^^^^^

To start MetaSearch, click the MetaSearch icon or select Web / MetaSearch / 
MetaSearch via the QGIS main menu.  The MetaSearch dialog will appear.
The main GUI consists of two tabs: 'Services' and 'Search'.

Managing Catalogue Services
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The 'Services' tab allows the user to manage all available catalogue services.
MetaSearch provides a default list of Catalogue Services, which can be added
by pressing 'Add default services' button.

To all listed Catalogue Service entries, click the dropdown select box.

To add a Catalogue Service entry, click the 'New' button, and enter a Name for
the service, as well as the URL/endpoint.  Note that only the base URL is
required (not a full GetCapabilities URL).  Clicking ok will add the service 
to the list of entries.

To edit an existing Catalogue Service entry, select the entry you would like
to edit and click the 'Edit' button, and modify the Name or URL values, then
click ok.

To delete a Catalogue Service entry, select the entry you would like to
delete and click the 'Delete' button.  You will be asked to confirm deleting
the entry.

MetaSearch allows for loading and saving connections to an XML file.  This is
useful when you need to share settings between applications.  Below is an example
of the XML file format.

.. code-block:: xml

  <qgsCSWConnections version="1.0">
      <csw name="data.gov" url="http://demo.pycsw.org/services/csw"/>
      <csw name="UK Location Catalogue Publishing Service" url="http://csw.data.gov.uk/geonetwork/srv/en/csw"/>
  </qgsCSWConnections>


To load a list of entries, click the 'Load' button.  A new window will appear;
click the 'Browse' button and navigate to the XML file of entries you wish to
load and click 'Open'.  The list of entries will be displayed.  Select the
entries you wish to add from the list and click 'Load'.

The 'Service info' button displays information about the selected Catalogue
Service such as service identification, service provider and contact
information.  If you would like to view the raw XML response, click the
'GetCapabilities response' button.  A separate window will open displaying
Capabilities XML.

Searching Catalogue Services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The 'Search' tab allows the user to query Catalogue Services for data and
services, set various search parameters and view results.

.. note:: When using the 'Search' tab, MetaSearch always queries the selected
          Catalogue Service entry in the 'Services' tab.

The following search parameters are available:

- *Keywords*: free text search keywords
- *Return records*: the number of records to return when searching.  Default is
  10 records
- *Bounding box*: the spatial area of interest to filter on.  The default
  bounding box is the map view / canvas.  Click 'Set global' to do a global
  search, or enter custom values as desired

Clicking the 'Search' button will search the Metadata Catalogue.  Search
results are displayed in a list and are sortable by clicking on the column
title.  You can navigate through search results with 'First', 'Last', 'Next'
and 'Prev' buttons.

Clicking a result will show the record's abstract in the 'Abstract' window and
provides the following options:

- clicking the 'Metadata' button to display record metadata
- clicking the 'Show XML' button opens a window with the service response in
  raw XML format
- if record has type "downloadableData" and there is a link in the metadata,
  the 'Open URL' button will be enabled. Pressing this button will open the
  link in the user's default browser
- if record has type 'liveData' and there is a link in the metadata, the
  'Add to WMS list' button will be enabled.  When clicking this button
  MetaSearch will verify if this is a valid WMS server.  On success you will
  be asked for name for this server and it will be added to the QGIS WMS
  servers list.  You can then connect to this WMS server by selecting the
  'Layer / Add WMS/WMTS Layer' menu item.

Support
-------

Mailing list: http://lists.osgeo.org/listinfo/qgis-user
IRC: irc://irc.freenode.net/qgis
Issue tracker: https://github.com/geopython/MetaSearch/issues
Source code: https://github.com/geopython/MetaSearch/
Wiki: https://github.com/geopython/MetaSearch/wiki
