"""Main goal: Extract correct ROI from image using darsia.CurvatureCorrection.

For this, we use a graphical assistant (only for interactive use). We learn how to
reuse the output of the graphical assistant. For this one boolean flag has to be
redefined - see below.

"""

# ! ---- IMPORTS ---- !

from pathlib import Path

import darsia

# ! ---- DATA MANAGEMENT ---- !

folder = None # TODO
image = None #TODO
path = Path(folder) / Path(image)

# ! ---- DARSIA IMAGES ---- !

# We allow for using a graphical assistant or to hardcode an input to define a cropping.
# The cropping requires four coordinates defining the corners of the ROI, which is
# supposed to be our 2d planar view onto the FluidFlower. The corners do not necessarily
# need to define a box.
if True:
    # Use, the graphical assistant to define the corners of the ROI.

    # Read a temporary image to define the ROI
    tmp_image = darsia.imread(path)

    # Read the instructions of the assistant in the terminal
    crop_assistant = darsia.CropAssistant(tmp_image)
    config = crop_assistant()

else:
    # Hardcode the corners of the ROI, e.g., by copying the output of the graphical
    # assistant.
    config = None # TODO

curvature_correction = darsia.CurvatureCorrection(config=config)

# Read physical image, and include the correction to extract the right ROI and giving it
#  the right physical dimensions.
darsia_image = darsia.imread(path, transformations=[curvature_correction])

# For testing purposes, double check physical dimensions
print(f"The physical dimensions of the image are: {darsia_image.dimensions} - note the use of matrix indexing.")

# For testing purposes, show the read image. NOTE: Physical coordinates in matplotlib!
darsia_image.show()

# We can also extract subregions directly from DarSIA.Image objects. The major
# difference compared to the correction is, the subregion has phsyically meaningful
# dimensions, and we can also use physically coordinates to extract such subregion!
coordinates = None # TODO
darsia_image_subregion = darsia_image.subregion(coordinates=coordinates)

# Again, we plot the subregion for testing purposes.
darsia_image_subregion.show()

# For testing purposes, double check physical dimensions
print(f"For the subregion, the physical dimensions of the image are: {darsia_image_subregion.dimensions} - note the use of matrix indexing.")
