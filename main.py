# This bot checks list of the chats specified below and kicks deleted accounts

from pyrogram import Client
import time
import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

api_id = cfg['telegram']['api_id']
api_hash = cfg['telegram']['api_hash']
notify_before = cfg['notifications']['notify_before']
notify_after = cfg['notifications']['notify_after']
notify_before_ids = cfg['notifications']['notify_before_ids']
notify_after_ids = cfg['notifications']['notify_after_ids']
chat_ids = cfg['bot']['chat_ids']
SLEEP_PER_CHAT = cfg['bot']['sleep_per_chat']
SLEEP_AFTER_KICK = cfg['bot']['sleep_after_kick']

def main():
    with Client("my_account", api_id, api_hash) as app:
        overall_kick_count = 0
        report = ""

        if notify_before:
            for user_id in notify_before_ids:
                do_notify_before(user_id, app)

        for chat_id in chat_ids:
            chat_id = int(chat_id)
            chat_info = app.get_chat(chat_id)
            
            print("==========================================")
            print("")
            print("Working on chat {} now".format(chat_info.title))
            report += "=========================== \n {}\n===========================\n".format(chat_info.title)
            member_list = app.iter_chat_members(chat_id)
            kick_list = []
            skip_chat = False

            found_self = False
            for member in member_list:
                if member.user.is_self:
                    found_self = True
                    if (not member.status == "administrator" or not member.can_restrict_members) and not member.status == "creator":
                        msg = "⚠️⚠️⚠️ I have no permissions to kick members in {}. Skipping this chat... \n\n".format(chat_info.title)
                        print(msg)
                        report += msg+"\n"
                        skip_chat = True
                if member.user.is_deleted:
                    kick_list.append(member)
            
            if not found_self:
                msg = "⚠️⚠️⚠️ I'm no member of the group {}! Skipping this chat...\n\n".format(chat_info.title)
                print(msg)
                report += msg+"\n"
                skip_chat = True
            if skip_chat:
                continue

            print("Members to kick from {}".format(chat_info.title))
            kick_count = 0
            for member in kick_list:
                display_userinfo(member)
                try:
                    app.kick_chat_member(chat_id, member.user.id)
                    kick_count += 1
                    time.sleep(SLEEP_AFTER_KICK)
                except:
                    msg = "Error occured when kicking user"
                    print(msg)
                    report += msg+"\n"
            overall_kick_count += kick_count

            msg = "Kicked {} deleted accounts from {}".format(kick_count, chat_info.title)
            print(msg)
            report += msg + "\n"

            print("Sleeping for {} seconds before continuing with next chat".format(SLEEP_PER_CHAT))
            time.sleep(SLEEP_PER_CHAT)
            report += "\n\n"
        msg = "Kicked {} users overall.".format(overall_kick_count)
        print(msg)
        report += "\n\n"+msg

        if notify_after:
            for user_id in notify_after_ids:
                do_notify_after(user_id, app, report)

def display_userinfo(chat_member):
    print("Name: {} {} (@{})".format(chat_member.user.first_name, chat_member.user.last_name, chat_member.user.username))
    print("is_deleted: {}".format(chat_member.user.is_deleted))

def do_notify_before(user_id, client):
    client.send_message(int(user_id), "Starting to clean up groups from deleted accounts")

def do_notify_after(user_id, client, report):
    client.send_message(int(user_id), "Sucessfully cleaned up. Full report: ```{}```".format(report), "markdown")



if __name__ == "__main__":
    main()

