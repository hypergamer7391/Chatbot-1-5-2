import json
from difflib import get_close_matches
import getweather as gw
from getweather import get_weather_forecast, get_current_temp
from taschenrechner import taschenrechner, taschenrechner_mal, taschenrechner_minus, taschenrechner_geteilt, taschenrechner_plus
import tracemalloc
import asyncio
import os

import re
from googletrans import Translator
from datetime import datetime

def username_password_prompt():
    with open('user_credentials.json', 'r') as file:
        user_credentials = json.load(file)

    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        for user in user_credentials["users"]:
            if user["username"] == username and user["password"] == password:
                return username, password

        print("Invalid username or password. Please try again.")

def create_log_file(username: str):
  log_folder = "logs"
  log_filepath = os.path.join(log_folder, f"{username}_chat_log.txt")
  if not os.path.exists(log_folder):
      os.makedirs(log_folder)
  if not os.path.exists(log_filepath):  # Überprüfen, ob die Logdatei bereits existiert
      with open(log_filepath, 'w') as log_file:
          log_file.write(f"Chat log for user: {username}\n")
  return log_filepath
  
def log_message(log_file: str, sender: str, message: str):
    with open(log_file, 'a') as log:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{current_time} - {sender}: {message}\n")

def translate_text(text, target_language):

  translator = Translator()
  translated_text = translator.translate(text, dest=target_language)
  print(f"Bot: Die Übersetzung von {text} nach {target_language} ist {translated_text.text}")





def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.8)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def delete_answer_by_question(knowledge_base: dict, question_to_delete: str):
  for q in knowledge_base["questions"]:
    if q["question"] == question_to_delete:
        knowledge_base['questions'].remove(q)
        save_knowledge_base('knowledge_base.json', knowledge_base)
        print(f"Die Frage '{question_to_delete}' und die dazugehörige Antwort wurden erfolgreich gelöscht.")
        return
  print(f'Die Frage "{question_to_delete}" wurde nicht gefunden.')


    


def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    username, password = username_password_prompt()
    if username.lower() != 'nolog':
      log_file = create_log_file(username)

    
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    while True:
    
        user_input: str = input('Du: '.encode('utf-8').decode('utf-8'))

        log_message(log_file, username, user_input)  
      
        

      
        pattern = re.compile(r"\d+")

        
        match = pattern.findall(user_input)
        matches = len(match)
        
        if user_input.lower() == 'quit':
            break
        if "wetter" in user_input.lower():
          location = input("Wo: ")
          tracemalloc.start()
          print(asyncio.run(get_weather_forecast(location)))
          tracemalloc.stop()

        if "übersetzen" in user_input.lower():
          text_to_translate = input("Bot: Text: ")
          target_sprache = input("Bot: Zielsprache: ")
          
          if target_sprache.lower() == "deutsch":
            target_language = "de"
            translate_text(text_to_translate, target_language)
          elif target_sprache.lower() == "englisch":
            target_language = "en"
            translate_text(text_to_translate, target_language)
          elif target_sprache.lower() == "französisch":
            target_language = "fr"
            translate_text(text_to_translate, target_language)
          else: 
            print("Bot: Das ist keine mir bekannte Sprache!")
            
          
            
          
          
        
        
        if "*" in user_input:
          if matches == 2:
            taschenrechner_mal(user_input)
          break
        if "/" in user_input:
          if matches == 2:
            taschenrechner_geteilt(user_input)
          break
        if "-" in user_input:
          if matches == 2:
            taschenrechner_minus(user_input)
          break
        if "+" in user_input:
          if matches == 2:
            taschenrechner_plus(user_input)
          break
        if user_input.lower() == "andern":
          question_to_change = input("Welche Frage möchtest du ändern? ")
          existing_answer = get_answer_for_question(question_to_change, knowledge_base)

          if existing_answer:
              new_answer = input(f"Gib die neue Antwort für \"{question_to_change}\" ein: ")
              for q in knowledge_base["questions"]:
                  if q["question"] == question_to_change:
                      q["answer"] = new_answer
              save_knowledge_base('knowledge_base.json', knowledge_base)
              print("Die Antwort wurde erfolgreich geändert")

          else:
              print(f'Die Frage "{question_to_change}" existiert nicht. Möchtest du sie hinzufügen?')
              add_new = input('Antworte mit "Ja" oder "Nein": ')
              if add_new.lower() == 'ja':
                  new_answer = input("Gib die Antwort ein: ")
                  knowledge_base['questions'].append({"question": question_to_change, "answer": new_answer})
                  save_knowledge_base('knowledge_base.json', knowledge_base)
                  print("Die Frage-Antwort wurde hinzugefügt.")

              else:
                  print("Ok, keine Änderungen wurden vorgenommen.")

        if user_input.lower() == "löschen":
          question_to_delete = input("Welche Frage möchtest du löschen? ")
          delete_answer_by_question(knowledge_base, question_to_delete)
      
        else: 
          if user_input != "übersetzen":
            
          
            best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

            if best_match:
                answer = get_answer_for_question(best_match, knowledge_base)
                print(f"Bot: {answer}")
                log_message(log_file, "Bot", answer)  

            else:
                print('Bot: Das kann ich nicht bringst du es mir bei?')
                new_answer: str = input('Schreib die Antwort oder  "Skip" zum skip: ')
                 
                log_message(log_file, username, new_answer) 

                if new_answer.lower() != 'skip':
                    knowledge_base['questions'].append({"question": user_input, "answer": new_answer})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    print("Bot: Danke ich habe gelernt")

while(True):
  chat_bot()

  