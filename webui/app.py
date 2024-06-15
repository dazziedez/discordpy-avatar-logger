from flask import Flask, render_template, abort
from werkzeug.middleware.proxy_fix import ProxyFix

from os import path, listdir
from datetime import datetime

import json
import os
from datetime import datetime
import requests

import handler
from handler import error_map

app = Flask(__name__)

app.register_error_handler(Exception, handler.handle_error)


class AvatarManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.avatar_directory = os.path.join(
            os.path.dirname(__file__), 'static/avatars/', user_id)
        self.user_info = self.fetch_user_info()

    def _load_avatars(self):
        if not os.path.exists(self.avatar_directory):
            abort(404)
        avatars = [avatar for avatar in os.listdir(
            self.avatar_directory) if avatar != 'user_info.json']
        avatars_info = []
        for avatar in avatars:
            date_str = avatar.split('.')[0]
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d_%H-%M-%S')
                formatted_date = date_obj.strftime('%B %d %Y')
                full_datetime = date_obj.isoformat()
            except ValueError:
                formatted_date = "Unknown Date"
                full_datetime = datetime.min.isoformat()
            avatars_info.append(
                (self.user_id, avatar, formatted_date, 'avatars/' + self.user_id + '/' + avatar, full_datetime))
        avatars_info.sort(key=lambda x: x[4], reverse=True)
        return avatars_info

    @property
    def avatars(self):
        return self._load_avatars()

    def fetch_user_info(self):
        cache_file = os.path.join(self.avatar_directory, 'user_info.json')
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as file:
                user_info = json.load(file)
                if len(os.listdir(self.avatar_directory)) - 1 > user_info.get('avatar_count', 0):
                    user_info = self._update_user_info(cache_file)
        else:
            user_info = self._update_user_info(cache_file)
        return user_info

    def _update_user_info(self, cache_file, _=None):
        config_path = os.path.join(
            os.path.dirname(__file__), '..', 'config.json')
        with open(config_path, 'r') as file:
            config = json.load(file)
        url = f"https://discord.com/api/v9/users/{self.user_id}"
        headers = {'Authorization': f'Bot {config["bot_token"]}'}
        updated_info = requests.get(url, headers=headers).json()
        updated_info['last_updated'] = datetime.now().isoformat()
        updated_info['avatar_count'] = len([file for file in os.listdir(
            self.avatar_directory) if file != 'user_info.json'])
        with open(cache_file, 'w') as file:
            json.dump(updated_info, file)
        return updated_info


@app.route('/<user_id>')
def user_avatars(user_id):
    avatar_manager = AvatarManager(user_id)
    users_avatars = avatar_manager.avatars
    user_info = avatar_manager.fetch_user_info()

    return render_template('index.html', user_id=user_id, user=user_info, users_avatars=users_avatars) or abort(404)


@app.route('/')
def list_users():
    avatar_directory = path.join(path.dirname(__file__), 'static', 'avatars')
    users_list = []
    try:
        user_ids = [name for name in listdir(avatar_directory) if path.isdir(
            path.join(avatar_directory, name))]

        if not user_ids:
            return render_template('error.html', error={"name": "Empty", "code": "000", "description": "Nothing to see here..\nWait for the avatars to be logged!"})

        for user_id in user_ids:
            user_info_path = path.join(
                avatar_directory, user_id, 'user_info.json')
            user_info_exists = path.exists(user_info_path)
            if user_info_exists:
                with open(user_info_path, 'r') as file:
                    user_info = json.load(file)
                username = user_info.get('username', user_id)
            else:
                username = user_id

            avatar_dir = path.join(avatar_directory, user_id)
            avatar_files = [f for f in listdir(avatar_dir) if path.isfile(
                path.join(avatar_dir, f)) and f != 'user_info.json']
            if avatar_files:
                try:
                    latest_avatar = max(avatar_files, key=lambda f: datetime.strptime(
                        f.split('.')[0], '%Y-%m-%d_%H-%M-%S'))
                except ValueError:
                    latest_avatar = avatar_files[0]
                avatar_url = path.join(
                    'static', 'avatars', user_id, latest_avatar)
            else:
                avatar_url = 'default_avatar.png'

            users_list.append({
                'id': user_id,
                'name': username,
                'avatar_count': len(avatar_files),
                'avatar_url': avatar_url
            })
        return render_template('root.html', users_list=users_list)
    except FileNotFoundError:
        return "Avatar directory not found", 404


app.run(debug=False)
