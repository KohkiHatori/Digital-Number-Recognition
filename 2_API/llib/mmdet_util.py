# -*- coding: utf-8 -*
import os, sys, gc
# import datarw as d
import pandas as pd
import numpy as np
# ----
import itertools
# ----
import sys
sys.path.insert(0, "/home/ubuntu/gbr/python/adhoc_src/06_api/llib/open_mmlab/mmcv-full/1.2.0")
sys.path.insert(0, "/home/ubuntu/gbr/python/adhoc_src/06_api/llib/open_mmlab/mmdetection-2.7.0/build/lib")
import mmcv

# detection, segmentationの両方に対応
def parse_res(res, confidence_thr=0.7):
    # --------
    # init
    # --------
    if isinstance(res, tuple):
        bbox_res, seg_res = res
    else:
        bbox_res, seg_res = res, None
    # --------
    # bbox
    # --------
    bboxes = np.vstack(bbox_res)
    # --------
    # labels
    # --------
    labels = [np.full(bbox.shape[0], i, dtype=np.int32) for i, bbox in enumerate(bbox_res)]
    labels = np.concatenate(labels)
    # --------
    # threshold
    # --------
    flg = (bboxes[:, -1] > confidence_thr)
    bboxes = bboxes[flg]
    labels = labels[flg]
    # --------
    # seg
    # --------
    masks = None
    if seg_res is not None:
        masks = []
        segs = list(itertools.chain(*seg_res))
        for seg, flg2 in zip(segs, flg):
            if flg2:
                masks.append(seg)
    # --------
    # judge_df
    # --------
    cols = ["left", "top", "right", "bottom", "confidence", "cls"]
    if len(bboxes) == 0:
        outdf = pd.DataFrame(columns=cols)
    else:
        df1 = pd.DataFrame(bboxes)
        df2 = pd.DataFrame(labels)
        outdf = pd.concat([df1, df2], axis=1)
        outdf.columns = cols
    gc.collect()
    return outdf, masks


def get_base_cfg(mmdet_config_fpath, cls_num):
    cfg = mmcv.Config.fromfile(mmdet_config_fpath)
    if "cascade_rcnn" in mmdet_config_fpath:
        # bbox
        cfg = mmcv.Config.fromfile(mmdet_config_fpath)
        cfg.model.roi_head.bbox_head[0].num_classes = cls_num
        cfg.model.roi_head.bbox_head[1].num_classes = cls_num
        cfg.model.roi_head.bbox_head[2].num_classes = cls_num
    elif "mask_rcnn" in mmdet_config_fpath:
        # iseg(mask)
        cfg.model.roi_head.bbox_head.num_classes = cls_num
        cfg.model.roi_head.mask_head.num_classes = cls_num
    elif "htc" in mmdet_config_fpath:
        # iseg(htc)
        cfg.model.bbox_head[0].num_classes = cls_num
        cfg.model.bbox_head[1].num_classes = cls_num
        cfg.model.bbox_head[2].num_classes = cls_num
        # ----
        cfg.model.mask_head[0].num_classes = cls_num
        cfg.model.mask_head[1].num_classes = cls_num
        cfg.model.mask_head[2].num_classes = cls_num
    return cfg
