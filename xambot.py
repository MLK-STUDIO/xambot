import discordmlk

token = open('token', 'r').read()
discord = discordmlk.Discord(token)

def main():
    discord.set_recieve_message_function(recieve_message)
    print('Все системы запущены, жук готов к бою!')


def recieve_message(response):
    print(f'{response["d"]["author"]["username"]}: {response["d"]["content"]}')
    univ_content = response['d']['content'].lower().replace(' ', '')

    apply_command = lambda x: discord.send_slash_command('1033663376938770482', '1023529522760532020', '1023540638186217473', 'ca14a31ab72e655413a2e93fffa2be25', x, '792042309503418400')
    if univ_content == 'жукпогладьхама':
        apply_command('pat')
    elif univ_content == 'жуккусихама':
        apply_command('bite')
    elif univ_content == 'жукобнимихама':
        apply_command('hug')
    elif univ_content == 'жукоближихама':
        apply_command('lick')
    elif univ_content == 'жукпоцелуйхама':
        apply_command('kiss')
    elif univ_content == 'жуклюбихама':
        discord.send_message('1023540638186217473', '<@792042309503418400> я тебя :heart:')

    author_id = response['d']['author']['id']
    apply_command = lambda x: discord.send_slash_command('1033663376938770482', '1023529522760532020', '1023540638186217473', 'ca14a31ab72e655413a2e93fffa2be25', x, f'{author_id}')
    if univ_content == 'жукпогладьменя':
        apply_command('pat')
    elif univ_content == 'жуккусименя':
        apply_command('bite')
    elif univ_content == 'жукобнимименя':
        apply_command('hug')
    elif univ_content == 'жукоближименя':
        apply_command('lick')
    elif univ_content == 'жукпоцелуйменя':
        apply_command('kiss')
    elif univ_content == 'жуклюбименя':
        discord.send_message('1023540638186217473', f'<@{author_id}> я тебя :heart:')


if __name__ == '__main__':
    main()
