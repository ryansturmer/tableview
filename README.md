Tableview
=========

A simple python module for manipulating tabular data.

Quick Example
-------------
```python

import tableview

table = tableview.load('example.csv')

print table.pretty()

first_three_rows = table.rows[:3]
first_three_cols = table.cols[:3]

intersection = table.rows[:3].cols[:3]

print intersection.pretty()

```

Running the Tests
-----------------

If you are a developer, running the unit tests requires pytest.  With pytest installed, execute ``py.test`` in the top level directory.


