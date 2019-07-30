# mapcalc (mean average precision calculator)


## Table of contents

- [Introduction](#introduction)
- [Explanation](#explanation)
- [Prerequisites](#prerequisites)
- [Data format](#data-format)
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
- NumPy

## Data format
Tbd

## Authors:
* **Simon Klimaschka**
* Adapted from **João Cartucho**
