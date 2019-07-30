"""
Adapted from https://github.com/Cartucho/mAP
"""


import numpy as np


class _ImageDetection:
    def __init__(self, score, label, boxes, used=False):
        self.boxes = boxes
        self.label = label
        self.score = score
        self.used = used


def _voc_ap(rec, prec):
    """
     Calculate the AP given the recall and precision array
        1st) We compute a version of the measured precision/recall curve with
             precision monotonically decreasing
        2nd) We compute the AP as the area under this curve by numerical integration.

    --- Official matlab code VOC2012---
    mrec=[0 ; rec ; 1];
    mpre=[0 ; prec ; 0];
    for i=numel(mpre)-1:-1:1
            mpre(i)=max(mpre(i),mpre(i+1));
    end
    i=find(mrec(2:end)~=mrec(1:end-1))+1;
    ap=sum((mrec(i)-mrec(i-1)).*mpre(i));
    """

    rec.insert(0, 0.0) # insert 0.0 at begining of list
    rec.append(1.0) # insert 1.0 at end of list
    mrec = rec[:]
    prec.insert(0, 0.0) # insert 0.0 at begining of list
    prec.append(0.0) # insert 0.0 at end of list
    mpre = prec[:]

    """
     This part makes the precision monotonically decreasing
        (goes from the end to the beginning)
        matlab: for i=numel(mpre)-1:-1:1
                    mpre(i)=max(mpre(i),mpre(i+1));
    """

    # matlab indexes start in 1 but python in 0, so I have to do:
    #     range(start=(len(mpre) - 2), end=0, step=-1)
    # also the python function range excludes the end, resulting in:
    #     range(start=(len(mpre) - 2), end=-1, step=-1)
    for i in range(len(mpre)-2, -1, -1):
        mpre[i] = max(mpre[i], mpre[i+1])
    """
     This part creates a list of indexes where the recall changes
        matlab: i=find(mrec(2:end)~=mrec(1:end-1))+1;
    """
    i_list = []
    for i in range(1, len(mrec)):
        if mrec[i] != mrec[i-1]:
            i_list.append(i) # if it was matlab would be i + 1
    """
     The Average Precision (AP) is the area under the curve
        (numerical integration)
        matlab: ap=sum((mrec(i)-mrec(i-1)).*mpre(i));
    """
    ap = 0.0
    for i in i_list:
        ap += ((mrec[i]-mrec[i-1])*mpre[i])
    return ap, mrec, mpre


def calculate_map(ground_truth_dict: dict, result_dict: dict, iou_threshold: float):
    """
    mAP@[iou_threshold]

    :param ground_truth_dict: dict with {labels:, boxes:}
    :param result_dict: dict with {scores:, labels:, boxes:}
    :param iou_threshold: minimum iou for which the detection counts as successful
    :return: mean average precision (mAP)
    """

    occurring_gt_classes = set(ground_truth_dict['labels'])
    unique, counts = np.unique(ground_truth_dict['labels'], return_counts=True)
    ground_truth_counter_per_class = dict(zip(unique, counts))
    count_true_positives = {}
    sum_average_precision = 0

    for class_index, class_name in enumerate(occurring_gt_classes):

        detections_with_certain_class = list()
        for idx in range(len(result_dict['labels'])):
            if result_dict['labels'][idx] == class_name:
                detections_with_certain_class.append(_ImageDetection(score=result_dict['scores'][idx],
                                                                     label=result_dict['labels'][idx],
                                                                     boxes=result_dict['boxes'][idx]))
        ground_truth_list = list()
        for idx in range(len(ground_truth_dict['labels'])):
            ground_truth_list.append(_ImageDetection(score=1,
                                                     label=ground_truth_dict['labels'][idx],
                                                     boxes=ground_truth_dict['boxes'][idx]))

        count_true_positives[class_name] = 0

        tp = [0] * len(detections_with_certain_class)
        fp = [0] * len(detections_with_certain_class)

        for i, elem in enumerate(detections_with_certain_class):
            ovmax = -1
            gt_match = -1

            bb = elem.boxes
            for j, elem in enumerate(ground_truth_list):
                if ground_truth_list[j].label == class_name:
                    bbgt = ground_truth_list[j].boxes
                    bi = [max(bb[0], bbgt[0]), max(bb[1], bbgt[1]), min(bb[2], bbgt[2]), min(bb[3], bbgt[3])]
                    iw = bi[2] - bi[0] + 1
                    ih = bi[3] - bi[1] + 1
                    if iw > 0 and ih > 0:
                        # compute overlap (IoU) = area of intersection / area of union
                        ua = (bb[2] - bb[0] + 1) * (bb[3] - bb[1] + 1) + (bbgt[2] - bbgt[0]
                                                                          + 1) * (bbgt[3] - bbgt[1] + 1) - iw * ih
                        ov = iw * ih / ua
                        if ov > ovmax:
                            ovmax = ov
                            gt_match = elem

            if ovmax >= iou_threshold:
                if not gt_match.used:
                    # true positive
                    tp[i] = 1
                    gt_match.used = True
                    count_true_positives[class_name] += 1
                    # update the ".json" file
                else:
                    # false positive (multiple detection)
                    fp[i] = 1
            else:
                # false positive
                fp[i] = 1

        # compute precision/recall
        cumsum = 0
        for idx, val in enumerate(fp):
            fp[idx] += cumsum
            cumsum += val

        cumsum = 0
        for idx, val in enumerate(tp):
            tp[idx] += cumsum
            cumsum += val

        rec = tp[:]
        for idx, val in enumerate(tp):
            rec[idx] = float(tp[idx]) / ground_truth_counter_per_class[class_name]

        prec = tp[:]
        for idx, val in enumerate(tp):
            prec[idx] = float(tp[idx]) / (fp[idx] + tp[idx])

        average_precision, mean_recall, mean_precision = _voc_ap(rec[:], prec[:])
        sum_average_precision += average_precision

    mean_average_precision = sum_average_precision / len(occurring_gt_classes)
    return mean_average_precision


def calculate_map_range(ground_truth_dict: dict, result_dict: dict, iou_begin: float, iou_end: float, iou_step: float):
    """
    Gives mAP@[iou_begin:iou_end:iou_step], including iou_begin and iou_end.

    :param ground_truth_dict: dict with {labels:, boxes:}
    :param result_dict: dict with {scores:, labels:, boxes:}
    :param iou_begin: first iou to evaluate
    :param iou_end: last iou to evaluate (included!)
    :param iou_step: step size
    :return: mean average precision
    """

    iou_list = np.arange(iou_begin, iou_end + iou_step, iou_step)

    mean_average_precision_sum = 0.
    for iou in iou_list:
        mean_average_precision_sum += calculate_map(ground_truth_dict, result_dict, iou)

    return mean_average_precision_sum / len(iou_list)