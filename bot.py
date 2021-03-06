from irc.bot import SingleServerIRCBot
from requests import get
import config
import time
import react

import json


class bot(SingleServerIRCBot):
    def __init__(self):
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.USERNAME = config.NAME.lower()
        self.CHANNEL = f"#{config.OWNER}"

        url = f"https://api.twitch.tv/kraken/users?login={self.USERNAME}"
        headers = {"Client-ID": config.CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"}
        resp = get(url, headers=headers).json()
        self.channel_id = resp["users"][0]["_id"]

        super().__init__([(self.HOST, self.PORT, f"oauth:{config.TOKEN}")], self.USERNAME, self.USERNAME)

    def on_welcome(self, cxn, event):
        for req in ("membership", "tags", "commands"):
            cxn.cap("REQ", f":twitch.tv/{req}")

        cxn.join(self.CHANNEL)
        self.send_message("Now online.")

    def on_pubmsg(self, cxn, event):
        named_tuple = time.localtime()
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S ", named_tuple)
        tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
        user = {"name": tags["display-name"], "id": tags["user-id"]}
        message = event.arguments[0]

        if user["name"] != self.USERNAME:
            react.process(bot, user, message)
            with open('chat_file.txt', 'a', encoding="utf-8") as outfile:
                outfile.writelines(message + '\n')

        #print(f"Message from {user['name']}:{message}")

    def send_message(self, message):
        self.connection.privmsg(self.CHANNEL, message)

if __name__ == "__main__":
    bot = bot()
    bot.start()
