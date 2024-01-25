Spotify Custom Playlist Generator
Backend Implemented through Python/Django
Frontend Implemented Through React + Bootstrap

Spotify Django Project
About
This project is a Django web application that integrates with the Spotify API. It allows users to interact with various Spotify features such as searching for songs, creating playlists, and exploring new music. The application aims to provide a seamless and interactive way to experience Spotify through a custom web interface.


Installation
Prerequisites
Python 3.6 or later
Django 3.1 or later
A Spotify Developer account and API key
Setup
Clone the Repository

Setup
git clone https://github.com/yourusername/spotify-django-project.git
cd spotify-django-project
Install Dependencies

Install Dependancies
pip install -r requirements.txt
Set up Spotify API Credentials

Create a .env file in the project root.
Add your Spotify API credentials:
SPOTIFY_CLIENT_ID='your_client_id'
SPOTIFY_CLIENT_SECRET='your_client_secret'

Initialize Database
python manage.py migrate

Run the Server
python manage.py runserver
