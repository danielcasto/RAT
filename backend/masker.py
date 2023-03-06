from ants import read_image, mask_image, image_write
from registration import Registration

class Masker():
    def __init__(self, image_path, image_mask_path: str) -> None:
        self.image_path = image_path
        self.image_mask_path = image_mask_path

        self.warped_image = None
        self.image_transforms == None
        self.atlas_path = None

    def alignToAtlas(self, atlas_path: str, roi_idx : list):
        registration = Registration(fixed_path = self.image_path, mask_path = self.image_mask_path, moving_path = self.atlas_path)
        result = registration.register()
        
        self.atlas_path = atlas_path
        self.warped_image = result.warped_fixed
        self.image_transforms = result.inverse_transform

        return self.warped_image

    def exportROIMask(self, roi_idxs, path):
        if self.warped_image == None or self.image_transforms == None or self.atlas_path == None:
            raise TypeError("Image has not been aligned to atlas! Call alignToAtlas first.")
        
        atlas = read_image(self.atlas_path)
        mask = mask_image(self.warped_image, mask=atlas, level=(roi_idxs), binarize=True)

        image_write(mask, filename=path)
    
    def exportAlignedImage(self, path: str):
        if self.warped_image == None:
            raise TypeError("Image has not been aligned to atlas! Call alignToAtlas first.")
        
        image_write(self.warped_image, filename=path)