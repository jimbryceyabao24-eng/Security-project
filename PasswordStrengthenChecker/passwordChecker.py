import string

def check_password(password):
   score = 0
   requirements = []


   #check length of password
   if len(password) >= 8:
      score += 1
      requirements.append("✔️ At least 8 characters")
   else :
      requirements.append("❌ At least 8 characters")

    #check the Upper-case
   if any(c in string.ascii_uppercase for c in password):
      score += 1
      requirements.append("✔️ Contains Upper_case letter")
   else:
      requirements.append("❌ Contains Upper_case letter")

     #check the Lower-case
   if any(c in string.ascii_lowercase for c in password):
          score += 1
          requirements.append("✔️ Contains lower_case letter")
   else:
          requirements.append("❌ Contains lower_case letter")


    #check number
   if any(c .isdigit() for c in password):
       score += 1
       requirements.append("✔️ Contains number")
   else:
       requirements.append("❌ Contains number")

   #check special character
   if any(c in string.punctuation for c in password):
          score += 1
          requirements.append("✔️ Contains special character")
   else:
          requirements.append("❌ Contains special character")

    #Determine the Strength
   if score == 5:
        strength = "VERY STRONG"
   elif score == 4:
        strength = "STRONG"
   elif score == 3:
        strength = "MEDIUM"
   elif score == 2:
        strength = "WEAK"
   else:
        strength = "VERY WEAK"

   return score, strength, requirements

print("=" *40)
print("    STRONG PASSWORD CHECKER")
print("=" *40)

password = input("Enter your password: ")

score, strength, requirements = check_password(password)

print("/n Password Requirement:")
for requirement in requirements:
     print(requirement)

print("/n Password Score:",score, "/5")
print("/n Password Strength", strength)
   