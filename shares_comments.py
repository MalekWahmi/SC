from tk_profile_post import post_shares_comments
from tk_posts import tk_post

def convert(value):
    if value:
        # determine multiplier
        multiplier = 1
        if value.endswith('K'):
            multiplier = 1000
            value = value[0:len(value)-1] # strip multiplier character
        elif value.endswith('M'):
            multiplier = 1000000
            value = value[0:len(value)-1] # strip multiplier character

        # convert value to float, multiply, then convert the result to int
        return int(float(value) * multiplier)

    else:
        return 0

def shares_comments(username):

    x = post_shares_comments(username)
    total_number_shares = 0
    total_number_comments = 0
    ls = []
    lc = []
    for url in x :
        out = tk_post(url)
        n_shares = out['total_shares']
        ls.append(n_shares)
        n_comments = out['total_comments']
        lc.append(n_comments)
        
    for i in ls :
        total_number_shares += convert(n_shares)

    for j in lc :
        total_number_comments += convert(n_comments)
        
    return total_number_shares,total_number_comments

#print(total_number_shares,total_number_comments)

'''y = 1
print(type(y))'''