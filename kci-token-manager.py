#!/usr/bin/env python

import sys
import requests
import json
import argparse

# Needs to be an admin token
BACKEND_URL = "http://????"
TOKEN = "????"

headers = {
        "Authorization": TOKEN
}

def print_error_msg(status_code):
    print 'Error in request, return code: {}'.format(status_code)

def get_token_from_oid(oid):
    url = BACKEND_URL + "/token" 
    payload = {
        "_id": oid,
    }
    response = requests.get(url, headers=headers, params=payload)
    if response.status_code != 200:
        print_error_msg(response.status_code)
    token_entry = response.json()
    return token_entry["result"][0]["token"]

def kci_show_all_tokens():
    url = BACKEND_URL + "/token"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print_error_msg(response.status_code)
    token_list = response.json()
    for token_entry in token_list["result"]:
        print '{0:30} {1:10}'.format(token_entry["username"], token_entry["token"])

        # print(str(token_entry["username"]) + ": \t" + str(token_entry["token"]))
    #print(json.dumps(rjson, indent=4))

def kci_show_labs():
    url = BACKEND_URL + "/lab"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print_error_msg(response.status_code)
    lab_list = response.json()
    for lab_entry in lab_list["result"]:
        token_value = get_token_from_oid(lab_entry["token"]["$oid"])
        print '{0:30} {1:} ({2:})'.format(lab_entry["name"],
                                          token_value,
                                          lab_entry["contact"]["email"])


def kci_add_lab_token():
    print("Adding a lab token, be careful no typo allowed")
    lab_name =  raw_input("Lab name: ")
    lab_mail =  raw_input("Lab mail: ")
    print "Adding lab {}({})".format(lab_name, lab_mail)
    payload = {
        "name": lab_name, "contact": {
            "name": lab_mail, "surname": lab_mail, "email": lab_mail
        }
    }
    url = BACKEND_URL + "/lab"
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 201:
        print_error_msg(response.status_code)
        print response
    print(response.json())

def parse_cmdline():
    parser = argparse.ArgumentParser(description="KernelCI Database token manager",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", action="version", version="%(prog)s 0.1")
    parser.add_argument("--list-tokens", "-l", help="list tokens",
                        action="store_true")
    parser.add_argument("--list-labs", help="list labs",
                        action="store_true")
    parser.add_argument("--add-lab", help="add lab token",
                        action="store_true")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_cmdline()
    if args.list_tokens:
        kci_show_all_tokens()
    if args.list_labs:
        kci_show_labs()
    if args.add_lab:
        kci_add_lab_token()
sys.exit(0)
