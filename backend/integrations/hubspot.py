# slack.py

import os
from dotenv import load_dotenv
import json
import base64
import secrets
import hashlib
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
import httpx
import asyncio
from redis_client import add_key_value_redis, get_value_redis, delete_key_redis


# Load environment variables from .env file
load_dotenv()

# HubSpot OAuth configuration
CLIENT_ID = os.getenv('HUBSPOT_CLIENT_ID')
CLIENT_SECRET = os.getenv('HUBSPOT_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8000/integrations/hubspot/oauth2callback'
AUTHORIZATION_URL = f'https://app-na2.hubspot.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=oauth'

TOKEN_URL = 'https://api.hubapi.com/oauth/v1/token'
async def authorize_hubspot(user_id, org_id):
    # Generate a random state and code_verifier
    state_data = {
        'state': secrets.token_urlsafe(32),
        'user_id': user_id,
        'org_id': org_id
    }
    encoded_state = base64.urlsafe_b64encode(json.dumps(state_data).encode('utf-8')).decode('utf-8')

    code_verifier = secrets.token_urlsafe(32)
    m = hashlib.sha256()
    m.update(code_verifier.encode('utf-8'))
    code_challenge = base64.urlsafe_b64encode(m.digest()).decode('utf-8').replace('=', '')

    # Build the authorization URL
    auth_url = f'{AUTHORIZATION_URL}&state={encoded_state}&code_challenge={code_challenge}&code_challenge_method=S256'

    # Store the state and code_verifier in Redis
    await asyncio.gather(
        add_key_value_redis(f'hubspot_state:{org_id}:{user_id}', json.dumps(state_data), expire=600),
        add_key_value_redis(f'hubspot_verifier:{org_id}:{user_id}', code_verifier, expire=600),
    )

    return auth_url

async def oauth2callback_hubspot(request: Request):
    if request.query_params.get('error'):
        raise HTTPException(status_code=400, detail=request.query_params.get('error_description'))

    code = request.query_params.get('code')
    encoded_state = request.query_params.get('state')
    state_data = json.loads(base64.urlsafe_b64decode(encoded_state).decode('utf-8'))

    original_state = state_data.get('state')
    user_id = state_data.get('user_id')
    org_id = state_data.get('org_id')

    # Retrieve the saved state and code_verifier from Redis
    saved_state, code_verifier = await asyncio.gather(
        get_value_redis(f'hubspot_state:{org_id}:{user_id}'),
        get_value_redis(f'hubspot_verifier:{org_id}:{user_id}'),
    )

    # Verify the state
    if not saved_state or original_state != json.loads(saved_state).get('state'):
        raise HTTPException(status_code=400, detail='State does not match.')

    # Exchange the authorization code for an access token
    async with httpx.AsyncClient() as client:
        response = await client.post(
            TOKEN_URL,
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': REDIRECT_URI,
                'client_id': CLIENT_ID,
                'code_verifier': code_verifier,
            },
            headers={
                'Authorization': f'Basic {base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()}',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        )

    # Store the access token in Redis
    await add_key_value_redis(f'hubspot_credentials:{org_id}:{user_id}', json.dumps(response.json()), expire=600)

    # Return a response to close the popup window
    close_window_script = """
    <html>
        <script>
            window.close();
        </script>
    </html>
    """
    return HTMLResponse(content=close_window_script)

async def get_hubspot_credentials(user_id, org_id):
    credentials = await get_value_redis(f'hubspot_credentials:{org_id}:{user_id}')
    if not credentials:
        raise HTTPException(status_code=400, detail='No credentials found.')
    credentials = json.loads(credentials)
    await delete_key_redis(f'hubspot_credentials:{org_id}:{user_id}')

    return credentials

async def create_integration_item_metadata_object(response_json, item_type, parent_id=None, parent_name=None):
    parent_id = None if parent_id is None else parent_id + '_' + item_type
    integration_item_metadata = {
        'id': response_json.get('id', None) + '_' + item_type,
        'name': response_json.get('name', None),
        'type': item_type,
        'parent_id': parent_id,
        'parent_path_or_name': parent_name,
    }

    return integration_item_metadata

async def get_items_hubspot(credentials):
    # credentials = json.loads(credentials)
    # access_token = credentials.get('access_token')
    # url = 'https://api.hubapi.com/crm/v3/objects/contacts'
    # headers = {'Authorization': f'Bearer {access_token}'}
    #
    # response = httpx.get(url, headers=headers)
    # if response.status_code != 200:
    #     raise HTTPException(status_code=400, detail='Failed to fetch HubSpot items.')
    #
    # contacts = response.json().get('results', [])
    # list_of_integration_item_metadata = []
    # for contact in contacts:
    #     list_of_integration_item_metadata.append(
    #         await create_integration_item_metadata_object(contact, 'Contact')
    #     )

    return { 'data' :'1234' }  #list_of_integration_item_metadata

# async def authorize_hubspot(user_id, org_id):
#     # TODO
#     pass

# async def oauth2callback_hubspot(request: Request):
#     # TODO
#     pass

# async def get_hubspot_credentials(user_id, org_id):
#     # TODO
#     pass

# async def create_integration_item_metadata_object(response_json):
#     # TODO
#     pass

# async def get_items_hubspot(credentials):
#     # TODO
#     pass