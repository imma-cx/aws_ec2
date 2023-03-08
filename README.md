# EC2 Instance Control Script

This script allows you to start or stop EC2 instances in your AWS account, based on their name or instance ID. You can also specify multiple names/IDs separated by commas.

## Prerequisites

- Python 3.x
- Boto3 library

## Setup

1. Install the Boto3 library: `pip install boto3`
2. Configure your AWS credentials:
   - Set up the AWS CLI: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
   - Set the `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_DEFAULT_REGION` environment variables.
3. Download the `aws_cli.py` script from this repository.

## Usage

'python ec2_control.py [instance_name_or_id] --start | --stop'

- Replace `[instance_name_or_id]` with the name or ID of the instance you want to start/stop. You can also specify multiple names/IDs separated by commas.
- Use the `--start` option to start the instance(s).
- Use the `--stop` option to stop the instance(s).

Example usage:

'python ec2_control.py my-instance-id --stop'
'python ec2_control.py my-instance-name,i-3nhi45bd --start'

## Notes

- The script assumes that instance IDs always start with `i-`.
- If you provide both instance names and IDs, the script will prioritize IDs over names.
- The script may require additional permissions depending on your AWS IAM configuration.
