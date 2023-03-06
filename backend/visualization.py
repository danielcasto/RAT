from nilearn import plotting
from nilearn import image

def plot_image(img_path, overlay_path = None, overlay_alpha = 0.5, display_mode = 'x'):
    if overlay_path == None:
        return plotting.plot_img(img = img_path, display_mode=display_mode)

    else:
        return plotting.plot_roi(overlay_path, 
                                 bg_img = img_path, 
                                 overlay_alpha = overlay_alpha, 
                                 display_mode=display_mode)