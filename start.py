#!/bin/python3
from bucket.utils import get_aws_ranges, process, export_csv, export_json
from bucket.collections import *

if __name__ == '__main__':

    collections: [Collection] = list()

    # aws_collection = AWSCollection()
    # aws_collection.set_keywords(ranges=get_aws_ranges())
    # collections.append(aws_collection)

    collections.append(NoneCollection())
    collections.append(ProductionCollection())
    collections.append(StagingCollection())
    collections.append(ClientCollection())
    collections.append(BrochureCollection())
    collections.append(VPNCollection())

    processed_collections = process(input_path='targets.txt', collections=collections,
                                    get_source=False, output_path='./output/sources/')

    export_json(output_path='./output/output.json',
                collections=processed_collections)
    export_csv(output_path='./output/output.csv',
               collections=processed_collections)
