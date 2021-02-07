# ip-emailer
Checks for ip address changes and sends user an email when difference is found


## How To
Make a throwaway Gmail account. You'll probably have to disable some extra security service within the account. Put the account information as well as the receiving email address in a .json with the following format
```json
{
    "USER": "robobobandy69@gmail.com",
    "PASS": "creamsoup",
    "RECEIVER": "bodogcheese@gmail.com"
}
```

## Operating
You'll need to add this to cron. 