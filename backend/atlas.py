from ants import image_read, image_write, mask_image
from numpy import logical_not
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
        self.template_path = path.join(folder_path,"WHS_SD_rat_T2star_v1.01.nii.gz")
        self.masked_template_path = path.join(folder_path,"masked_atlas_template.nii.gz")

        self.labels = get_labels_dictionary(path.join(folder_path,"WHS_SD_rat_atlas_v4.label"))

        if not path.exists(self.masked_template_path):
            print('Preprocessing step: masked template file not found, building masked template file...')
            map_ants = image_read(self.map_path)
            template_ants = image_read(self.template_path)
            inverted_template_mask = mask_image(template_ants, map_ants, 0, binarize=True)
            inverted_template_mask_data = inverted_template_mask.numpy()

            template_mask = inverted_template_mask.new_image_like(logical_not(inverted_template_mask_data).astype(float))
            masked_template = mask_image(template_ants, template_mask)

            image_write(masked_template, self.masked_template_path)