# mapcalc (mean average precision calculator)


## Table of contents

- [Introduction](#introduction)
- [Explanation](#explanation)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Authors](#authors)

## Introduction
For object detection in images the mAP (mean average precision) metric is often used to see how good the implementation is.
As no packages that make the calculation for you were available at this time, I adapted the implementation from João Cartucho,
which uses files which hold the detection results. It now can be installed as a package with pip and simply gives you the
mAP value at a certain iou threshold. 

## Explanation
The performance of your neural net will be judged using the mAP criterium defined in the [PASCAL VOC 2012 competition](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/). The code from [official Matlab code](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/#devkit) was adapted into Python.

## Prerequisites
Packages needed:
- numpy

## Usage
```python
from mapcalc import calculate_map, calculate_map_range

ground_truth = {
    'boxes':
        [[60., 80., 66., 92.],
         [59., 94., 68., 97.],
         [70., 87., 81., 94.],
         [8., 34., 10., 36.]],

    'labels':
        [2, 2, 3, 4]}

result_dict = {
    'boxes':
        [[57., 87., 66., 94.],
         [58., 94., 68., 95.],
         [70., 88., 81., 93.],
         [10., 37., 17., 40.]],

    'labels':
        [2, 3, 3, 4],

    'scores':
        [0.99056727, 0.98965424, 0.93990153, 0.9157755]}

# calculates the mAP for an IOU threshold of 0.5
print(calculate_map(ground_truth, result_dict, 0.5))

# calculates the mAP average for the IOU thresholds 0.05, 0.1, 0.15, ..., 0.90, 0.95.
print(calculate_map_range(ground_truth, result_dict, 0.05, 0.95, 0.05))

```

The methods expect two dicts:
* ground_truth_dict with {boxes:, labels:} 
* result_dict with {boxes:, labels:, scores:}

Boxes: A list of [x1, x2, y1, y2], each representing a box that was detected.

Labels: List of classes (int) the algorithm assigned to the box

Scores: List of scores (float) the algorithm generated. If not specified, scores will be set to 1.

## Authors:
* **Simon Klimaschka**
* Adapted from **João Cartucho** (https://github.com/Cartucho/mAP)