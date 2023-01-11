
from imbox import Imbox
import datetime
from urlextract import URLExtract

# SSL Context docs https://docs.python.org/3/library/ssl.html#ssl.create_default_context
# outlook_host = 'imap-mail.outlook.com'
# hotmail = 'outlook.office365.com'

def find_url(content):
    extractor = URLExtract()
    urls = extractor.find_urls(content)
    print(urls)
    return urls


#hotmail用
def get_verify_link(email, email_pw, sent_from="verify@twitter.com"):

    if 'outlook' in email:
        host = 'imap-mail.outlook.com'
    elif 'hotmail' in email:
        host = 'outlook.office365.com'
    else:
        host = 'outlook.office365.com'

    msglist = []
    with Imbox(host,
            username=email,
            password=email_pw,
            ssl=True,
            ssl_context=None,
            starttls=False) as imbox:

        # Messages sent FROM
        inbox_messages = imbox.messages(sent_from=sent_from)
        for uid, message in inbox_messages:
            # emaildict = dict(**message.sent_from[0], **{"plain": message.body.get('plain')[0]})
            msglist.append(dict(**message.sent_from[0], **{"plain": message.body.get('plain')[0], "date": message.date}))

    return msglist



if __name__ == "__main__":

    email = "@hotmail.com"
    email_pw = "ue4lMK41"
    msgs = get_verify_link(email, email_pw, sent_from="verify@twitter.com")
    import pdb;pdb.set_trace()
    print(msgs)

    
    # outlook_host = 'imap-mail.outlook.com'
    # hotmail = 'outlook.office365.com'
    # with Imbox('outlook.office365.com',
    #         username='rukamiotkei@hotmail.com',
    #         password='ue4lMK41',
    #         ssl=True,
    #         ssl_context=None,
    #         starttls=False) as imbox:

    #     # Get all folders
    #     status, folders_with_additional_info = imbox.folders()

    #     # Gets all messages from the inbox
    #     all_inbox_messages = imbox.messages()

    #     # import pdb;pdb.set_trace()

    #     # Unread messages
    #     unread_inbox_messages = imbox.messages(unread=True)

    #     # Messages sent FROM
    #     inbox_messages_from = imbox.messages(sent_from='sender@example.org')
    #     # import pdb;pdb.set_trace()


    #     # Flagged messages
    #     inbox_flagged_messages = imbox.messages(flagged=True)

    #     # Un-flagged messages
    #     inbox_unflagged_messages = imbox.messages(unflagged=True)

    #     # Flagged messages
    #     flagged_messages = imbox.messages(flagged=True)

    #     # Un-flagged messages
    #     unflagged_messages = imbox.messages(unflagged=True)

    #     # Messages sent FROM
    #     inbox_messages_from = imbox.messages(sent_from='sender@example.org')

    #     # Messages sent TO
    #     inbox_messages_to = imbox.messages(sent_to='receiver@example.org')

    #     # Messages received before specific date
    #     inbox_messages_received_before = imbox.messages(date__lt=datetime.date(2018, 7, 31))

    #     # Messages received after specific date
    #     inbox_messages_received_after = imbox.messages(date__gt=datetime.date(2018, 7, 30))

    #     # Messages received on a specific date
    #     inbox_messages_received_on_date = imbox.messages(date__on=datetime.date(2018, 7, 30))

    #     # Messages whose subjects contain a string
    #     inbox_messages_subject_christmas = imbox.messages(subject='Christmas')

    #     # Messages whose UID is greater than 1050
    #     inbox_messages_uids_greater_than_1050 = imbox.messages(uid__range='1050:*')

    #     # Messages from a specific folder
    #     # messages_in_folder_social = imbox.messages(folder='Social')

    #     # Some of Gmail's IMAP Extensions are supported (label and raw):
    #     # all_messages_with_an_attachment_from_martin = imbox.messages(folder='all', raw='from:martin@amon.cx has:attachment')
    #     # all_messages_labeled_finance = imbox.messages(folder='all', label='finance')

    #     for uid, message in all_inbox_messages:
    #     # Every message is an object with the following keys
    #         print(message.sent_from)
    #         print(message.body.get('plain'))
            
            
    #         # message.sent_to
    #         # message.subject
    #         # message.headers
    #         # message.message_id
    #         # message.date
            
    #         # message.body.plain
    #         import pdb;pdb.set_trace()