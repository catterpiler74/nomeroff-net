import json
import os
from tensorflow.python.client import device_lib
import urllib.request
from tqdm import tqdm
import pathlib

# load latest paths
dirpath = os.getcwd()
with open(os.path.join(dirpath, "../models/latest.json")) as jLatest:
    latest_models = json.load(jLatest)

def load_last_models():
    print(latest_models)

def get_mode():
    local_device_protos = device_lib.list_local_devices()
    for x in local_device_protos:
        if x.device_type == 'GPU':
            return "gpu"
    return "cpu"

device_mode = get_mode()



class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

def download_latest_model(detector, model_name, ext="h5", mode = device_mode):
    info = latest_models[detector][model_name][ext]
    info["path"] = os.path.join(dirpath, "../models", detector, model_name, os.path.basename(info[mode]))

    p = pathlib.Path(os.path.dirname(info["path"]))
    p.mkdir(parents=True, exist_ok=True)

    if not os.path.exists(info["path"]):
        #print("downloading model {} to {} ...".format(info[mode], info["path"]))
        download_url(info[mode], info['path'])

    return info

