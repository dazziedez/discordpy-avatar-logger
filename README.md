# Avatar Logger

This repo contains a Flask-based web application designed for managing and displaying user avatars, alongside a Discord bot responsible for logging the avatars themselves. The system allows for the fetching and displaying of user avatars and information through a web interface, as well as updating and storing this information efficiently.

## Features

- **Avatar Management**: Users can view a history of their avatars stored in a dedicated directory, accessible through a web interface.
- **User Information Fetching**: The system fetches and displays user information, including the latest avatar, using Discord's API.
### Screenshots
|Main (WIP)|User view|
|---------|----------|
|![Main](https://i.imgur.com/9Aat9Cj.png)|![User](https://i.imgur.com/MTBvCnp.png)|

## Installation

To set up the Avatar Logger and Management System, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/dazziedez/discordpy-avatar-logger.git
   cd discordpy-avatar-logger
   ```

2. **Install Dependencies**
   Ensure you have Python 3.6+ installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration**
   - Create a `config.json` file in the root directory with the following structure:
     ```json
     {
       "bot_token": "YOUR_DISCORD_BOT_TOKEN"
     }
     ```
   - Adjust the Flask and bot settings as necessary in their respective files.

> [!NOTE]
> Please refer to [this article](flask.palletsprojects.com/en/2.3.x/deploying/proxy_fix/) when using a reverse proxy.
> 
> I'd recommend you generally refer to [this article](https://flask.palletsprojects.com/en/2.3.x/deploying/) as well!
4. **Run the application**
   This will run the bot AND the flask app, simultaneously
   ```bash
   python start.py
   ```

## Usage
> [!NOTE]
> You may need to tell Flask that you're using a proxy.

- Navigate to `http://your.domain/<user_id>` to view the avatars and information for a specific user.
- The Discord bot will automatically log avatar changes when configured and running.

## Contributing

Contributions to the Avatar Logger and Management System are welcome!!
Do whatever i don't care lmaoao

## License

See the LICENSE file.

## Acknowledgments

- Flask for the web framework.
- Discord API for user information and avatar management.
- The Python community for the various libraries used in this project. (I stole a lot)
