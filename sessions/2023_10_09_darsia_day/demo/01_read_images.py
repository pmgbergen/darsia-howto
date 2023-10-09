"""Main goal: Read images from file to DarSIA.

Also: Try to understand some of the basics how to use Python and DarSIA.

"""

# ! ---- IMPORTS ---- !

# Import necessary directories:
# Most importantly, import DarSIA:
import darsia

# A useful library is pathlib, which allows to convert paths to the required format on your local machine.
# In order to use pathlib, paths need to be used together with "Path", e.g., instead of "folder/image.png",
# use "Path(folder/image.png")
from pathlib import Path

# ! ---- DATA MANAGEMENT ---- !

# Define directory containing images
folder = None # TODO

# Define image
image = None # TODO

# Define path in correct format
path = Path(folder) / Path(image)

# ! ---- DARSIA IMAGES ---- !

# Define physically meaningful dimensions
width = None # TODO
height = None # TODO

# Read physical image
darsia_image = darsia.imread(path, width = width, height = height)

# For testing purposes, show the read image
darsia_image.show()
