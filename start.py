#!/bin/python3
from bucket.utils import get_aws_ranges, process, export_csv, export_json
from bucket.collections import Collection, NoneCollection, EnvironmentCollection, PaymentCollection, VPNCollection, SocialCollection, AWSCollection, LoginCollection, InputCollection

if __name__ == '__main__':

    collections: [Collection] = list()

    aws_collection = AWSCollection()
    aws_collection.set_keywords(ranges=get_aws_ranges())

    collections.append(aws_collection)
    collections.append(NoneCollection())
    collections.append(EnvironmentCollection())
    collections.append(PaymentCollection())
    collections.append(VPNCollection())
    collections.append(SocialCollection())
    collections.append(LoginCollection())
    collections.append(InputCollection())

    processed_collections = process(input_path='targets.txt', collections=collections,
                                    get_source=True, output_path='./output/sources/')

    export_json(output_path='output.json', collections=processed_collections)
    export_csv(output_path='output.csv', collections=processed_collections)
