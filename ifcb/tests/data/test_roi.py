import unittest
import sys
from contextlib import contextmanager

import numpy as np

from .fileset_info import TEST_FILES, list_test_filesets
from ifcb.data.roi import RoiFile

class TestRoi(unittest.TestCase):
    def setUp(self):
        self.data = { fs.lid: fs for fs in list_test_filesets() }
    def fsinfo(self):
        for lid, info in TEST_FILES.items():
            fs = self.data[lid]
            roi_file = RoiFile(fs.adc_path, fs.roi_path)
            yield lid, info, roi_file
    def test_images(self):
        for lid, info, roi in self.fsinfo():
            assert len(roi) == info['n_rois']
            image = roi[info['roi_number']]
            assert image.shape == info['roi_shape']
            A = info['roi_slice']
            c = info['roi_slice_coords']
            B = image[tuple(c)] # small slice
            assert np.all(A == B)
    def test_with(self):
        for lid, info, roi in self.fsinfo():
            with roi as o:
                assert o.isopen()
                _ = o[o.keys()[0]]
            assert not roi.isopen()
    def test_not_with(self):
        for lid, info, roi in self.fsinfo():
            assert not roi.isopen()
            assert roi[roi.keys()[0]] is not None
            assert not roi.isopen()
    def test_dictlike(self):
        for lid, info, roi in self.fsinfo():
            rn = info['roi_numbers']
            assert set(roi.keys()) == set(rn)
            for n in rn:
                assert n in roi
            no = 0
            assert no not in roi

