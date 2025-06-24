@ECHO OFF
pushd %~dp0

echo Please check that you have the following done:
echo.
echo ### Increment the version number
echo   - check the [semantic versioning rules](https://semver.org/) (- [french version](https://semver.org/lang/fr/))
echo     - Use 4th number (_._.\_.X) for minor changes that don't impact code (typo, description, readme ...)
echo   - Increment the package/realease version number in `/egs-api/api/__init__.py` (mandatory)
echo     - change the codename if the major version changes (X._._)
echo     - increase the codename if the minor version changes (_.X._)

echo ### release a new version on GitHub
echo   - commit the changes
echo   - push the changes
echo   - create a [new release on GitHub](https://github.com/LaurentOngaro/egs-api-py/releases/new)
echo     - create a new tag on GitHub using the new version number
echo     - set the release title as the codename in `/egs-api-py/__init__.py`
echo     - add a description (extract from commit messages)
echo   - publish the release

cd ..
set root_folder=%cd%
set python_folder=E:/Apps/Python
set pip_install=%python_folder%/Scripts/pip install

echo root_folder = %root_folder%
%python_folder%/python --version
pause

set relaunched=0
:build
echo #################
echo Building dist...
echo #################
pause
cd %root_folder%
if exist dist (
  rmdir dist /S /Q
)
%python_folder%/python.exe setup.py sdist bdist_wheel
if %errorlevel% neq 0 (
    if %relaunched% neq 0 (
      echo setup.py execution can not be fixed. Please check the console log and try to fix it manually
      goto end
    )
    echo An issue occurred when running setup.py. Try to fix by installing some modules...
    set relaunched=1
    %pip_install% --ignore-installed setuptools
    %pip_install% --ignore-installed wheel
    %pip_install% --ignore-installed sdist
    %pip_install% --ignore-installed requirements-parser
    goto build
)

set relaunched=0
:dist
echo #################
echo Check dist...
echo #################
cd %root_folder%
twine check dist/*
if %errorlevel% neq 0 (
    if %relaunched% neq 0 (
      echo twine execution can not be fixed. Please check the console log and try to fix it manually
      goto end
    )
    echo An issue occurred when running twine. Try to fix by installing some modules...
    set relaunched=1
    %pip_install% --ignore-installed twine
    goto dist
)

echo.
echo Please check that you have no error in the previous step before continuing
echo.
pause

echo #################
echo Uploading dist...
echo #################
twine upload dist/*

:end
popd
