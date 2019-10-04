#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sep 02, 2019

@author: kubilaykarapinar

"""
from abc import ABC, abstractmethod
import numpy as np
import xml.etree.ElementTree as et
import glob


class BaseAnnParser(ABC):
    def __init__(self):
        self._data_dict = {}

    @abstractmethod
    def get_data_dict(self, ann_directory):
        pass


class PascalVocAnnParser(BaseAnnParser):
    def get_data_dict(self, ann_directory):
        for ann in glob.glob(ann_directory + '*.xml'):
            with open(ann, 'r') as file:
                root = et.fromstring(file.read())

            filename = root.find('filename').text

            # Can be more than one label in photo
            labels = {}
            for elem in root.iter('name'):
                label = elem.text
                labels[label] = None
            try:
                random_label = np.random.choice(list(labels.keys()))
            except ValueError:
                random_label = 'no-label'

            if random_label not in self._data_dict.keys():
                self._data_dict[random_label] = [filename]
            else:
                self._data_dict[random_label].append(filename)

        return self._data_dict


class YOLOAnnParser(BaseAnnParser):
    def get_data_dict(self, ann_directory):
        pass
