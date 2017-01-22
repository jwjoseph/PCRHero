# EC500 PCR Hero
PCR Hero - Personal Challenge Recognition Software

# <a href="https://www.youtube.com/watch?v=xAlnnOnYW4E">Trailer</a>

PCR Hero is an open-source web application that adds a gaming element to synthetic biology applications, serving as an interface for keeping track of users’ progress and awarding badges as a result. Gamification, or the division of tasks into personal and group challenges, has become a serious business in management and in commercializing software. When tasks are gamified, external goals are set, such as badges or awards, which provide the learner with a tangible sense of progress, and also as an external credential to other team members and colleagues through social media sites. PCR allows administrators (PIs, lab managers) to set external goals (e.g. “permute a set number of designs through such a date,”) as well as challenges to spark creativity and friendly competition within and between research groups.


###Dependencies

The application has the following dependencies (feel free to use a virtual environment):

Python3 (3.4 and above should be good, latest preferable)

bottle for Python

pymongo for Python

MongoDB

The environment I ran this on was an Amazon Web Services (AWS) Ubuntu server (of the free variety).

## Filesystem setup
The filesystem was arranged as follows:
/home/ubuntu/pythonproject/   <-- base directory, contains the server file, libraries file, and .tpls

/home/ubuntu/pythonproject/apps/

/home/ubuntu/pythonproject/awardedbadges/

/home/ubuntu/pythonproject/badges/

/home/ubuntu/pythonproject/images/

/home/ubuntu/pythonproject/issuers/

/home/ubuntu/pythonproject/criteria/

/home/ubuntu/pythonproject/static/

/home/ubuntu/pythonproject/users/

There is absolutely nothing special about this file structure; apart from a few references that I have likely neglected to link to CONSTANT variables at the begining, you may substitute another base directory ad libitum. 

###MongoDB setup
You will need to set up a database (pcrhero) and collections (apps, badges, issuers, tasks, users).

###Python server and library file setup
You will need to replace the value of HOSTIP in both the server and library file (it's at the top).
You will also need to replace the IP address at the very bottom of the file
```
run(host='172.31.57.1', port=8000, debug=True)
```
With your host, any port number that you wish to use, and remember to set ```debug=False``` when you are deploying your server to the public as this will leak important information about the server code and file dependencies!

Finally, you will need to add your email to the admins database before you can award badges.

To run, simply ```python3 pcrserver.py```
