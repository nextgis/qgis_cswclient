MetaSearch Catalogue Client
===========================

Introduction
------------

MetaSearch is a QGIS plugin to interact with metadata catalogue services.  The OGC Catalogue Service (CSW) standard is initially supported.  Additional catalogue types are planned for future development.

MetaSearch provides an easy and intuitive approach and user-friendly interface to searching metadata catalogues within QGIS.

Installation
------------

MetaSearch is designed for QGIS 2.0 and higher. All dependencies are included within MetaSearch.

Install MetaSearch from the QGIS plugin manager, or manually from http://plugins.qgis.org/plugins/MetaSearch.

.. note:: for developers, please see the Developers section for specific instructions on on installing MetaSearch.


Working with Metadata Catalogues in QGIS
----------------------------------------

CSW (Catalogue Service for the Web)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CSW (Catalogue Service for the Web) is an OGC (Open Geospatial Consortium)
specification, that defines common interfaces to discover, browse, and query
metadata about data, services, and other potential resources.

Startup
^^^^^^^

To start MetaSearch, click the MetaSearch icon or select Web / MetaSearch / MetaSearch via the QGIS main menu.  The MetaSearch dialog will appear.  The main GUI consists of two tabs: 'Services' and 'Search'.

Managing Catalogue Services
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The 'Services' tab allows the user to manage all available catalogue services.  MetaSearch provides a default list of Catalogue Services, which can be added by by pressing 'Add default services' button.

To all listed Catalogue Service entries, click the dropdown select box.

To add a Catalogue Service entry, click the 'New' button, and enter a Name for the service, as well as the URL/endpoint.  Note that only the base URL is required (not a full GetCapabilities URL).  Clicking ok will add the server to the list of entries.

To edit an existing Catalogue Service entry, select the entry you would like to edit and click the 'Edit' button, and modify the Name or URL values, then click ok.

To delete a Catalogue Service entry, select the entry you would like to delete and click the 'Delete' button.  You will be asked to confirm deleting the entry.

MetaSearch allows for loading and saving connections to an XML file.  This is useful when you need to share settings between applications.  Below is an example of the XML file format.

.. code:: xml

  <qgsCSWConnections version="1.0">
      <csw name="data.gov" url="http://demo.pycsw.org/services/csw"/>
      <csw name="UK Location Catalogue Publishing Service" url="http://csw.data.gov.uk/geonetwork/srv/en/csw"/>
  </qgsCSWConnections>


To load a list of entries, click the 'Load' button.  A new window will appear; click the 'Browse' button and navigate to the XML file of entries you wish to load and click 'Open'.  The list of entries will be displayed.  Select the entries you wish to add from the list and click 'Load'.

The 'Service info' button displays information about the selected Catalogue Service such as service identification, service provider and contact information .  If you would like to view the raw, full XML response, click the 'GetCapabilities response' button.  A separate window will open displaying Capabilities XML.

Searching Catalogue Services
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The 'Search' tab allows the user to query Catalogue Services for data and services, set various search parameters and view results.

.. note: When using the 'Search' tab, MetaSearch always queries thethe selected Catalogue Service entry in the 'Services' tab.

The following search parameters are available:

- Keywords: 
- Return records:
- Bounding box: map or global
- 

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


