import discordmlk as discordmlk

token = open('token', 'r').read()
discord = discordmlk.Discord(token)

def main():
    print('Все системы запущены, жук готов к бою!')

@discord.event
def on_message(response):
    print(f'{response["author"]["username"]}: {response["content"]}')
    content = response['content'].lower()
    univ_content = response['content'].lower().replace(' ', '')

    guild_id = None
    if 'guild_id' in response:
        guild_id = response['guild_id']
    channel_id = response['channel_id']
    author_id = response['id']
    apply_command = None

    if '<@912000324808617984>' in content or 'жук' in content:
        if 'спать' in content:
            discord.send_message(guild_id, channel_id, 'Не пойду!!!!', author_id)

        if 'хама' in univ_content:
            apply_command = lambda x: discord.send_slash_command('1033663376938770482', '1023529522760532020', '1023540638186217473', x, '792042309503418400')
            if 'люби' in univ_content:
                discord.send_message(guild_id, '1023540638186217473', '<@792042309503418400> я тебя :heart:')

        if 'меня' in univ_content:
            author_id = response['author']['id']
            apply_command = lambda x: discord.send_slash_command('1033663376938770482', '1023529522760532020', '1023540638186217473', x, f'{author_id}')
            if 'люби' in univ_content:
                discord.send_message(guild_id, '1023540638186217473', f'<@{author_id}> я тебя :heart:')

        if apply_command is not None:
            if 'погладь' in univ_content:
                apply_command('pat')
            if 'куси' in univ_content:
                apply_command('bite')
            if 'обними' in univ_content:
                apply_command('hug')
            if 'оближи' in univ_content:
                apply_command('lick')
            if 'поцелуй' in univ_content:
                apply_command('kiss')

if __name__ == '__main__':
    main()
