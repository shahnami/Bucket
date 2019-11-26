#!/bin/python3
# pylint: disable=unused-wildcard-import, method-hidden

from bucket.utils import get_aws_ranges, process
from bucket.collections import *
from bucket.exporters import *

if __name__ == '__main__':
    collections: [Collection] = list()

    collections.append(NoneCollection())
    collections.append(StagingCollection())
    collections.append(ClientCollection())
    collections.append(BrochureCollection())
    collections.append(VPNCollection())
    collections.append(AuthCollection())

    processed_collections, pages = process(input_path='targets.txt', collections=collections,
                                           get_source=False, output_path='./output/sources/')

    try:
        # Create your own exporters in ./exporters/
        csv_exporter = CSVExporter(output='./output/output.csv')
        csv_exporter.export(pages=pages)

        json_exporter = JSONExporter(output='./output/output.json')
        json_exporter.export(collections=processed_collections)

    except NotImplementedError as e:
        print(f"[x] {e}")

    # export_csv(output_path='./output/output.csv', pages=pages)
