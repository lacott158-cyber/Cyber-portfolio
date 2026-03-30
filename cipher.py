def encode(message):
    encoded_text = ""
    #Moves characters 15 spaces
    shift = 15
    for char in message:
        if char.isupper():
            #Function to handle uppercase characters
            encoded_text += chr((ord(char) - 65 + shift) % 26 + 65) 
        elif char.islower():
            #Function to handle lowercase letter
            encoded_text += chr((ord(char) - 97 + shift) % 26 + 97)
        else: 
            encoded_text += char
    return encoded_text

#Allows user to input letters and test program
user_message = input("Enter: ")

result = encode(user_message)

print(result)