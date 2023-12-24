from selenium_module import *
import random
import traceback
from pyvirtualdisplay import Display

def time_to_seconds(time_str):
    # Split the string into minutes and seconds
    minutes, seconds = map(int, time_str.split(':'))
    
    # Convert minutes to seconds and add to the total seconds
    total_seconds = minutes * 60 + seconds
    
    return total_seconds

class SpotifyBot:
    
    def __init__(self, account_file, proxy_file, song_file):
        self.account_file = account_file
        self.proxy_file = proxy_file
        self.song_file = song_file
        self.get_all_accounts()
        self.get_all_proxies()
        self.get_all_songs()
        self.display = Display(visible=0, size=(1920, 1080)).start()
        
    def __del__(self):
        self.display.stop()
    
    
    def login(self, driver: webdriver.Chrome, email: str = None, password: str = None):
        login_url = r'https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com'
        driver.get(login_url)
        sleep(500)
        if email and password:
            print('logging in')
            try:
                wait = WebDriverWait(driver, 15)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="login-username"]'))).send_keys(email)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="login-password"]'))).send_keys(password)
                sleep(random.uniform(1,3))
                submit = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[id="login-button"]')))
                driver.execute_script("arguments[0].click();", submit)
                sleep(random.uniform(3,5))
                return True
            except:
                print('unable to login')
                return False
            
    def get_all_accounts(self):
        print('getting accounts')
        self.accounts = []
        with open(self.account_file, 'r') as file:
            data = file.readlines()
        for line in data:
            if line.strip():
                mail, password = line.strip().split(':', 1)
                self.accounts.append({'mail': mail, 'pass':password})
                    
    def get_random_account(self):
        if self.accounts:
            account = random.choice(self.accounts)
            return account
        else:
            return None
    
    def get_all_proxies(self):
        self.proxies = []
        with open(self.proxy_file) as file:
            data = file.readlines()
        for line in data:
            if line.strip():
                host, port, user, passw = line.strip().split(':', 3)
                self.proxies.append({'host': host, 'port': port, 'user': user, 'pass' : passw})
    
    def get_random_proxy(self):
        if self.proxies:
            proxy = random.choice(self.proxies)
            return proxy
        else:
            return None
        
    def get_all_songs(self):
        self.song_urls = []
        with open(self.song_file, 'r') as file:
            data = file.readlines()
        for line in data:
            if line.strip():
                self.song_urls.append(line.strip())
                
    def get_random_song(self):
        if self.song_urls:
            url = random.choice(self.song_urls)
            return url
        else:
            return None
            
    def listen_to_song(self, driver: webdriver.Chrome, url: str):
        driver.save_screenshot('aa.png')
        if driver and url:
            driver.get(url)
            print(f'listening to song {url}')
            wait = WebDriverWait(driver, 15)
            actionbar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="action-bar"]')))
            try:
                cookie_banner = driver.find_element(By.CSS_SELECTOR, 'div[id="onetrust-banner-sdk"]')
                close_button = cookie_banner.find_element(By.CSS_SELECTOR, 'button[aria-label="Close"]')
                driver.execute_script("arguments[0].click();", close_button)
            except:
                pass
            for i in range(10):
                try:
                    play = actionbar.find_element(By.CSS_SELECTOR, 'button[aria-label="Play"]')
                    driver.execute_script("arguments[0].click();", play)
                    sleep(random.uniform(0.5,1.5))
                except:
                    break


            sleep(3)
            try:
                back_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="control-button-skip-back"]')))
                driver.execute_script("arguments[0].click();", back_button)
                driver.execute_script("arguments[0].click();", back_button)
            except:
                print('unable to go back')
            sleep(15)
            driver.save_screenshot('bb.png')
            try:
                duration_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="playback-duration"]')))
                duration = time_to_seconds(duration_div.text.strip()) - 15
            except:
                duration = 180
            
            print(duration)
            sleep(duration)
    
    def account_listening(self):
        proxy = self.get_random_proxy()
        account = self.get_random_account()
        song = self.get_random_song()
        try:
            driver = getDriver(proxy=proxy)
            if not self.login(driver=driver, email = account['mail'], password= account['pass']):
                driver.quit()
                return
            self.listen_to_song(driver, song)
            driver.quit()
        except:
            traceback.print_exc()
            pass
        
            
    def start_loop(self):
        while True:
            self.account_listening()

print('starting')
spotify = SpotifyBot(account_file=dir_path + sep +'accounts.txt', proxy_file= dir_path +sep +'proxies.txt', song_file=dir_path + sep + 'songs.txt')
spotify.start_loop()
