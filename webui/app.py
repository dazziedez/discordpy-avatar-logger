from flask import Flask, render_template, abort
from werkzeug.middleware.proxy_fix import ProxyFix

import json
import os
from datetime import datetime, timedelta
import requests

app = Flask(__name__)


class AvatarManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.avatar_directory = os.path.join('./static/avatars/', user_id)
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
                formatted_date = date_obj.strftime('%B %d, %Y, %H:%M:%S')
            except ValueError:
                formatted_date = "Unknown Date"
            avatars_info.append(
                (self.user_id, avatar, formatted_date, 'avatars/' + self.user_id + '/' + avatar))
        avatars_info.sort(key=lambda x: datetime.strptime(
            x[2], '%B %d, %Y, %H:%M:%S') if x[2] != "Unknown Date" else datetime.min, reverse=True)
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
                    user_info = self._update_user_info(cache_file, user_info)
        else:
            user_info = self._update_user_info(cache_file, {})
        return user_info

    def _update_user_info(self, cache_file, user_info):
        with open("config.json", 'r') as file:
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

    return render_template('index.html', user_id=user_id, user=user_info, users_avatars=users_avatars)


app.run(debug=True)
