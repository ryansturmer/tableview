tables.py

A simple python module for loading, manipulating and saving data from text files.

```python

import tables

table = tables.load('example.csv')

print table.pretty()

first_three_rows = table.rows[:3]
first_three_cols = table.cols[:3]

intersection = table.rows[:3].cols[:3]

print intersection.pretty()

```
