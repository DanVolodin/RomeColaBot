# RomeColaBot
A simple telegram bot for managing groups with convenient and easy to use inline-commands

## Basic commands

**/help** - show help message with all commands

**/add_to_chat** - add bot to chat (It is important to give him necessary admin privileges)

## Commands in groups and supergroups:

**/promote_to_admin @username** - promote a user to administrator (He will be granted all the privileges that you have, unless you are not an owner. In this case the user will be given basic admin rights)

**/ban @username** - ban a user (The user will not be able to return to the chat on their own using invite links, etc., unless you unban him/her or add to chat manually)

**/unban @username** - unban a user (The user will not return automatically, but will be able to join via link, etc.)

**/stats** - see chat statistics: number of users and administrators

**/kick_romecolabot_no_please_no** - a super-powerful command to force bot to leave the chat (However, chat members information won't be demolished)

For "powerful" commands you need to have appropriate admin rights to run them.

## Inline commands

To make life and chat-management easier RomeColaBot provides an opportunity to use all this commands in inline mode, so that you don't need to type "/command" every time.
What you need to do - is just type "**@romecolabot**" or choose it from the list and commands will appear: "**Help**", "**Add RomeColaBot to chat**", "**Show chat statistics**" and "**Kick RomeColaBot**", which do completely the same as the commands above. (NB: if you type something after "**@romecolabot**" the commands will disappear).
For commands that manipulate with chat members you need to type "**@romecolabot @username**" and choose an appropriate command: "**Promote member**", "**Ban member**", "**Unban member**".

## TroubleShooting

If something goes wrong (incorrect username, no permission, etc.) RomeColaBot will tell you the exact problem in a short message, which will disappear in 10 seconds.

## Technical Issues

Chat members are handled using ChatsHandler class, so that it is easy to expansion the usage of the bot. All the data about chat members is stored in *data/chat_users/users_<chat_id>.json*. You can carefully change the path in ChatsHandler.

**Be Careful!** To clear all data within all chats you need to rerun bot setting *CLEAR* to true in paths.py.

In *paths.py* you can also change stickers/icons and bot messages.

If you want to add an exception to troubleshooting - just add it to *parse_exceptions* decorator in *main.py*.

Use wisely!
