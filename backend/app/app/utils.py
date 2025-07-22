import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_s3_and_get_url(filepath: str, filename: str, bucket_name: str, expiration: int = 3600) -> str:
    s3_client = boto3.client("s3")

    try:
        s3_client.upload_file(filepath, bucket_name, filename)

        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': filename},
            ExpiresIn=expiration
        )
        return url

    except NoCredentialsError as e:
        raise Exception("Credenciais da AWS não encontradas.") from e

    except Exception as e:
        raise Exception(f"Erro ao fazer upload para o S3: {str(e)}")
