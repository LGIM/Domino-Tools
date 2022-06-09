#!/usr/bin/env python3
import requests
import json
import sys
import os
import urllib3

VERBOSE = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
domino_endpoint = os.getenv('DOMINO_ENDPOINT')

'''
examples
    domino_client.py '{ "function":"echo", "message":"hello" } '
    domino_client.py '{ "function":"random_number",   "start":1, "stop":100 } '
    domino_client.py '{ "function":"function_create", "function_name":"test2", "function_file":"function/test.py" } '
    domino_client.py '{ "function":"test2",           "q":"hello from user defined function" } '
    domino_client.py '{ "function": "cache_read",    "path": "file1.snappy.parquet",    "storage": "s3" } '
    domino_client.py '{ "function": "cache_read", "path": "10MB.bin" } '
'''

if __name__ == "__main__":
    cli_input = json.loads(sys.argv[1])
    if VERBOSE: print(f'{cli_input=}')

    if cli_input['function'] == 'function_create':
        function_file_name = cli_input["function_file"]
        if VERBOSE: print(f'{function_file_name=}')
        function_file = open(function_file_name, "r")
        if VERBOSE: print(f'{function_file=}')
        function_file_data = function_file.read()
        function_file.close()

        function_body = requests.utils.quote(function_file_data)

        cli_input.pop('function_file')
        cli_input['function_body'] = function_body
        if VERBOSE: print(f'{cli_input=}')
        wrapper = f'{{ "data": {cli_input}  }}'.replace("'", "\"")
        if VERBOSE: print(f'{wrapper=}')
        wrapper_json = json.loads(wrapper)
    else:
        wrapper_json = json.loads(f'{{ "data": {sys.argv[1]}  }}')

    if VERBOSE: print(f'{wrapper_json=}')

    response = requests.post(domino_endpoint, verify=False, json=wrapper_json)
    if VERBOSE: print(f'{response.status_code=}')
    if VERBOSE: print(f'{response.headers=}')

    is_json = True
    try:
        response_json = response.json()
    except:
        is_json = False

    if VERBOSE and is_json: print(f"{response.json()=}")
    if is_json:
        print(f"{response.json()['result']}")
    else:
        print(f"{response}")
