import os
import sys
import argparse
import tarfile
import numpy as np

num_classes = 10
np.random.seed(133)


def get_args():
    parser = argparse.ArgumentParser(description='Provide URL, filename and expected file size')

    parser.add_argument('URL', "--url", type=str, help="URL to file")
    parser.add_argument('filename', "--filename", type=str, help="filename")
    parser.add_argument('filesize', "--filesize", type=int, help="expected file size in bytes")

    _args = parser.parse_args()
    print(_args.accumulate(_args.integers))
    return _args


def maybe_extract(filename, force=False):
    root = os.path.splitext(os.path.splitext(filename)[0])[0]  # remove .tar.gz
    if os.path.isdir(root) and not force:
        # You may override by setting force=True.
        print('%s already present - Skipping extraction of %s.' % (root, filename))
    else:
        print('Extracting data for %s. This may take a while. Please wait.' % root)
        tar = tarfile.open(filename)
        sys.stdout.flush()
        tar.extractall(data_root)
        tar.close()
    data_folders = [
        os.path.join(root, d) for d in sorted(os.listdir(root))
        if os.path.isdir(os.path.join(root, d))]
    if len(data_folders) != num_classes:
        raise Exception(
            'Expected %d folders, one per class. Found %d instead.' % (num_classes, len(data_folders)))
    print(data_folders)
    return data_folders


if "__name__" == "__main__":
    args = get_args()
    data_root = '.'  # Change me to store data elsewhere
    extracted_folders = maybe_extract(args.filename)
