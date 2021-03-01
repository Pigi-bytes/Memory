from timeit import default_timer
from functools import partial
from tkinter import *
import random

class Coter():
    def __init__(self, fen):
        super().__init__()
        self.font = ("", 16)
        self.fen = fen
        self.start = default_timer()

        self.right = 0
        self.wrong = 0
        
        # frameP = Frame(self.fen)
        # frameP.pack()

        frame_temps = Frame(self.fen, bd='0.5', bg = "#FF0000")
        frame_temps.grid(column=0, row=0, padx=10, pady=10, sticky=N)

        label_time = Label(frame_temps, text="Time :", font=self.font)
        label_time.grid(column=0, row=0, padx=10, pady=5, sticky=N)

        self.compteur_t = Label(frame_temps, text="0:00:00", font=self.font)
        self.compteur_t.grid(column=0, row=1, padx=10, pady=5, sticky=N)
        self.fen.after(1000, self.update_time)

        frame_point = Frame(self.fen, bd='0.5', bg='#E0E055')
        frame_point.grid(column=0, row=1, padx=5, pady=5, sticky=N)

        text = "Wrong : " + str(self.wrong)
        self.label_wrong = Label(frame_point, text = text, font=self.font)
        self.label_wrong.grid(column=0, row=0, padx=5, pady=5, sticky=W)

        text = "Right :   " + str(self.right)
        self.label_right = Label(frame_point, text = text, font=self.font)
        self.label_right.grid(column=0, row=1, padx=5, pady=5, sticky=W)

        frame_liste = Frame(self.fen, bd='0.5', bg='#000FFF')
        frame_liste.grid(column=0, row=2, padx=5, pady=5, sticky=N)

        complete_label = Label(frame_liste, text="Liste:",font=self.font)
        complete_label.grid(column=0, row=0, padx=5, pady=5, sticky=N)

        frame_liste2 = Frame(frame_liste, bd='0.5', bg='#E0E055')
        frame_liste2.grid(column=0, row=1, padx=5, pady=5, sticky=N)

        scrollbarY = Scrollbar(frame_liste2, orient="vertical")
        self.mylist = Listbox(frame_liste2 ,width=40, height=10, yscrollcommand=scrollbarY.set, bd=0)
        self.mylist.select_set(0)
        scrollbarY.config(command=self.mylist.yview)
        scrollbarY.pack(side=RIGHT, fill=BOTH)
        self.mylist.pack()


    def update_time(self):
        "Incrémente le compteur à chaque seconde"
        now = default_timer() - self.start
        minutes, seconds = divmod(now, 60) 
        hours, minutes = divmod(minutes, 60)
        str_time = "%d:%02d:%02d" % (hours, minutes, seconds)
        self.compteur_t.configure(text=str_time)
        self.fen.after(1000, self.update_time)

    def update_wrong(self):
        self.wrong += 1
        text = "Wrong : " + str(self.wrong)
        self.label_wrong.config(text = text)

    def update_right(self):
        self.right += 1
        text = "Right : " + str(self.right)
        self.label_right.config(text = text)

    def add_liste(self, data):
        self.mylist.insert(END, data)

class Memory():
    """
    Une classe pour gerer le jeu de memory
    """
    def __init__(self, fen, fen2, data):

        self.fen = Frame(fen)
        self.fen.grid()

        self.coter = Coter(fen2)
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
        for child in self.fen.winfo_children():
            child['state'] = NORMAL
        self.coter.update_right()
        # reactivation des bouttons

class Applications():
    """
    Classe qui permet de gerer l'applications 
    """
    def __init__(self, fen):
        super().__init__()
        self.fen = fen

        self.data = self.recuperations_carte()
        self.number_player = 0
        self.number_of_player()

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
            liste_ligne = lines[i].split("|",1)
            # on separe la liste en deux avec le character |
            for j in range(2):
                # repeter dans les deux bout de texte separer par le |
                liste_ligne[j] = liste_ligne[j].strip()
                # on enleve les retour chariots et les espaces devant ou deriere
            data_memory1.append(liste_ligne[0])
            data_memory2.append(liste_ligne[1])
        return [data_memory1, data_memory2]

    def number_of_player(self):

        def p1():
            self.number_player = 1
            self.fenetre_principale()

        def p2():
            self.number_player = 2
            self.fenetre_principale()

        self.frame_player_choose = Frame(self.fen)
        self.frame_player_choose.pack()

        frame_texte = Frame(self.frame_player_choose, bd="0.5", bg ="#4dd0e1")
        frame_texte.grid(column=0, row=0, padx=20, pady=10, sticky=N)

        frame_button = Frame(self.frame_player_choose, bd="0.5", bg="#5e35b1")
        frame_button.grid(column=0, row=1, padx=20, pady=10, sticky=N)

        label_how_many_player = Label(frame_texte, text="How many player")
        label_how_many_player.grid(column=0, row=0, padx=20, pady=10, sticky=N)

        button_1p = Button(frame_button, text="1 player", command=p1)
        button_1p.grid(column=0, row=0, padx=5, pady=10, sticky=N)

        button_2p = Button(frame_button, text="2 players", command=p2)
        button_2p.grid(column=1, row=0, padx=5, pady=10, sticky=N)

    def fenetre_principale(self):

        self.frame_player_choose.pack_forget()    

        # Affichage frame
        frame_secondaire = Frame(self.fen, bd="0.5", bg ="#5e35b1")
        frame_secondaire.grid(column=2, row=0, padx=20, pady=10, sticky=N)
        # coter = Coter(frame_secondaire)

        frame_principale = Frame(self.fen, bd="0.5", bg ="#4dd0e1")
        frame_principale.grid(column=0, row=0, padx=20, pady=10, sticky=N, columnspan=2)
        jeuMemory = Memory(frame_principale,frame_secondaire, self.data)

#  TODO : Add the hability to change player and all the stuff 
#  TODO : commentaire 
#  TODO : optimizations 
#  TODO : make the app more nice
#  TODO : add the win menu / lose 
#  TODO : changer la maniere est afficher le texte pour que sa rentre sur le boutton
#  TODO : Setting a la voler 
#  TODO : App to add all of the texte
if __name__ == "__main__":
    root = Tk()
    app = Applications(root)
    root.mainloop()
