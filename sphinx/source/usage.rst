How to use nz-stream-depletion
===============================

This section will describe how to use the nz-stream-depletion package.


The SD class
-------------
The SD class in the nz-stream-depletion package provides access to all of the stream depletion methods withouthaving to specify each function. You just feed in the appropriate input parameters and the SD will use the most appropriate method given the input parameters.

First we need to import the package and define some of those input aquifer parameters.


.. code:: python

  from nz_stream_depletion import SD

  # Pumped aquifer
  pump_aq_trans = 1000 # m/d
  pump_aq_s = 0.1

  # Well
  pump_q = 50 # l/s
  sep_distance = 500 # m

  time1 = 6 # days
  time2 = 7 # days
  time1 = 30 # days
  n_days = 150 # days

  # streambed
  stream_k = 1000 # m/d
  stream_thick = 1 # m
  stream_width = 1 # m
  stream_cond = stream_k * stream_thick / stream_width

  # aquitard
  aqt_k = 0.1 # m/d
  aqt_thick = 10 # m
  aqt_s = 0.1

  # upper aquifer
  upper_aq_trans = 500
  upper_aq_s = 0.05


.. ipython:: python
  :suppress:

  from nz_stream_depletion import SD
  import pandas as pd

  pd.options.display.max_columns = 5

  # Pumped aquifer
  pump_aq_trans = 1000 # m/d
  pump_aq_s = 0.1

  # Well
  pump_q = 50 # l/s
  sep_distance = 500 # m

  time1 = 6 # days
  time2 = 7 # days
  time1 = 30 # days
  n_days = 150 # days

  # streambed
  stream_k = 1000 # m/d
  stream_thick = 1 # m
  stream_width = 1 # m
  stream_cond = stream_k * stream_thick / stream_width

  # aquitard
  aqt_k = 0.1 # m/d
  aqt_thick = 10 # m
  aqt_s = 0.1

  # upper aquifer
  upper_aq_trans = 500
  upper_aq_s = 0.05

  params1 = {'pump_aq_trans': pump_aq_trans, 'pump_aq_s': pump_aq_s, 'sep_distance': sep_distance}

  params2 = {'pump_aq_trans': pump_aq_trans, 'pump_aq_s': pump_aq_s, 'sep_distance': sep_distance, 'stream_k': stream_k, 'stream_thick': stream_thick, 'stream_width': stream_width}

  params3 = {'pump_aq_trans': pump_aq_trans, 'pump_aq_s': pump_aq_s, 'sep_distance': sep_distance, 'stream_k': stream_k, 'stream_thick': stream_thick, 'stream_width': stream_width, 'aqt_k': aqt_k, 'aqt_thick': aqt_thick, 'aqt_s': aqt_s}

  params4 = {'pump_aq_trans': pump_aq_trans, 'pump_aq_s': pump_aq_s, 'sep_distance': sep_distance, 'stream_k': stream_k, 'stream_thick': stream_thick, 'stream_width': stream_width, 'aqt_k': aqt_k, 'aqt_thick': aqt_thick, 'aqt_s': aqt_s, 'upper_aq_trans': upper_aq_trans, 'upper_aq_s': upper_aq_s}

  n_days = 30

  extract_csv = 'https://raw.githubusercontent.com/mullenkamp/nz-stream-depletion/main/nz_stream_depletion/data/sample_flow.csv'


Then we need to initialize the SD class. Once the SD class is initialized, we can take a look at the all_methods attribute to see all of the emthods and the parameter requirements.


.. ipython:: python

  sd = SD()

  print(sd.all_methods)


Then we need to load the input aquifer parameters. The available methods attribute tells us what methods are available given the input parameters.


.. ipython:: python

  sd = SD()

  available = sd.load_aquifer_data(pump_aq_trans=pump_aq_trans, pump_aq_s=pump_aq_s, sep_distance=sep_distance)

  print(available)


Once the input parameters have been loaded, you can calculate the stream depletion ratios using either sd.sd_ratio for a specific number of pumping days (n_days) or sd.sd_ratios for all of the ratios up to the pumping days. It can be helpful in certain coding circumstances to put the input parameters into a dictionary before passing them to the SD class.


.. ipython:: python

  params2 = {'pump_aq_trans': pump_aq_trans, 'pump_aq_s': pump_aq_s, 'sep_distance': sep_distance, 'stream_k': stream_k, 'stream_thick': stream_thick, 'stream_width': stream_width}

  sd = SD()

  available = sd.load_aquifer_data(**params2)

  sd_ratio = sd.sd_ratio(7)
  sd_ratios = sd.sd_ratios(7)

  print(available)
  print(sd_ratio)
  print(sd_ratios)


The last bit of functionality allows you to take a time series of extraction (pumping) data and determine the amount that is stream depleting over the entire record.


.. ipython:: python

  params2 = {'pump_aq_trans': pump_aq_trans, 'pump_aq_s': pump_aq_s, 'sep_distance': sep_distance, 'stream_k': stream_k, 'stream_thick': stream_thick, 'stream_width': stream_width}

  extract_csv = 'https://raw.githubusercontent.com/mullenkamp/nz-stream-depletion/main/nz_stream_depletion/data/sample_flow.csv'

  extraction = pd.read_csv(extract_csv, index_col='time', parse_dates=True, infer_datetime_format=True, dayfirst=True).flow

  sd = SD()

  available = sd.load_aquifer_data(**params2)

  sd_rates = self.calc_sd_extraction(extraction)

  print(sd_rates)
