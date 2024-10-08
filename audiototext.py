import tkinter as tk
from tkinter import filedialog, messagebox
import speech_recognition as sr

# Fonction pour la reconnaissance vocale à partir du microphone
def mic_to_text():
    language = language_var.get()  # Récupère la langue sélectionnée
    recognizer = sr.Recognizer()  # Crée un objet Recognizer pour la reconnaissance vocale
    
    try:
        with sr.Microphone() as source:  # Utilise le microphone comme source audio
            print("Ajustement pour le bruit ambiant...")  # Ajuste pour le bruit ambiant
            recognizer.adjust_for_ambient_noise(source, duration=5)  # Ajuste la sensibilité
            print("Écoutez, parlez dans le micro...")  # Invite l'utilisateur à parler
            audio = recognizer.listen(source, timeout=10)  # Écoute l'audio du microphone
            text = recognizer.recognize_google(audio, language=language)  # Reconnaît le texte à partir de l'audio
            result_text.delete(1.0, tk.END)  # Efface le texte précédent dans la zone de résultat
            result_text.insert(tk.END, text)  # Affiche le texte reconnu
            save_to_file(text, "mic_to_text.txt")  # Sauvegarde le texte reconnu dans un fichier
    except Exception as e:
        messagebox.showerror("Erreur", str(e))  # Affiche une erreur en cas d'exception

# Fonction pour la reconnaissance vocale à partir d'un fichier
def file_to_text():
    language = language_var.get()  # Récupère la langue sélectionnée
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3")])  # Ouvre un dialogue pour choisir un fichier audio
    
    if file_path:  # Si un fichier a été sélectionné
        recognizer = sr.Recognizer()  # Crée un objet Recognizer pour la reconnaissance vocale
        with sr.AudioFile(file_path) as source:  # Utilise le fichier audio comme source
            audio = recognizer.record(source)  # Enregistre l'audio du fichier
            try:
                text = recognizer.recognize_google(audio, language=language)  # Reconnaît le texte à partir de l'audio
                result_text.delete(1.0, tk.END)  # Efface le texte précédent dans la zone de résultat
                result_text.insert(tk.END, text)  # Affiche le texte reconnu
                save_to_file(text, "audio_file_to_text.txt")  # Sauvegarde le texte reconnu dans un fichier
            except Exception as e:
                messagebox.showerror("Erreur", str(e))  # Affiche une erreur en cas d'exception

# Fonction pour sauvegarder le texte reconnu dans un fichier
def save_to_file(text, filename):
    with open(filename, "w") as file:  # Ouvre un fichier en mode écriture
        file.write(text)  # Écrit le texte dans le fichier

# Création de la fenêtre principale
root = tk.Tk()  # Initialise la fenêtre Tkinter
root.title("Application de Reconnaissance Vocale")  # Titre de la fenêtre

# Variable pour la sélection de la langue
language_var = tk.StringVar(value="en-US")  # Valeur par défaut pour la langue

# Création des boutons et des options
tk.Label(root, text="Choisissez la langue:").pack(pady=10)  # Label pour choisir la langue

# Boutons radio pour sélectionner la langue
tk.Radiobutton(root, text="Anglais (en-US)", variable=language_var, value="en-US").pack(anchor=tk.W)
tk.Radiobutton(root, text="Français (fr-FR)", variable=language_var, value="fr-FR").pack(anchor=tk.W)
tk.Radiobutton(root, text="Espagnol (es-ES)", variable=language_var, value="es-ES").pack(anchor=tk.W)

# Boutons pour utiliser le microphone ou un fichier audio
tk.Button(root, text="Utiliser le Microphone", command=mic_to_text).pack(pady=10)
tk.Button(root, text="Utiliser un Fichier Audio", command=file_to_text).pack(pady=10)

# Zone de texte pour afficher le résultat
result_text = tk.Text(root, wrap=tk.WORD, width=50, height=10)  # Crée une zone de texte
result_text.pack(pady=10)  # Ajoute la zone de texte à la fenêtre

# Lancement de l'interface
root.mainloop()  # Démarre la boucle principale de l'interface graphique
