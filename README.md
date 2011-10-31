# ESProxy

This is a simple HTTP proxy, designed primarily for
[ElasticSearch](http://www.elasticsearch.org/).  It is used to allow/deny
specific operations on an ElasticSearch instance, by filtering on the
request paths.

Configuration of allowed paths is done in config.py.  The default
permissions allow only `_count` and `_search` commands on index/doc_type/command
paths:

    allowed_paths = {
        'GET': [
            re.compile(r'^/(.*?)/(.*?)/(_count|_search)'),
        ],
    }

## Usage

    python esproxy.py elasticsearch_address [--port=port]

where `elasticsearch_address` is the host:port of the elasticsearch
instance you want to proxy to, and `--port` is an optional argument
specifying the port you'd like to run the proxy on, e.g.,

    python esproxy.py 10.10.1.100:9200 --port 9210

