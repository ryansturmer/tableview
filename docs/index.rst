.. Tableview documentation master file, created by
   sphinx-quickstart on Wed Feb 20 19:43:26 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tableview : Tabular Data Manipulation
=====================================

.. toctree::
   :maxdepth: 2

Tableview is a python library for loading, manipulating and presenting tabular data.  The heart of the Tableview library is the TableView object, which presents a view of a tabular dataset that can be indexed, sliced, sorted, searched and filtered.  The power of the Tableview library lies in its ability to create multiple "shallow" views of the same dataset, which can be manipulated separately, to affect the source dataset.

::

  >> source_data = [['Character','Actor','Rank','Position'],
                    ['Jean-Luc Picard','Patrick Stewart','Captain', 'Commanding Officer'],
                    ['William Riker', 'Jonathan Frakes', 'Commander', 'First Officer'],
                    ['Geordi LaForge', 'Levar Burton', 'Lieutenant', 'Chief Engineer'],
                    ['Data','Brent Spiner', 'Lieutenant Commander', 'Science Officer'],
                    ['Worf','Michael Dorn', 'Lieutenant', 'Tactical Officer'],
                    ['Natasha Yar', 'Denise Crosby', 'Lieutenant', 'Security Chief']]

  >> print table.pretty()

  Character       Actor           Rank                 Position          
  Jean-Luc Picard Patrick Stewart Captain              Commanding Officer
  William Riker   Jonathan Frakes Commander            First Officer     
  Geordi LaForge  Levar Burton    Lieutenant           Chief Engineer    
  Data            Brent Spiner    Lieutenant Commander Science Officer   
  Worf            Michael Dorn    Lieutenant           Tactical Officer  
  Natasha Yar     Denise Crosby   Lieutenant           Security Chief    

  >> lieutenants = table.select_rows(lambda row : row[2] == 'Lieutenant')
  
  >> print lieutenants.pretty()

  Geordi LaForge Levar Burton  Lieutenant Chief Engineer  
  Worf           Michael Dorn  Lieutenant Tactical Officer
  Natasha Yar    Denise Crosby Lieutenant Security Chief  

  >> for row in lieutenants:
        row[2] = 'Lieutenant Commander'

  >> print table.pretty()

  Character       Actor           Rank                 Position          
  Jean-Luc Picard Patrick Stewart Captain              Commanding Officer
  William Riker   Jonathan Frakes Commander            First Officer     
  Geordi LaForge  Levar Burton    Lieutenant Commander Chief Engineer    
  Data            Brent Spiner    Lieutenant Commander Science Officer   
  Worf            Michael Dorn    Lieutenant Commander Tactical Officer  
  Natasha Yar     Denise Crosby   Lieutenant Commander Security Chief    


