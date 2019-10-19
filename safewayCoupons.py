# Adds all Safeway Just4U coupons using selenium webdriver

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

config = {
    'email':        '<safeway email address',
    'password':      '<safeway password>',
    'homepage':     'https://www.safeway.com/home.html',
    'couponsPage':  'https://www.safeway.com/justforu/coupons-deals.html'
    }
    
locators = {
    'changeLocationPopup_xpath': '//*[@id="tooltip-inside"]/div[2]/button',
    'loginButton_id': 'sign-in-profile-text',
    'loginButton2_link_text': 'SIGN IN',
    'email_id': 'label-email',
    'password_id': 'label-password',
    'signIn_id': 'btnSignIn',
    'makeStore_xpath': '//*[@id="make-store"]/button',
    'justForU_link_text': 'just for U',
    'addCoupon_xpath': '//button[text()="ADD"]',
    'loadMore_xpath': '//button[@class="btn load-more"]',
}    

# Create driver
print('Creating webdriver...')
driver = webdriver.Chrome()
# Maximize window
driver.maximize_window()

# Load home page
print('Navigating to home page...')
driver.get("https://www.safeway.com/home.html")

# Try to click 'Okay' on change location popup
try:
    driver.find_element(By.XPATH, locators['changeLocationPopup_xpath']).click()
except: pass

# Click the login button
print('Logging in...')
driver.find_element(By.ID, locators['loginButton_id']).click()
# Click the sign in button on the popup
time.sleep(3)
driver.find_element(By.LINK_TEXT, locators['loginButton2_link_text']).click()

# Fill in email/pass
try:
    driver.find_element(By.ID, locators['email_id']).send_keys(config['email'])
    driver.find_element(By.ID, locators['password_id']).send_keys(config['password'])
except: # sometimes the login screen didn't open, try that again
    # Click the login button
    driver.find_element(By.ID, locators['loginButton_id']).click()
    # Click the sign in button on the popup
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, locators['loginButton2_link_text']).click()
    # Fill in email/pass
    driver.find_element(By.ID, locators['email_id']).send_keys(config['email'])
    driver.find_element(By.ID, locators['password_id']).send_keys(config['password'])

# Submit email/pass
driver.find_element(By.ID, locators['signIn_id']).click()
time.sleep(5)

# Try to click a store on make store popup
try:
    driver.find_element(By.XPATH, locators['makeStore_xpath']).click()
except: pass

# Click link to Just4U coupon page
print('Navigating to coupon page...')
try:
    driver.find_element(By.PARTIAL_LINK_TEXT, locators['justForU_link_text']).click()
except: 
    time.sleep(5)
    driver.find_element(By.PARTIAL_LINK_TEXT, locators['justForU_link_text']).click()

# Infinite loop to add all the coupons, will break out when there are no more
print('Starting add coupons loop...')
i=0
while 1:

    # Find all coupon add button elements
    try:
        coupons = driver.find_elements(By.XPATH, locators['addCoupon_xpath'])
        # Loop over each coupon and add it
        for coupon in coupons:
            print('We are on coupon number ', i)
            i+=1
            coupon.click()
    except: #sometimes we get a stale refrence, if this happens then refresh page and try again
        driver.refresh()
        continue
        
    # Try to add more coupons to page    
    try:  
        try:
            print('All visible coupons have been added, trying to load more')
            driver.find_element(By.XPATH, locators['loadMore_xpath']).click()
            print('More coupons loaded, adding them now')
        except:
            time.sleep(3)
            print('All visible coupons have been added, trying to load more')
            driver.find_element(By.XPATH, locators['loadMore_xpath']).click()
            print('More coupons loaded, adding them now')
    except: break

print('All coupons have been added! We added ', i, ' new coupons!')
driver.quit()
