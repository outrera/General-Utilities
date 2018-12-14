"""
Download Datasets from a URL
Show download progress

Inputs:
--url
--filename
--filesize

Example:
>> python download_dataset  --url 'https://commondatastorage.googleapis.com/books1000/'
                            --filename notMNIST_large.tar.gz --filesize 247336696

train_filename = maybe_download('notMNIST_large.tar.gz', 247336696)
"""

import argparse
import os
import sys
from six.moves.urllib.request import urlretrieve

last_percent_reported = None
data_root = '.'  # Change me to store data elsewhere


def get_args():
    parser = argparse.ArgumentParser(description='Provide URL, filename and expected file size')

    parser.add_argument('URL', "--url", type=str, help="URL to file")
    parser.add_argument('filename', "--filename", type=str, help="filename")
    parser.add_argument('filesize', "--filesize", type=int, help="expected file size in bytes")

    _args = parser.parse_args()
    print(_args.accumulate(_args.integers))
    return _args


def download_progress_hook(count, block_size, total_size):
    """
    A hook to report the progress of a download. This is mostly intended for users with
    slow internet connections. Reports every 5% change in download progress.
    """
    global last_percent_reported
    percent = int(count * block_size * 100 / total_size)

    if last_percent_reported != percent:
        if percent % 5 == 0:
            sys.stdout.write("%s%%" % percent)
            sys.stdout.flush()
        else:
            sys.stdout.write(".")
            sys.stdout.flush()

    last_percent_reported = percent


def maybe_download(url, filename, expected_bytes, force=False):
    """Download a file if not present, and make sure it's the right size."""
    dest_filename = os.path.join(data_root, filename)
    if force or not os.path.exists(dest_filename):
        print('Attempting to download:', filename)
        filename, _ = urlretrieve(url + filename, dest_filename, reporthook=download_progress_hook)
        print('\nDownload Complete!')
    statinfo = os.stat(dest_filename)
    if statinfo.st_size == expected_bytes:
        print('Found and verified', dest_filename)
    else:
        raise Exception('Failed to verify ' + dest_filename + '. Can you get to it with a browser?')
    return dest_filename


if "__name__" == "__main__":
    args = get_args()
    file = maybe_download(args.url, args.filename, args.filesize)
