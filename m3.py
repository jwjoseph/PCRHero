# m3.py
###########################################################################################
# Author: Josh Joseph joshmd@bu.edu
# 4/29/16
# This is the main function library file for PCR hero....


from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib
import json
import bson.json_util
import requests
import time
import datetime

HOSTIP = 'http://www.pcrhero.org:8000/'

class PCRUser:
    '''This is a convenience class which verifies that entries to the users collection are valid'''
    def __init__(self, email, name, hashword):
        self.email = email
        self.name = name
        self.hashword = hashword
  
    def output(self):
        return {"email" : self.email, "name" : self.name, "hashword" : self.hashword}

class PCRIssuer:
    '''This is a convenience class which verifies that entries to the issuers collection are valid'''
    def __init__(self, name, description, url):
        self.name = name
        self.description = description
        self.url = url
  
    def output(self):
        """returns attributes as a python dictionary"""
        return {"name" : self.name, "description" : self.description, "url" : self.url}

    def jsonize(self):
        """Returns a JSON file with the base badge info - needed for posting/hosting, baking, and awarding"""
        data = json.dumps(self.output())
        return data

    def establish_here(self, hostdir="/home/ubuntu/pythonproject/issuers/"):
        """Uploads a JSON version of the issuer to the host server.
        Needed to award the badge."""
        badgeJSON = self.jsonize() 
        outfile = open(hostdir + self.name + ".json", 'w')
        outfile.write(badgeJSON)
        outfile.close()

    def add_issuer(self, db):
        """adds the issuer to the database"""
        db.issuers.insert(self.output())

class OpenBadge:
    def __init__(self, name, description, image, criteria, tags, issuer):
        """This creates the base badge with the badge name, image URL, description, criteria URL, issuer json URL"""
        self.name = name
        ## need sanitizing function here for name - sub for space
        self.description = description
        self.image = HOSTIP + "images/" + image
        self.criteria = establish_criteria(name, criteria)
        self.tags = tags.split()
        self.issuer = HOSTIP + "issuers/" + issuer + ".json"
        ## need sanitizing function here for issuer - sub for space 

    def jsonize(self):
        """Returns a JSON file with the base badge info - needed for posting/hosting, baking, and awarding"""
        data = json.dumps({"name": self.name, "description": self.description, "image": self.image,  "criteria": self.criteria, "tags": self.tags, "issuer": self.issuer})
        return data

    def output(self):
        """Returns a dict with the base badge info - needed for posting/hosting, baking, and awarding"""
        data = {"name": self.name, "description": self.description, "image": self.image,  "criteria": self.criteria, "tags": self.tags, "issuer": self.issuer}
        return data

    def establish_here(self, hostdir="/home/ubuntu/pythonproject/badges/"):
        """Uploads a JSON version of the base badge class to the host server.
        Needed to award the badge. Creates a .json file and adds it to the database"""
        badgeJSON = self.jsonize() 
        outfile = open(hostdir + self.name + ".json", 'w')
        outfile.write(badgeJSON)
        outfile.close()

    def add_badge(self, db):
        """add the badge to the database"""
        db.badges.insert(self.output())


class Task:
    """base class for tasks
        tasks are instantiated by the admin-tasks menu, which also assigns them"""
    def __init__(self, user, badge, app):
        self.user = user
        self.badge = badge
        self.app = app

    def output(self):
        pass

    def assign(self, db):
        """checks for duplicates, returns false if duplicate, if not, logs the task and returns true"""
        ## check for duplicates
        if(check_for_task(db, self.badge, self.user, self.app) != None):
            return False
        ## if not, assign away...
        else:
            db.tasks.insert(self.output())
            return True

class PercentTask(Task):
    def __init__(self, user, badge, app, circuit, score, percent):
        super().__init__(user, badge, app)
        self.type = "percent"
        self.circuit = circuit
        self.score = score
        self.percent = percent
        self.goalScore = score * (percent / 100.0) ## this is the improved target score

    def output(self):
        """returns output as a dict - exactly as we'll need for mongodb...
        returns useremail, badgename, app, type, circuit, initial score, target score"""
        data = {"user": self.user, "badge": self.badge, "app": self.app, "type": self.type, "circuit": self.circuit, "score": self.score, "goalScore": self.goalScore}
        return data

class RepeatTask(Task):
    def __init__(self, user, badge, app, circuit, repeat):
        super().__init__(user, badge, app)
        self.type = "repeat"
        self.circuit = circuit
        self.repeatTarget = repeat
        self.repeatCount = 0 ## the number of times it has been repeated...

    def output(self):
        """returns output as a dict - exactly as we'll need for mongodb..."""
        data = {"user": self.user, "badge": self.badge, "app": self.app, "type": self.type, "circuit": self.circuit, "repeatTarget": self.repeatTarget, "count": self.repeatCount}
        return data

class UniqueTask(Task):
    def __init__(self, user, badge, app, unique):
        super().__init__(user, badge, app)
        self.type = "unique"
        self.uniqueGoal = unique  ## needed number of unique submissions 
        self.uniqueList = []  ## list of submissions

    def output(self):
        """returns output as a dict - exactly as we'll need for mongodb..."""
        data = {"user": self.user, "badge": self.badge, "app": self.app, "type": self.type, "uniqueGoal": self.uniqueGoal, "uniqueList": self.uniqueList}
        return data

class TimeTrialTask(Task):
    def __init__(self, user, badge, app, days, hours, minutes, circuit, tasknum):
        super().__init__(user, badge, app)
        self.type = "timetrial"
        self.circuit = circuit
        self.tasknumGoal = tasknum
        self.tasksDone = 0
        self.days = days
        self.hours = hours
        self.minutes = minutes
        now = datetime.datetime.now()
        setTime = now + datetime.timedelta(days = self.days, hours=self.hours, minutes=self.minutes)
        self.duedate = setTime

    def output(self):
        """returns output as a dict - exactly as we'll need for mongodb..."""
        data = {"user": self.user, "badge": self.badge, "app": self.app, "type": self.type, "circuit": self.circuit, "tasknumGoal": self.tasknumGoal, "tasksDone": self.tasksDone, "duedate" : self.duedate}
        return data

class PerformanceTask(Task):
    def __init__(self, user, badge, app, circuit, targetyield, cost):
        super().__init__(user, badge, app)
        self.type = "performance"
        self.circuit = circuit
        self.targetyield = targetyield
        self.cost = cost ## the cost that one needs to stay below...

    def output(self):
        """returns output as a dict - exactly as we'll need for mongodb..."""
        data = {"user": self.user, "badge": self.badge, "app": self.app, "type": self.type, "circuit": self.circuit, "targetyield": self.targetyield, "cost": self.cost}
        return data



def award_badge_to_user(db, badgename, username, hostdir="/home/ubuntu/pythonproject/awardedbadges/"):
    """awards a badge to a recipient, creating a publicly hosted json of the badge info (a badge assertion)
    located at "http://www.pcrhero.org:8000/awardedbadges/"
    the recipient will be a json with the user's email (hashed), type (email), hashed (boolean), and salt"""
    ### Part one - create the badge assertion
    email = username
    username = sanitize(username)
    badgesource = open("/home/ubuntu/pythonproject/badges/" + badgename + ".json", "r")
    badgedict = json.load(badgesource)
    uid = username + badgename ## this is a unique internal identifier for the mozilla standard
    verifyAddress = "http://www.pcrhero.org/awardedbadges/" + uid + ".json"
    badgeAddress = "http://www.pcrhero.org/badges/" + badgename + ".json"
    issuedOn = str(time.time()).split('.')[0]
    verify = {"type": "hosted", "url": verifyAddress}
    recipient = create_recipient(email)
    data = json.dumps({"uid": uid, "recipient": recipient, "image": badgedict['image'], "issuedOn": issuedOn, "badge": badgeAddress, "verify": verify})
    print(data)
    outfile = open(hostdir + uid + ".json", 'w') ## so the final assertion is at /awardedbadges/sanitized+badgename.json
    outfile.write(data)
    outfile.close()

    ### Part two - add the badge to the user's profile
    entry = {"email": email}
    # get the stored JSON data from the badge file, store it in a dict
    
    db.users.update_one(entry, {"$push":{"badges": badgedict}})

################################################################################################################
# Badge Baking Function - use with caution
# This sends the badge info to the Mozilla Badge Baking API. The issue with this is that you need somewhere to
# actually put it - unless the mozilla badge display API is also added to the site (needs node.js)
# then it only shows the png, rather than any of the metadata.
# one option would be to email it to users, or to simply host it at a specific location and add a download link.
################################################################################################################

def bake(badge, username, filename, hostname="http://www.pcrhero.org/badges/"):
    """Uses the existing Mozilla Badge Baking Web API to create a png with baked-in data
    badgename is a json, host is a url leading to the badge directory, filename is the output png (needs a path!)"""
    email = username
    username = sanitize(username)
    uid = username + badgename
    hostedURL = "http://www.pcrhero.org/awardedbadges/" + uid + ".json"
    print("Badge hosted at " + hostedURL)
    getURL = "http://backpack.openbadges.org/baker?assertion=" + hostedURL
    print("Baking badge at " + getURL)

    r = requests.get(getURL, stream=True)
    if(r.status_code == 200):
        print("Baking badge... %s" % filename)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    else:
        print("Something went wrong...")
        print(r.status_code)
        print(r.text)


def check_for_task(db, badgename, username, appname):
    return db.tasks.find_one({"user": username, "badge": badgename, "app": appname})

def find_task_by_id(db, id):
    entry = {'_id': ObjectId(id)}
    return db.tasks.find_one(entry)

def increment_task_by_id(db, id, field):
    entry = {'_id': ObjectId(id)}
    db.tasks.update_one(entry, {'$inc': {field: 1}})

def update_task_by_id(db, id, field, score):
    entry = {'_id': ObjectId(id)}
    db.tasks.update_one(entry, {'$set': {field: score}})

def remove_task_by_id(db, id):
    entry = {'_id': ObjectId(id)}
    db.tasks.delete_one(entry)

def get_users_tasks(db, username):
    return db.tasks.find({"user": username})

def get_users_tasks_for_app(db, username, appname):
    return db.tasks.find({"user": username, "app": appname})

def check_task_datetime(db, task):
    '''checks the task's due date - returns true if time is up!'''
    now = datetime.datetime.now()
    if(task['duedate'] < now):
        return True
    else:
        return False

## badge bake utility




def sanitize(username):
    username = username.replace('.', '-dot-')
    username = username.replace('@', '-at-')
    return username

def create_recipient(email):
    data = {"identity": shaHash(email, "deadsea"), "type": "email", "hashed": "true", "salt": "deadsea"}
    return data

def get_badges(db):
    return db.badges.find()

def find_badge(db, badgename):
    entry = {"name": badgename}
    return db.badges.find_one(entry)

def establish_criteria(badgename, criteria):
    """establishses a criteria file at /criteria/badgename.html to satisfy OpenBadges Requirements
    returns a link for use in the badge"""
    criteria_file = open("/home/ubuntu/pythonproject/criteria/" + badgename + ".html", 'w')
    criteria_file.write(criteria)
    criteria_file.close()
    return HOSTIP + "criteria/" + badgename + ".html"


def get_db(dbname):
    client = MongoClient('localhost:27017')
    db = getattr(client, dbname)
    return db

def add_person(db, personObj):
    entry = personObj
    db.users.insert(entry.output())
    
def get_person(db, email):
    entry = {"email": email}
    return db.users.find_one(entry)

def get_user_hashword(db, email):
    targetperson = get_person(db, email)
    return targetperson['hashword']

def get_users(db):
    return db.users.find()

def find_person(db):
    '''finds a person - underlying assumption is that user emails will be unique...'''
    email = input("Please enter an email: ")
    print(get_person(db, email))


def shaHash(email, salt):
    target = (email + salt).encode('UTF-8')
    return 'sha256$' + hashlib.sha256(target).hexdigest()

def add_person_request(db):
    newEmail = input("please enter an email: ")
    newName = input("please enter a name: ")
    newHashword = input("please enter a password: ")
    newHashword = shaHash(newHashword, "deadsea")

    personObj = PCRUser(newEmail, newName, newHashword)
    add_person(db, personObj.output())

def menu(db):
    ''' used to test functions without using the main server file. deprecated, but has its uses'''
    command = input("Please choose an option (A)dd, (F)ind, (B)adge Utilities, (Q)uit: ")
    if(command == "A" or command == 'a'):
        add_person_request(db)
        return True
    elif(command == "B" or command == "b"):
        email = input("Enter the user's email: ")
        get_users_badges(db, email)
    elif(command == "F" or command == "f"):
        find_person(db)
        return True
    elif(command == "Q" or command == "q"):
        return False
    else:
        print("Invalid command!")
        return True

def get_users_badges(db, email):
    '''obtains badge info from a user's profile - returns an array of arrays'''
    entry = {"email": email}
    badges = db.users.find_one(entry, {"badges":1}) # this is a 'mask' for the return 
    try:
        return badges['badges']
    except KeyError:
        badges = []
        return badges

def get_users_apps(db, email):
    '''obtains app info from a user's profile - returns an array of arrays'''
    entry = {"email": email}
    apps = db.users.find_one(entry, {"apps":1}) # this is a 'mask' for the return
    try:
        return apps['apps'] ## this is an array of app names
    except KeyError:
        apps = []
        return apps 

def get_app(db, appname):
    '''obtains an app from the list'''
    entry = {"name": appname}
    return db.apps.find_one(entry)

def get_all_apps(db):
    '''returns a list of all app names in the database'''
    apps = db.apps.find()
    applist = []
    for app in apps:
        applist.append(app['name'])
    return applist

def add_issuer(db, issuerObject):
    '''adds an issuer to the library of issuers'''
    entry = issuerObject
    db.issuers.insert(entry.output())

def get_issuers(db):
    issuers = db.issuers.find()
    issuerList = []
    for issuer in issuers:
        issuerList.append(issuer['name'])
    return issuerList

def find_issuer(db, issuername):
    entry = {"name": issuername}
    return db.issuers.find_one(entry)

def main():
    '''deprecated now that the site seems to work, but useful if testing utilities'''
    db = get_db("pcrhero")
    menuFlag = True
    while(menuFlag):
        menuFlag = menu(db)

    badges = (get_users_badges(db, 'joshmd@bu.edu'))
    for badge in badges:
        print(badge)
        print('\n')

    for person in (db.users.find()):
        print(person)

    print(get_issuers(db))

if __name__ == "__main__":
    main()
