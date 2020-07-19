import random

def gen_msg(wrd,letters):
    ret=""
    for x in wrd:
        if x in letters:
            ret+=x
        else:
            ret+="-"
    return ret

def get_choice():
    print("H A N G M A N\n")
    choice = input("Type play to play the game, exit to quit:")
    return choice

choice=get_choice()
while choice == "play" or choice =="exit":
    if choice =="play":
        words = ['python', 'java', 'kotlin', 'javascript']
        check_wrd = random.choice(words)
        all_letters=set(check_wrd)
        input_letters=set()
        i=0
        while(i < 8):
            out_str=gen_msg(check_wrd,input_letters)
            print("\n"+out_str)
            x=input("Input a letter: ")
            if x in all_letters:
                all_letters.remove(x)
                input_letters.add(x)
            elif x in input_letters:
                print("You already typed this letter")
            elif len(x) != 1:
                print("You should input a single letter")
            elif x.islower() == False:
                print("It is not an ASCII lowercase letter")
            else:
                print("No such letter in the word")
                input_letters.add(x)
                #The above statement doesnt affect input prompt as 
                #prompt is made by cross referencing check_wrd
                i+=1
            
        if(out_str == check_wrd):
            print(f"You guessed the word {check_wrd}!\nYou survived!")
        else:
            print("You are hanged!")
        choice=get_choice()
    elif choice =="exit":
        break
else:
     choice=get_choice()