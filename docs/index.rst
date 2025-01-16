Welcome to the EnAcuity Coding Challenge's documentation!
=================================================

Source code is available at `enAcuity-coding-challenge <https://github.com/solenedietsch/enAcuity-coding-challenge>`_.
.. toctree::
    :maxdepth: 2
   api

Overview
--------

This project is a coding challenge focused on building an **interactive
application** for analysing surgical videos. The application is designed
to perform **frame-by-frame analysis** and support **real-time
processing** for in-depth exploration of surgical procedures.

Features
--------

-  **Frame-by-frame video analysis**: Allows users to step through each
   frame of a surgical video.
-  **Real-time processing**: Provides an efficient interface for
   real-time surgical video review.
-  **Simple and interactive GUI**: Built using ``PySimpleGUI`` for a
   user-friendly experience.

Prerequisites
-------------

Ensure you have the following installed on your machine:

1. **Python 3.9+**
2. ``pip`` for installing Python packages

Installation Instructions
-------------------------

1. Clone the repository
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   git clone https://github.com/solenedietsch/enAcuity-coding-challenge
   cd enAcuity-coding-challenge

2. Set up a virtual environment (optional but recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate

3. Install dependencies
~~~~~~~~~~~~~~~~~~~~~~~

The project requires ``PySimpleGUI`` and other libraries for video
processing. Run the following command:

.. code:: bash

   pip install -r requirements.txt

Running the Application
-----------------------

Once the setup is complete, you can run the application with the
following command:

.. code:: bash

   python app.py

Usage Instructions
------------------

1. **Start the application**: Launch the GUI by running ``main.py``.
2. **Load video**: Use the file picker to load a video from the Cholec80
   dataset.
3. **Frame controls**:

   -  Navigate frame-by-frame using the provided buttons.
   -  Pause and play for real-time processing.

4. **Analysis Tools**: The interface provides basic real-time processing
   tools for video exploration.

Troubleshooting
---------------

If you encounter GUI issues:

-  Make sure PySimpleGUI is correctly installed.
-  Update PySimpleGUI using:
-  pip install –upgrade pysimplegui

-  Create a PySimpleGUI account: https://www.pysimplegui.com/pricing.
-  Create a Hobbyist account.

Future Enhancements
-------------------

-  Add annotation features for labeling surgical phases.
-  Integrate machine learning models for automatic event detection.

Contributing
------------

Contributions are welcome! Feel free to submit issues or pull requests.

License
-------

This project is licensed under the MIT License. See ``LICENSE`` for
details.




