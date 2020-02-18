#!/bin/python3
# pylint: disable=unused-wildcard-import, method-hidden

import itertools

from bucket.utils import get_aws_ranges
from bucket.collections import *
from bucket.exporters import *
from bucket.bucketer import *


if __name__ == '__main__':
    collections: [Collection] = list()

    aws_collection = AWSCollection()
    aws_collection.set_keywords(ranges=get_aws_ranges())
    collections.append(aws_collection)

    collections.append(ClientCollection())
    collections.append(NoneCollection())
    collections.append(StagingCollection())
    collections.append(BrochureCollection())
    collections.append(VPNCollection())
    collections.append(AuthCollection())
    collections.append(EnvironmentCollection())

    configuration: dict = {
        "input_path": "targets.txt",
        "collections": collections,
        "get_source": False,
        "resolve_dns": False,
        "is_recursive": True,
        "output_path": "./output/sources/"
    }

    bucketer: Bucketer = Bucketer(configuration=configuration)
    bucketer.run()

    processed_collections = bucketer.get_collections()
    processed_pages = bucketer.get_pages()

    try:
        # Create your own exporters in ./exporters/
        csv_exporter = CSVExporter(output_path='./output/output.csv')
        csv_exporter.export(pages=processed_pages,
                            collections=processed_collections)

        json_exporter = JSONExporter(output_path='./output/output.json')
        json_exporter.export(collections=processed_collections)

    except NotImplementedError as e:
        print(f"[x] {e}")
