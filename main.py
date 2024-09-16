import csv
import os 
import webbrowser
import datetime
import pyttsx3
from pathlib import Path

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        greet = "Good morning!"
    elif 12 <= hour < 18:
        greet = "Good afternoon!"
    else:
        greet = "Good evening!"
    speak(greet)
    print(greet)


def delete_old():
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    months = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
              "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}

    activity_list = []
    
    with open("todolist.csv", "r", newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for line in reader:
            activity_list.append(line)

    # Write back only the activities that are from the current or future months/years
    with open("todolist.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

        for activity in activity_list:
            try:
                # Ensure month is valid and handle case sensitivity
                activity_month = months[activity[4].strip().lower()]
                activity_year =  int(activity[5].strip())  

                if activity_month >= current_month and activity_year >= current_year:
                    writer.writerow(activity)
            except KeyError as e:
                print(f"Skipping invalid entry (Invalid month): {activity}, Error: {e}")
                continue  # Skip invalid months
            except ValueError as e:
                print(f"Skipping invalid entry (Invalid day or month): {activity}, Error: {e}")
                continue  # Skip invalid day or month



def take_command():
    command = input("How can I assist you? ").lower()
    return command

def process_command(command):
    if "time" in command:
        time_now = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {time_now}")
        print(f"The current time is {time_now}")

    elif "date" in command:
        today = datetime.datetime.now().strftime('%B %d, %Y')
        speak(f"Today's date is {today}")
        print(f"Today's date is {today}")

    elif "add new thing to do" in command:
        speak("What is it this time?")

        activity = input("New activity:").lower()
        activity_info = activity.split(",")

        activity_list = [] 
        with open("todolist.csv","r",newline='') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                activity_list.append(line)

        with open("todolist.csv","w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(activity_list)
            writer.writerow(activity_info)
        speak("The new activity was added to the list")
    
    elif "tell me what i have to do" in command:
        current_month = datetime.datetime.now().strftime('%B').lower()
        current_day = str(int(datetime.datetime.now().strftime('%d')))
        activity_list = []
        activity_today = 0

        with open("todolist.csv","r", newline='') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                activity_list.append(line)

        speak("You have ")

        for activity in activity_list:
            if activity[3].strip() == current_day and activity[4].strip() == current_month:
                speak(f"{activity[0]} at {activity[2]}")
                activity_today = 1

        if activity_today == 0:
            speak("nothing scheduled")

        speak("today")
        
        with open("todolist.csv","w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(activity_list)

        

    elif "search" in command:
        search_term = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search_term}")
        speak(f"Searching for {search_term} on Google")
    
    elif "youtube" in command:
        search_term = command.replace("youtube","").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")
        speak(f"Searching for {search_term} on YouTube")

    elif "exit" in command:
        speak("Goodbye!")
        exit()

    else:
        speak("Sorry, I didn't understand that command.")
        print("Sorry, I didn't understand that command.")

def main():
    greet_user()
    delete_old()
    while True:
        command = take_command()
        process_command(command)

if __name__ == "__main__":
    main()
