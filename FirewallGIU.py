import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, scrolledtext # Importato scrolledtext
import subprocess

# --- 1. Nuova Funzione di Visualizzazione Scrollabile ---

def visualizza_output_scrollabile(titolo, contenuto):
    """Crea una finestra Toplevel con un'area di testo scrollabile per output lunghi."""
    
    output_window = tk.Toplevel()
    output_window.title(titolo)
    output_window.geometry("600x600")
    output_window.configure(bg="#2c3e50")

    # Area di testo scrollabile
    txt_area = scrolledtext.ScrolledText(output_window, 
                                        wrap=tk.WORD, 
                                        width=70, 
                                        height=20, 
                                        font=("Consolas", 10), 
                                        bg="#ecf0f1", 
                                        fg="#2c3e50")
    txt_area.pack(padx=10, pady=10, fill="both", expand=True)

    # Inserisce il contenuto e lo rende non modificabile
    txt_area.insert(tk.INSERT, contenuto)
    txt_area.configure(state='disabled') 

# --- 2. Funzione di Logica (Aggiornata per la visualizzazione scrollabile) ---

def esegui_comando_ufw(comando, visualizza_scrollabile=False):
    """Esegue un comando UFW o iptables con subprocess e gestisce i permessi.
       Se visualizza_scrollabile è True, usa la finestra separata per l'output.
    """
    
    comando_completo = f"sudo {comando}"
    
    try:
        risultato = subprocess.run(comando_completo, shell=True, check=True, 
                                   capture_output=True, text=True)
        
        output_stdout = risultato.stdout.strip()
        
        if visualizza_scrollabile:
            # Se è richiesta la visualizzazione scrollabile (es. per ufw status)
            visualizza_output_scrollabile(f"Risultato: {comando}", output_stdout)
            # Mostriamo un messaggio breve di successo nella GUI principale
            messagebox.showinfo("Successo", f"Comando '{comando}' eseguito. Aprire la finestra di output.")
        else:
            # Per tutti gli altri comandi brevi (allow, deny, enable, disable, ICMP)
            messagebox.showinfo("Comando Eseguito", 
                                f"Comando: {comando_completo}\n\nRisultato:\n{output_stdout}")

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Errore Esecuzione Comando", 
                             f"Errore nell'esecuzione del comando:\n\n{e.stderr.strip()}")
    except FileNotFoundError:
        messagebox.showerror("Errore", "Assicurati che 'ufw' e 'iptables' siano installati.")

# --- 3. Funzioni associate ai pulsanti GUI (La maggior parte non cambia) ---

def blocca_protocollo():
    """Funzione per l'opzione 1: Blocca Traffico su uno specifico protocollo"""
    porta = simpledialog.askstring("Blocca Protocollo", "Inserisci il PROTOCOLLO (es. 21, 80, o nome come 'ftp') da BLOCCARE:")
    if porta:
        comando = f"ufw deny in {porta}"
        esegui_comando_ufw(comando)

def blocca_tutto():
    """Funzione per l'opzione 2: Blocca Tutto il traffico su tutte le porte"""
    if messagebox.askyesno("Attenzione", "Sei sicuro di voler BLOCCARE TUTTO il traffico IN ENTRATA?"):
        comando = "ufw default deny incoming"
        esegui_comando_ufw(comando)

def accetta_protocollo():
    """Funzione per l'opzione 3: Accetta una connessione su uno specifico protocollo"""
    protocollo = simpledialog.askstring("Accetta Protocollo", "Inserisci il PROTOCOLLO (es. 22, 443, o nome come 'ssh') da CONSENTIRE:")
    if protocollo:
        comando = f"ufw allow {protocollo}"
        esegui_comando_ufw(comando)

def accetta_tutto():
    """Funzione per l'opzione 4: Accetta le connessioni su tutte le porte"""
    if messagebox.askyesno("Attenzione", "Sei sicuro di voler CONSENTIRE TUTTO il traffico IN ENTRATA?"):
        comando = "ufw default allow incoming"
        esegui_comando_ufw(comando)

# --- 4. La funzione 'mostra_status' ora chiama la modalità scrollabile ---

def mostra_status():
    """Funzione per l'opzione 5: Status, usa la visualizzazione scrollabile."""
    comando = "ufw status verbose"
    # Passiamo True al nuovo parametro 'visualizza_scrollabile'
    esegui_comando_ufw(comando, visualizza_scrollabile=True) 

def attiva_firewall():
    """Funzione per l'opzione A: Attiva Firewall ufw"""
    comando = "ufw enable"
    esegui_comando_ufw(comando)

def disattiva_firewall():
    """Funzione per l'opzione D: Disattiva Firewall ufw"""
    if messagebox.askyesno("Attenzione", "Sei sicuro di voler DISATTIVARE il firewall? Questo espone il tuo sistema!"):
        comando = "ufw disable"
        esegui_comando_ufw(comando)

def blocca_icmp():
    """Blocca traffico ICMP (ping) - Opzione Block"""
    comando = "iptables -I INPUT -p icmp --icmp-type echo-request -j DROP"
    esegui_comando_ufw(comando)

def consenti_icmp():
    """Consenti traffico ICMP (ping) - Opzione Allow"""
    comando = "iptables -D INPUT -p icmp --icmp-type echo-request -j DROP"
    esegui_comando_ufw(comando)


# --- Setup della GUI principale (La parte Layout non cambia) ---

def crea_gui():
    """Crea e configura la finestra principale di Tkinter"""
    
    # Finestra principale
    root = tk.Tk()
    root.title("🛡️ UFW Manager GUI (Powered by Python) 💻")
    root.geometry("700x700") # Ho mantenuto la dimensione 700x700
    root.configure(bg="#2c3e50") 

    # Titolo principale
    titolo = tk.Label(root, 
                      text="Gestione Firewall UFW", 
                      font=("Helvetica", 18, "bold"), 
                      fg="#ecf0f1", 
                      bg="#2c3e50")
    titolo.pack(pady=20)

    # --- Frame per le Azioni Principali (1-4) ---
    
    frame_azioni = tk.LabelFrame(root, text=" Azioni Veloce", padx=10, pady=10, 
                                 font=("Helvetica", 12), fg="#ecf0f1", bg="#34495e", borderwidth=2)
    frame_azioni.pack(padx=10, pady=10, fill="x")

    # Bottone 1
    tk.Button(frame_azioni, text="Blocca Protocollo Specifico", command=blocca_protocollo, 
              bg="#7f8c8d", fg="white", font=("Helvetica", 10, "bold")).pack(fill="x", pady=5)

    # Bottone 2
    tk.Button(frame_azioni, text="BLOCCA TUTTO IN ENTRATA", command=blocca_tutto, 
              bg="#7f8c8d", fg="white", font=("Helvetica", 10, "bold")).pack(fill="x", pady=5)
    
    # Bottone 3
    tk.Button(frame_azioni, text="Accetta Protocollo Specifico", command=accetta_protocollo, 
              bg="#7f8c8d", fg="white", font=("Helvetica", 10, "bold")).pack(fill="x", pady=5)

    # Bottone 4
    tk.Button(frame_azioni, text="ACCETTA TUTTO IN ENTRATA", command=accetta_tutto, 
              bg="#7f8c8d", fg="white", font=("Helvetica", 10, "bold")).pack(fill="x", pady=5)
    
    # --- Frame per Attivazione/Disattivazione e Status (A, D, 5) ---
    
    frame_stato = tk.LabelFrame(root, text="Controllo e Stato", padx=10, pady=10, 
                                font=("Helvetica", 12), fg="#ecf0f1", bg="#34495e", borderwidth=2)
    frame_stato.pack(padx=10, pady=10, fill="x")

    # Bottone A
    tk.Button(frame_stato, text="Attiva Firewall UFW", command=attiva_firewall, 
              bg="#7f8c8d", fg="white", font=("Helvetica", 10)).pack(fill="x", pady=5)
    
    # Bottone D
    tk.Button(frame_stato, text="Disattiva Firewall UFW", command=disattiva_firewall, 
              bg="#7f8c8d", fg="white", font=("Helvetica", 10)).pack(fill="x", pady=5)
    
    # Bottone 5 (NOTA: questo ora aprirà una finestra separata)
    tk.Button(frame_stato, text="Mostra Status Dettagliato", command=mostra_status, 
              bg="#7f8c8d", fg="white", font=("Helvetica", 10, "bold")).pack(fill="x", pady=5)
    
    # --- Frame per ICMP (Ping) ---
    
    frame_icmp = tk.LabelFrame(root, text="Gestione ICMP (Ping)", padx=10, pady=10, 
                                 font=("Helvetica", 12), fg="#ecf0f1", bg="#34495e", borderwidth=2)
    frame_icmp.pack(padx=10, pady=10, fill="x")

    # Bottone Block ICMP
    tk.Button(frame_icmp, text="Block. Blocca traffico ICMP (Ping)", command=blocca_icmp, 
              bg="#7f8c8d", fg="white", font=("Helvetica", 10, "bold")).pack(fill="x", pady=5)
    
    # Bottone Allow ICMP
    tk.Button(frame_icmp, text="Allow. Consenti traffico ICMP (Ping)", command=consenti_icmp, 
              bg="#7f8c8d", fg="white", font=("Helvetica", 10)).pack(fill="x", pady=5)

    # Bottone 6 (Exit)
    tk.Button(root, text="Esci", command=root.quit, 
              bg="#7f8c8d", fg="white", font=("Helvetica", 12, "bold")).pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    # Avvia la GUI
    crea_gui()
