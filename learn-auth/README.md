# SECURITY 
Strong Passwords
Strong Encryption
Secure Communication
Password Storage
Man in the Middle Attacks
2 Factor Authentication
Password Recovery
# Make sure passwords are strong on both client and server
# Securely store passwords in the server
# Protection against man in the middle attacks should be considered on both client and server
# OAuth handles all concerns above sufficiently

# Authenticate
You say who you are; typically resolved by passwords
# Authorization
Permission rights depending on user.
# Cookies
Manage sessions with cookies for better ux (no need to constantly authenticate), but
beware of session hijacking where a user steals your cookie. 

# Third Party Auth practices:
Keep Auth scopes to a minimum (only ask for info you really need)

# Anti-forgery State Tokens
Ensures authenticated user is the one that sent requests.
Solve by creating a unique session token from client 
and google authorization code.

# Google API Signin
https://developers.google.com/identity/sign-in/web/sign-in
data-approvalprompt="force" (disable this in-production)

# Determine public and protected pages
Implement Local Permission System so users can only affect their data 
  Need to modify db tables by creating a users table
