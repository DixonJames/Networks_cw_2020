type_display = ['TO-ALL:', 'WHISPER:', 'CHANGE NAME REQUEST:', "REQUEST TO QUIT", "REQUEST LIST OF USERS", "BROADCAST TO EVERYONE", "REQUESTED LIST OF COMMANDS"]
command_prefixes = ['/all', '/whisper', '/newname', '/quit', '/users', '/broadcast', '/help']

command_description = ['sends to all OTHER users (selected by default if no \'/\' entered)', 'sends to one user '
                                                                                             'specified user',
                       'changes users username to a new one of users choice', 'asks server to remove user\'s socket '
                                                                              'from the list on the server. also '
                                                                              'closes the users client program',
                       'send a list of all current users usernames to users client', 'sends message to ALL clients '
                                                                                     'currently connected to server', 'displays all command and their descriptions (this!)']
command_templates = ['/all -message here-', '/whisper -username- -message-', '/newname -username to chang to-', '/quit', '/users', '/broadcast -message-', '/help' ]



def helpString():
    whole = ''

    for c in range(len(command_prefixes)):

        whole += '\n'+ 'command: ' + command_prefixes[c]
        whole += '\n' +'template: '+ command_templates[c]
        whole += '\n' + 'description: ' + command_description[c]
        whole += '\n'
    return whole
print(helpString())