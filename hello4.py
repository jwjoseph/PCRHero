from bottle import route, run, template, get, post, request, response, redirect, static_file
import m3
import os

pcrDB = m3.get_db("pcrhero")



@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='/home/ubuntu/pythonproject/static/')
    ##This is a filepath to static addresses on the site. You will need to use an appropriate
    ##address (or a system link for security purposes) when using on a different host

@get('/badges/<filename:path>')
def badge(filename):
    return static_file(filename, root='/home/ubuntu/pythonproject/badges/')
    ##This is a filepath to static addresses on the site. You will need to use an appropriate
    ##address (or a system link for security purposes) when using on a different host

@get('/issuers/<filename:path>')
def issuer(filename):
    return static_file(filename, root='/home/ubuntu/pythonproject/issuers/')
    ##This is a filepath to static addresses on the site. You will need to use an appropriate
    ##address (or a system link for security purposes) when using on a different host

@get('/users/<filename:path>')
def issuer(filename):
    return static_file(filename, root='/home/ubuntu/pythonproject/users/')
    ##This is a filepath to static addresses on the site. You will need to use an appropriate
    ##address (or a system link for security purposes) when using on a different host

@get('/images/<filename:path>')
def image(filename):
    return static_file(filename, root='/home/ubuntu/pythonproject/images/')
    ##This is a filepath to static addresses on the site. You will need to use an appropriate
    ##address (or a system link for security purposes) when using on a different host

@get('/criteria/<filename:path>')
def criteria(filename):
    return static_file(filename, root='/home/ubuntu/pythonproject/criteria/')
    ##This is a filepath to static addresses on the site. You will need to use an appropriate
    ##address (or a system link for security purposes) when using on a different host

@get('/awardedbadges/<filename:path>')
def awardedbadge(filename):
    return static_file(filename, root='/home/ubuntu/pythonproject/awardedbadges/')
    ##This is a filepath to static addresses on the site. You will need to use an appropriate
    ##address (or a system link for security purposes) when using on a different host


@route('/')
def home():
    return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + '''\
<h1>PCR Hero - your journey to achievement begins here!</h1>
</body>
'''


@get('/register')
def show_registration():
    return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + '''\
<h1>Thanks for registering with PCR Hero - your journey to achievement begins here!</h1>
<form action="" method="POST">
    <p>
    <label for="name">What is your name?</label>
    <input type="text" name="name"/> </p>
    <p>
    <label for="email">What is your email?</label>
    <input type="email" name="email"/> </p>
    <p>
    <label for="password">Enter a strong password:</label>
    <input type="password" name="password"/> </p>
    <p>
    <label for="password">Reenter that strong password:</label>
    <input type="password" name="passwordcheck"/> </p>
    <input type="submit"/>
</form>
</body>
'''

@post('/register')
def show_name():
    name = request.params.name
    email = request.params.email
    password = request.params.password
    passwordcheck = request.params.passwordcheck
    if(password != passwordcheck):
        return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + '''\
    <h1>Thanks for registering with PCR Hero - your journey to achievement begins here!</h1>
    <form action="" method="POST">
        <p>
        <label for="name">What is your name?</label>
        <input type="text" name="name" required/> </p>
        <p>
        <label for="email">What is your email?</label>
        <input type="email" name="email" required/> </p>
        <p>
        <label for="password">Enter a strong password:</label>
        <input type="password" name="password" required/> </p>
        <p>
        <label for="password">Reenter that strong password:
        <input type="password" name="passwordcheck" required/> 
        <div style = "color: red; display: inline;"> Passwords need to match! </div> </label></p>
        <input type="submit"/>
    </form>
    </body>
    '''
    elif(m3.get_person(pcrDB, email) != None):
        return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + '''\
    <h1>Thanks for registering with PCR Hero - your journey to achievement begins here!</h1>
    <form action="" method="POST">
        <p>
        <label for="name">What is your name?
        <input type="text" name="name"/> 
        </label></p>
        <p>
        <label for="email">What is your email?</label>
        <input type="email" name="email" required/> 
        <div style = "color: red; display: inline;"> That email is taken! </div></p>
        <p>
        <label for="password">Enter a strong password:</label>
        <input type="password" name="password" required/> </p>
        <p>
        <label for="password">Reenter that strong password:</label>
        <input type="password" name="passwordcheck" required/> 
        </p>
        <input type="submit"/>
    </form>
    </body>
    '''    
    else:
        ## It worked!
        ## Hash the password
        hashword = m3.shaHash(password, "deadsea")
        ## create the new user object
        newUser = m3.PCRUser(email, name, hashword)
        m3.add_person(pcrDB, newUser)
        return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + '''\
<h2>Hello, {}!</h2><p>Thanks for registering.</p>
</body>
</html>
'''.format(request.POST.name)

@get('/myprofile')
def home():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        userbadges = m3.get_users_badges(pcrDB, useremail)
        for badge in userbadges:
            print(badge)
        return template('base.tpl', title='PCR Hero', email= useremail) + '''\
            <h1>Welcome to PCR Hero - {}</h1>
        '''.format(useremail) + template('profile.tpl', badges=userbadges) + "</body>"
    else:
        redirect("/login")

@get('/login')
def show_registration():
    return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + '''\
<h1>Welcome to PCR Hero - please login here!</h1>
<form action="" method="POST">
    <p>
    <label for="email">Email:</label>
    <input type="email" name="email" required/> </p>
    <p>
    <label for="password">Password:</label>
    <input type="password" name="password" required/> </p>
    <p>
    <input type="submit"/>
</form>
</body>
'''

@post('/login')
def show_name():
    email = request.params.email
    password = request.params.password
    hashword = m3.shaHash(password, "deadsea")
    ### need to begin with checking for username (email) - otherwise we'll get a keyerror
    if(m3.get_person(pcrDB, email) == None):
        return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + "Sorry - this username is not registered!"
    else:
        ### need to load up the user's hashword for comparison purposes
        loginHashword = m3.get_user_hashword(pcrDB, email)
        print(hashword)
        print(loginHashword)
        if(hashword != loginHashword):
            return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + "Sorry - your password is incorrect!"
        elif(hashword == loginHashword):
            response.set_cookie('loggedin', email, max_age= 600, secret='applesauce', path='/')
            return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + "<h2>Hello, {}!<p>Welcome back!</p></h2>".format(request.POST.email)
        else:
            return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce'))+ "Sorry, something went wrong!"

@get('/admin-badge')
def badge_menu():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        userbadges = m3.get_users_badges(pcrDB, useremail)
        issuers = m3.get_issuers(pcrDB)
        image_path = "/home/ubuntu/pythonproject/images"
        available_images = os.listdir(image_path)
        return template('base.tpl', title='PCR Hero', email= useremail) + '''\
            <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
        '''.format(useremail) + template('admin-badge.tpl', badges=userbadges, issuers=issuers, images=available_images) + "</body>"
    else:
        redirect("/login")

@post('/admin-badge')
def badge_submit():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        userbadges = m3.get_users_badges(pcrDB, useremail)
        issuers = m3.get_issuers(pcrDB)
        image_path = "/home/ubuntu/pythonproject/images"
        available_images = os.listdir(image_path)
        
        ## return args
        name = request.params.name
        if(m3.find_badge(pcrDB, name) != None):
            return template('base.tpl', title='PCR Hero', email= useremail) + '''\
                <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
                <h2 style="color:red">A badge with that name already exists!</h2>
            '''.format(useremail) + template('admin-badge.tpl', badges=userbadges, issuers=issuers, images=available_images) + "</body>"

        else:
            description = request.params.description
            image = request.params.image
            criteria = request.params.criteria
            tags = request.params.tags
            issuer = request.params.issuer

            newBadge = m3.OpenBadge(name, description, image, criteria, tags, issuer)
            newBadge.establish_here()
            newBadge.add_badge(pcrDB)

            return template('base.tpl', title='PCR Hero', email= useremail) + '''\
                <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
                <h2 style="color:blue">Your badge was successfully created!</h2>
            '''.format(useremail) + template('admin-badge.tpl', badges=userbadges, issuers=issuers, images=available_images) + "</body>"

    else:
        redirect("/login")

@get('/admin-issuer')
def issuer_create_menu():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        userbadges = m3.get_users_badges(pcrDB, useremail)
        issuers = m3.get_issuers(pcrDB)
        return template('base.tpl', title='PCR Hero', email= useremail) + '''\
            <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
        '''.format(useremail) + template('admin-issuer.tpl', badges=userbadges, issuers=issuers) + "</body>"
    else:
        redirect("/login")

@post('/admin-issuer')
def issuer_create_submit():
    name = request.params.name
    description = request.params.description
    url = request.params.description
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        userbadges = m3.get_users_badges(pcrDB, useremail)
        issuers = m3.get_issuers(pcrDB)
        if(m3.find_issuer(pcrDB, name) != None):
            return template('base.tpl', title='PCR Hero', email= useremail) + '''\
                <h1>Welcome to PCR Hero's Admin Menu - {}</h1> <p style="color:red;">Sorry, that issuer is taken!</p>
            '''.format(useremail) + template('admin-issuer.tpl', badges=userbadges, issuers=issuers) + "</body>"
        else:
            newIssuer = m3.PCRIssuer(name, description, url)
            m3.add_issuer(pcrDB, newIssuer)
            newIssuer.establish_here()
            issuers = m3.get_issuers(pcrDB)
            return template('base.tpl', title='PCR Hero', email= useremail) + '''\
                <h1>Welcome to PCR Hero's Admin Menu - {}</h1> <p style="color:blue;">Your issuer has been created!</p>
            '''.format(useremail) + template('admin-issuer.tpl', badges=userbadges, issuers=issuers) + "</body>"
    else:
        redirect("/login")


@get('/admin-awards')
def badge_award_menu():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        badge_list = m3.get_badges(pcrDB)
        user_list = m3.get_users(pcrDB)
        return template('base.tpl', title='PCR Hero', email= useremail) + '''\
            <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
        '''.format(useremail) + template('admin-award.tpl', badges=badge_list, users=user_list) + "</body>"
    else:
        redirect("/login")

@post('/admin-awards')
def badge_award_submit():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        badge_list = m3.get_badges(pcrDB) # list of all badges
        user_list = m3.get_users(pcrDB) # list of all users
        current_user = request.params.user
        current_user_badges = m3.get_users_badges(pcrDB, current_user)
        current_badge = request.params.badge
        ## check that the user doesn't already have the badge
        # if so, send back to the menu
        if(current_badge in current_user_badges):
             return template('base.tpl', title='PCR Hero', email= useremail) + '''\
                <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
                <h2 style="color:red;">That user already has that badge!</h2>
            '''.format(useremail) + template('admin-award.tpl', badges=badge_list, users=user_list) + "</body>"           
        # if not, award the badge
        ## awarding badge magic
        else:
            m3.award_badge_to_user(pcrDB, current_badge, current_user)
        return template('base.tpl', title='PCR Hero', email= useremail) + '''\
            <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
            <h2 style="color:blue;">Badge successfully awarded!<h2>
        '''.format(useremail) + template('admin-award.tpl', badges=badge_list, users=user_list) + "</body>"
    else:
        redirect("/login")



@get('/admin-images')
def images_menu():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        userbadges = m3.get_users_badges(pcrDB, useremail)
        image_path = "/home/ubuntu/pythonproject/images"
        available_images = os.listdir(image_path)
        return template('base.tpl', title='PCR Hero', email= useremail) + '''\
            <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
        '''.format(useremail) + template('admin-images.tpl', badges=userbadges, images=available_images, image_path=image_path) + "</body>"
    else:
        redirect("/login")

@post('/admin-images')
def upload_image():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        userbadges = m3.get_users_badges(pcrDB, useremail)

        upload = request.files.image
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.png'):
            return "File extension not allowed."

        save_path = "/home/ubuntu/pythonproject/images"

        file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
        upload.save(file_path)

        return template('base.tpl', title='PCR Hero', email= useremail) + '''\
            <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
            <h2 style="color:blue">Image successfully uploaded!</h2>
        '''.format(useremail) + template('admin-images.tpl', badges=userbadges) + "</body>"
    else:
        redirect("/login")


@get('/logout')
def logout():
    response.set_cookie('loggedin', '', path='/')
    redirect("/")

run(host='172.31.57.1', port=8000, debug=True)
