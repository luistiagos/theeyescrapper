import requests

def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v3/sandboxf63db4bd694b419fbdeaeeb68ef662c9.mailgun.org",
		auth=("api", "0ae16421d19c461680a2356bcbac0f1f-a5d1a068-7853f6a3"),
		data={"from": "luistiago.andrighetto@gmail.com",
			"to": ["luistiago.andrighetto@gmail.com"],
			"subject": "Hello",
			"text": "Testing some Mailgun awesomness!"})

print(send_simple_message())