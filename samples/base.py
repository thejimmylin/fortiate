import os
import sys
"""
In case fortiate is not installed as a package and is added to the $PYTHONPATH
we add it to sys.path manually here. If fortiate has been added to your
$PYTHONPATH already, this could be skipped.
"""
fortiate_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
)
sys.path.insert(1, fortiate_path)
"""
The above sys things could be skipped if you add fortiate to the $PYTHONPATH.
"""
from fortiate.commands import *  # NOQA
from fortiate.configs import *  # NOQA
