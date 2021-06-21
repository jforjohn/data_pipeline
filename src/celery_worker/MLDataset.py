from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image
from torchvision.transforms import Resize
from .custom_tranformations import DynamicCrop

class MLDataset(Dataset):
    """
    Class to access metadata df and
    apply transformations
    """
    def __init__(self, metadata):
        # metadata are indexed by col id
        self.metadata = metadata
        self.transform = transforms.Compose(self._get_transforms_list())
    
    def _get_transforms_list(self):
        ratio = 0.8
        crop_transform = DynamicCrop(ratio)
        resize_h = 256
        resize_w = 256
        resize_transform = Resize((resize_h, resize_w))
        return [crop_transform, resize_transform]
        
    def __len__(self):
        return len(self.metadata)
    
    def __getitem__(self, idx):
        element = self.metadata.loc[idx]
        img_name = element['url']
        image = Image.open(img_name).convert('RGB')
        image = self.transform(image)
        return image