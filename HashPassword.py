import bcrypt

def HashPassword(password,salt):
    hashed = bcrypt.hashpw(password, salt)
    return hashed

def GetSalt():
    salt = bcrypt.gensalt()
    return salt