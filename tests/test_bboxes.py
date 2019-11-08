import os
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(os.path.realpath(__file__))))
if path not in sys.path:
    sys.path.insert(0, path)
import unittest

import numpy as np

from bboxes import BboxList, Bbox


class TestBbox(unittest.TestCase):

    def init_bbox(self):
        id_ = 1
        score = 0.7
        bb = [1,1,2,2]
        class_name = 'a'
        bb = Bbox(bb, id_, score, class_name)
        return bb
    def test_init(self):
        _ = self.init_bbox()


    def test_draw(self):
        bb = self.init_bbox()
        img = np.zeros((10,10))
        dimg = bb.draw(img)

    def test_crop(self):

        bb = self.init_bbox()
        img = np.zeros((10,10))
        cimg = bb.cropped_image(img)

    def test_mask(self):

        bb = self.init_bbox()
        img = np.zeros((10,10))
        mimg = bb.mask_image(img)


class TestBBoxList(unittest.TestCase):

    def test_loader(self):
        ids = np.array([1, 2, 3])
        scores = np.array([0.5, 0.7, 0.6])
        bboxes = np.array([[1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1]])
        class_names = list('abcd')
        bblist = BboxList.from_arrays(ids, scores, bboxes, class_names)

    def test_append(self):
        bblist = BboxList()

        ids = np.array([1, 2, 3, 2])
        scores = np.array([0.5, 0.7, 0.6, 0.65])
        bboxes = np.array([[1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1]])
        classes = list('abcb')
        for i, s, b, c in zip(ids, scores, bboxes, classes):
            bb = Bbox(b, i, s, c)
            bblist.append(bb)

        self.assertEqual(len(bblist), 4)
        self.assertEqual(bblist.class_names, list('abc'))
        self.assertEqual(bblist.get_scores(), [0.7, 0.65, 0.6, 0.5])

    def test_draw(self):

        ids = np.array([1, 2, 3, 2])
        scores = np.array([0.5, 0.7, 0.6, 0.65])
        bboxes = np.array([[1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1]])
        classes = list('abcb')
        bblist = BboxList.from_arrays(ids, scores, bboxes, classes=classes)

        img = np.zeros((100, 100, 3))
        dimg = bblist.draw(img)


if __name__ == '__main__':

    unittest.main()