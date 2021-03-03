from timeit import default_timer
from functools import partial
from tkinter import *
import random
import sys
# limite 420 characters

class Coter():
    """
    class which allows to manage all the right frame
    """

    def __init__(self, fen, bonneRep):
        """
        Init the class

            parameters:
                fen, tk.frame() => the frame where all of the app will occur
                bonneRep, integer => Number of good answer needed for winning
        """
        self.amount_right = bonneRep
        self.fen = fen
        self.font = ("", 16)
        # The font use for all of the widgets
        self.right, self.wrong = 0, 0
        # the number of right/wrong answer 

        self.start = default_timer()
        # we init the timer 
        self.frameP = Frame(self.fen)
        # the main frame
        self.frameP.grid()

        frame_time = Frame(self.frameP , bd='0.5')
        frame_time.grid(column=0, row=0, padx=10, pady=10, sticky=N)
        # Frame for the chrono

        label_time = Label(frame_time, text="Time :", font=self.font)
        label_time.grid(column=0, row=0, padx=10, pady=5, sticky=N)
        # the Label of the chrono

        self.compteur_t = Label(frame_time, text="0:00:00", font=self.font)
        self.compteur_t.grid(column=0, row=1, padx=10, pady=5, sticky=N)
        # the chrono
        self.fen.after(1000, self.update_time)
        # each second we refresh the chrono

        frame_point = Frame(self.frameP , bd='0.5')
        frame_point.grid(column=0, row=1, padx=5, pady=5, sticky=N)
        # the frame for the counter

        self.label_wrong = Label(frame_point, text = "Wrong : 0", font=self.font)
        self.label_wrong.grid(column=0, row=0, padx=5, pady=5, sticky=W)
        # the counters of the wrong answer

        self.label_right = Label(frame_point, text = "Right :   0", font=self.font)
        self.label_right.grid(column=0, row=1, padx=5, pady=5, sticky=W)
        # the counter of the right answer 

        frame_liste = Frame(self.frameP , bd='0.5')
        frame_liste.grid(column=0, row=2, padx=5, pady=5, sticky=N)
        # the frame of the liste of all the good answer 

        complete_label = Label(frame_liste, text="Liste:",font=self.font)
        complete_label.grid(column=0, row=0, padx=5, pady=5, sticky=N)
        # the label above the slist

        frame_liste2 = Frame(frame_liste, bd='0.5')
        frame_liste2.grid(column=0, row=1, padx=5, pady=5, sticky=N)
        # frame that can let us use .pack()

        scrollbarY = Scrollbar(frame_liste2, orient="vertical")
        scrollbarX = Scrollbar(frame_liste2, orient="horizontal")

        # we init the scrollbar
        self.mylist = Listbox(frame_liste2 ,width=40, height=10, yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set, bd=0)
        self.mylist.select_set(0)
        # we create the list widget
        scrollbarY.config(command=self.mylist.yview)
        scrollbarY.pack(side=RIGHT, fill=BOTH)
        scrollbarX.config(command=self.mylist.xview)
        scrollbarX.pack(side=BOTTOM, fill=BOTH)
        self.mylist.pack()
        # we place the widget

    def update_time(self):
        """
        function that updates the stopwatch every second
        """
        now = default_timer() - self.start
        # init the time pass betwen the start of the chrono
        minutes, seconds = divmod(now, 60) 
        # we get the minute and second
        hours, minutes = divmod(minutes, 60)
        # we get the hour 
        str_time = "%02d:%02d:%02d" % (hours, minutes, seconds)
        # we convert the time into a string format
        self.compteur_t.configure(text=str_time)
        # we uptade the label with the new text
        if self.right == self.amount_right:
            # if the player have win we pass
            pass
        else:
            # if not , we call the function each second
            self.fen.after(1000, self.update_time)

    def update_wrong(self):
        """
        Function call when the player made a mistake
        """
        self.wrong += 1
        # we add 1 to the counter
        text = "Wrong : " + str(self.wrong)
        self.label_wrong.config(text = text)
        # we update the label 

    def update_right(self):
        """
        Function call when the player found the cards
        """
        self.right += 1
        # we add 1 to the counter
        text = "Right : " + str(self.right)
        self.label_right.config(text = text)
        # we update the label 
        if self.right == self.amount_right:
            # if the player have find all of the cards we call the function for winning
            self.win()

    def add_liste(self, data):
        """
        Function call to add data to the list widget

            Parameters:
                data, / => the data to add to the list
        """
        self.mylist.insert(END, data)

    def win(self):
        """
        Function call when you have win the game
        """
        now = default_timer() - self.start
        # init the time pass betwen the start of the chrono
        minutes, seconds = divmod(now, 60) 
        # we get the minute and second
        hours, minutes = divmod(minutes, 60)
        # we get the hour 
        str_time = "%02d:%02d:%02d" % (hours, minutes, seconds)
        # wee get the time of the player

        self.frameP.grid_forget()
        # we suppr the main frame
        img = PhotoImage(file="coupe.gif")
        # we get the picture
        canvas = Canvas(self.fen)
        canvas.configure(width=img.width(), height=img.height())
        canvas.create_image(img.width()/2,img.height()/2,image=img)
        # we creat the canvas 
        canvas.image = img
        # we add the picture to the canvas
        canvas.grid(row=0,column=0)
        # we show it 
        
        text = "you win in " + str_time
        label_ = Label(self.fen, text=text, font=self.font)
        label_.grid(row=1, column = 0)
        # we add a label for saying YOU Wwin

        boutton_ = Button(self.fen, text = "Quit", command=self.quitter, font=self.font)
        boutton_.grid(row=2, column = 0)
        # we add a button for quitting

    def quitter(self):
        """
        function to quit the programme 
        """
        sys.exit()

class Memory():
    """
    A class to manage the memory game
    """
    def __init__(self, fen, fen2, data):
        """
        init the class

            Parameters:
                fen, Tk.frame => the main frame for the memory game
                fen2, Tk.frame => the secondary frame on the right 
                data, list => all of the cards
        """    
        self.right = 0
        # number of good answers
        self.fen = fen
        self.police = ('helvetica', 10)
        # font of the app
        self.data_carte1 = data[0] 
        self.data_carte2 = data[1]
        # value of the second cards
        # Connect to each other by their index, example =>
        # If we look for the value which is store in the list (data_carte1) to place x
        # the associated value, in the list (map2) will be present at location x
        self.data = self.data_carte1[:] 
        self.data.extend(self.data_carte2)
        # we copy the list self.data_carte1 locally
        # we modify the local copy by adding list two to it
        # to make it a list of all the values
        self.liste_button = []
        # List which contains all the buttons
        self.button_click = 0
        # Variable which alternates between 2 values:
        # 0: No raise card, 1: one raise card
        self.valeur_1carte, self.valeur_2carte = None, None
        # Variable which has in memory which cards is return
        self.amount_right = len(self.data_carte1)
        # the amount of good andwers
        self.coter = Coter(fen2, self.amount_right)
        # we creat a instance of the coter class
        self.create_button()
        # call de la fonction create button

    def create_button(self):
        """
        Function to creat all the button on the window
        """
        for i in range(len(self.data)):
            # Repeat for the number of buttons to create
            button = Button(self.fen, 
                            text = "", 
                            width=30, 
                            height=15, 
                            relief = "flat",
                            font = self.police, 
                            bg='#FFFFFF',
                            disabledforeground = '#000000',
                            wraplength= 200, 
                            borderwidth = 0,
                            # justify=LEFT,
                            command=partial(self.button_press, i)) 
            # we create an empty button, with a command which returns a value, which, associated with the index
            # of the list tells us the button (in the list)
            # the partial function allows us to give an argument (even if it a tkinter event)
            self.liste_button.append(button)
            # we add the button to the list
        self.affichage_boutton()
        # call tath for showing the button
    
    def affichage_boutton(self):
        """
        Funtion to show all of the button
        """
        nbCarte = len(self.liste_button) 
        # The number of cards in total
        nb_carte_quotient = nbCarte // 5 
        # the number of times we can make lines of 5
        # Return the quotien Euclidean division by 5
        nb_carte_reste = nbCarte % 5
        # the number of cards to add after, the rest of the Euclidean division
        # returns the reste of the Euclidean division by 5

        liste_coord = []
        # list which will contain all the coordinates
        for j in range(nb_carte_quotient):
           # we repeat the number of times we can make lines of 5
            for i in range(5):
                liste_coord.append([i, j]) 
                # we add the coord in a list, that we add in the list of coord
        if nb_carte_reste != 0:
            # if there are still cards to add
            j = nb_carte_quotient + 1
            # we add a row
            for i in range(nb_carte_reste):
                # we repeat this the number of times there are cards left to display
                liste_coord.append([i, j]) 
                # we add the coord in a list that we add in the list of coord
        
        random.shuffle(liste_coord)
        # we randomize the coord list
        for i in range(len(liste_coord)):
            # we repeat the number of coordinates available times
            self.liste_button[i].grid(column=liste_coord[i][0], row=liste_coord[i][1], padx=10, pady=10, sticky=N)
            # we display the buttons according to the coordinates

    def button_press(self, n):
        """
        Function call when a user press a button

            Parameters:
                n, int => allows us to know which button we clicked
                          this is the index of the button in the button list
                          the button is therefore in self.liste_button [n]
        """
        if self.button_click == 0:
            # If no card is returned
            self.liste_button[n].configure(text = self.data[n])
            # we display the text assign to the button above
            self.button_click = 1
            # we indicate that a button has been clicked
            self.valeur_1carte = n
            # we indicate which button has been returned
        elif (self.button_click == 1) and (self.liste_button[self.valeur_1carte]) != self.liste_button[n]:
            # otherwise if a card has already been raised, and you do not click on the same card
            for child in self.fen.winfo_children():
                child['state'] = DISABLED
            # we deactivate the buttons
            self.liste_button[n].configure(text = self.data[n])
            # we display the text assign to the button above
            self.valeur_2carte = n
            carte1 = self.liste_button[self.valeur_1carte].cget('text')
            carte2 = self.liste_button[self.valeur_2carte].cget("text")
            #We Recover The Two Cards ToD isplay
            self.button_click = 0
            # we indicate that 2 button we are to click, => we reset to button click to 0
            index_carte1 = self.data.index(carte1) 
            # we look at where the index of card number 1 is found in all the data given together
            # if the index of card 1 is greater than the length of the list with all the data
            # we know then that the index of the first card is in part 1 of the list,
            # so the list is self.data_card1, otherwise it's in self.data_carte2
            if index_carte1 < (len(self.data) / 2):
                index_carte1 = self.data_carte1.index(carte1)
            else: index_carte1 = self.data_carte2.index(carte1)
           
           # we do the same but for card 2
            index_carte2 = self.data.index(carte2) 
            if index_carte2 < (len(self.data) / 2):
                index_carte2 = self.data_carte1.index(carte2)
            else: index_carte2 = self.data_carte2.index(carte2)

            if index_carte1 == index_carte2:
                # if the cards go together 
                self.liste_button[self.valeur_1carte].config(bg="#008000")
                self.liste_button[self.valeur_2carte].config(bg="#008000")
                # we display them in green
                self.fen.after(500, self.good)
                # we wait 0.5s and say they are good
            else:
                #if the cards don't go together
                self.liste_button[self.valeur_1carte].config(bg="#FF0000")
                self.liste_button[self.valeur_2carte].config(bg="#FF0000")
                # we display them in red
                self.fen.after(800, self.wrong)
                # we wait 0.8s sand say they are good
            
    def wrong(self):
        """
        function to call when the cards are wrong
        """
        self.liste_button[self.valeur_1carte].config(bg="#FFFFFF")
        self.liste_button[self.valeur_1carte].config(text=" ")
        self.valeur_1carte = None
        # we reset the value of card1 to 0
        self.liste_button[self.valeur_2carte].config(bg="#FFFFFF")
        self.liste_button[self.valeur_2carte].config(text=" ")
        self.valeur_2carte = None
       # we reset the value of card2 to 0
        for child in self.fen.winfo_children():
            child['state'] = NORMAL
       # reactivation of buttons
        self.coter.update_wrong()
        # we update the other panel to tell that we have do a error

    def good(self):
        """
        function to call when the cards are right
        """
        data = [self.liste_button[self.valeur_1carte].cget('text'), self.liste_button[self.valeur_2carte].cget('text')]
        # we recover what is written on the cards
        self.coter.add_liste(data)
        # we update the list on the quotation
        self.liste_button[self.valeur_1carte].destroy()
        self.liste_button[self.valeur_2carte].destroy()
        # we destruct the button
        self.coter.update_right()
        # we update the good answer on the other
        self.right += 1
        # add 1 to the correct answer counter
        if self.amount_right == self.right:
            # if the number of good answer is equal to the number of good answer needed for winning
            self.win()
            #we call the function for winning
        else:
            # else if not, we reactivate the buttons
            for child in self.fen.winfo_children():
                child['state'] = NORMAL
                # reactivation of buttons

    def win(self):
        """
        Unction to cal when winning
        """
        self.fen.grid_forget()
        # we delete the frame 

class Applications():
    """
    Class used to manage the applications
    """
    def __init__(self, fen):
        """
        init the class

            Parameters:
                fen, Tk.frame => the main frame for the memory game
        """
        self.fen = fen
        self.fen.minsize(800, 1000) 
        self.data = self.recuperations_carte()
        # the data of the cards
        self.fenetre_principale()

    def recuperations_carte(self):
        """
        Function that allows you to get memory cards from the text file
        returns the list of cards
        """
        data_memory1 = []
        data_memory2 = []
        with open("Carte_memory.txt", "r") as file:
            # we open the file and store all of his lines in a list
            lines = file.readlines()
        lines = [x for x in lines if x!='\n']
        # deletion of line breaks
        for i in range(len(lines)):
            # repeat the length of lines
            liste_ligne = lines[i].split(";",1)
            # we split the list in two with the character ;
            for j in range(2):
                # repeat in both ends of text separated by the ;
                liste_ligne[j] = liste_ligne[j].strip()
                # remove the carriage returns and the spaces in front or behind
            data_memory1.append(liste_ligne[0])
            data_memory2.append(liste_ligne[1])
        return [data_memory1, data_memory2]

    def fenetre_principale(self):
        """
        Fonction pour afficher la fenetre principal
        """
        frame_principale = Frame(self.fen, bd="0.5")
        frame_principale.grid(column=0, row=0, padx=20, pady=10, sticky=N,rowspan=2)
        
        frame_secondaire = Frame(self.fen, bd="0.5")
        frame_secondaire.grid(column=1, row=0, padx=20, pady=10, sticky=N)
        # show the first frame

        # show the secound frame

        jeuMemory = Memory(frame_principale, frame_secondaire, self.data)

if __name__ == "__main__":
    root = Tk()
    app = Applications(root)
    root.mainloop()
