import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import quote
import time
import signal
import sys
import os
from colorama import Fore, init, Back, Style
init()	
if not os.path.exists('urled_support.txt'):
	print("***  URLED INITIAL SETUP PROGRAM ***")
	print("")
	lootpath = input("Input exact directory in which to store downloaded files: ")
	variable_values = {
		'downloadpath': f'{lootpath}'
	}
	with open('support_urled.json', 'w') as file:
		json.dump(variable_values, file)
	with open('urled_support.txt', 'w') as file:
		file.write('Placeholder')
else:
	with open('support_urled.json', 'r') as file:
		variable_values = json.load(file)
downloadpath = variable_values['downloadpath']
print("")
user_interrupt_occured = False
def user_interrupt(signal, frame):
	global user_interrupt_occured
	user_interrupt_occured = True
	print("")
	print("")
	print(Fore.RED + "Error: KeyboardInterrupt" + Fore.RESET)
	print("")
	sys.exit()
signal.signal(signal.SIGINT, user_interrupt)
def type_text(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.001)
    print("")
def type_text_slow(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print("")
def loading_screen(message):
    print(message, end="")
    spinner = ["|", "/", "-", "\\"]
    start_time = time.time()
    i = 0
    while True:
        if time.time() - start_time > 3:
            print("\b \b" * (len(message) + 1), end="")
            break
        print(f"\b{spinner[i%4]}", end="", flush=True)
        i += 1
        time.sleep(0.05)
os.system("clear")
logo = '''

   __________ 
  |          |\\ 
  |          | \\
  |          |  \\
  |          |   \\
  |          |    |     URLED
  |          |    |
  |          |    |     URL Enumerator/Downloader
  |          |    |
  |          |    |
  |          |  @ |
  |__________|    |
              \   |
               \  |
                \ |
                 \|    by Codeiology on GitHub

'''
type_text(logo)
type_text_slow("URLED successfully initialized. Type, 'help' to get started")
while True:
	prompt = input("urled> ")
	if prompt.startswith("download"):
		downloadfilepath = prompt[len("download "):]
		print("")
		loading_screen("Downloading file... ")
		os.chdir(f"{downloadpath}")
		os.system(f"curl -O {downloadfilepath}")
		print(Fore.GREEN + "Done!" + Fore.RESET)
	elif prompt == "enumerate":
		print("")
		linkorimg = input("Would you like to enumerate links, images, or filepaths? (link/img/path): ")
		if linkorimg == "img":
			imgurl = input("Target URL: ")
			print("")
			loading_screen("Testing connection... ")
			def is_connected():
				try:
					requests.get(imgurl, timeout=3)
					return True
				except requests.ConnectionError:
					return False
			if is_connected():
				loading_screen("Enumerating images... ")
				print("")
				print("====================================================================")
				print("")
				imgresponse = requests.get(imgurl)
				imgsoup = BeautifulSoup(imgresponse.text, 'html.parser')
				img_tags = imgsoup.find_all('img')
				if len(img_tags) == 0:
					print(Fore.RED + "No images found." + Fore.RESET)
				else:
					for img_tag in img_tags:
						src = img_tag.get('src')
						if src:
							imgabsolute_url = urljoin(imgurl, src)
							type_text(imgabsolute_url)
				print("")
				print("====================================================================")
				print("")
		elif linkorimg == "path":
			print("")
			website_url = input("URL to enumerate: ")
			loading_screen("Preparing... ")
			print("")
			print("======================================================================")
			file_paths = enumerate_files(website_url)
			for file_path in file_paths:
				type_text(file_path)
			print("")
			print("======================================================================")
			print("")
		elif linkorimg == "link":
			url = input("Target URL: ")
			loading_screen("Testing connection... ")
			def is_connected():
				try:
					requests.get(url, timeout=3)
					return True
				except requests.ConnectionError:
					return False
			if is_connected():
				loading_screen("Enumerating links... ")
				print("")
				print("====================================================================")
				print("")
				headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.1234.5678 Safari/537.36'
				}
				response = requests.get(url, headers=headers)
				soup = BeautifulSoup(response.text, 'html.parser')
				links = soup.find_all('a')
				if len(links) == 0:
					print(Fore.RED + "No links found." + Fore.RESET)
				else:
					for link in links:
						href = link.get('href')
						if href:
							absolute_url = urljoin(url, href)
							type_text(absolute_url)
				print("")
				print("====================================================================")
				print("")
			else:
				print("")
				type_text_slow(Fore.RED + "Computer or website is offline. Cannot continue. " + Fore.RESET)
				print("")
	elif prompt == "help":
		instruct = f'''

URLED

enumerate = enumerate links from a target webpage URL.
download <link> = download a file from an enumerated URL. (saved to {downloadpath} )
help = show this menu
exec <command> = execute command in regular terminal
read <filename> = run a cat() command on a downloaded file
dump <url> = dump website source code (server response)
meta = start dumping wizard for web metadata
dork = start google dorking wizard
exit = exit

'''
		type_text(instruct)
	elif prompt == "exit":
		print("")
		print("")
		sys.exit()
	elif prompt.startswith("exec"):
		execommand = prompt[len("exec "):]
		print("")
		os.system(f"{execommand}")
		print("")
	elif prompt.startswith("read"):
		readfile = prompt[len("read "):]
		print("")
		os.system(f"cat {downloadpath}/{readfile}")
		print("")
	elif prompt.startswith("dump"):
		dumpurl = prompt[len("dump "):]
		print("")
		loading_screen("Dumping server response... ")
		print("")
		headers = {
    		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.1234.5678 Safari/537.36'
		}
		response = requests.get(dumpurl, headers=headers)
		html_source = response.text
		print(html_source)
		print("")
		print("")
	elif prompt == "meta":
		print("")
		metaurl = input("Target URL: ")
		metafiletyp = input("Filetype to search for: ")
		metaurlen = f"https://www.google.com/search?q=site%3A{metaurl}+filetype%3A{metafiletyp}&client=safari"
		print("")
		type_text_slow(Fore.GREEN + "Ready." + Fore.RESET)
		print("")
		loading_screen("Testing connection... ")
		def is_connected():
			try:
				requests.get(metaurlen, timeout=3)
				return True
			except requests.ConnectionError:
				return False
		if is_connected():
			loading_screen("Enumerating associated links... ")
			print("")
			print("====================================================================")
			print("")
			headers = {
    			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.1234.5678 Safari/537.36'
			}
			response = requests.get(metaurlen, headers=headers)
			soup = BeautifulSoup(response.text, 'html.parser')
			links = soup.find_all('a')
			if len(links) == 0:
				print(Fore.RED + "No links found." + Fore.RESET)
			else:
				for link in links:
					href = link.get('href')
					if href:
						absolute_url = urljoin(metaurlen, href)
						type_text(absolute_url)
			print("")
			print("====================================================================")
			print("")
		else:
			print("")
			type_text_slow(Fore.RED + "Computer or website is offline. Cannot continue. " + Fore.RESET)
			print("")
	elif prompt == "dork":
		print("")
		dorkquery = input("Enter dork query: ")
		encoded_text = urllib.parse.quote(dorkquery)
		dorkurl = f"https://www.google.com/search?q={encoded_text}&client=safari"
		print("")
		type_text_slow(Fore.GREEN + "Ready." + Fore.RESET)
		print("")
		loading_screen("Testing connection... ")
		def is_connected():
			try:
				requests.get(dorkurl, timeout=3)
				return True
			except requests.ConnectionError:
				return False
		if is_connected():
			loading_screen("Searching results... ")
			loading_screen("Enumerating results... ")
			print("")
			print("====================================================================")
			print("")
			headers = {
    			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.1234.5678 Safari/537.36'
			}
			response = requests.get(dorkurl, headers=headers)
			soup = BeautifulSoup(response.text, 'html.parser')
			links = soup.find_all('a')
			if len(links) == 0:
				print(Fore.RED + "No links found." + Fore.RESET)
			else:
				for link in links:
					href = link.get('href')
					if href:
						absolute_url = urljoin(dorkurl, href)
						type_text(absolute_url)
			print("")
			print("====================================================================")
			print("")
			while True:
				nextpage = input("Would you like to view the next page? (y/n): ")
				if nextpage == "y":
					dorkurl = f"https://www.google.com/search?q={encoded_text}&client=safari"
					print("")
					type_text_slow(Fore.GREEN + "Ready." + Fore.RESET)
					print("")
					loading_screen("Testing connection... ")
					def is_connected():
						try:
							requests.get(dorkurl, timeout=3)
							return True
						except requests.ConnectionError:
							return False
					if is_connected():
						loading_screen("Searching results... ")
						loading_screen("Enumerating results... ")
						print("")
						print("====================================================================")
						print("")
						headers = {
							'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.1234.5678 Safari/537.36'
						}
						response = requests.get(dorkurl, headers=headers)
						soup = BeautifulSoup(response.text, 'html.parser')
						links = soup.find_all('a')
						if len(links) == 0:
							print(Fore.RED + "No links found." + Fore.RESET)
						else:
							for link in links:
								href = link.get('href')
								if href:
									absolute_url = urljoin(dorkurl, href)
									type_text(absolute_url)
						print("")
						print("====================================================================")
						print("")
					else:
						print("")
						type_text_slow(Fore.RED + "Computer or website is offline. Cannot continue. " + Fore.RESET)
						print("")
	else:
		print("")
		print(Fore.RED + "Invalid command. type, 'help' to see available commands" + Fore.RESET)
		print("")
if user_interrupt_occured:
	sys.exit(0)
