## Python-CICD
## Steps 1: ##
create project in github
alwasy create with Virtual Environment
# 1. Create virtual environment:
#    python -m venv venv
# 2. Activate environment:
#    source venv/bin/activate (Linux/Mac)
#    venv\Scripts\activate (Windows)


## Steps 2: ##
create folder
a) src
b) tests
c)create manually -> requirements.txt or pip freeze requirements.txt
# 3. Install requirements:
#    pip install -r requirements.txt
# 4. For development:
#    pip install -r requirements-dev.txt


## Steps 3.1: execute setup.py##
Purpose: Installs the package in development mode (linked to source code).
When to use:
During active development (no reinstall needed after code changes).
When testing CLI tools defined in entry_points.

pip install -e .     =>It create Python_CICD.egg-info

.egg-info Directory
Creates a <package_name>.egg-info folder in your project root.
Contains metadata like:
PKG-INFO (package name, version, dependencies).
SOURCES.txt (list of included files).
dependency_links.txt (if any).


## Steps 3.2: execute setup.py##
Purpose: Builds distribution packages for sharing/uploading.
When to use:
When preparing to upload to PyPI or share the package.
To generate pre-built binaries (wheels) for faster user installations.

python setup.py sdist bdist_wheel
it will create
sdist (Source Distribution)
dist/<package_name>-<version>.tar.gz

and It will create

bdist_wheel (Built Distribution)
dist/<package_name>-<version>-<python_tag>-<abi_tag>-<platform_tag>.whl
dist/my_package-1.0.0-py3-none-any.whl
py3: Supports Python 3.
none: No ABI (Application Binary Interface) requirements.
any: Works on any platform (Linux, Windows, macOS).

## Steps 3.3: execute setup.py##
python setup.py install
Purpose: Installs the package permanently into the Python environment (non-editable).
When to use:
For production deployments where you want a static, immutable install.
To test how the package behaves when installed as a user would see it.

Key Comparison Table
Command	                           Purpose                        Output Location        Editable?    Recommended For
python setup.py install            Permanent install              site-packages/         ❌           Production deployments
pip install -e .                   Development install           .egg-link + source dir  ✅           Local development
python setup.py sdist bdist_wheel  Create distributable files     dist/                  ❌           Releasing/PyPI uploads




