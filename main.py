import datetime as dt
import pandas as pd
import random
import smtplib
import os

# ==================== CONFIGURATION ====================
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

CSV_PATH = r"birthdays.csv"
TEMPLATE_DIR = r"letter_templates"
# =======================================================

# 1. Get today's month and day
today = dt.datetime.now()
today_month = today.month
today_day = today.day

try:
    # 2. Read the birthdays CSV file
    df = pd.read_csv(CSV_PATH)
    
    # 3. Filter for rows where the birthday matches today
    birthday_matches = df[(df["month"] == today_month) & (df["day"] == today_day)]
    
    if not birthday_matches.empty:
        # 4. Establish a single secure connection to the SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:
            connection.starttls()  # Encrypt the connection
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            
            # Loop through everyone celebrating a birthday today
            for index, row in birthday_matches.iterrows():
                recipient_name = row["name"]
                recipient_email = row["email"]
                
                # Pick a random template file (1, 2, or 3)
                random_digit = random.randint(1, 3)
                template_path = f"{TEMPLATE_DIR}\letter_{random_digit}.txt"
                
                try:
                    # Open and read the template
                    with open(template_path, "r", encoding="utf-8") as file:
                        letter_content = file.read()
                        
                    # Replace placeholder with the actual name
                    personalized_letter = letter_content.replace("[NAME]", recipient_name)
                    
                    # Construct email structure
                    subject = f"Happy Birthday, {recipient_name}!"
                    email_message = f"Subject: {subject}\n\n{personalized_letter}"
                    
                    # Send the email
                    connection.sendmail(
                        from_addr=MY_EMAIL,
                        to_addrs=recipient_email,
                        msg=email_message.encode("utf-8")  # encode to support special characters
                    )
                    print(f"Successfully sent birthday email to {recipient_name} ({recipient_email}).")
                    
                except FileNotFoundError:
                    print(f"Error: Template file not found at {template_path}")
    else:
        print("No birthdays matching today's date found.")

except FileNotFoundError:
    print(f"Error: The file at {CSV_PATH} could not be found. Please check your path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
