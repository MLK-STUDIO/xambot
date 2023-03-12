import discordmlk
import discordmlk.covers as covers

data = open('token', 'r').read().split(';')
discord = discordmlk.Discord(login=data[0], password=data[1], token=data[2])

def main():
    print('Все системы запущены, жук готов к бою!')

rob = False

@discord.event
def on_message(message):
    print(f'{message.author.name}: {message.content}')
    content = message.content.lower()
    slash_command = None

    if not '<@912000324808617984>' in content and not 'жук' in content:
        return

    application_id = '1033663376938770482'
    guild_id = '1023529522760532020'
    channel_id = message.channel_id if message.member is not None else '1023540638186217473'

    if 'спать' in content or 'спи' in content:
        no_message = covers.Message(channel_id)
        no_message.set_message(message.channel_id, f'Не пойду!!!!')
        no_message.reply_to(message.guild_id, message.channel_id, message.id)
        discord.send_message(no_message)

    if 'хама' in content:
        print('start')
        slash_command = covers.SlashCommand(application_id, guild_id, channel_id, '')
        slash_command.add_option(6, 'user', '792042309503418400')
        if 'люби' in content:
            love_message = covers.Message(channel_id)
            love_message.set_message(channel_id, f'<@792042309503418400> я тебя :heart:')
            if message.member is not None:
                love_message.reply_to(guild_id, channel_id, message.id)
            discord.send_message(love_message)

    elif 'деда' in content:
        slash_command = covers.SlashCommand(application_id, guild_id, channel_id, '')
        slash_command.add_option(6, 'user', '431103899425046539')
        if 'люби' in content:
            love_message = covers.Message(channel_id)
            love_message.set_message(channel_id, f'<@431103899425046539> я тебя :heart:')
            if message.member is not None:
                love_message.reply_to(guild_id, channel_id, message.id)
            discord.send_message(love_message)

    elif 'меня' in content:
        slash_command = covers.SlashCommand(application_id, guild_id, channel_id, '')
        slash_command.add_option(6, 'user', message.author.id)
        if 'люби' in content:
            love_message = covers.Message(channel_id)
            love_message.set_message(channel_id, f'<@{message.author.id}> я тебя :heart:')
            if message.member is not None:
                love_message.reply_to(guild_id, channel_id, message.id)
            discord.send_message(love_message)

    if slash_command is not None and not 'люби' in content:
        if 'погладь' in content:
            slash_command.set_command_name('pat')
            discord.send_slash_command(slash_command)
        if 'куси' in content:
            slash_command.set_command_name('bite')
            discord.send_slash_command(slash_command)
        if 'обними' in content:
            slash_command.set_command_name('hug')
            discord.send_slash_command(slash_command)
        if 'оближи' in content:
            slash_command.set_command_name('lick')
            discord.send_slash_command(slash_command)
        if 'поцелуй' in content:
            slash_command.set_command_name('kiss')
            discord.send_slash_command(slash_command)

if __name__ == '__main__':
    main()
