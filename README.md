# assetallocation_arp

sist[3~[3~[3~[3~[3~

## Setup
1. Install git and checkout the [git code repository]
    *  https://confluence/display/PYTH/Setting+up+Git+and+Git+Remote+Repository
2. Install [anaconda] python version 3.6+
    * https://confluence/display/PYTH/Installing+Python
    for setting up python paths, please refer to
    * https://confluence/display/PYTH/Windows+Python+packages+installer
3. Change working directory into the git code repository root

4. Install python packages required using

   `pip install --upgrade <package_name> -i http://n00-buildtools:8081/nexus/repository/pypi.org-proxy/simple/ --trusted-host n00-buildtools `

   The above command points to nexus repository which mirrors the python packages in pypi
   
   you can set the python path directly from the console, within notebooks, test scripts
    etc. From Pycharm you can also right click the assetallocation_arp folder and select the _Mark Directory As | Source Root_ option.


5. .. Place your own project specific setup steps here e.g. document on sources, models etl etc, copying data files ...

When distributing your module, you can create a source distribution or Python egg or whl file with the command `python setup.py sdist bdist_egg bdist_whl` and upload the .egg or .whl files.

## Using the Python virtualenv environment

Once the Python Conda environment has been set up, you can

* Activate the environment using the following command in a terminal window:

  * Windows: `virtualenv my_environment; source my_environment/Scripts/activate`
  * The __environment is activated per terminal session__, so you must activate it every time you open terminal.

* Deactivate the environment using the following command in a terminal window:

  * Windows: `deactivate`

## Initial File Structure

```
├── .gitignore               <- Files that should be ignored by git. Add seperate .gitignore files in sub folders if 
│                               needed
├── LICENSE
├── README.md                <- The top-level README for developers using this project.
├── requirements.txt         <- The requirements file for reproducing the analysis environment, e.g.
│                               generated with `pip freeze > requirements.txt`. Might not be needed if using conda.
├── setup.py                 <- Metadata about your project for easy distribution.
│
├── data│
│   ├── processed            <- The final, canonical data sets for modeling.
│   ├── raw                  <- The original, immutable data dump.
│   └── temp                 <- Temporary files.
│
├
├── notebooks                <- Experimental code in Notebooks for analysis and testing
│   ├── eda                  <- Notebooks for EDA
│   │   └── example.ipynb    <- Example python notebook
│   ├── features             <- Notebooks for generating and analysing features (1 per feature)
│   ├── modelling            <- Notebooks for modelling
│   └── preprocessing        <- Notebooks for Preprocessing 
│
├── scripts                  <- Standalone scripts
│   └── example.py           <- Example script
│
│   └── assetallocation_arp       <- Code for use in this project.Example python package - place shared code in such a package
│               ├── __init__.py      <- Python package initialisation
│               ├──  data_etl   <- I/o functionality code
                    ├──  __init__.py   <- module initialization
│               ├── models     <- model functionality code
│               ├── visualization            <- visualization if needed
│
└── tests                    <- Test cases (named after module)
    └── assetallocation_arp       <- assetallocation_arp tests
        ├──  test_hello_world.py   <- examplemodule tests (1 file per method tested)
        ├── test_etl.py         <- data_etl tests
        ├── test_model.py       <- test the model
        └── test_utils         <- test the utilities
```

## Testing
Reproducability and the correct functioning of code are essential to avoid wasted time. If a code block is copied more 
than once then it should be placed into a common script / module under assetallocation_arp and unit tests added. The same applies for
any other non trivial code to ensure the correct functioning.

More details on unit testing can be found in
 * https://confluence/pages/viewpage.action?pageId=111156820

To run tests, install pytest using pip in Step 4 and
then from the repository root run
 
```
pytest
```

On Windows this will run the make.bat, a Makefile is also included for those using the 'make' command.

## Development Process
You are now ready to get started, however you should first create a new github repository for your new project and add your
project using the following commands (substitute myproject with the name of your project and REMOTE-REPOSITORY-URL
with the remote repository url).

    cd myproject
    git init
    git add .
    git commit -m "Initial commit"
    git remote add origin root@gogs-ose-btprod.inv.adroot.lgim.com:<project_organisation_in_gogs/repo_name_in_gogs.git>
    git remote -v
    git push origin master

Its always good practice to work on a branch
    git checkout -b <branch_name>  #creates the branch locally and checks out in your local repo
    git add <files/direcorites/.)
    git commit -m ""
    git push -u origin <branch_name>

### Continuous Integration
Continuous Integration (CI) increase quality by building, running tests and performing other validation whenever
code is committed. The template contains a build pipeline in Jenkins, this is just a sample template which will change in future
after the deveops has created a jenkins for the project.
Once you commit the code, the CI pipeline will automatically triggered by the Jenkins file. Unit testing, integration testing,
code quality checks will be performed automatically. The results will be shown in Jenkins dashboard.

You are now setup for CI and automated test / building. This is work under progress individual projects will have a Jenkins jobs of their own

### test generation
create tests for your code

##

## References
* http://docs.python-guide.org/en/latest/writing/structure/
* https://drivendata.github.io/cookiecutter-data-science/

[//]: #
   [anaconda]: <https://www.continuum.io/downloads>