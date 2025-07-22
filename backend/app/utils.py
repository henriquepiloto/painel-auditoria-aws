import boto3

def make_creds_dict(creds):
    return {
        'aws_access_key_id': creds['Credentials']['AccessKeyId'],
        'aws_secret_access_key': creds['Credentials']['SecretAccessKey'],
        'aws_session_token': creds['Credentials']['SessionToken']
    }

def check_iam(creds, cliente, account_id):
    iam = boto3.client('iam', **creds)
    findings = []

    response = iam.list_users()
    for user in response.get("Users", []):
        if user['UserName'].lower().startswith('test'):
            findings.append({
                "cliente": cliente,
                "account_id": account_id,
                "usuario": user['UserName'],
                "problema": "Usuário de teste identificado"
            })

    return findings
