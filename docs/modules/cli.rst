.. _cli:

Command Line Interface
======================



.. contents::
    :backlinks: entry

How to use:
-----------

To use the command line interface, you need to install ``heatpro`` with ``cli`` option:

::

    pip install heatpro[cli]

You can get help on how to use cli by using:

::

    heatpro cold -h

::

    Usage: heatpro cold [OPTIONS] WEATHER_CSV OUTPUT_CSV YEAR_ENERGY_REFERENCE

    Options:
    --set-temperature FLOAT         Default set temperature
    --loss FLOAT                    Cold energy loss
    -fws, --full-week-share FLOAT   Share of cold energy consummed following a
                                    full week activity profile
    -fwts, --full-week-temperature-sensitivity FLOAT
                                    Share of cold energy within consumption
                                    associated to full week profile consummed in
                                    a temperature sensitive manner
    -wets, --week-end-temperature-sensitivity FLOAT
                                    Share of cold energy within consumption
                                    associated to low activity on weekend
                                    profile consummed in a temperature sensitive
                                    manner
    -start, --date-start TEXT       date start
    -end, --date-end TEXT           date end
    -v, --verbose                   Enable debug logging
    -s, --show                      Show graphs of the result
    -h, --help                      Show this message and exit.

Base example will be:

::

    heatpro cold ./input/weather.csv ./output/results.csv H2

where ``./input/weather.csv`` is a CSV file that look like this:

::

    "timestamp_utc_num";"temperature";
    978307200;5,1
    978310800;5,1
    978314400;5

Results will be written in ``output/results.csv``.

.. note::

    ``YEAR_ENERGY_REFERENCE`` can be a numeric value (energy expressed in kWh) but it can also be 'H1','H2' or 'H3'. It will then used numeric values for :class:`ReferenceCold` (see :ref:`helpers-section`)

.. automodule:: heatpro.cli
    :members:
    :undoc-members:
    :show-inheritance:

To filter calculation on a smaller sample, you can use ``-start`` and ``-end`` to filter on a smaller period. For instance, if my CSV weather file contains years from 2000 to 2199, using

::

    heatpro cold ./input/weather.csv ./output/results.csv H2 -start 2005 -end 2010

Will calculate demand from beginning of 2005 to ending of 2009. It is usefull to launch short testing calculation.

you can use it with ``-s`` flag to display graphs of the calculation.

Cold
----

.. automodule:: heatpro.cli.cold
    :members:
    :undoc-members:
    :show-inheritance:

.. _helpers-section:

Helpers
-------
.. automodule:: heatpro.cli.helpers
    :members:
    :undoc-members:
    :show-inheritance:

Plotting
--------
.. automodule:: heatpro.cli.plotting
    :members:
    :undoc-members:
    :show-inheritance: