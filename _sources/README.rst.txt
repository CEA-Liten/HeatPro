Make documentation
==================

To make the documentation:

Install required packages:

.. code-block:: shell

   poetry install --with doc

Go to the `docs` folder:

.. code-block:: shell

   cd docs

Build the documentation in HTML format:

.. code-block:: shell

   poetry run sphinx-build -M html . _build

Open the `docs/_build/html/index.html` file.


