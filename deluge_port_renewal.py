from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyotp import TOTP
import os
from dotenv import load_dotenv


options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)

WINDSCRIBE_USERNAME = os.getenv(WINDSCRIBE_USERNAME)
WINDSCRIBE_PASSWORD = os.getenv(WINDSCRIBE_PASSWORD)
WINDSCRIBE_TOTP = os.getenv(WINDSCRIBE_TOTP)
DELUGE_PASSWORD = os.getenv(DELUGE_PASSWORD)


def main():
	try:
		windscribe_login(
			'REDACTED'
			,'REDACTED'
			,'REDACTED'
			)
		print("Windscribe login successful.")
	except:
		print("UNABLE TO LOGIN TO WINDSCRIBE!!!!")
		quit()

	try:	
		port = windscribe_port_change()
		print(f"Port changed to {port} in Windscribe successfully.")
	except:
		print("UNABLE TO CHANGE PORT IN WINDSCRIBE!!!!")
		quit()

	try:
		deluge_login("REDACTED")
		print("Deluge login successful.")
	except:
		print("UNABLE TO LOGIN TO DELUGE!!!!")
		quit()

	try:
		deluge_port_change(port)
		print(f"Port changed to {port} in Deluge successfully.")
	except:
		print("UNABLE TO CHANGE PORT IN DELUGE!!!!")
		quit()

	driver.close()




def windscribe_port_change():
	"""Establishes an ephemeral port and returns it"""
	driver.get('https://windscribe.com/myaccount#porteph')
	driver.refresh()

	"""
	If a port is already assigned, it will be deleted and a new one will be assigned.
	If there is no port, it will be assigned.
	"""
	try:
		delete_button = WebDriverWait(
			driver, 3).until(
			EC.element_to_be_clickable(
			(By.CSS_SELECTOR, 'button.green-btn:nth-child(3)')))
		delete_button.click()
		_get_port_button().click()
	except TimeoutException:
		_get_port_button().click()

	"""Gets the port from the browser and returns it."""
	port = WebDriverWait(
		driver, 2).until(
		EC.element_to_be_clickable(
		(By.CSS_SELECTOR, '#epf-port-info > span:nth-child(3)')))
	return port.text`




def windscribe_login(user, password, token):
	"""Logs in to Windscribe."""
	driver.get('https://windscribe.com/login')
	driver.implicitly_wait(3)

	user_login = driver.find_element_by_id('username')
	user_login.send_keys(user)
	pass_login = driver.find_element_by_id('pass')
	pass_login.send_keys(password)
	fa_button = driver.find_element_by_class_name('have_2fa')
	fa_button.click()
	fa_login = driver.find_element_by_id('code')
	fa_login.send_keys(_get_token(token))
	confirm_login = driver.find_element_by_id('login_button')
	confirm_login.click()




def deluge_login(password):
	"""Logs into Deluge."""
	driver.get('https://mrcaters.me/deluge')

	login_prompt = WebDriverWait(driver, 2).until(
		EC.element_to_be_clickable(
		(By.CSS_SELECTOR, '#_password')))
	login_prompt.send_keys(password)

	login_confirm_button = driver.find_element_by_id('ext-gen157')
	login_confirm_button.click()




def deluge_port_change(port):
	"""Changes the port in Deluge and saves it."""
	preferences = WebDriverWait(
		driver, 2).until(
		EC.element_to_be_clickable(
		(By.CSS_SELECTOR, '#ext-gen68')))
	preferences.click()

	network = WebDriverWait(
		driver, 1).until(
		EC.element_to_be_clickable(
		(By.XPATH, '/html/body/div[17]/div[2]/div[1]/div/div/div/div[1]/div/div/div/div[2]/div/dl[2]/dt')))
	network.click()

	incoming_port = WebDriverWait(
		driver, 1).until(
		EC.visibility_of_element_located(
		(By.CSS_SELECTOR, '#ext-comp-1189')))
	incoming_port.clear()
	incoming_port.send_keys(port)

	apply_button = WebDriverWait(
		driver, 1).until(
		EC.element_to_be_clickable(
		(By.CSS_SELECTOR, '#ext-comp-1168')))
	apply_button.click()

	ok_button = driver.find_element_by_css_selector('#ext-comp-1169')
	ok_button.click()




def _get_token(token):
	"""Returns the value of the given 2fa token."""
	totp = TOTP(token)
	token = totp.now()
	return token




def _get_port_button():
	"""Gets the button that will get the port."""
	assign_port_button = WebDriverWait(
		driver, 1).until(
		EC.element_to_be_clickable(
		(By.CSS_SELECTOR, 'button.green-btn:nth-child(4)')))
	return assign_port_button




if __name__ == '__main__':
	main()