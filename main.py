from timeit import default_timer
from functools import partial
from tkinter import *
import random
import sys


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

        frame_time = Frame(self.frameP , bd='0.5', bg = "#FF0000")
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

        frame_point = Frame(self.frameP , bd='0.5', bg='#E0E055')
        frame_point.grid(column=0, row=1, padx=5, pady=5, sticky=N)
        # the frame for the counter

        self.label_wrong = Label(frame_point, text = "Wrong : 0", font=self.font)
        self.label_wrong.grid(column=0, row=0, padx=5, pady=5, sticky=W)
        # the counters of the wrong answer

        self.label_right = Label(frame_point, text = "Right :   0", font=self.font)
        self.label_right.grid(column=0, row=1, padx=5, pady=5, sticky=W)
        # the counter of the right answer 

        frame_liste = Frame(self.frameP , bd='0.5', bg='#000FFF')
        frame_liste.grid(column=0, row=2, padx=5, pady=5, sticky=N)
        # the frame of the liste of all the good answer 

        complete_label = Label(frame_liste, text="Liste:",font=self.font)
        complete_label.grid(column=0, row=0, padx=5, pady=5, sticky=N)
        # the label above the slist

        frame_liste2 = Frame(frame_liste, bd='0.5', bg='#E0E055')
        frame_liste2.grid(column=0, row=1, padx=5, pady=5, sticky=N)
        # frame that can let us use .pack()

        scrollbarY = Scrollbar(frame_liste2, orient="vertical")
        # we init the scrollbar
        self.mylist = Listbox(frame_liste2 ,width=40, height=10, yscrollcommand=scrollbarY.set, bd=0)
        self.mylist.select_set(0)
        # we create the list widget
        scrollbarY.config(command=self.mylist.yview)
        scrollbarY.pack(side=RIGHT, fill=BOTH)
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

        label_ = Label(self.fen, text="You win !!", font=self.font)
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
    Une classe pour gerer le jeu de memory
    """
    def __init__(self, fen, fen2, data):
        
        
        self.right = 0
        


        self.fen = fen
        # self.fen.grid()

        # Creation de la frame qui va afficher tout les widgets 
        self.police = ('Helvetic', 8)
        # font de l'applications
        self.data_carte1 = data[0] 
        self.data_carte2 = data[1]
        # valeur des deuxiemes cartes
        # Relier entre elle par leur index , exemple =>
        # Si on cherche la valeur qui est store dans la liste (data_carte1) a l'emplacement x
        # la valeur associer, dans la liste (carte2) sera presente a l'emplacement x  
        self.data = self.data_carte1[:] 
        self.data.extend(self.data_carte2)
        # on copie la liste self.data_carte1 localement
        # on modifie la copie local en lui rajoutant la liste deux 
        # pour en faire une liste de toute les valeurs 
        self.liste_button = []
        # Liste qui contient la valeur et le boutton 
        self.button_click = 0
        # Variable qui alterne entre 3 valeurs : 
        # 0: Aucune carte de lever, 1: une carte de lever
        self.valeur_1carte, self.valeur_2carte = None, None
        # Variable qui a en memoire quelle bouton est retourner
        
        self.amount_right = len(self.data_carte1)

        self.coter = Coter(fen2, self.amount_right)
        
        self.create_button()
        # call de la fonction create button

    def create_button(self):
        """
        Function to creat all the button on the window
        """
        for i in range(len(self.data)):
            # Repeter pour le nombre de boutton a crer 
            # TODO : changer la maniere don est afficher le texte pour que sa rentre sur le
            button = Button(self.fen, text = "", width=20, height=5, font = self.police,
                            bg='#FFFFFF', disabledforeground = '#000000', 
                            command=partial(self.button_press, i))
            # on crer un bouton vide, avec une commande qui renvois une valeur, qui , associer a l'index 
            # de la liste nous indique le bouton ( dans la liste ) 
            # la fonction partial nous permet de donner un argument ( meme sic un button tkinter)
            self.liste_button.append(button)
            # on ajoute le bouton dans la liste 
        self.affichage_boutton()
        # on affiche tout ce beau monde 
    
    def affichage_boutton(self):
        """
        Fonction pour afficher les boutons
        """
        nbCarte = len(self.liste_button) 
        # Le nombre de carte au totale 
        nb_carte_quotient = nbCarte // 5 
        # le nombre de fois que on peut faire des lignes de 5
        # Renvois le quotien division euclidienne par 5
        nb_carte_reste = nbCarte % 5
        # le nombre de carte a rajouter apres, le reste de la divison euclidienne
        # renvois le rste de la division euclidienne par 5

        liste_coord = []
        # liste qui va contenir toute les coordonées 
        for j in range(nb_carte_quotient):
            # on repete le nombre de fois que on peut faire des lignes de 5
            for i in range(5):
                liste_coord.append([i, j]) 
                # on rajoute les coord dans une liste, que on rajoute dans la liste de coord
        
        if nb_carte_reste != 0:
            # si il reste des cartes a rajouter 
            j = nb_carte_quotient + 1
            # on rajoute une colonne
            for i in range(nb_carte_reste):
                # on repete sa le nombre de fois qu'il reste de carte a afficher 
                liste_coord.append([i, j]) 
                # on rajouter les coord dans une liste que on rajoute dans la liste de coord
        
        random.shuffle(liste_coord)
        # on randomise la liste de coord
        for i in range(len(liste_coord)):
            # on repete sa le nombre de coordoner disponible fois  
            self.liste_button[i].grid(column=liste_coord[i][0], row=liste_coord[i][1], padx=10, pady=10, sticky=N)
            # on affiche les bouttons en fonction des coordonnes

    def button_press(self, n):
        """
        Fonction quand l'utilisateur appuis sur un bouton
        """
        if self.button_click == 0:
            # Si aucune carte est retourner 
            self.liste_button[n].configure(text = self.data[n])
            # on affiche le texte attribuer au bouton dessus
            self.button_click = 1
            # on indique que un bouton a ete cliquer
            self.valeur_1carte = n
            # on indique quelle bouton a ete retourner 
        elif (self.button_click == 1) and (self.liste_button[self.valeur_1carte]) != self.liste_button[n]:
            # desactivation des bouttons 
            for child in self.fen.winfo_children():
                child['state'] = DISABLED

            # Si une carte est deja retourner 
            self.liste_button[n].configure(text = self.data[n])
            # on affiche le texte attribuer au bouton dessus
            self.valeur_2carte = n
            carte1 = self.liste_button[self.valeur_1carte].cget('text')
            carte2 = self.liste_button[self.valeur_2carte].cget("text")
            # on recupere les deux carte d'afficher

            self.button_click = 0
            # on indique que 2 boutton on ete cliquer, => ont remet a 0 

            index_carte1 = self.data.index(carte1) 
            # on regarde ou se trouve l'index de la carte numero 1 dans tout les donner ensemble
            # si l'index de la carte 1 est plus grande que la longeur de la liste avec tout les donners
            # on sais alors que l'index de la premiere carte est dans la partie 1 de la liste ,
            # donc que la liste est self.data_carte1, sinon c'est dans self.data_carte2
            if index_carte1 < (len(self.data) / 2):
                index_carte1 = self.data_carte1.index(carte1)
            else: index_carte1 = self.data_carte2.index(carte1)
            
            # on fait pareil mais pour la carte 2
            index_carte2 = self.data.index(carte2) 
            if index_carte2 < (len(self.data) / 2):
                index_carte2 = self.data_carte1.index(carte2)
            else: index_carte2 = self.data_carte2.index(carte2)

            if index_carte1 == index_carte2:
                # si les cartes vont ensemble 
                self.liste_button[self.valeur_1carte].config(bg="#008000")
                self.liste_button[self.valeur_2carte].config(bg="#008000")
                # on les affiches en vert
                self.fen.after(500, self.good)
                # on attend 1.5s => apelle 
                
            else:
                # si les cartes ne vont pas ensemble
                self.liste_button[self.valeur_1carte].config(bg="#FF0000")
                self.liste_button[self.valeur_2carte].config(bg="#FF0000")
                # on les affiche en rouge 
                self.fen.after(800, self.wrong)
                # on attend 1s => apelle 
            
    def wrong(self):
        """
        call when carte are worng
        """
        self.liste_button[self.valeur_1carte].config(bg="#FFFFFF")
        self.liste_button[self.valeur_1carte].config(text=" ")
        self.valeur_1carte = None
        # on remet la valeur de la carte1 a 0 
        self.liste_button[self.valeur_2carte].config(bg="#FFFFFF")
        self.liste_button[self.valeur_2carte].config(text=" ")
        self.valeur_2carte = None
        # on remet la valeur de la carte2 a 0 
        for child in self.fen.winfo_children():
            child['state'] = NORMAL
        self.coter.update_wrong()
        # reactivation des bouttons

    def good(self):
        data = [self.liste_button[self.valeur_1carte].cget('text'),self.liste_button[self.valeur_2carte].cget('text')]
        self.coter.add_liste(data)
        self.liste_button[self.valeur_1carte].destroy()
        self.liste_button[self.valeur_2carte].destroy()
        # destruction des bouttons
        self.coter.update_right()
        self.right += 1
        if self.amount_right == self.right:
            self.win()
        else:
            for child in self.fen.winfo_children():
                child['state'] = NORMAL
                # reactivation des bout

    def win(self):
        self.fen.grid_forget()

class Applications():
    """
    Classe qui permet de gerer l'applications 
    """
    def __init__(self, fen):
        super().__init__()
        self.fen = fen

        self.data = self.recuperations_carte()
        self.number_player = 0
        self.fenetre_principale()

    def recuperations_carte(self):
        """
        Fonction qui permet de recuperer les cartes du memory depuis le fichier texte
        renvoie la liste des cartes 
        """
        # ajouter un message d'erreur si sa fail
        data_memory1 = []
        data_memory2 = []
        with open("Carte_memory.txt", "r") as file:
            # we open the file and store all of his lines in a list
            lines = file.readlines()
        lines = [x for x in lines if x!='\n']
        # suppresion des saut de lignes
        for i in range(len(lines)):
            # repeter la longeur de lignes 
            liste_ligne = lines[i].split(";",1)
            # on separe la liste en deux avec le character |
            for j in range(2):
                # repeter dans les deux bout de texte separer par le |
                liste_ligne[j] = liste_ligne[j].strip()
                # on enleve les retour chariots et les espaces devant ou deriere
            data_memory1.append(liste_ligne[0])
            data_memory2.append(liste_ligne[1])
        return [data_memory1, data_memory2]

    def fenetre_principale(self):

        # Affichage frame
        frame_secondaire = Frame(self.fen, bd="0.5", bg ="#5e35b1")
        frame_secondaire.grid(column=2, row=0, padx=20, pady=10, sticky=N)
        # coter = Coter(frame_secondaire)

        frame_principale = Frame(self.fen, bd="0.5", bg ="#4dd0e1")
        frame_principale.grid(column=0, row=0, padx=20, pady=10, sticky=N, columnspan=2)
        jeuMemory = Memory(frame_principale, frame_secondaire, self.data)



#  TODO : commentaire 
#  TODO : optimizations 
#  TODO : make the app more nice
#  TODO : changer la maniere est afficher le texte pour que sa rentre sur le boutton
#  TODO : App to add all of the texte





if __name__ == "__main__":
    root = Tk()
    app = Applications(root)
    root.mainloop()
