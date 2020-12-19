import unittest


ttype_lookup = {'/all':0, '/whisper':1, '/newname':2, '/quit':3, '/users':4}

type_display = ['TO-ALL:', 'WHISPER:', 'CHANGE NAME REQUEST:', "REQUESTING TO QUIT", "REQUESTS LIST OF USERS"]
command_prefixes = ['/all', '/whisper', '/newname', '/quit', '/users']

sockets = ['james', 'seb', 'baz', 'dixon']

def recipientsViaType(message_type, all_posible_recipients, sender, message_data=None):
    """
    type_lookup = {'all': 0, 'whisper':1, 'command':2, 'USERNAME':3}
    :param message_type:
    :param all_posible_recipients:
    :param message_data:
    :return:
    """

    try:
        sender = next(key for key, value in sockets.items() if value == f'{message_data.split(" ")[0]}')
    except:
        sender = False

    # to all
    if message_type == 0 or message_type == 2 or message_type == 3:
        return all_posible_recipients

    # to one whisperUser
    elif message_type == 1:
        if sender:
            # reverse dict lookup
            all_posible_recipients = [rev_dict_lookup(self.client_username, message_data.split(" ")[0])]

            if not (all_posible_recipients[0]):
                return all_posible_recipients
        else:
            return False

    else:
        return False

    if message_type == 4:
        return [sender]

message_type = 1
sender = 'james'

recipients = recipientsViaType(message_type, [[recipient] for recipient in sockets if not sender],current_socket, message_data)
