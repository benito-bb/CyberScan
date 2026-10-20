import subprocess


def executer_commande(commande):
    subprocess.run(commande, shell=True)


if __name__ == "__main__":
    commande = input("Entrer votre commande : ")
    executer_commande(commande)