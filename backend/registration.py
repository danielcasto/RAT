from ants import registration, image_read, mask_image

class RegistrationResult():
    def __init__(self, result: dict):
        self.warped_moving = result['warpedmovout']
        self.warped_fixed = result['warpedfixout']
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
        else:
            raise NotImplemented("Masks cannot be generated automatically yet so a mask path is required.")

    def register(self, type_of_transform = "SyNRA", reg_iterations = (10000, 1000, 100, 0), grad_step = 0.2) -> RegistrationResult:
        result = registration(
            fixed=self.fixed, 
            moving=self.moving, 
            mask=self.mask, 
            type_of_transform=type_of_transform, 
            reg_iterations=reg_iterations,
            grad_step = grad_step )
        
        
        return RegistrationResult(result)