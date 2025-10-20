import boto3
import json
import os
from botocore.exceptions import ClientError

def get_secret():
    secret_name = "myapp/prod/env"
    region_name = "us-west-1"
    
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

def load_secrets_to_env():
    """Load secrets from AWS Secrets Manager into environment variables"""
    
    # Check if we're running in AWS (production)
    is_aws = os.getenv('AWS_EXECUTION_ENV') or os.getenv('EC2_INSTANCE_ID') or os.path.exists('/opt/aws')
    
    if is_aws:
        try:
            secrets = get_secret()
            
            # Set each secret as an environment variable
            for key, value in secrets.items():
                os.environ[key] = str(value)
                
            print("✅ Loaded secrets from AWS Secrets Manager")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load secrets from AWS: {e}")
            print("🔧 Falling back to local .env file")
            return False
    else:
        print("🔧 Running locally - using .env file")
        return False
