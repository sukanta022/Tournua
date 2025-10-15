from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import random

BASE_URL = "http://127.0.0.1:8000"
EMAIL = "sukantacb20@gmail.com"
PASSWORD = "12345678"
TOURNAMENT_NAME = "Testing Premier League"

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)


def human_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.15))


def scroll_and_click(element):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(0.7)
    driver.execute_script("arguments[0].click();", element)
    time.sleep(1)

# LOGIN
driver.get(f"{BASE_URL}/login")

email_input = wait.until(EC.visibility_of_element_located((By.NAME, "email")))
password_input = driver.find_element(By.NAME, "password")

human_type(email_input, EMAIL)
human_type(password_input, PASSWORD)
login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
scroll_and_click(login_btn)

print("Logged in successfully!")
time.sleep(2)

# CREATE NEW TOURNAMENT
create_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='verify_modal']")))
scroll_and_click(create_btn)

# PAGE 1
tournament_name_input = wait.until(EC.visibility_of_element_located((By.ID, "tournament_name")))
desc_input = driver.find_element(By.ID, "tournament_descriptions")

human_type(tournament_name_input, TOURNAMENT_NAME)
human_type(desc_input, "This tournament is created for selenium testing")

trophy = driver.find_element(By.CSS_SELECTOR, "input[name='trophy'][value='Trophy1.png']")
scroll_and_click(trophy)

Select(driver.find_element(By.ID, "select_type")).select_by_value("offline")
Select(driver.find_element(By.ID, "player_type")).select_by_value("team")

next1 = driver.find_element(By.ID, "next1")
scroll_and_click(next1)

# PAGE 2
format_radio = driver.find_element(By.CSS_SELECTOR, "input[name='format'][value='League']")
scroll_and_click(format_radio)

Select(driver.find_element(By.ID, "select_group")).select_by_value("2")
Select(driver.find_element(By.ID, "team_num")).select_by_value("8")

next2 = driver.find_element(By.ID, "next2")
scroll_and_click(next2)

# PAGE 3 -Add team names
team_inputs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='text'][name^='team']")))
team_names = ["Tigers", "Lions", "Eagles", "Sharks", "Falcons", "Dragons", "Panthers", "Wolves"]

for field, name in zip(team_inputs, team_names):
    human_type(field, name)
    time.sleep(random.uniform(0.1, 0.3))

submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
scroll_and_click(submit_btn)

print("Tournament created successfully!")
time.sleep(4)

# VIEW TOURNAMENT
cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".tournament-card")))
latest_card = cards[0]
view_button = latest_card.find_element(By.LINK_TEXT, "View")
scroll_and_click(view_button)
time.sleep(4)

# LEADERBOARD
leaderboard_link = wait.until(EC.element_to_be_clickable((By.ID, "tournament-leaderboard")))
scroll_and_click(leaderboard_link)

home_link = wait.until(EC.element_to_be_clickable((By.ID, "leaderboard_home")))
scroll_and_click(home_link)

# FOLLOW PUBLIC TOURNAMENT
follow_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='add_tournament2']")))
scroll_and_click(follow_btn)

code_input = wait.until(EC.presence_of_element_located((By.ID, "tournament_code2")))
code_input.clear()
human_type(code_input, "CO4289")

go_button = wait.until(EC.element_to_be_clickable((By.ID, "go_button")))
scroll_and_click(go_button)

leaderboard_link = wait.until(EC.element_to_be_clickable((By.ID, "tournament-leaderboard")))
scroll_and_click(leaderboard_link)

home_link = wait.until(EC.element_to_be_clickable((By.ID, "leaderboard_home")))
scroll_and_click(home_link)

# ADD TOURNAMENT MANUALLY
add_btn = wait.until(EC.element_to_be_clickable((By.ID, "add_tournament_btn")))
scroll_and_click(add_btn)

tournament_input = wait.until(EC.presence_of_element_located((By.ID, "tournament_code")))
tournament_input.clear()
human_type(tournament_input, "9G1PI1")

add_submit = wait.until(EC.element_to_be_clickable((By.ID, "add_new_tournament")))
scroll_and_click(add_submit)

print("Follow Public Tournament flow completed successfully!")

driver.quit()
