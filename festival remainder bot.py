import datetime
import time
import smtplib
from plyer import notification
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

festivals = {
    "Makara Sankrathi":"2026-01-14",
    "Ugadhi":"2026-03-19",
    "Sri Rama Navami":"2026-03-26",
    "Hanuman Jayanti":"2026-04-02",
    "Holi": "2026-03-04",
    "Vijaya Dhashami":"2025-10-2",
    "Ganesh chatruthi":"2025-08-27",
    "Janmastami":"2025-08-16",
    "Diwali": "2025-10-20",
    "Christmas": "2025-12-25",
    "Eid": "2025-06-07"
}
EMAIL_ENABLED=False 
EMAIL_ADDRESS="your_email@gmail.com"
EMAIL_PASSWORD="your_app_password"
TO_EMAIL="recipient@example.com"

def send_email(subject,body):
    msg=MIMEMultipart()
    msg['From']=EMAIL_ADDRESS
    msg['To']=TO_EMAIL
    msg['Subject']=subject

    msg.attach(MIMEText(body,'plain')) 

    try:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:",e)

def notify(title,message):
    notification.notify(title=title,message=message,timeout=10)
    if EMAIL_ENABLED:
        send_email(title,message)

def check_festivals():
    today=datetime.date.today()
    for name,date_str in festivals.items():
        fest_date=datetime.datetime.strptime(date_str,"%Y-%m-%d").date()
        delta=(fest_date-today).days

        if delta==0:
            notify(f"{name} is today!",f"Celebrate {name} with joy!")
        elif 0<delta<=3:
            notify(f"{name} is coming soon!", f"Only {delta} day(s) left until {name}!")

def add_or_edit_festival():
    name = input("Enter festival name: ").strip()
    date_str = input("Enter date (YYYY-MM-DD): ").strip()
    try:
        datetime.datetime.strptime(date_str,"%Y-%m-%d")
        festivals[name] = date_str
        print(f"{name} set for {date_str}")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")

def show_festivals():
    print("\nUpcoming Festivals:")
    for name, date_str in sorted(festivals.items(),key=lambda x:x[1]):
        print(f"{name} - {date_str}")



print("Starting Festival Reminder Bot...")

while True:
    print("\nMenu:\n1. Check Festivals\n2. Add/Edit Festival\n3. Show Festivals\n4. Exit")
    choice=input("Choose an option (1–4): ").strip()

    if choice=="1":
        check_festivals()
    elif choice=="2":
        add_or_edit_festival()
    elif choice=="3":
        show_festivals()
    elif choice=="4":
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please enter a number from 1 to 4.")

    print("Waiting 5 seconds before next check...\n")
    time.sleep(5)