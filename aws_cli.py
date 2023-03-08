import argparse
import boto3

region = 'us-east-1'

def get_instance_name(instance_id, region):
    ec2 = boto3.resource('ec2', region_name=region)
    instance = ec2.Instance(instance_id)
    instance_tags = {tag['Key']: tag['Value'] for tag in instance.tags}
    return instance_tags.get('Name', 'unknown')

def get_instance_name_array(array):
    results = []
    for string in array:
        if isinstance(string, str):
            result = get_instance_name(string, region)
            results.append(result)
        elif isinstance(string, list):
            nested_results = get_instance_name_array(string)
            results.extend(nested_results)
        else:
            raise ValueError('Invalid element type: {}'.format(type(string)))
        result_string = ', '.join(results)
    return result_string

def get_instance_ids(instance_names_or_ids, region):
    ec2 = boto3.resource('ec2', region_name=region)
    instance_ids = []
    for instance_name_or_id in instance_names_or_ids:
        if instance_name_or_id.startswith('i-'):
            instance_ids.append(instance_name_or_id)
        else:
            filters = [{'Name': 'tag:Name', 'Values': [instance_name_or_id]}]
            instances = ec2.instances.filter(Filters=filters)
            for instance in instances:
                instance_ids.append(instance.id)
    return instance_ids

def start_instances(instance_names_or_ids, region):
    ec2 = boto3.client('ec2', region_name=region)
    instance_ids = get_instance_ids(instance_names_or_ids, region)
    response = ec2.start_instances(InstanceIds=instance_ids)
    return response

def stop_instances(instance_names_or_ids, region):
    ec2 = boto3.client('ec2', region_name=region)
    instance_ids = get_instance_ids(instance_names_or_ids, region)
    response = ec2.stop_instances(InstanceIds=instance_ids)
    return response

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start or stop EC2 instances')
    parser.add_argument('instance_names_or_ids', metavar='INSTANCE', nargs='+',
                        help='name or ID of EC2 instance(s) to start or stop')
    parser.add_argument('--region', dest='region', default='us-east-1',
                        help='AWS region where the instances are located (default: us-east-1)')
    parser.add_argument('--start', dest='start', action='store_true',
                        help='start the specified EC2 instance(s)')
    parser.add_argument('--stop', dest='stop', action='store_true',
                        help='stop the specified EC2 instance(s)')
    args = parser.parse_args()

    if args.start:
        response = start_instances(args.instance_names_or_ids, args.region)
        print(response)
    elif args.stop:
        response = stop_instances(args.instance_names_or_ids, args.region)
        print(response)
    else:
        print('Please specify either --start or --stop')
