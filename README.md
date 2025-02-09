# Lokalise API v2 official Python interface

![PyPI](https://img.shields.io/pypi/v/python-lokalise-api)
[![Build Status](https://travis-ci.com/lokalise/python-lokalise-api.svg?branch=master)](https://travis-ci.com/github/lokalise/python-lokalise-api)
[![Test Coverage](https://codecov.io/gh/lokalise/python-lokalise-api/graph/badge.svg)](https://codecov.io/gh/lokalise/python-lokalise-api)
[![Downloads](https://pepy.tech/badge/python-lokalise-api)](https://pepy.tech/project/python-lokalise-api)
[![Docs](https://readthedocs.org/projects/python-lokalise-api/badge/?version=latest&style=flat)](https://python-lokalise-api.readthedocs.io)

Official Python 3 interface for the [Lokalise APIv2](https://app.lokalise.com/api2docs) that represents returned data as Python objects.

## Quick start

This plugin requires Python 3.6 and above. Install it:

    pip install python-lokalise-api

Obtain a Lokalise API token (in your *Personal profile*) and use it:

```python
import lokalise
client = lokalise.Client('YOUR_API_TOKEN')
project = client.project('123.abc')
print(project.name)

client.upload_file(project.project_id, {
    "data": 'ZnI6DQogIHRlc3Q6IHRyYW5zbGF0aW9u',
    "filename": 'python_upload.yml',
    "lang_iso": 'en'
})

translation_keys = client.keys(project.project_id, {"page": 2,
    "limit": 3,
    "disable_references": "1"})
translation_keys.items[0].key_name['web'] # => "sign_up"
```

## Documentation

Find detailed documentation at [python-lokalise-api.readthedocs.io](https://python-lokalise-api.readthedocs.io).

## License

This plugin is licensed under the [BSD 3 Clause License](https://github.com/lokalise/python-lokalise-api/blob/master/LICENSE).

Copyright (c) [Lokalise team](https://lokalise.com) and [Ilya Bodrov](http://bodrovis.tech)
