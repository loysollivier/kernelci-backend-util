#!/usr/bin/env python

import pickle
import yaml
import requests
import sys

BACKEND_URL = "?????"
# Correct token if the dB was restored from kernelci-dev
TOKEN = "????"
LAB_NAME = "????"

headers = {
    "Authorization": TOKEN
}


def fake_callback():
    file = open('./raw_json.pkl', 'rb')
    payload = pickle.load(file)
    url = BACKEND_URL + "/callback/lava/test?lab_name=" + LAB_NAME + "&status=2&status_string=complete"
    print url
    return
    response = requests.post(url, headers=headers, json=payload)
    print response


if __name__ == "__main__":
    fake_callback()
    sys.exit(0)
