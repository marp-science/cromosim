# Authors:
#     Sylvain Faure <sylvain.faure@universite-paris-saclay.fr>
#     Bertrand Maury <bertrand.maury@universite-paris-saclay.fr>
#
# License: GPL

# Modified (slightly):
#    Marcin Piekarczyk <mpiekarczyk@agh.edu.pl>

name = "cromosim"

import numpy as np
import numpy as sp      # import scipy as sp
import sys
import random
import matplotlib
import matplotlib.pyplot as plt
import cvxopt

from .domain import Domain
from .domain import Destination
from . import ca
from . import ftl
from . import micro
from . import comp

from .version import version as __version__
