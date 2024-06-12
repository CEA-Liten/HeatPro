<div style="text-align:center">
<img style="height: 5cm;" alt="HeatPro App logo" src=docs/logo/heatpro_logo.png>
</div>

[![PyPI Version](https://img.shields.io/pypi/v/heatpro.svg)](https://pypi.python.org/pypi/heatpro)
[![pages-build-deployment](https://github.com/CEA-Liten/HeatPro/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/CEA-Liten/HeatPro/actions/workflows/pages/pages-build-deployment)
[![License](https://img.shields.io/badge/License%20-%20CeCILL_B-red)](http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html)

The present package finds its roots in the need of using representative heating load curve for the simulation and optimization of various District Heating Network (DHN) production plant. The main principle is to disagreggate monthly or yearly heat load into an hourly heat load using an hourly based external temperature profile. The resulting load curve also includes DHN supply and return temperatures.

This package was used for the study of a production plant combining Power-to-Heat, Biomass and Storage ([Lamaison et al., 2019](https://doi.org/10.1016/j.energy.2019.07.044)). It was also the tool used to generate various heat load curves in a study of long term storage management ([Cuisinier et al., 2022](https://doi.org/10.1016/j.energy.2021.122773)).

More recently, it was used in a collaboration between RTE and CEA with the aim of representing DHN in the RTE tool Antares. The final objective was to study the additional flexibility offered by DHN to the electrical grid.

------------

    ├── .gitignore                  <- Specifies files and directories that should be ignored by Git during version control.
    ├── .gitlab-ci.yml              <- Configuration file for Gitlab CI, a continuous integration service.
    ├── AUTHORS.rst                 <- A file listing the authors of the project.
    ├── CONTRIBUTING.rst            <- Guidelines for contributing to the project.
    ├── HISTORY.rst                 <- A file documenting the project's version history and changelog.
    ├── README.md                   <- The main documentation file providing an overview and usage instructions for the project.
    ├── poetry.lock                 <- Dependency lock file which ensures consistent and repeatable installations of project dependencies.
    ├── pyproject.toml              <- Configuration file used to specify project metadata, dependencies, build requirements, and other settings.
    ├── requirements_dev.txt        <- A file listing development dependencies for the project.
    ├── .gitlab                     <- Directory containing GitLab-specific files.
    │   └── issue_templates         <- Folder containing template for creating new issue reports on GitLab.
    │       └── ISSUE_TEMPLATE.md       <- Template for creating new issue reports.
    ├── docs                        <- Directory containing documentation files.
    │   ├── authors.rst             <- Authors documentation.
    │   ├── conf.py                 <- Configuration file for Sphinx, a documentation generator.
    │   ├── contributing.rst        <- Contributing guidelines documentation.
    │   ├── history.rst             <- History and changelog documentation.
    │   ├── index.rst               <- Main documentation index file.
    │   ├── installation.rst        <- Installation documentation.
    │   ├── make.bat                <- Batch file for building documentation on Windows.
    │   ├── Makefile                <- Makefile for building documentation.
    │   ├── readme.rst              <- Readme documentation.
    │   └── usage.rst               <- Usage documentation.
    ├── heatpro                     <- Package directory for the main project code.
    └── tests                       <- Directory containing test files.


## To install

```shell
pip install heatpro
```

- Documentation: [https://heat-load-profile-generator.readthedocs.io](https://heat-load-profile-generator.readthedocs.io)



