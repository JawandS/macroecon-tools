# Upload to pypi (export PYPI_USERNAME=<username> PYPI_TOKEN=<password>)
twine upload -r pypi dist/* -u $PYPI_USERNAME -p $PYPI_TOKEN
# Change the local package
pip install --upgrade macroecon_tools
