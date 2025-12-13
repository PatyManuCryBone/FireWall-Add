import subprocess

def menu1():
    while True:
        menu = ("\n\n\n1. Blocca Traffico su uno specifico protocollo(ES. ftp)\n2. Blocca Tutto il traffico su tutte le porte\n3. Accetta una connessione su uno specifico protocollo\n4. Accetta le connessioni su tutte le porte\n5. Status\n6. Exit\n\nA) Attiva Firewall ufw\nD) Disattiva Firewall ufw\n\n\nBlock. Blocca traffico ICMP\nAllow. Consenti traffico ICMP")
        print(menu)
        print("")
        scelta = input("Scegli un'opzione >> ")

        if scelta == "1":
            porta = int(input("PROTOCOLLO DA BLOCCARE LA CONNESSIONE >> "))
            comando = f" ufw deny in {porta}/tcp"
            print("comando inviato...", comando)
            subprocess.run(comando, shell=True)
            input("")
        elif scelta == "2":
            comando1 = f"ufw default deny incoming"
            print("Comando inviato...", comando1)
            subprocess.run(comando1, shell=True)
            input("")
        elif scelta == "3":
            protocollo2 = int(input("PROROCOLLO DA CONSENTIRE LA CONNESSIONE >> "))
            comando2 = f"ufw allow {protocollo2}/tcp"
            print("Comando inviato...", comando2)
            subprocess.run(comando2, shell=True)
            input("")
        elif scelta == "4":
            comando3 = f"ufw default allow incoming"
            print("Comando inviato...", comando3)
            subprocess.run(comando3, shell=True)
            input("")
        elif scelta == "5":
            comando4 = f"ufw status"
            print("Comando inviato...", comando4)
            subprocess.run(comando4, shell=True)
            input("")
        elif scelta == "6":
            print("A presto. Ciaoo")
            break
        elif scelta == "A":
            comandoA = f"ufw enable"
            print("Comando  inviato...", comandoA)
            subprocess.run(comandoA, shell=True)
            input("")
        elif scelta == "D":
            comandoD = f"ufw disable"
            print("Comando  inviato...", comandoD)
            subprocess.run(comandoD, shell=True)
            input("")
        elif scelta == "Block":
            comandoB = f"iptables -I INPUT -p icmp --icmp-type echo-request -j DROP"
            print("Comando inviato...", comandoB)
            subprocess.run(comandoB, shell=True)
            input("")
        elif scelta == "Allow":
            comandoALL = f"iptables -D INPUT -p icmp --icmp-type echo-request -j DROP"
            print("Comando inviato...", comandoALL)
            subprocess.run(comandoALL, shell=True)
            input("")
        else:
            print("Numero sconosciuto!")

if __name__ == "__main__":
    menu1()
