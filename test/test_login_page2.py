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
wait = WebDriverWait(driver, 15)


# 🧠 Type like a human (slow typing)
def human_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.12))


# 🖱️ Scroll into view + smooth click
def scroll_and_click(element):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(random.uniform(0.5, 1.0))
    driver.execute_script("arguments[0].click();", element)
    time.sleep(random.uniform(0.5, 1.0))

def confirmation_done():
    confirmation = wait.until(EC.element_to_be_clickable((By.ID, "confirmation_ok")))
    scroll_and_click(confirmation)
# ================================
# 🔹 STEP 1: LOGIN
# ================================
driver.get(f"{BASE_URL}/login")

email_input = wait.until(EC.visibility_of_element_located((By.NAME, "email")))
password_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))

human_type(email_input, EMAIL)
human_type(password_input, PASSWORD)

login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
scroll_and_click(login_btn)

print("✅ Logged in successfully!")
time.sleep(2)


# ================================
# 🔹 STEP 2: OPEN CREATE TOURNAMENT MODAL
# ================================
create_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='verify_modal']")))
scroll_and_click(create_btn)

# ================================
# 🔹 STEP 3: FILL PAGE 1
# ================================
tournament_name_input = wait.until(EC.visibility_of_element_located((By.ID, "tournament_name")))
desc_input = driver.find_element(By.ID, "tournament_descriptions")

human_type(tournament_name_input, TOURNAMENT_NAME)
human_type(desc_input, "This tournament is created for selenium testing")

trophy_radio = driver.find_element(By.CSS_SELECTOR, "input[type='radio'][value='Trophy3.png']")
scroll_and_click(trophy_radio)


next_btn = driver.find_element(By.ID, "next1")
scroll_and_click(next_btn)

try:
    alert = wait.until(EC.alert_is_present())
    alert.accept()
    print("✅ JS alert handled successfully")
except:
    print("⚠️ No alert appeared — continuing...")

select_type = Select(driver.find_element(By.ID, "select_type"))
select_type.select_by_value("online")

player_type = Select(driver.find_element(By.ID, "player_type"))
player_type.select_by_value("single")


next_btn = driver.find_element(By.ID, "next1")
scroll_and_click(next_btn)


format_radio = wait.until(EC.element_to_be_clickable((By.ID, "League")))
scroll_and_click(format_radio)

team_select = Select(driver.find_element(By.ID, "team_num"))
team_select.select_by_value("6")

submit_btn = driver.find_element(By.ID, "next2")
scroll_and_click(submit_btn)


# ✅ Final Confirmation
confirmation_ok = wait.until(EC.element_to_be_clickable((By.ID, "confirmation_ok")))
scroll_and_click(confirmation_ok)
print("✅ Confirmation OK clicked!")

# Wait for tournament cards to load
cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".tournament-card")))

# Assume the latest tournament appears at the top (index 0)
latest_card = cards[0]

# Smooth scroll into view
driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", latest_card)
time.sleep(random.uniform(1.0, 1.5))

# Highlight card for visual debugging (optional)
driver.execute_script("arguments[0].style.border='2px solid #00FF99';", latest_card)

# Find and click "View" button inside the latest card
view_button = latest_card.find_element(By.LINK_TEXT, "View")
scroll_and_click(view_button)

print("🎯 Scrolled to latest tournament card and clicked 'View' successfully!")
time.sleep(2)




# === Step 2: Click "Add Teams" button ===
add_teams_btn = wait.until(EC.element_to_be_clickable((By.ID, "add_teams")))
driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", add_teams_btn)
time.sleep(1)
add_teams_btn.click()
print("✅ 'Add Teams' modal opened!")

# === Step 3: Wait for input fields to appear ===
team_inputs = wait.until(EC.presence_of_all_elements_located(
    (By.CSS_SELECTOR, "#team_fields_container input[type='text']")
))
print(f"🧩 Found {len(team_inputs)} team name fields")

# === Step 4: Fill 6 team names (with a duplicate) ===
team_names = ["Tigers", "Lions", "Eagles", "Lions", "Sharks", "Wolves"]

for input_box, name in zip(team_inputs, team_names):
    input_box.clear()
    input_box.send_keys(name)
    time.sleep(random.uniform(0.2, 0.4))

# === Step 5: Submit Form ===
submit_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "team_submit")
))
submit_btn.click()
print("🚀 Clicked 'Save Teams' with duplicate names... waiting for alert")

# === Step 6: Handle Alert (Duplicate Names Detected) ===
try:
    alert = wait.until(EC.alert_is_present())
    print(f"⚠️ Alert Text: {alert.text}")
    alert.accept()
    print("✅ Alert accepted")
except Exception as e:
    print("❌ No alert appeared (check JS logic).")

# === Step 7: Fix the duplicate name ===
team_inputs = wait.until(EC.presence_of_all_elements_located(
    (By.CSS_SELECTOR, "#team_fields_container input[type='text']")
))

# Change 4th input (duplicate) to a new name
team_inputs[3].clear()
team_inputs[3].send_keys("Panthers")
print("🧠 Changed duplicate team name to 'Panthers'")

time.sleep(1)
submit_btn = wait.until(EC.element_to_be_clickable(
    (By.ID, "team_submit")
))
submit_btn.click()
print("✅ Submitted again successfully!")

time.sleep(3)

# === Step 8: Scroll through entire page ===
driver.execute_script("""
    window.scrollTo({top: 0, behavior: 'smooth'});
    const scrollHeight = document.body.scrollHeight;
    let position = 0;
    const step = 300;
    const delay = 200;
    function smoothScroll() {
        if (position < scrollHeight) {
            window.scrollBy(0, step);
            position += step;
            setTimeout(smoothScroll, delay);
        }
    }
    smoothScroll();
""")
print("🌀 Smoothly scrolling through the page...")

time.sleep(5)

# === Smooth Scroll Up ===
leaderboard_btn = wait.until(EC.element_to_be_clickable((By.ID, "tournament-leaderboard")))
driver.execute_script("""
    arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});
    arguments[0].style.transition = 'box-shadow 0.3s ease';
    arguments[0].style.boxShadow = '0 0 20px 3px #13C4C6';
""", leaderboard_btn)
scroll_and_click(leaderboard_btn)
time.sleep(5)
driver.execute_script("""
    window.scrollTo({top: 0, behavior: 'smooth'});
    const scrollHeight = document.body.scrollHeight;
    let position = 0;
    const step = 300;
    const delay = 200;
    function smoothScroll() {
        if (position < scrollHeight) {
            window.scrollBy(0, step);
            position += step;
            setTimeout(smoothScroll, delay);
        }
    }
    smoothScroll();
""")

print("🏆 Clicked 'Leaderboard' button!")

time.sleep(3)
fixture_btn = wait.until(EC.element_to_be_clickable((By.ID, "fixture")))
driver.execute_script("""
    arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});
    arguments[0].style.transition = 'box-shadow 0.3s ease';
    arguments[0].style.boxShadow = '0 0 20px 3px #13C4C6';
""", fixture_btn)
scroll_and_click(fixture_btn)
time.sleep(3)

search_input = wait.until(EC.visibility_of_element_located((By.NAME, "q")))
search_input.clear()
for ch in "Eagles":
    search_input.send_keys(ch)
    time.sleep(0.1)  # human-like typing

# 2️⃣ Click the search button
search_btn = wait.until(EC.element_to_be_clickable((By.ID, "team_search")))
driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", search_btn)
time.sleep(0.5)
driver.execute_script("arguments[0].click();", search_btn)
print("🔍 Searched for 'Eagles'")
time.sleep(2)

# 3️⃣ Scroll down the entire page
driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
time.sleep(2)

# Then scroll back to the top
driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
time.sleep(2)
print("📜 Scrolled down and back up")

# 4️⃣ Clear the search box
search_input = wait.until(EC.visibility_of_element_located((By.NAME, "q")))
search_input.clear()
time.sleep(1)


delete_btn = wait.until(EC.element_to_be_clickable((By.ID, "delete_tournament")))
scroll_and_click(delete_btn)


delete_confirm = wait.until(EC.element_to_be_clickable((By.ID, "delete_confirmation")))
scroll_and_click(delete_confirm)

time.sleep(1)

confirmation_ok = wait.until(EC.element_to_be_clickable((By.ID, "confirmation_ok")))
scroll_and_click(confirmation_ok)


# 1️⃣ Click the "Add Tournament" button
add_btn = wait.until(EC.element_to_be_clickable((By.ID, "add_tournament_btn")))
scroll_and_click(add_btn)

tournament_input = wait.until(EC.presence_of_element_located((By.ID, "tournament_code")))
tournament_input.clear()
human_type(tournament_input, "THN14M")

add_submit = wait.until(EC.element_to_be_clickable((By.ID, "add_new_tournament")))
scroll_and_click(add_submit)

confirmation_done()
# Assume the latest tournament appears at the top (index 0)
latest_card = cards[0]

# Smooth scroll into view
driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", latest_card)
time.sleep(random.uniform(1.0, 1.5))


# Find and click "View" button inside the latest card
view_button = latest_card.find_element(By.LINK_TEXT, "View")
scroll_and_click(view_button)

print("🎯 Scrolled to latest tournament card and clicked 'View' successfully!")
time.sleep(2)


print("✅ Done! Page scrolled and leaderboard opened successfully.")
driver.quit()
