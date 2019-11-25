#!/bin/python3
from bucket.utils import get_aws_ranges, process, export_csv, export_json
from bucket.collections import *

if __name__ == '__main__':

    collections: [Collection] = list()

    collections.append(NoneCollection())
    collections.append(StagingCollection())
    collections.append(ClientCollection())
    collections.append(BrochureCollection())
    collections.append(VPNCollection())
    collections.append(AuthCollection())

    processed_collections = process(
        input_path='targets.txt', collections=collections, get_source=False, output_path='./output/sources/')

    export_csv(output_path='./output/output.csv',
               collections=processed_collections)
