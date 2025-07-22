import boto3

def assume_role(account_id, role_name, session_name="auditoria"):
    sts_client = boto3.client('sts')
    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
    return sts_client.assume_role(RoleArn=role_arn, RoleSessionName=session_name)
