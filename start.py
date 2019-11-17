#!/bin/python3
from bucket.utils import get_aws_ranges, run
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

    run(input_path='targets.txt', output_json='targets.json',
        collections=collections, get_source=True, output_path='output/sources/')
