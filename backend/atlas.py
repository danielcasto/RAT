from ants import image_read
from os import path
import re

def get_labels_dictionary(path: str):
    with open(path) as f:
        text = f.read()
        labels_text = text.split("\n")[14:]

        labels = {}

        for line in labels_text:
            if line != "":

                label = re.findall(r'"(.*?)"', line)[0]
                index = re.findall(r'[0-9]+ ', line)[0]

                labels[label] = index
            
        return labels


class WaxholmAtlas():
    def __init__ (self, folder_path = "../../Waxholm-v4/"):

        self.map_path = path.join(folder_path,"WHS_SD_rat_atlas_v4.nii.gz")
        self.template_path = path.join(folder_path,"WHS_SD_rat_atlas_v4.nii.gz")
        self.labels = get_labels_dictionary(path.join(folder_path,"WHS_SD_rat_atlas_v4.label"))