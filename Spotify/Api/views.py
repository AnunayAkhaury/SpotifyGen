from django.shortcuts import render
from requests import post
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from requests import Request
from django.http import HttpResponseRedirect, JsonResponse
from .cred import CLIENT_ID, CLIENT_SECRET, REDIRECT_URL
from .extras import create_or_update_tokens, is_spotify_authenticated,spotify_requests_execution, refresh_token_function
from .models import Token
from .SongOpenAI import SongInput
import json
from django.core.cache import cache

# Create your views here.
class AuthenticationURLView(APIView):
    def get(self, request, format = None):
        scopes = "user-read-private user-read-email playlist-modify-public playlist-modify-private user-read-playback-state user-read-currently-playing"
        url = Request('GET', 'https://accounts.spotify.com/authorize', params= {
            'scope' : scopes,
            'response_type' : 'code',
            'redirect_uri' : REDIRECT_URL,
            'client_id' : CLIENT_ID
        }).prepare().url
        return HttpResponseRedirect(url)
    
def spotify_redirect(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    if error:
        return error
    
    response = post('https://accounts.spotify.com/api/token', data = {
        'grant_type' : 'authorization_code',
        'code' : code,
        'redirect_uri' : REDIRECT_URL,
        'client_id' : CLIENT_ID,
        'client_secret' : CLIENT_SECRET
    }).json()
    
    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    token_type = response.get('token_type')
    
    authKey = request.session.session_key
    if not request.session.exists(authKey):
        request.session.create()
        authKey = request.session.session_key
        
    create_or_update_tokens(
        session_id=authKey,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in,
        token_type=token_type
    )
    
    user_id = GetUserId(authKey)
    redirect_url = f"http://127.0.0.1:8000/spotify/CreatePlaylist?key={authKey}&user_id={user_id}"
    return HttpResponseRedirect(redirect_url)

class CheckAuthentication(APIView):
    def get(self, request, format = None):
        key = self.request.session.session_key
        if not self.request.session.exists(key):
            self.request.session.create()
            key = self.request.session.session_key
        
        auth_status = is_spotify_authenticated(key)
        
        if auth_status:

            user_id = GetUserId(key)
            if user_id:

                redirect_url = f"http://127.0.0.1:8000/spotify/CreatePlaylist?key={key}&user_id={user_id}"

                return HttpResponseRedirect(redirect_url)
            else:
                return Response({'error': 'Failed to get user ID'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print('auth required')
            redirect_url =f"http://127.0.0.1:8000/spotify/auth-url"
            return HttpResponseRedirect(redirect_url)


def GetUserId(key):
        token = Token.objects.get(user = key)
        print(token)
        
        endpoint = 'me'
        headers = {'Content-Type': 'application/json', 'Authorization' : 'Bearer ' + token.access_token}
        response = spotify_requests_execution(key,endpoint,'GET',data=None)
        
        if "error" in response or "id" not in response:
            return Response({}, status= status.HTTP_204_NO_CONTENT)
        user_id = response.get('id')
        print(user_id)
        
        return(user_id)

class CreatePlaylist(APIView):
    kwarg1 = "key"
    kwarg2 = "user_id"
    def get(self,request,format = None):
        key = request.GET.get(self.kwarg1)
        user_id = request.GET.get(self.kwarg2)
        try:
            token = Token.objects.get(user=key)
        except Token.DoesNotExist:
            return Response({'error': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)
        refresh_token_function(key)

        songName = getCurrentSong(key)
        if(songName ==  False):
            message = 'error: No Song is playing please try again after playing song'
            frontend_url = 'http://localhost:3000/'
            return HttpResponseRedirect(f'{frontend_url}?message={message}')
            
        
        
        endpoint = f"users/{user_id}/playlists"
        
        playlist_data = {
        "name": "Custom Spotify Playlist",
        "description": "Based of Current Playing Song",
        "public": False
        }

        
        response = spotify_requests_execution(key,endpoint,'POST',playlist_data)
        
        if response is None:
            return Response({'error': 'No response from Spotify API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        if "error" in response or "id" not in response:
            return Response({}, status= status.HTTP_204_NO_CONTENT)
        
        playlist_id = response.get('id')
        
        
        AIresponse = (SongInput(songName).content)
        AIresponse = AIresponse.split('\n')
        
        message = f'CURRENT SONG {songName} PLAYLIST CREATED WITH CUSTOM SONGS' if AddSongs(AIresponse, playlist_id, key) else f'CURRENT SONG {songName} Playlist Was not able to be created'
        frontend_url = 'http://localhost:3000/' 
        
        return HttpResponseRedirect(f'{frontend_url}?message={message}')
        
def getCurrentSong(key):
    try:
    
        token = Token.objects.get(user = key)
        print(token)
        
        endpoint = "me/player/currently-playing"
        response = spotify_requests_execution(key,endpoint,'GET',data=None)
        if (response == False):
            return False
        
        if "error" in response or "item" not in response:
            return Response({}, status= status.HTTP_204_NO_CONTENT)
        
        item = response.get('item')
        title = item.get('name')
        artist = item["artists"][0].get("name")
        is_playing = response.get('is_playing')
        
        
        if not is_playing:
            return False
        
        return (f'{title} by {artist}')
    except:
        return Response({'error': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)
        
def AddSongs(input, playlist_id, key):
    songStr =''
    for title in input:
        id = SearchSong(title, key)
        if (id == '204'):
            continue
        else:
            songStr += f'spotify:track:{id}, '
    
    
    
    songStr = songStr.rstrip(',')
    songStr = songStr.split(',')
    
    uri_list = []
    
    
    for uri in songStr:
        uri = uri.strip()
        if uri:
            uri_list.append(uri)
        
    json_data = {"uris": uri_list}
    
    print(json_data)
    
    try:
        token = Token.objects.get(user=key)
    except Token.DoesNotExist:
        return Response({'error': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)
    
    endpoint = f'playlists/{playlist_id}/tracks'
    
    response = spotify_requests_execution(key,endpoint,'POST', data=json_data)
    
    if response is None:
        return Response({'error': 'No response from Spotify API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    if "error" in response:
        return Response({}, status= status.HTTP_204_NO_CONTENT)
    
    return True
    
    
    
def SearchSong(input, key):
    endpoint = f'search?q={input}&type=track'
    
    
    response = spotify_requests_execution(key,endpoint,'GET',data=None)
    
    tracks = response.get('tracks')

    if "items" in tracks and len(tracks["items"]) > 0:
        first_track = tracks["items"][0]
        id = first_track.get("id")
        print(id)
        return(id)
    else:
        return ('204')