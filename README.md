# Overview

This is a GitHub Action that publishes a GitHub-flavored Markdown file to Confluence.

It based on https://github.com/lovoo/Github-action-confluence-sync. That package succumbed to bit rot, however, since the underlying libraries it was using quit working. This package uses `pycmarkgfm` to the the markdown-to-HTML rendering, and that package still works.

# Build Docker image

docker build -t jdawson/publish-confluence-action:v1 -t jdawson/publish-confluence-action:latest -f Dockerfile .

# Publish to Docker Hub

docker push jdawson/publish-confluence-action
