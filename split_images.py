#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sep 02, 2019

@author: kubilaykarapinar

"""
import os
import shutil
import argparse
import math
import numpy as np
import parsers as p

parser = argparse.ArgumentParser(description='Split dataset into training, validation and test set')
parser._action_groups.pop()
required = parser.add_argument_group('required arguments')
optional = parser.add_argument_group('optional arguments')
required.add_argument('-s', '--source', type=str, required=True,
                      help='source directory')
required.add_argument('-d', '--destination', type=str, required=True,
                      help='destination directory')
optional.add_argument('-v', '--val_perc', type=int, required=True,
                      help='val data percentage, s.t. 10, 15, 20 ...')
optional.add_argument('-t', '--test_perc', type=int, default=0,
                      help='test data percentage, s.t. 10, 15, 20 ...')
args = parser.parse_args()

source = args.source
destination = args.destination
val_perc = args.val_perc
test_perc = args.test_perc

# Cannot exceed 100%
if val_perc + test_perc > 100:
    raise ValueError("Sum of the val percentage and the test percentage cannot be bigger than 100%")

img_directory = os.path.join(source, 'images/')
ann_directory = os.path.join(source, 'annotations/')
train_img_directory = os.path.join(destination, 'train', 'images/')
train_ann_directory = os.path.join(destination, 'train', 'annotations/')
validation_img_directory = os.path.join(destination, 'validation', 'images/')
validation_ann_directory = os.path.join(destination, 'validation', 'annotations/')
test_img_directory = os.path.join(destination, 'test', 'images/')
test_ann_directory = os.path.join(destination, 'test', 'annotations/')


# Remove folder with files inside and create empty one again
def re_create_folder(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)


# Recreate folders
re_create_folder(train_img_directory)
re_create_folder(train_ann_directory)
re_create_folder(validation_img_directory)
re_create_folder(validation_ann_directory)
re_create_folder(test_img_directory)
re_create_folder(test_ann_directory)


# Copy images and annotations to main image and annotation folder
# to specific train, val or test folder
def copy_list(data_list, img_from, ann_from, img_to, ann_to):
    for f_name in data_list:
        img_name = f_name.split('.')[0]
        shutil.copy2(os.path.join(img_from, img_name + '.jpg'), img_to)
        shutil.copy2(os.path.join(ann_from, img_name + '.xml'), ann_to)


parser = p.PascalVocAnnParser()
data_dict = parser.get_data_dict(ann_directory)

for label in data_dict.keys():
    data = data_dict[label]
    # Calculate size of splits
    data_size = len(data)
    val_size = math.ceil(val_perc * data_size / 100)
    test_size = math.ceil(test_perc * data_size / 100)

    # Create list of indices
    indices = np.arange(data_size)
    np.random.shuffle(indices)
    # Get Split Indices
    test_indices = indices[0: test_size + 1]
    val_indices = indices[test_size + 1: test_size + val_size + 2]
    training_indices = indices[test_size + val_size + 2:]
    # Split data
    train_data = np.take(data, training_indices)
    val_data = np.take(data, val_indices)
    test_data = np.take(data, test_indices)

    # Copy data into specific folder
    copy_list(train_data, img_directory, ann_directory, train_img_directory, train_ann_directory)
    copy_list(val_data, img_directory, ann_directory, validation_img_directory, validation_ann_directory)
    copy_list(test_data, img_directory, ann_directory, test_img_directory, test_ann_directory)
print('Done')
