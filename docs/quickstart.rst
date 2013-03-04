.. _quickstart:

Quickstart
==========
This page gives a good introduction to the basics of Tableview.  This assumes that you have tableview installed and up to date.

Create a TableView
------------------
The heart of the Tableview library is the ``TableView`` object.  It represents a shallow view of any tabular data.  To create one, pass some tabular data to its constructor::

  d = [['Name', 'Age', 'Drink', 'Color'], \
           ['Ryan', 30, 'Tea', 'Purple'], \
           ['Michael', 31, 'Coffee', 'Blue'], \
           ['Keith', 40, 'Tea', 'Maroon'], \
           ['Brent', 26, 'Coffee', 'Blue'], \
           ['Craig', '??', 'Bourbon', 'Turquoise']]

  table = tableview.TableView(d)

.. admonition:: Example Context

   From here on, if you see ``table``, assume that it is a fresh ``TableView`` object that represents the data above.

Pretty Printing
---------------
The ``pretty()`` method returns a pretty string for a ``TableView``::
  
  >>> print table.pretty()
  Name    Age Drink     Color 
  Ryan    30  Tea       Purple
  Michael 31  Coffee    Blue  
  Keith   40  Tea       Maroon
  Brent   26  Coffee    Blue  
  Craig   ??  Bourbon    Turquoise

Rows and Columns
----------------
Views are indexed by by row, just like a 2D list ::

  >>> print table[0].pretty()
  Name Age Drink Color

But to make operations symmetrical between rows and columns, the ``rows`` and ``cols`` properties are provided.  They work just like you think::

  >>> print table.rows[0].pretty()
  Name Age Drink Color
  >>> print table.cols[0].pretty()
  Name
  Ryan
  Michael
  Keith
  Brent
  Craig

.. admonition:: Row Notation

  From here on, the ``table.rows[]`` notation will be used, but any such operation can be done using the ``table[]`` notation.  They are equivalent.



Removing Data from a View
-------------------------
You can delete a row or column from a view using the standard ``del`` operator::

  del table.rows[0] 

The same operation works on columns::
 
  del table.cols[1]

Looking at the data now, we see there are no column headers, and the Age column has been removed::

  >>> print table.pretty()
  Ryan    Tea       Purple
  Michael Coffee    Blue  
  Keith   Tea       Maroon
  Brent   Coffee    Blue  
  Craig   Bourbon   Turquoise

It is important to remember that we haven't modified the source data.  Row and column operations only affect the view itself.  We can create a new view from the data, and take a look at it::
  
  >>> table2 = tableview.TableView(d)
  >>> print table2.pretty()
  Name    Age Drink     Color 
  Ryan    30  Tea       Purple
  Michael 31  Coffee    Blue  
  Keith   40  Tea       Maroon
  Brent   26  Coffee    Blue  
  Craig   ??  Bourbon   Turquoise

Selecting Rows and Columns
--------------------------
Frequently, we want to select data based on some criteria, rather than by index.  ``select_rows`` and ``select_cols`` do just that.  Let's say we are only interested in the coffee drinkers::

  selection = table.select_rows(lambda row : row[2] == 'Coffee')

The select methods take a single callable that takes a single argument (a row or column). They return True if the row or column is to be returned in the selection.  Let's inspect our selected data::

  >>> print selection.pretty()
  Michael 31  Coffee    Blue  
  Brent   26  Coffee    Blue  

Like all operations, the same can be done with columns.  Using a fresh ``table``::

  >>> print table.select_cols(lambda col : col[0] in ('Name', 'Drink')).pretty()
  Name    Drink     
  Ryan    Tea       
  Michael Coffee    
  Keith   Tea       
  Brent   Coffee    
  Craig   Bourbon    

Selection operations return *new* tableview objects.  Our original ``TableView`` is untouched by calls to ``select_rows`` and ``select_cols``

Stripping Rows and Columns
--------------------------
Stripping works just like selecting, except that the matching rows/columns are removed from the output, rather than included.  Back to our coffee drinkers::

  >>> print table.strip_rows(lambda row : row[2] == 'Coffee').pretty()
  Name    Age Drink     Color
  Ryan    30  Tea       Purple
  Keith   40  Tea       Maroon
  Craig   ??  Bourbon   Turquoise

Tea is better for you, anyway.

Manipulating Data
-----------------
While row and column operations don't affect a ``TableView's`` source data, assignments to its members do.  Once you have the view configured to show the data you want, it can be modified.  This is the real power of Tableview::

  selection = table.select_rows(lambda row : row[2] == 'Coffee')
  for row in selection:
     row[-1] = 'Yellow'

We've singled out all the coffee drinkers, and changed their favorite color to yellow.  Remember that when we select rows, we're getting a new view of the table.  Our original ``table`` object is still a view of all the source data.  Let's inspect::
 
  >>> print table.pretty()
  Name    Age Drink     Color 
  Ryan    30  Tea       Purple
  Michael 31  Coffee    Yellow  
  Keith   40  Tea       Maroon
  Brent   26  Coffee    Yellow  
  Craig   ??  Bourbon   Turquoise

Raw Data
--------
A copy of the contents of a view can be retrieved using its ``raw`` property.  This returns *a copy* of the view's data as a list of lists::
  
  >>> table.raw
  [['Ryan', 30, 'Tea', 'Purple'], ['Michael', 31, 'Coffee', 'Blue'], ['Keith', 40, 'Diet Coke', 'Maroon'], ['Brent', 26, 'Coffee', 'Blue'], ['Craig', '??', 'Turquoise', 'Red']]

Loading Data from Disk
----------------------
If you are working with CSV or text files, data can be easily loaded from disk::
  
  table = tableview.load('data.csv')

In this case, the ``TableView`` object wasn't invoked directly.  Like any ``TableView``, we can access its source data using the ``data`` property::

  >>> print table.data
  [['Name', 'Age', 'Drink', 'Color'], ['Ryan', 30, 'Tea', 'Purple'], ['Michael', 31, 'Coffee', 'Blue'], ['Keith', 40, 'Tea', 'Maroon'], ['Brent', 26, 'Coffee', 'Blue'], ['Craig', ??, 'Bourbon', 'Turquoise']]

The ``tableview.load`` function uses the file extension to determine how to parse the file.  A .csv extension indicates comma-separated-values, and any other extension is assumed to be tab-separated text.
