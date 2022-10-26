#!/usr/bin/env python

import os
import requests
import pycmarkgfm

def get_inputs():
    try:
        workspace = os.environ['GITHUB_WORKSPACE']
        envs = {
            key: os.environ[f'INPUT_{key.upper()}']
            for key in ['from', 'to', 'cloud', 'user', 'token']
        }
    except KeyError as e:
        raise Exception(f'Missing value for {e}')
    return (workspace, envs)

def main():
    (workspace, envs) = get_inputs()
    input_path = os.path.join(workspace, envs['from'])
    with open(input_path) as f:
        markdown_text = f.read()

    content_url = f"https://{envs['cloud']}.atlassian.net/wiki/rest/api/content/{envs['to']}"
    print('Fetching old page')
    response = requests.get(content_url, auth=(envs['user'], envs['token']))
    response.raise_for_status()
    current = response.json()
    print('Rendering')
    html = pycmarkgfm.gfm_to_html(markdown_text)
    content = {
        'id': current['id'],
        'type': current['type'],
        'title': current['title'],
        'version': {'number': current['version']['number'] + 1},
        'body': {
            'editor': {
                'value': html,
                'representation': 'editor'
            }
        }
    }

    updated = requests.put(content_url, json=content, auth=(
        envs['user'], envs['token'])).json()
    link = updated['_links']['base'] + updated['_links']['webui']
    print(f'Uploaded content successfully to page {link}')

main()
