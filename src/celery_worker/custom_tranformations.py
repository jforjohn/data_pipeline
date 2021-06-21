from torchvision.transforms import RandomCrop

class DynamicCrop(object):
    # gives priority if the exact size of the
    # cropped images is given
    def __init__(self, ratio):
        self.ratio = ratio
    
    def __call__(self, img):
        width, height = img.size
        # TODO: add checks eg ratio to be (0,1)
        crop_h, crop_w = round(height*self.ratio), round(width*self.ratio)
        crop = RandomCrop((crop_h, crop_w))
        return crop(img)
  
    def __repr__(self):
        func = 'Random'
        arguments = '(ratio={0})'.format(self.ratio)
        return func + self.__class__.__name__ + arguments