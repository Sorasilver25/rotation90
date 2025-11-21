#!/usr/bin/env python3
"""
Logiciel de rotation automatique d'images
Fait pivoter les images en portrait (90° vers la gauche) pour les mettre en paysage
Supporte: PNG, JPG, JPEG, BMP, GIF, TIFF, WEBP
"""

import os
import sys
from pathlib import Path
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading


class ImageRotator:
    # Extensions d'images supportées
    SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tif', '.webp'}
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Rotation 90° - Images")
        self.window.geometry("600x400")
        self.window.resizable(False, False)
        
        # Définir l'icône de la fenêtre
        try:
            icon_path = self.get_resource_path('feather.ico')
            if os.path.exists(icon_path):
                self.window.iconbitmap(icon_path)
        except:
            pass  # Si l'icône n'est pas trouvée, continuer sans
        
        self.setup_ui()
    
    def get_resource_path(self, relative_path):
        """Obtenir le chemin absolu d'une ressource, fonctionne pour dev et pour exe"""
        try:
            # PyInstaller crée un dossier temp et stocke le chemin dans _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)
        
    def setup_ui(self):
        # Titre
        title = tk.Label(
            self.window,
            text="Rotation automatique d'images",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(
            self.window,
            text="Sélectionnez un dossier contenant des images.\n"
                 "Les images en portrait seront pivotées de 90° (tête à gauche).\n"
                 "Formats: PNG, JPG, JPEG, BMP, GIF, TIFF, WEBP",
            font=("Arial", 10)
        )
        instructions.pack(pady=10)
        
        # Bouton de sélection de dossier
        self.select_btn = tk.Button(
            self.window,
            text="Sélectionner un dossier",
            command=self.select_folder,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.select_btn.pack(pady=20)
        
        # Zone de log
        log_label = tk.Label(self.window, text="Logs:", font=("Arial", 10, "bold"))
        log_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            self.window,
            width=70,
            height=10,
            font=("Courier", 9)
        )
        self.log_text.pack(padx=20, pady=(0, 20))
        
    def log(self, message):
        """Ajoute un message dans la zone de log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.window.update()
        
    def select_folder(self):
        """Ouvre le dialogue de sélection de dossier"""
        folder = filedialog.askdirectory(title="Sélectionner un dossier")
        if folder:
            self.log(f"Dossier sélectionné: {folder}\n")
            # Lancer le traitement dans un thread séparé
            thread = threading.Thread(target=self.process_folder, args=(folder,))
            thread.start()
            
    def process_folder(self, folder_path):
        """Traite toutes les images du dossier"""
        self.select_btn.config(state="disabled")
        
        try:
            # Trouver tous les fichiers d'images supportés
            folder = Path(folder_path)
            image_files = [
                f for f in folder.iterdir() 
                if f.is_file() and f.suffix.lower() in self.SUPPORTED_EXTENSIONS
            ]
            
            if not image_files:
                self.log("⚠ Aucune image trouvée dans ce dossier.")
                messagebox.showwarning("Aucun fichier", "Aucune image supportée trouvée dans ce dossier.")
                return
                
            self.log(f"🪶 {len(image_files)} fichier(s) image trouvé(s)\n")
            
            rotated_count = 0
            skipped_count = 0
            error_count = 0
            
            for image_file in image_files:
                try:
                    # Ouvrir l'image
                    with Image.open(image_file) as img:
                        width, height = img.size
                        
                        # Vérifier si l'image est en portrait
                        if height > width:
                            self.log(f"🪶 Rotation: {image_file.name} ({width}x{height})")
                            
                            # Pivoter de 90° vers la gauche (sens antihoraire)
                            # Cela met la tête à gauche
                            rotated_img = img.rotate(90, expand=True)
                            
                            # Sauvegarder (écrase l'original)
                            # Préserver le format original
                            rotated_img.save(image_file)
                            rotated_count += 1
                            
                        else:
                            self.log(f"⏭ Ignoré (déjà paysage): {image_file.name} ({width}x{height})")
                            skipped_count += 1
                            
                except Exception as e:
                    self.log(f"❌ Erreur avec {image_file.name}: {str(e)}")
                    error_count += 1
                    
            # Résumé
            self.log(f"\n{'='*60}")
            self.log(f"🪶 Traitement terminé!")
            self.log(f"   🪶 Images pivotées: {rotated_count}")
            self.log(f"   • Images ignorées (paysage): {skipped_count}")
            if error_count > 0:
                self.log(f"   • Erreurs: {error_count}")
            self.log(f"{'='*60}\n")
            
            messagebox.showinfo(
                "Terminé",
                f"Traitement terminé!\n\n"
                f"Images pivotées: {rotated_count}\n"
                f"Images ignorées: {skipped_count}\n"
                f"Erreurs: {error_count}"
            )
            
        except Exception as e:
            self.log(f"❌ Erreur générale: {str(e)}")
            messagebox.showerror("Erreur", f"Une erreur s'est produite:\n{str(e)}")
            
        finally:
            self.select_btn.config(state="normal")
            
    def run(self):
        """Lance l'application"""
        self.window.mainloop()


if __name__ == "__main__":
    app = ImageRotator()
    app.run()
