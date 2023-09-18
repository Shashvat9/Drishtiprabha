api_key = "dp123"
url="https://drishtiprabha.000webhostapp.com/android_api.php"

# to validate \(^_^)/
 1. set validate = 1 in post
 2. pass this json to api
    {
        "api_key":"",
        "email":"",
        "password":""
    }
 3. in response php will echo email which will be stored in share dprefrance 
    if there is no account with that email will echo 0

    CODES; 
            code = 1 > success > print a email
            code = 2 > wrong password
            code = 3 > no rows or no user with that email
            code = 4 > db problame

# to add user \(^_^)/
    1.  set add_user = 1 using post
    2.  pass this json to api
        {
            "api_key":"",
            "name":"",
            "email":"",
            "mobile":""
            "password":""
        }
    3.  in response php will echo 1 if done 0 if there is a error;

    CODES: 
            code = 5 > user allrady exists
            code = 6 > success 
            code = 6 > db problame
            code = 7 > db error

# to delete user

# to get location \(^_^)/ 

    1. set get_loc = 1 using post
    2. pass this json to api 
        {
            "api_key":"",
            "type":""           LAST = last loc
                                    CODES: 
                                        code = 8 > success
                                        code = 9 > error in sql
                                UNREAD = all unread
                                    CODES: 
                                        code = 10 > success
                                        code = 11 > error in sql

                                ALL = all
                                    CODES: 
                                        code = 12 > success
                                        code = 13 > error in sql
        }
    3. in response php will echo a jsonstring with lontitude,letitude,timestamp,flag,id

# to set flag in location table
    1. set set_flag = 1 using post
    2. pass this json to api
        {
            "api_key":""
            "id":""
        }

        CODES:
            code = 14 > success
            code = 15 > there has been error for set flag
            code = 16 > no such id exists 


# to map the device