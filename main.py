import imaplib
import email
from lib import *
from email.parser import HeaderParser
from email.header import Header, decode_header, make_header


ip = 'imap.server.com'
port = 993
user = 'user@server.com'
password = 'password'

retrieveMailFrom = 'INBOX'
transferMailToFolder = 'INBOX.Analysed'


# Connection to the server
server = imaplib.IMAP4_SSL(ip, port)
server.login(user, password)

# We can print the available folders
#print(mail.list())
#print('\n' * 3)

# We select one folder
server.select(retrieveMailFrom)

# List of the client names. If no client is found, Unknown is written
clientNames = NameTranslation()
clientNames.add('Name to find in the header')
clientNames.add('Name to find in the header', 'Name that will be written down in the CSV')

# Let's now configure the types of emails where looking for.
listSearch = []

search = SearchTechnic('Name of the Technic', 'This string describe what is Success', 'Same for warning', 'And Failed')
search.addSender('anAdress@site.com')
search.addSender('another@site.com')
search.addCriteria(Criteria('The mails have to include at least one of those', True))
search.addCriteria(Criteria('Another one', True))
search.addCriteria(Criteria('Negative ones are mandatory, the value MUST not be there', False))
listSearch += [search]

# Performs all the queries to get the appropriate emails's headers
parser = HeaderParser()
for search in listSearch:
    for sender in search.senders:
        # We get all mails from scm-medecin@sma33.fr
        result, data = server.search(None, '(FROM "' + sender + '")')

        # For each mail id
        for num in data[0].split():
            
            # Get the header and body
            result, header = server.fetch(num, '(BODY[HEADER])')
            #result, body = mail.fetch(num, '(RFC822)')

            parsedMessage = parser.parsestr(str(email.message_from_bytes(header[0][1])))

            # Get the UID
            resp, valueUid = server.fetch(num, '(UID)')
            num_uid = parse_uid(valueUid[0])

            # Specific data
            date = parsedMessage['Date']
            subject = str(make_header(decode_header(parsedMessage['Subject']))).replace('\n','')

            # Saving as a mailMessage object
            search.addMail(MailMessage(sender, date, subject, num_uid))




# Now for all the emails's headers, if they correspond the emails we're looking for
# adds them to the csv file and move the emails to another folder.
with open('export.csv','a') as file:
    for search in listSearch:
        for mail in search.mails:
            if search.isValid(mail.subject):

                # Write the infos into the file
                file.write(clientNames.find(mail.subject) + ";")
                file.write(search.getState(mail.subject) + ";")
                file.write(mail.date)
                file.write("\n")

                # Show a message
                print(mail.date + " - " + mail.subject)

                # Copy the email to transferMailToFolder and mark them to deletion
                apply_lbl_msg = server.uid('COPY', mail.uid, transferMailToFolder)
                if apply_lbl_msg[0] == 'OK':
                    mov, data = server.uid('STORE', mail.uid, '+FLAGS', '(\Deleted)')

                
# Apply the deletion of the copied email                        
server.expunge()









