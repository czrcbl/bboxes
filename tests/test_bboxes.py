import os
import sys
import unittest
import numpy as np
from bboxes import BboxList, Bbox


class TestBbox(unittest.TestCase):

    def setUp(self):
        self.bbs, self.bbns = self.init_bboxes()
    
    def init_bboxes(self):
        id_ = 1
        score = 0.7
        coords = [10,20,200,300]
        width, height = 400, 400
        class_name = 'cls1'
        bbs = Bbox(coords, id_, class_name, width, height, score=score)
        bbns = Bbox(coords, id_, class_name, width, height)
        
        return bbs, bbns
    
    def test_resize(self):
        
        t_width = 200
        t_height = 200
        out = self.bbs.resize((t_width, t_height))
        
        self.assertEqual(out.img_height, t_height)
        self.assertEqual(out.img_width, t_width)
        self.assertEqual(out.x1, self.bbs.x1//2)
        self.assertEqual(out.x2, self.bbs.x2//2)
        self.assertEqual(out.y1, self.bbs.y1//2)
        self.assertEqual(out.y2, self.bbs.y2//2)
        
    def test_draw(self):
            
        img = np.zeros((400, 400))
        dimg = self.bbs.draw(img)
        dimg = self.bbns.draw(img)

    def test_crop(self):

        img = np.zeros((400, 400))
        cimg = self.bbs.crop_image(img)

    def test_mask(self):

        img = np.zeros((400,400))
        mimg = self.bbs.mask_image(img)


class TestBBoxList(unittest.TestCase):

    def test_loader(self):
        ids = np.array([1, 2, 3])
        scores = np.array([0.5, 0.7, 0.6])
        bboxes = np.array([[10,10,200,200], [50,60,150,200], [30,25,350,300], [20,30,100,120]])
        class_names = list('abcd')
        width, height = 400, 400
        bblist = BboxList.from_arrays(ids, scores, bboxes, width, height, class_names)

    def test_draw(self):

        ids = np.array([1, 2, 3, 2])
        scores = np.array([0.5, 0.7, 0.6, 0.65])
        bboxes = np.array([[1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1]])
        class_names = list('abcb')
        width, height = 400, 400
        bblist = BboxList.from_arrays(ids, scores, bboxes, width, height, class_names)

        img = np.zeros((100, 100, 3))
        dimg = bblist.draw(img)


if __name__ == '__main__':

    unittest.main()