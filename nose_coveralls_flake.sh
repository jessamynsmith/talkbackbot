#!/bin/bash

# This script exists because tox only reports errors if a single command is specified

return_code=0

flake8
return_code=${return_code/#0/$?}

coverage run -m nose
return_code=${return_code/#0/$?}

coveralls
return_code=${return_code/#0/$?}

exit $return_code
