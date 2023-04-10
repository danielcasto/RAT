from ants import registration, image_read, mask_image

class RegistrationResult():
    def __init__(self, result: dict):
        self.warped_moving = result['warpedmovout']
        self.warped_fixed = result['warpedmfixout']
        self.forward_transform = result['fwdtransforms']
        self.inverse_transform = result['invtransforms']
    

class Registration():
    def __init__(self, fixed_path: str, moving_path: str, mask_path = None) -> None:
        self.fixed = image_read(fixed_path, dimension=3)
        self.moving = image_read(moving_path, dimension=3)
        self.mask = None
        self.result = None

        if mask_path != None:
            self.mask = image_read(mask_path, dimension=3)
            self.fixed = mask_image(self.fixed, mask=self.mask)

    def register(self, type_of_transform = "SyN", reg_iterations = (1000, 1000, 500, 100), syn_metric = "mattes") -> RegistrationResult:
        result = registration(
            fixed=self.fixed, 
            moving=self.moving, 
            mask=self.mask, 
            type_of_transform=type_of_transform, 
            reg_iterations=reg_iterations,
            syn_metric=syn_metric)
        
        
        return RegistrationResult(result)