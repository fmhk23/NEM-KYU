# NEM-KYU
---
NEM based simple attendance management system  
Instead of installing it by yourself, during hackathon  you can try NEM-KYU here:  
[http://52.14.91.53:5000/](http://52.14.91.53:5000)  

I recommend you check my app by accessing here since you need many settings to install &run NEM-KYU correctly.


## Requirements
All developments & tests are done in Ubuntu 16.04.

### NIS(>= 0.6.9.5)

### python(>= 3.6.4)
- bokeh(>= 0.12.13)
- flask(>= 0.12.2)
- Flask-Misaka(>= 0.4.1)
- pandas(>= 0.22.0)
- requests(>= 2.18.4)

### node.js(>= 9.4.0)
- nem-sdk

If you try sample using google calendar, below are also required:

### python
- google-api-python-client(>= 1.6.4)
- httplib2(>=0.10.3)
- oauth2client(>=4.1.2)

## How to install

- Install required packages.
- Prepare config files.
- Activate your local NIS.(testnet mode is recommended.)
- "python app.py"
- In other screen, "node trigger.js"
- Access http://127.0.0.1:5000/

## Prepare NEM Address
Create at least 2 addresses.One is company and the other is employee.  
From company address, create name space and issue holiday mosaics.  
Send them to emploee address.  

Set config files properly.  
Now you can simulate taking holiday via NEM-KYU.  

## Config settings

### client_secret.json
API Key to use google calendar  

### config.ini
[employee_info]  
signer:signer of employee  
privatekey:private key of employee  

[company_info]  
address: NEM Address of company  

[mosaic]  
namespace:namespace which issued holiday mosaic.  
mosaic:holiday mosaic, this mosaic is sent to company adress by nem-kyu.  

[app]  
secret: secret key for Flask.  

### trigger.js
Since company address is coded in the script directly, update it.  

### update_calendar.js
Update calendarId in line 71.

## Issue

## License
MIT
