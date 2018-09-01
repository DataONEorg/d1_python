Standalone
==========

In this approach, search and discovery is exposed directly as a filesystem hierarchy within ONEDrive. This is done by changing the semantics of files and folders. Instead of folders being containers of files, they are used as filters and filter parameters. The files become DataONE objects that match the currently applied filters.

Main advantages:

* Search and discovery functionality is in the same place as object access.
* Virtually the same code base can be used for all supported platforms.

Main disadvantages:

* Giving folders different semantics than they have in a regular filesystem is
  unintuitive.
* There is a learning curve in interpreting and navigating the search/discovery
  filesystem.
* Input data such as keywords cannot be typed in -- they can only be selected.

Mockups
~~~~~~~

In the mockups, filter operations and filter values are prefixed with "@" and
"#" respectively. These decorators have two purposes. The first is to cause filter operations, filter values and results from previously applied filters to be displayed as separate groups in the filesystem when the files and folders are sorted alphabetically. The second is to make it easier for ONEDrive to parse the path when the file and folder names are returned to ONEDrive as path elements by the client. The filesystem path serves as the only channel of communication from the client to ONEDrive and there is no opportunity to do interpretation or translation on the client. Without the decorations, ONEDrive would have to keep track of more context to determine the semantics embedded in the path.


Member Node
-----------

Member Node filtering fits well in the filesystem. The mockup exposes it as a
@MemberNode folder that appears in all folders in which a new filter can be started. Opening the folder exposes a list of Member Nodes. Selecting a Member Node applies the filter and brings the user back to a folder in which the resulting objects appear and the @MemberNode filter is no longer available. We can also implement an "OR" filter by leaving the Member Node filter available to be selected again.


Geographical Area
-----------------

ONEMercury exposes the geographical area search in two ways, as names of continents/states/countries and as a bounding box defined by latitude and longitude. The first type maps pretty well to the folder hierarchy and the mockup exposes it as two hierarchies, one which allows the user to first select a continent then a state/country in that continent and another that allows selecting a state/country directly. Letting the user select latitude and longitude floating point numbers in a filesystem is tricky. It might involve having the user open one folder for each digit. Letting the user select the coordinates as degrees, minutes and seconds is more feasible. We could expose a system which lets the user define coordinates only to the granularity that they need. The user would first select the degrees for upper left and lower right coordinates in a list of numbers between 0 and 359. Then, if they wish, they can refine that by selecting the minutes in a list between 0 and 59, then the same for seconds. Also, only the numbers for which there are actually results within the currently filtered objects are displayed. The mockup illustrates these idea.


Keyword
-------

The only way to let the user type a keyword in filesystem based search/discovery would be to have them type it directly into the path, which I don't think is feasible. So the mockup shows a system where the user must know up front which keyword he wants. The idea is to have the user click through a hierarchy of groups until there are few enough keywords that they can be displayed directly in a list. The groups are displayed as folders named after the first and last keyword in the group. If the keyword filter is the first one that the user applies, my guess is that it will normally be 2-3 levels deep. If the keyword filter is applied after other filters, it may be just 0 or 1 levels deep (where 0 levels means that the keywords are displayed directly, without having to select groups first).


Date-time filtering
-------------------

Date-time filtering is implemented in a way similar to the bounding box geographical area filtering. The goal is have the user filter only to the granularity that they need and select only from date-times for which there are existing objects. So a user that is searching for data up to and including 2005 can select @EndYear/#2005, but does not have to refine with month and day selections and if the current set of objects contain data only up to January and February 2005, only those months are displayed, with the same for year and day
(Solr faceting is used for retrieving the options in a single query). The mockup illustrates this and shows how to make the user aware that refinements are available but optional. This is done by displaying the currently filtered list of objects plus other options for filtering together with each optional date-time refinement step.

As both start and end date-time filtering is available and objects can contain data for a period of time, I think that filtering should be applied in such a way that objects that contain data for a time period that has any overlap with the specified start and end date-time filter should be included in the filter. So, an object with data for 2005-2007 would be included in a search for objects for 2000-2005. And an object with data for 2000-2010 would be included in a search for objects for 2005.

From an implementation standpoint, the mockup also shows how ONEDrive can parse the path in such a way that an optional elements in the path are seen in the context of earlier elements.
