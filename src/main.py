#!/usr/bin/env python

import os
import requests
import pycmarkgfm

class Config:
    def __init__(self):
        self.publish_map = {}
        try:
            self.workspace = os.environ['GITHUB_WORKSPACE']
            self.cloud = os.environ['INPUT_CLOUD']
            self.user = os.environ['INPUT_USER']
            self.token = os.environ['INPUT_TOKEN']
            if 'INPUT_FROM' in os.environ:
                from_path = os.environ['INPUT_FROM']
                to_page_id = os.environ['INPUT_TO']
                self.publish_map[from_path] = to_page_id
            if 'INPUT_PUBLISH_MAP' in os.environ:
                publish_map_path = os.path.join(self.workspace, os.environ['INPUT_PUBLISH_MAP'])
                self.publish_map.update(self.read_publish_map(publish_map_path))
        except KeyError as e:
            raise Exception(f'Missing value for {e}')
    
    @staticmethod
    def read_publish_map(publish_map_path: str) -> dict:
        publish_map = {}
        print(f"Reading publish map file {publish_map_path}")
        with open(publish_map_path, "r") as publish_map_file:
            for line in publish_map_file:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                try:
                    (from_path, to_page_id) = line.split()
                except Exception as e:
                    raise Exception(f"Invalid publish map line: {line}") from e
                publish_map[from_path] = to_page_id
        return publish_map
                

def publish(config: Config, from_path: str, to_page_id: str):
    input_path = os.path.join(config.workspace, from_path)
    print(f"Reading file {from_path}")
    with open(input_path) as f:
        markdown_text = f.read()

    content_url = f"https://{config.cloud}.atlassian.net/wiki/rest/api/content/{to_page_id}"
    print(f'Fetching old page: {to_page_id}')
    auth = (config.user, config.token)
    response = requests.get(content_url, auth=auth)
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

    print("Uploading to Confluence")
    updated = requests.put(content_url, json=content, auth=auth).json()
    link = updated['_links']['base'] + updated['_links']['webui']
    print(f'Uploaded content successfully to page {link}')

def main():
    config = Config()
    for (from_path, to_page_id) in config.publish_map.items():
        publish(config, from_path, to_page_id)


main()
