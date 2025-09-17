"""
Digit Detection and Recognition Module

This module contains the Prediction_maker class which processes images through
the trained Cascade R-CNN model to detect and recognize digits from alcohol
detector displays.
"""

import sys
sys.path.insert(0, "llib/open_mmlab/mmdetection-2.7.0/build/lib")
import llib.mmdet_util
from mmdet.apis.inference import inference_detector

class Prediction_maker:

    def __init__(self, image_data, model, cls_nms, confidence=0.5):
        """
        Initialize the prediction maker.

        Args:
            image_data: Input image data (OpenCV format)
            model: Trained MMDetection model
            cls_nms: Class names list [".", "0", "1", ..., "9"]
            confidence: Confidence threshold for detection (default: 0.5)
        """
        self.image_data = image_data
        self.model = model
        self.cls_nms = cls_nms
        self.cls_nms[0] = "."  # Ensure first class is decimal point
        self.confidence = confidence


    def convert_to_numbers(self, resdf):
        """
        Convert detected bounding boxes to a number string.

        This method sorts detected digits spatially and concatenates them
        into a readable number string. It handles both horizontal and
        vertical digit arrangements.

        Args:
            resdf: DataFrame containing detection results with bounding boxes

        Returns:
            str: Concatenated string of detected digits
        """
        # Sort by vertical position first
        resdf_by_y = resdf.sort_values("top")
        diff = resdf_by_y.iloc[-1]["top"] - resdf_by_y.iloc[0]["top"]

        # Choose sorting strategy based on layout
        if diff < 0:  # Horizontal layout
            resdf = resdf.sort_values("right")
        else:  # Vertical layout
            resdf = resdf.sort_values("left")

        # Concatenate detected class names into number string
        res_in_str = "".join([str(self.cls_nms[cls_ind]) for cls_ind in resdf["cls"]])
        return res_in_str

    def main(self):
        """
        Main prediction pipeline.

        Processes the input image through the ML model to detect and recognize
        digits, then converts the results to a readable number string.

        Returns:
            str: Detected number string from the alcohol detector display
        """
        # Run model inference
        res = inference_detector(self.model, self.image_data)

        # Parse detection results with confidence filtering
        resdf, _ = llib.mmdet_util.parse_res(res, confidence_thr=self.confidence)

        # Convert detections to number string
        result = self.convert_to_numbers(resdf)

        return result
