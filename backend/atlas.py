from ants import image_read

class WaxholmAtlas():
    def __init__ (self, folder_path = "../../Waxholm/"):
        atlas_map = image_read(folder_path + "WHS_SD_rat_atlas_v4.nii.gz")
    
    def getAtlasMap(self):
        return atlas_map