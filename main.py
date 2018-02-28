# coding=utf-8
import requests, json, time, random, datetime, threading, pickle, os
from termcolor import colored

sitekey = "6LfYhz0UAAAAAJFKp28Sg0NnAEIPMfKI1RJSGsdB"


def log(event):
	d = datetime.datetime.now().strftime("%H:%M:%S")
	print("Raffle SJS by Azerpas :: " + str(d) + " :: " + event)

"""

def notify(title, subtitle, message, sound):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    so = '-sound {!r}'.format(sound) 
    os.system('terminal-notifier {}'.format(' '.join([m, t, s, so])))

"""
		
class Raffle(object):
	def __init__(self):
		self.s = requests.session()
		self.shoes = [
		#{"shoe_id":"5","shoe_name":"AIR FORCE 1","raffle_id":"8"},
		#{"shoe_id":"6","shoe_name":"AIR JORDAN 1","raffle_id":"19"},
		#{"shoe_id":"7","shoe_name":"PRESTO","raffle_id":"10"},
		#{"shoe_id":"8","shoe_name":"AM90","raffle_id":"11"},
		#{"shoe_id":"9","shoe_name":"AM97","raffle_id":"12"},
		#{"shoe_id":"10","shoe_name":"VAPORMAX","raffle_id":"13"},
		#{"shoe_id":"13","shoe_name":"VAPORFLY","raffle_id":"16"},
		{"shoe_id":"45","shoe_name":"AIR JORDAN 1 WHITE","raffle_id":"49"},
		]
		self.url = "https://slamjamsocialism-drops.com/graphql"

	def register(self,identity,proxy):
			# register to each shoes.
			for dshoes in self.shoes:
				print('------------------------')
				print("Signin: "+identity['mail'])
				print("for: " + dshoes['shoe_name'])
				print('------------------------')

				d = datetime.datetime.now().strftime('%H:%M')
				log("Getting Captcha")
				flag = False
				while flag != True:
					d = datetime.datetime.now().strftime('%H:%M')
					try:
						file = open(str(d)+'.txt','r') #r as reading only
						flag = True
					except IOError:
						time.sleep(2)
						log("No captcha generated for this minute")
						flag = False
				flag2 = False
				while flag2 != True:
					try:
						d = datetime.datetime.now().strftime('%H:%M')
						file = open(str(d)+'.txt','r')
						FileList = pickle.load(file) #FileList the list where i want to pick out the captcharep
						flag2 = True
					except Exception as e:
						#log("Can't open file")
						#print(e)
						time.sleep(0.2)
				while len(FileList) == 0: #if len(FileList) it will wait for captcha scraper 
						d = datetime.datetime.now().strftime('%H:%M')
						try:
							file = open(str(d)+'.txt','r')
							print('debug 2')
							FileList = pickle.load(file)
							if FileList == []:
								log("No captcha available(2)")
								time.sleep(3)
						except IOError as e:
							log("No file, waiting...")
							print(e)
							time.sleep(3)
				captchaREP = random.choice(FileList) 
				FileList.remove(captchaREP)
				file  = open(str(d)+'.txt','w')
				pickle.dump(FileList,file)
				log("Captcha retrieved")

				headers = {
					":authority":"slamjamsocialism-drops.com",
					":method":"POST",
					":path":"/graphql",
					":scheme":"https",
					"accept":"*/*",
					"accept-encoding":"gzip, deflate, br",
					"accept-language":"fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
					"authorization":"null",
					"content-length":"840",
					"content-type":"application/json",
					"origin":"https://slamjamsocialism-drops.com",
					"referer":"https://slamjamsocialism-drops.com/drops/"+dshoes['shoe_id'],
					"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
					"x-requested-with":"XMLHttpRequest",}

				"""
				if identity['shoesize'] == "18":
					identity['shoesize'] = random.choice(['3 ½','4','4 ½','5','5 ½','6','6 ½','7','7 ½','8','9','9 ½','10 ½','11','11 ½','12','12 ½'])
					log("Changed size to: " + identity['shoesize'])
				#################
				"""
				dateSJS = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+01:00")

				# 2018-02-27T16:12:28+01:00

				payload = {"query":"mutation RequestOrdertMutation($data: OrderRequestInput!) {\n  requestOrder(data: $data)\n}\n",
				"operationName":"RequestOrdertMutation",
				"variables":{
					"data":{
						"firstName":identity['Vesna'],
						"lastName":identity['Carapic'],
						"email":identity['aaronjsgremseck@gmail.com'],
						"phone":identity['+4915778950810'],
						"country":"276",
						"city":"Remseck",
						"order":[{"product":dshoes['45'],"size":identity['9']}],
						"raffle":dshoes['49'],
						"captcha":captchaREP,
						"date":dateSJS
					}
				}
				}


				req = self.s.post(self.url,headers=headers,data=payload,proxies=proxy)
				print(req)
				jsonn = json.loads(req.text)
				if req.status_code == 200:
					if jsonn['errors']:
						try:
							print(jsonn['errors'])
						except:
							print("ERROR 2302")
						raise ValueError('ERROR 200 BUT CANT ENTER')
					else:
						print(colored('Successfully entered','red', attrs=['bold']))
				if req.status_code == 400:
					raise ValueError('ERROR 400')
				sleep = random.uniform(2.3,2.9)
				log("Sleeping: " + str(sleep) + " seconds")
				time.sleep(sleep)
				self.s.cookies.clear()

if __name__ == "__main__":
	ra = Raffle()
	accounts = [
		# sizes = ['3 ½','4','4 ½','5','5 ½','6','6 ½','7','7 ½','8','9','9 ½','10 ½','11','11 ½','12','12 ½']
    # Check the sizes on the site first
{"fname":"Mike","lname":"VanCappel","mail":"mikevancap@gmail.com","phone":"+33612345678","shoesize":"11",},
]
	# catpcha 
	proxies = [
		"username:password@host:port"
	]
	errors = []
	index = 0
	regis = 0
	for i in accounts:
		print("\n\n-------------------------")
		print('NEW TASK')
		print("-------------------------\n")

		p = random.choice(proxies)
		proxies.remove(p)
		if '@' in p:
			proxy = { 'https' : 'https://{}'.format(p) }
			log('Using proxy:')
			print(colored(proxy,'red', attrs=['bold']))
		else:
			proxy = {'http':p,
					'https':p}
			log('Using proxy:')
			print(colored(proxy['https'],'red', attrs=['bold']))
		try:
			ra.register(i,proxy)
			regis += 1
		except Exception as e:
			print(e)
			if e == "local variable 'FileList' referenced before assignment":
				try:
					ra.register(i,proxy)
				except:
					pass
			errors.append(i)
	print(errors)
	print("-------------------------")
	print("-------------------------")
	print("-------------------------")
	print(accounts)
	print("Nb of accounts registered: " + str(regis))
