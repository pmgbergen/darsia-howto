"""Main goal: Apply relative corrections as part of image definition.

"""

# ! ---- IMPORTS ---- !

from pathlib import Path

import cv2
import darsia
import matplotlib.pyplot as plt
import numpy as np
import skimage

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
pts_cc = [[4291, 56], [5283, 740]]
drift_correction = darsia.DriftCorrection(baseline_darsia_image, roi=pts_cc)

# Assume we have successfully defined our geometry correction.
# Thus, the curvature correction has to base on the baseline
# image we
curvature_correction_config = {
    "crop": {
        "width": 0.899,
        "height": 0.55,
        "pts_src": [
            [96.239979445015479, 127.92754367934231],
            [96.239979445015479, 3017.958376156218],
            [5345.9830421377201, 2997.4033915724563],
            [5350.094039054472, 115.59455292908524],
        ],
    }
}
curvature_correction = darsia.CurvatureCorrection(config=curvature_correction_config)

# Read physical image, and include the correction to extract the right ROI and giving it
#  the right physical dimensions. Extract immediately a subregion.
coordinates = [[0.0, 0.0], [0.899, 0.5]]
darsia_image = darsia.imread(
    path, transformations=[drift_correction, curvature_correction]
).subregion(coordinates=coordinates)

# Repeat the same for the baseline image to have a baseline image with the same
# physical dimensions.
darsia_baseline_image = darsia.imread(
    baseline_path, transformations=[drift_correction, curvature_correction]
).subregion(coordinates=coordinates)

# ! ---- Concentration analysis ---- !

# Define signal reduction
signal_reduction = darsia.MonochromaticReduction(color="negative-key")

# Define restoration/upscaling object - coarsen, tvd, resize
original_shape = darsia_image.shape[:2]
restoration = darsia.CombinedModel(
    [
        darsia.Resize(resize=0.5),
        darsia.TVD(method="isotropic bregman", weight=0.1, eps=1e-4, max_num_iter=100),
        darsia.Resize(shape=original_shape),
    ]
)

# Define conversion routine
if True:
    # We use a threshold model, i.e., we cut off values lower than a certain value.
    # Do not look at the messy definition of the model - it will be improved in the future.
    threshold_parameter = 0.1  # Only have a look here!
    model = darsia.ThresholdModel(
        labels=None, key="", **{"threshold value": threshold_parameter}
    )
else:
    model = darsia.CombinedModel(
        [
            darsia.LinearModel(key="model ", **self.config["tracer"]),
            darsia.ClipModel(**{"min value": 0.0, "max value": 1.0}),
        ]
    )

# Define the verbosity level. verbosity controls how much output is generated during
# the analysis. The higher the value, the more output is generated. A zero value
# means no output.
verbosity = 5

concentration_analysis = darsia.ConcentrationAnalysis(
    base=darsia_baseline_image,
    signal_reduction=signal_reduction,
    restoration=restoration,
    model=model,
    verbosity=verbosity,
)

# Extract concentration and plot the result
concentration = concentration_analysis(darsia_image)
concentration.show()

# Plot both images side by side - not nicely implemented in DarSIA

# Start with the original image
# original_img = np.clip(np.copy(darsia_image.img), 0, 1)
original_img = skimage.img_as_ubyte(darsia_image.img)

# Overlay the original image with contours for CO2
contours, _ = cv2.findContours(
    skimage.img_as_ubyte(concentration.img), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
)
cv2.drawContours(original_img, contours, -1, (0, 255, 0), 5)

# Plot
plt.figure("Image with contours of detected fluid")
plt.imshow(original_img)
plt.show()

# Integrate the concentration over the whole image
shape_meta = concentration.shape_metadata()
depth = 0.02
geometry = darsia.ExtrudedGeometry(depth, **shape_meta)
concentration_integrated = geometry.integrate(geometry)
print(
    f"At time {concentration_integrated.time} the integrated volume is: {concentration_integrated} m**3."
)
