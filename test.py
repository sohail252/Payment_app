import requests

BASE  = "http://127.0.0.1:5000/"
#Valid Data
response1 = requests.get(BASE + "ProcessPayments" , {"CreditCardNumber": "4596871236547895", "CardHolder": "Sohail Khan", "SecurityCode": "786",
                   "ExpirationDate": "2021/02/15", "Amount": 5})
#Empty Data
response2 = requests.get(BASE + "ProcessPayments" , {})
#Invalid Data
response3 = requests.get(BASE + "ProcessPayments" , {"CreditCardNumber": "4587dd1247895dd", "CardHolder": "Sohail Khan", "SecurityCode": "786",
                   "ExpirationDate": "2021/02/15", "Amount": 5})
print(response1.json())
print(response2.json())
print(response3.json())
