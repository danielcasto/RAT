from ants import image_read, mask_image, image_write
from .registration import Registration
from .atlas import WaxholmAtlas

class Masker():
    def __init__(self, image_path, image_mask_path: str, atlas_path: str) -> None:
        self.image_path = image_path
        self.image_mask_path = image_mask_path

        self.warped_image = None
        self.image_transforms = None
        self.atlas = WaxholmAtlas(atlas_path)

    def alignToAtlas(self):
        registration = Registration(fixed_path = self.image_path, moving_path = self.atlas.template_path, mask_path = self.image_mask_path)
        result = registration.register()

        self.warped_image = result.warped_fixed
        self.image_transforms = result.inverse_transform

        return self

    def exportROIMask(self, roi_labels, path):
        if self.warped_image is None or self.image_transforms is None:
            raise TypeError("Image has not been aligned to atlas! Call alignToAtlas first.")
        
        if roi_labels is None or len(roi_labels) == 0:
            self.exportAlignedImage(path) # TODO this may need to be changed

        atlas = image_read(self.atlas.map_path)
        roi_idxs = [self.atlas.labels[label] for label in roi_labels]

        mask = mask_image(self.warped_image, mask=atlas, level=(roi_idxs), binarize=True)

        image_write(mask, filename=path)

        return self
    
    def exportROIMaskedImage(self, mask_path, result_path):
        if self.warped_image is None or self.image_transforms is None:
            raise TypeError("Image has not been aligned to atlas! Call alignToAtlas first.")
            
        image = self.warped_image
        roi_mask = image_read(mask_path)

        masked_image = mask_image(image, mask=roi_mask)

        image_write(masked_image, filename=result_path)

        return self

    def exportAlignedImage(self, path: str):
        if self.warped_image is None or self.image_transforms is None:
            raise TypeError("Image has not been aligned to atlas! Call alignToAtlas first.")
        
        image_write(self.warped_image, path)
        
        return self