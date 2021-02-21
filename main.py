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
            liste_ligne = lines[i].split("|")
            # on separe la liste en deux avec le character |
            for j in range(2):
                # repeter dans les deux bout de texte separer par le |
                liste_ligne[j] = liste_ligne[j].strip()
                # on enleve les retour chariots et les espaces devant ou deriere
            data.append(liste_ligne)

        return data







if __name__ == "__main__":
    root = Tk()
    app = Applications(root)
    root.mainloop()