"""
This file is used for importing all the foriate things, so other .py file in
samples could import foriate things from here

In case fortiate is not installed as a package and is added to the $PYTHONPATH
we add it to sys.path manually here. If fortiate has been added to your
$PYTHONPATH already, the sys things below could be skipped.
"""
import os
import sys
fortiate_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)
sys.path.insert(1, fortiate_path)

from fortiate.commands import *  # NOQA
from fortiate.configs import *  # NOQA
