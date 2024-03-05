from .models import Token
from django.utils import timezone
from datetime import timedelta
from requests import post, get
from .cred import CLIENT_ID,CLIENT_SECRET
import json
import aiohttp
import asyncio

BASE_URL = 'https://api.spotify.com/v1/'

def check_tokens(session_id):
    tokens = Token.objects.filter(user = session_id)
    print(tokens)
    if tokens:
        return tokens[0]
    else:
        return None
    
def create_or_update_tokens(session_id, access_token, refresh_token, expires_in, token_type):
    tokens = check_tokens(session_id)
    if expires_in is not None:
        expires_in = timezone.now() + timedelta(seconds = expires_in)
    else:
        expires_in = timezone.now() + timedelta(days=1)
    
    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token' , 'expires_in', 'token_type'])
    else:
        tokens = Token(
            user = session_id,
            access_token = access_token,
            refresh_token = refresh_token,
            expires_in = expires_in,
            token_type = token_type
        )
        tokens.save()
        
def is_spotify_authenticated(session_id):
    tokens = check_tokens(session_id)
    
    if tokens:
        if tokens.expires_in <= timezone.now():
            refresh_token_function(session_id)
        return True
    return False

def refresh_token_function(session_id):
    refresh_token = check_tokens(session_id).refresh_token
    
    response = post('https://accounts.spotify.com/api/token', data = {
        'grant_type' : 'refresh_token',
        'refresh_token' : refresh_token,
        'client_id' : CLIENT_ID,
        'client_secret' : CLIENT_SECRET
    }).json()
    
    if 'error' in response:
        print(f"Error refreshing token: {response['error']}")
        return
    
    access_token = response.get('access_token')
    expires_in = response.get('expires_in')
    token_type = response.get('token_type')
    
    if access_token is not None:
        create_or_update_tokens(
            session_id=session_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            token_type=token_type
        )
    
def spotify_requests_execution(session_id, endpoint, method, data):
    token = check_tokens(session_id)
    
    full_url = BASE_URL + endpoint
    headers = {'Content-Type': 'application/json', 'Authorization' : 'Bearer ' + token.access_token}
    if method == 'GET':
        response = get(full_url, headers=headers)
    elif method == 'POST':
        response = post(full_url, headers=headers, data=json.dumps(data))

    try:
        if response:
            print('Response Status Code:', response.status_code)
        return response.json()
    except:
        print(response.status_code)
        print('No Response!')
        return False

