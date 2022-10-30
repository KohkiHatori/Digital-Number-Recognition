import sys
sys.path.insert(0, "llib/open_mmlab/mmdetection-2.7.0/build/lib")
import llib.mmdet_util
from mmdet.apis.inference import inference_detector

class Prediction_maker:

    def __init__(self, image_data, model, cls_nms, confidence=0.5):
        self.image_data = image_data
        self.model = model
        self.cls_nms = cls_nms
        self.cls_nms[0] = "."
        self.confidence = confidence


    def convert_to_numbers(self, resdf):
        resdf_by_y = resdf.sort_values("top")
        diff = resdf_by_y.iloc[-1]["top"] - resdf_by_y.iloc[0]["top"]
        if diff < 0:
            resdf = resdf.sort_values("right")
        else:
            resdf = resdf.sort_values("left")
        res_in_str = "".join([str(self.cls_nms[cls_ind]) for cls_ind in resdf["cls"]])
        return res_in_str

    def main(self):
        """
        @para: 
        1.image_data: 生の画像データ
        2.path_to_model: Dockerコンテナの中のモデルへのパス
        @return:
        画像から読み取られた数字のstring
        """ 
        res = inference_detector(self.model, self.image_data)
        resdf, _ = llib.mmdet_util.parse_res(res, confidence_thr=self.confidence)
        result = self.convert_to_numbers(resdf)
        return result




