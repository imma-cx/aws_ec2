import boto3
import argparse

ec2_sast_95 = 'i-0472093c8ac85b82f' 
ec2_reporting = 'i-0a29ae053aab7a357'

# Replace the values in the following variables with your own information
region = 'us-east-1'
instance_ids = [ec2_sast_95, ec2_reporting] # Replace with your own instance IDs
ec2 = boto3.client('ec2', region_name=region)

def get_instance_name(instance_id, region):
    ec2 = boto3.resource('ec2', region_name=region)
    instance = ec2.Instance(instance_id)
    instance_tags = {tag['Key']: tag['Value'] for tag in instance.tags}
    return instance_tags.get('Name', 'unknown')

def get_instance_name_array(array):
    results = []
    for string in array:
        if isinstance(string, str):
            # If the current element is a string, call the function with the string
            result = get_instance_name(string, region)
            results.append(result)
        elif isinstance(string, list):
            # If the current element is a list, call this function recursively with the list
            nested_results = get_instance_name_array(string)
            results.extend(nested_results)
        else:
            # If the current element is not a string or a list, raise an exception
            raise ValueError('Invalid element type: {}'.format(type(string)))
        result_string = ', '.join(results)
    return result_string

def start_instances(instance_ids):

    # Start the instances
    response = ec2.start_instances(InstanceIds=instance_ids)
    print('Starting instances:', get_instance_name_array(instance_ids))

    # Print the response from AWS
    print('Response:', response)


def get_instance_id(instance_name_or_id, region):
    ec2 = boto3.resource('ec2', region_name=region)
    if instance_name_or_id.startswith('i-'):  # assume it's an ID
        instances = list(ec2.instances.filter(InstanceIds=[instance_name_or_id]))
    else:  # assume it's a name
        filters = [{'Name': 'tag:Name', 'Values': [instance_name_or_id]}]
        instances = list(ec2.instances.filter(Filters=filters))
    if not instances:
        raise ValueError('Instance not found: {}'.format(instance_name_or_id))
    elif len(instances) > 1:
        raise ValueError('Multiple instances found: {}'.format(instance_name_or_id))
    else:
        return instances[0].id

def start_instance(instance_name_or_id, region):
    ec2 = boto3.client('ec2', region_name=region)
    instance_id = get_instance_id(instance_name_or_id, region)
    ec2.start_instances(InstanceIds=[instance_id])
    print('Starting instance {}...'.format(instance_id))

def stop_instance(instance_name_or_id, region):
    ec2 = boto3.client('ec2', region_name=region)
    instance_id = get_instance_id(instance_name_or_id, region)
    ec2.stop_instances(InstanceIds=[instance_id])
    print('Stopping instance {}...'.format(instance_id))

def main():
    parser = argparse.ArgumentParser(description='Start or stop an EC2 instance by name or ID')
    parser.add_argument('instance_name_or_id', type=str, help='The name or ID of the EC2 instance')
    parser.add_argument('--region', type=str, default='us-east-1', help='The AWS region where the instance is located (default: us-east-1)')
    parser.add_argument('--start', action='store_true', help='Start the specified EC2 instance')
    parser.add_argument('--stop', action='store_true', help='Stop the specified EC2 instance')
    args = parser.parse_args()

    if args.start and args.stop:
        print('Error: Only one of --start or --stop can be specified')
    elif args.start:
        start_instance(args.instance_name_or_id, args.region)
    elif args.stop:
        stop_instance(args.instance_name_or_id, args.region)
    else:
        print('Error: Either --start or --stop must be specified')

if __name__ == '__main__':
    main()