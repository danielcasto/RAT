from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from os import listdir
from sys import stderr

ATLAS_PATH = "https://www.nitrc.org/frs/download.php/12264/WHS_SD_rat_atlas_v4_pack.zip"

def download_waxholm_v4():
    print("Waxholm Atlas v4 not found. Downloading atlas....")
    
    if "Waxholm-v4" not in listdir():
        resp = urlopen(ATLAS_PATH)
        myzip = ZipFile(BytesIO(resp.read()))
        myzip.extractall("Waxholm-v4/")

    print("Download Complete!")

if __name__ == "__main__":
    download_waxholm_v4()