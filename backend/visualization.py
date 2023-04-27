from nilearn import plotting

def plot_image(img_path, overlay_path = None, overlay_alpha = 0.5, display_mode = 'ortho', figure = None):
    if overlay_path == None:
        return plotting.plot_img(img = img_path, display_mode=display_mode, figure= figure)

    else:
        return plotting.plot_roi(overlay_path, 
                                 bg_img = img_path, 
                                 alpha = overlay_alpha, 
                                 display_mode=display_mode,
                                 figure = figure)