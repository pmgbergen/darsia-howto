"""Main goal: Apply relative corrections as part of image definition.

"""

# ! ---- IMPORTS ---- !

from pathlib import Path

import darsia

# ! ---- DATA MANAGEMENT ---- !

# Define two image: baseline image and 'current' image (here an injection image).

baseline_folder = None # TODO
baseline_image = None # TODO
baseline_path = Path(baseline_folder) / Path(baseline_image)

folder = None # TODO
image = None # TODO
path = Path(folder) / Path(image)

# ! ---- BASELINE IMAGE ---- !
baseline_darsia_image = darsia.imread(baseline_path)

# ! ---- DARSIA IMAGES ---- !

# First correction - drift correction: This image will be used as reference to
# align other images through pure translation wrt some chosen ROI - e.g.
# the color checker.

# Define ROI corresponding to colorchecker
if True:
    # Use assistant
    point_selector = darsia.PointSelectionAssistant(baseline_darsia_image)
    pts_cc = point_selector()
else:
    pts_cc = None # TODO
drift_correction = darsia.DriftCorrection(baseline_darsia_image, roi = pts_cc)

# Assume we have successfully defined our geometry correction.
# Thus, the curvature correction has to base on the baseline
# image we
curvature_correction_config = None # TODO
curvature_correction = darsia.CurvatureCorrection(config=curvature_correction_config)

# NOTE: Curvature correction only meaningful, if pts_src correct. Thus, we need to apply a drift correction.

# Read physical image, and include the correction to extract the right ROI and giving it
#  the right physical dimensions.
darsia_image = darsia.imread(
    path, transformations=[drift_correction, curvature_correction]
)
darsia_image.show()

# We can also extract subregions directly from DarSIA.Image objects. The major
# difference compared to the correction is, the subregion has phsyically meaningful
# dimensions, and we can also use physically coordinates to extract such subregion!
coordinates = None # TODO
darsia_image_subregion = darsia_image.subregion(coordinates=coordinates)

# Again, we plot the subregion for testing purposes.
darsia_image_subregion.show()
