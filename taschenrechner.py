import re 

def taschenrechner():
  rechenart = input("Welche Rechenart möchtest du verwenden?")
  zahl1 = int(input("Was ist deine erste Zahl? "))
  zahl2 = int(input("Was ist deine zweite Zahl? "))
  if rechenart.lower() == "addition":
    antwort = zahl1+ zahl2
    print(f"Bot: {antwort}")

def taschenrechner_mal(user_input):
  numbers = [int(num) for num in re.findall(r'\d+', user_input)]
  ergebniss = numbers[0] * numbers[1]
  print(f"Bot: {ergebniss}")


def taschenrechner_geteilt(user_input):
  numbers = [int(num) for num in re.findall(r'\d+', user_input)]
  
  ergebniss = numbers[0] / numbers[1]
  print(f"Bot: {ergebniss}")
  


def taschenrechner_minus(user_input):
  numbers = [int(num) for num in re.findall(r'\d+', user_input)]
  ergebniss = numbers[0] - numbers[1]
  print(f"Bot: {ergebniss}")


def taschenrechner_plus(user_input):
  numbers = [int(num) for num in re.findall(r'\d+', user_input)]
  ergebniss = numbers[0] + numbers[1]
  print(f"Bot: {ergebniss}")
