import mirrativ

def message_test():
    live_id = ''

    client = mirrativ.Mirrativ()
    client.login('', '')

    client.join_live(live_id)
    client.comment(live_id, 1, 'pog')

if __name__ == '__main__':
    message_test()
