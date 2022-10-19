from pytive import Pytive, CommentType

def message_test():
    live_id = ''

    client = Pytive()
    client.login('', '')

    client.join_live(live_id)
    client.comment(live_id, CommentType.NORMAL, 'pog')

if __name__ == '__main__':
    message_test()
