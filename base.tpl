<!doctype HTML>
<head>
<title>{{title}}</title>
<link type="text/css" href="/static/main.css" rel="stylesheet">
</head>
<body>
<header>
<div id = "maintext">PCR Hero</div>
<div id = "userinfo">user: {{email}}</div>
<nav>
<ul>
<a href="http://www.pcrhero.org:8000/"><li>Home</li></a>
% if(email == None):
	<a href="http://www.pcrhero.org:8000/login"><li>Login</li></a>
% else:
	<a href="http://www.pcrhero.org:8000/logout"><li>Logout</li></a>
% end
<a href="http://www.pcrhero.org:8000/myprofile"><li>My Profile</li></a>
<a href="http://www.pcrhero.org:8000/register"><li>Register</li></a>
<a href="http://cidarlab.org/"><li>About CIDAR</li></a>
% if(email == 'joshmd@bu.edu'):
	<a href="http://www.pcrhero.org:8000/admin-badge"><li>Admin-Badges</li></a>
	<a href="http://www.pcrhero.org:8000/admin-issuer"><li>Admin-Issuers</li></a>
	<a href="http://www.pcrhero.org:8000/admin-awards"><li>Admin-Awards</li></a>
	<a href="http://www.pcrhero.org:8000/admin-images"><li>Admin-Images</li></a>
	<a href="http://www.pcrhero.org:8000/admin-tasks"><li>Admin-Tasks</li></a>
% end
</ul>
</nav>
</header>
<div id = "spacer"></div>
