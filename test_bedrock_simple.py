"""
Simple AWS Bedrock API Test
Tests connection to AWS Bedrock with Claude 3 Haiku

Before running, set your AWS credentials as environment variables:
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_SESSION_TOKEN="your_session_token"
"""

import boto3
import json
import os
from botocore.exceptions import ClientError


def test_bedrock_connection():
    """Test AWS Bedrock connection with a simple Claude API call"""
    
    print("=" * 60)
    print("Testing AWS Bedrock Connection")
    print("=" * 60)
    
    # Check if credentials are set
    if not all([
        os.getenv('AWS_ACCESS_KEY_ID'),
        os.getenv('AWS_SECRET_ACCESS_KEY'),
        os.getenv('AWS_SESSION_TOKEN')
    ]):
        print("\n❌ ERROR: AWS credentials not found!")
        print("Please set the following environment variables:")
        print("  - AWS_ACCESS_KEY_ID")
        print("  - AWS_SECRET_ACCESS_KEY")
        print("  - AWS_SESSION_TOKEN")
        return False
    
    # Create Bedrock Runtime client
    region_name = "eu-west-1"
    print(f"\n📍 Region: {region_name}")
    
    try:
        client = boto3.client("bedrock-runtime", region_name=region_name)
        print("✅ Client created successfully")
    except Exception as e:
        print(f"❌ Failed to create client: {e}")
        return False
    
    # Set the model ID (Claude 3 Haiku)
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    print(f"🤖 Model: {model_id}")
    
    # Define the prompt
    prompt = "Describe the purpose of a 'hello world' program in one line."
    print(f"\n💬 Prompt: {prompt}")
    
    # Format the request payload
    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }
    
    # Convert to JSON
    request = json.dumps(native_request)
    
    # Invoke the model
    print("\n⏳ Calling Bedrock API...")
    try:
        response = client.invoke_model(modelId=model_id, body=request)
        print("✅ API call successful!")
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"\n❌ AWS ClientError:")
        print(f"   Code: {error_code}")
        print(f"   Message: {error_message}")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
    
    # Decode the response
    try:
        model_response = json.loads(response["body"].read())
        response_text = model_response["content"][0]["text"]
        
        print("\n" + "=" * 60)
        print("📝 RESPONSE:")
        print("=" * 60)
        print(response_text)
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to parse response: {e}")
        return False


if __name__ == "__main__":
    success = test_bedrock_connection()
    
    if success:
        print("\n✅ Test completed successfully!")
        exit(0)
    else:
        print("\n❌ Test failed!")
        exit(1)

