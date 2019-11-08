from __future__ import division, print_function, absolute_import
import cv2
import numpy as np
import matplotlib.pyplot as plt


def center_width_height2xyxy(data):
    out = np.zeros((4,))
    bbox_width = float(data[2]) 
    bbox_height = float(data[3])
    center_x = float(data[0])
    center_y = float(data[1])
    out[0] = (center_x - (bbox_width / 2))
    out[1] = (center_y - (bbox_height / 2))
    out[2] = (center_x + (bbox_width / 2))
    out[3] = (center_y + (bbox_height / 2))
    return out


def xyxy2center_width_height(data):
    out = np.zeros((4,))
    bbox_width = data[2] - data[0]
    bbox_height = data[3] - data[1]
    center_x = data[0] + (bbox_width / 2)
    center_y = data[1] + (bbox_height / 2)
    out[0] = center_x
    out[1] = center_y
    out[2] = bbox_width
    out[3] = bbox_height
    return np.array(out)


class Bbox(object):

    def __init__(self, coords, class_id, score, class_name, parent=None):
        self.x1 = coords[0] # left top
        self.y1 = coords[1] # left top
        self.x2 = coords[2] # right bottom
        self.y2 = coords[3] # right bottom
        self.coords = coords
        self.class_id = int(class_id)
        self.score = score
        self.parent = parent
        self.class_name = class_name
        
    def __repr__(self):
        return 'Bbox({:.2f}, {:.2f}, {:.2f}, {:.2f}, class_id={}, score={:.2f}, class_name=\'{}\')'.format(self.x1, self.y1, self.x2, self.y2, self.class_id, self.score, self.class_name)

    @property
    def xyxy(self):
        return np.array([self.x1, self.y1, self.x2, self.y2])

    @property
    def yxyx(self):
        return np.array([self.y1, self.x1, self.y2, self.x2])

    @property
    def center_width_height(self):
        return xyxy2center_width_height(self.xyxy)

    def cropped_image(self, img, border=0.0):
        """Return the original image cropped on the bounding box limits
        border: percentage of the bounding box width and height to enlager the bbox
        """
        h, w = img.shape[:2]
        
        # percentage of bbox dimensions
        bbh, bbw = self.y2 - self.y1, self.x2 - self.x1
        i1 = int(np.max([0, self.y1 - bbh * border / 2.0]))
        i2 = int(np.min([h, self.y2 + bbh * border / 2.0]))
        j1 = int(np.max([0, self.x1 - bbw * border / 2.0]))
        j2 = int(np.min([w, self.x2 + bbw * border / 2.0]))
        cropped = img[i1: i2, j1: j2]

        # # percentage of total image dimensions
        # i1 = int(np.max([0, self.y1 - h * border / 2.0]))
        # i2 = int(np.min([h, self.y2 + h * border / 2.0]))
        # j1 = int(np.max([0, self.x1 - w * border / 2.0]))
        # j2 = int(np.min([w, self.x2 + w * border / 2.0]))
        # cropped = img[i1: i2, j1: j2]

        return cropped

    def mask_image(self, img=None):

        if img is None:
            img = self.parent.img
        
        if len(img.shape) == 2:
            h, w = img.shape
            out = np.zeros((h, w))
        elif len(img.shape) == 3:
            h, w, c = img.shape
            out = np.zeros((h, w, c))

        bbh, bbw = self.y2 - self.y1, self.x2 - self.x1
        i1 = int(np.max([0, self.y1]))
        i2 = int(np.min([h, self.y2]))
        j1 = int(np.max([0, self.x1]))
        j2 = int(np.min([w, self.x2]))
        out[i1: i2, j1: j2] = img[i1: i2, j1: j2]
  
        return out
    
    
    def draw(self, img):
        """Draw bbox on image, expect an int image"""
        img = np.copy(img)
        height, width = img.shape[:2]
        if (self.parent is not None) and (self.parent.all_classes is not None):
            color = plt.get_cmap('hsv')(self.class_id / len(self.parent.all_classes))
        else:
            color = plt.get_cmap('hsv')(self.class_id / 80) # Number of classes on COCO
        color = [x * 255 for x in color]
        thickness = 1 + int(img.shape[1]/300)
        cv2.rectangle(img, (int(self.x1), int(self.y1)), (int(self.x2), int(self.y2)), color, thickness)
        text = '{} {:d}%'.format(self.class_name, int(self.score * 100))
        font_scale = 0.5/600 * width
        thickness = int(2/600 * width)
        vert = 10/1080 * height
        cv2.putText(img, text, (int(self.x1), int(self.y1 - vert)), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)
        return img


def get_position(val, l):
    for i, e in enumerate(l):
        if val > e:
            return i


class BboxList(list):

    def __init__(self):
        super(BboxList, self).__init__()
        self.th = None
        self.all_classes = None

    @classmethod
    def from_arrays(_cls, ids, scores, bboxes, classes=None, class_names=None, th=0.0):
        if (classes is None) and (class_names is None):
            raise ValueError('You should provide classes or class_names param.')
        elif (classes is not None) and (class_names is not None):
            raise ValueError('You should provide only classes or class_names param.')
        if class_names is not None:
            classes = [class_names[i] for i in ids]
        bblist = _cls()
        bblist.th = th
        bblist.all_classes = class_names
        out_bboxes = []
        for _id, score, bbox, _cls in zip(ids, scores, bboxes, classes):
            _id = int(_id)
            if score > th: 
                out_bboxes.append(Bbox(bbox, _id, score, _cls, parent=bblist))
        # Sort the boxes only once
        out_bboxes = sorted(out_bboxes, key=(lambda x: x.score), reverse=True)
        bblist.extend(out_bboxes)
        return bblist

    @property
    def class_names(self):
        """Return the names of classes in the order of the id values"""
        id_cls_map = {}
        for bb in self:
            id_cls_map[bb.class_id] = bb.class_name
        return [id_cls_map[e] for e in self.get_uids()]

    def append(self, bb):
        """Overload append to ensure that the boxes will always be ordered"""
        super(BboxList, self).append(bb)
        if len(self) > 1:
            self.sort(key=lambda x: x.score, reverse=True)

    def get_scores(self):
        """Return a list with the scores in the boxes order"""
        return [bb.score for bb in self]

    def get_uids(self):
        """Get the unique ids from the boxes on the list"""
        return sorted(list(set([bb.class_id for bb in self])))

    def to_arrays(self):
        """Convert to arrays in gluoncv output convention"""
        ids = []
        scores = []
        bboxes = []
        for bbox in self:
            ids.append(bbox.class_id)
            scores.append(bbox.score)
            bboxes.append(bbox.xyxy())
        return np.array(ids), np.array(scores), np.array(bboxes)

    def draw(self, img):
        """Draw all bounding boxes in inverse order, to focus on higher score boxes."""
        for bbox in self[::-1]:
            img = bbox.draw(img)

        return img

    def filter(self, classes):
        out = BboxList()
        for _cls in classes:
            for bbox in self:
                if bbox.class_name == _cls:
                    out.append(bbox)
        return out


if __name__ == '__main__':
    pass