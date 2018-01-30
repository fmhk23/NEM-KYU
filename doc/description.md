# DEMO
Read the description and you can try my application. 

## Take a Holiday!
You can have an experience to request a holiday using NEM-KYU.  
You can use Alice(who is working for company_a) address for test.(Address is embeded.)  

Select the date you take a holiday and click the button to send a holiday mosaic to company address.  
From company-side, when transaction monitoring program detects receiving a holiday mosaic, it automatically inserts the holiday event to the google calendar.  
It needs up to 1 minute until the calendar is updated since NEM transaction is confirmed approximately every 1 minute.  

## Dashboard
It visualizes the ratio of (amount of mosaics company address received) / (mosaic total supply)  
You can see the company's holiday digestibility ratio.  

By modifying URL, you can see any combination of address/namespace/mosaic.  
(If the address has never received the designated mosaics, it would be error, though.)  

I prepared two virtual company for demo:  

#### company_a(TCJ2QE-7WZQLY-WAF5EK-EY2H3T-57A2NP-54W7HB-SN5L)

[Link to company_a dashboard](http://52.14.91.53:5000/dashboard?address=TCJ2QE7WZQLYWAF5EKEY2H3T57A2NP54W7HBSN5L&namespace=company_a&mosaic=holiday2018)  
Only Alice is working here.  
Since Alice has many holiday mosaics, holiday digestibility ratio is very low now.  
It is fetching data from NEM testnet. If you request a holiday from "Take a Holiday!" page, this page is also updated.  
Please request holidays much time to improve the ratio!  
(test mosaic is used during development, you can ignore it.)  

#### company_b(TCEUJ2-AV33YE-RSL56Z-MQKK5R-XFMQ7G-VAPVEY-VAJ6)

[Link to company_b dashboard](http://52.14.91.53:5000/dashboard?address=TCEUJ2AV33YERSL56ZMQKK5RXFMQ7GVAPVEYVAJ6&namespace=company_b&mosaic=holiday2016)  
I made it as a more likely company.  
It started their buisiness in 2016 with 5 employees.  
It have issued 3 mosaics:holiday2016, holiday2017, holiday2018.  
Each mosaic's total supply = 100 and one employee gets 20 holiday mosaics every year.  
You can trace the holiday digestibility ratio every year.  

## Restriction
Since it is demo widely open to many people, some points are different from actual possible use case.

- No Authentication: In actual use case, you would login to NEM-KYU using your privatekey as you login to NanoWallet.
- Alice can request a holiday even if the designated date is holiday.  
- Destination address is preset.
- Alice has large amount of holidays.

Fixing/Updating them is not difficult but I leave them in order to let many people try my application easily.  

# Detailed description of NEM-KYU

## Basic Idea/Problems I want to solve
In Japan, many employees can't take all of their paid holidays.  
[This article](https://www.travelvoice.jp/english/japan-is-the-worst-country-in-the-paid-holiday-acquisition-rate-ranking/) explains about this problem.  
NEM-KYU is a simple application for Attendance Management.  
With this application, employees can offer paid holiday by sending mosaics.  
They don't have to make a phone-call/e-mail or talk with their boss.(I don't like all of them!)  
Since it is working on public chain, anyone can visualize if the company is employee-friendly or not.  
It is very helpful for job finders. They can know if they can take holidays easily or not.  
Currently companys let us know the paid holiday axquisition rate, but can you trust it?  
By using public chain, not employee-friendly company can't recruit anyone!  

## System Description
In this hackathon, I have developed 2 screens.

### Offering paid holiday by sending a mosaic.
In this system, company has its own NEM address and namespace.  
It issues mosaics like "holiday2018" and distribute them to its employees.  
When an employee wants to take a holiday, he just needs to send a mosaic to company address using NEM-KYU.  
Instead of using NEM-KYU, he can send it using Nanowallet, too. (Need to set appropriate message, though.)  
By triggering mosaic-recieving, company-side can run any program like sending messages to sender's colleagues, updating calendar and so on.  
Because of this feature, I believe it can be integrated with conventional system with minimum effort.  

In developed test version, as company-side, transaction-monitoring program automatically calls program to update the Google calendar.  

### Paid Holiday Acquistion Dashboard
This dashboard helps you to check how many holidays are requested until now.  
Since it is fetching data from blockchain, updating is almost in realtime.  
By modifying URL, you can check any combination of address and mosaic incomes.  

## Future Plan

### Updating NEM-KYU

With using blockchain, these functions would be easily implemented.  

- Trading holidays with colleagues.
Even in current system, you can trade holidays with your colleagues using Nanowallet.  
If company provides the exchange, you can trade your holidays more easily.  

- Get XEM refunds for expired holidays.
It is a very simple idea and not difficult to implement:  
Just make a xem transaction when company-side receives holiday mosaic with "refund" message.  

- Use multisig transaction when employee offers a holiday.
In Japan, company-side can ask employees to change the date of holiday.  
With using multi-sig transaction, the boss can confirm the request and if there are any problem, he can stop transaction.  

- Update Dashboard
Current dashboard has only simple functions but it is possible to visualize when employees offers holidays.  
Depending on their business, there are busy season and off-season. It can visualize them with actual data.  


### Usecase as emergency-contact-tool
Moreover, NEM-KYU is not just Attendance Management Application, but is useful for Emergency Contact.  
At the time of disaster, company wants to know if their colleagues are safe or not as soon as possible.  
In such cases, workers can tell by sending “Company_NAME:Safe” mosaic to company address.  

Since it is completely same system with Attendance management, workers don’t need another training for using specific system.  
If server is down due to disaster and can't access to NEM-KYU, users can tell by using Nanowallet.  
If their family/friends knows his address, they can know if he is safe by checking the transactions from the address.  
No need to contact directly, which causes traffic jam in network.  


