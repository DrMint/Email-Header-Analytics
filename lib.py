import re


class MailMessage(object):
    
    def __init__(self, sender, date, subject, uid):
        self.sender = sender
        self.date = date
        self.subject = subject
        self.uid = uid



class SearchTechnic(object):
    
    def __init__(self, name, success, warning, failed):
        self.name = name
        self.senders = []
        self.mails = []
        self.criterias = []
        self.resultState = ResultState(success, warning, failed)

    def addCriteria(self, criteria):
        self.criterias += [criteria]

    def addSender(self, sender):
        self.senders += [sender]

    def addMail(self, mail):
        self.mails += [mail]

    def isValid(self, string):
        pos = False;
        neg = True;
        for criteria in self.criterias:
            if criteria.boolean == False:
                neg = neg and criteria.isValid(string)
            else:
                pos = pos or criteria.isValid(string)
        return neg and pos

    def getState(self, string):

        if self.resultState.isSuccess(string):
            return 'Success'
        elif self.resultState.isWarning(string):
            return 'Warning'
        elif self.resultState.isFailed(string):
            return 'Failed'
        else:
            return 'State undefined'

    def getPartSubject(self, string, index):
        array = string.split(' - ')
        return array[index]

        
    
class Criteria(object):

    def __init__(self, string, boolean):
        self.string = string
        self.boolean = boolean

    def isValid(self, string):
        return (self.string in string) == self.boolean



class ResultState(object):

    def __init__(self, success, warning, failed):
        self.success = success
        self.warning = warning
        self.failed = failed

    def isSuccess(self, string):
        return self.success != None and self.success in string
            
    def isWarning(self, string):
        return self.warning != None and self.warning in string
    
    def isFailed(self, string):
        return self.failed != None and self.failed in string



class NameTranslation(object):

    def __init__(self):
        self.names = []

    def add(self, searchName, displayName = None):
        if displayName == None: displayName = searchName            
        self.names += [[searchName, displayName]]

    def find(self, string):
        for name in self.names:
            if name[0] in string:
                return name[1]
        return 'Unknown'



def parse_uid(data):
    pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')
    match = pattern_uid.match(data.decode('utf-8'))
    return match.group('uid')











    
