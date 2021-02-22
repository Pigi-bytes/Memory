from tkinter import * 


# memory game
# Choose 1p or 2p 
# Carte importer dans un fichier 

class Applications():
    """
    Classe qui permet de gerer l'applications 
    """
    def __init__(self, fen):
        super().__init__()
        self.data = self.recuperations_carte()
        self.number_player = 0
        self.number_of_player(fen)

    def recuperations_carte(self):
        """
        Fonction qui permet de recuperer les cartes du memory depuis le fichier texte
        renvoie la liste des cartes 
        """
        # ajouter un message d'erreur si sa fail
        data = []
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
            data.append(liste_ligne)

        return data

    def number_of_player(self, fen):

        def p1():
            self.number_player = 1
            self.fenetre_principale(fen)

        def p2():
            self.number_player = 2
            self.fenetre_principale(fen)

        self.frame_player_choose = Frame(fen)
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

    def fenetre_principale(self, fen):

        self.frame_player_choose.pack_forget()    

        # Affichage frame
        frame_principale = Frame(fen, bd="0.5", bg ="#4dd0e1")
        frame_principale.grid(column=0, row=0, padx=20, pady=10, sticky=N, columnspan=2)

        frame_secondaire = Frame(fen, bd="0.5", bg ="#5e35b1")
        frame_secondaire.grid(column=2, row=0, padx=20, pady=10, sticky=N)
        
        





if __name__ == "__main__":
    root = Tk()
    app = Applications(root)
    root.mainloop()