from functools import partial
from time import sleep
from tkinter import *


# memory game
# Choose 1p or 2p 
# Carte importer dans un fichier 
class Memory():
    def __init__(self, fen, data):
        self.fen = fen 
        # Fenetre principal ou afficher les trucs ( une frame )
        self.data_carte1 = data[0] 
        self.data_carte2 = data[1]
        # valeur des deuxiemes cartes
        # Relier entre elle par leur index , exemple =>
        # Si on cherche la valeur qui est store dans la liste (data_carte1) a l'emplacement x
        # la valeur associer, dans la liste (carte2) sera presente a l'emplacement x  
        self.data = self.data_carte1[:] 
        self.data.extend(self.data_carte2)
        print(self.data)
        # on copie la liste self.data_carte1 localement
        # on modifie la copie local en lui rajoutant la liste deux 
        # pour en faire une liste de toute les valeurs 

        self.liste_button = []
        # Liste qui contient la valeur et le boutton 

        self.button_click = 0

        self.create_button()
        # call de la fonction create button

    def create_button(self):
        """
        Function to creat all the button on the window
        """
        for i in range(len(self.data_carte1 * 2)):
            button = Button(self.fen, text = " ", bg='#FFFFFF', command=partial(self.button_press, i))
            self.liste_button.append(button)
        self.affichage_boutton()
    
    def affichage_boutton(self):
        """
        Fonction pour afficher les boutons
        """
        for i in range(len(self.liste_button)):
            self.liste_button[i].grid(column=i, row=0, padx=20, pady=10, sticky=N)

    def button_press(self, n):
        """
        Fonction quand l'utilisateur appuis sur un bouton
        """
        if self.button_click == 0:
            self.liste_button[n].configure(text = self.data[n])
            self.button_click = 1
        else:
            self.liste_button[n].configure(text = " ")
            self.button_click = 0

        # sleep(1)
        # self.liste_button[n].configure(text = " ")




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
        frame_principale = Frame(self.fen, bd="0.5", bg ="#4dd0e1")
        frame_principale.grid(column=0, row=0, padx=20, pady=10, sticky=N, columnspan=2)

        frame_secondaire = Frame(self.fen, bd="0.5", bg ="#5e35b1")
        frame_secondaire.grid(column=2, row=0, padx=20, pady=10, sticky=N)

        jeuMemory = Memory(self.fen, self.data)


if __name__ == "__main__":
    root = Tk()
    app = Applications(root)
    root.mainloop()
