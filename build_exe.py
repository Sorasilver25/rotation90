"""
Script pour créer un exécutable Windows du logiciel de rotation d'images
"""
import PyInstaller.__main__
import os

# Chemin du script principal
script_path = 'rotation90.py'

# Options PyInstaller
PyInstaller.__main__.run([
    script_path,
    '--name=Rotation90',
    '--onefile',                    # Un seul fichier exe
    '--windowed',                   # Pas de console (interface graphique uniquement)
    '--icon=feather.ico',           # Icône plume
    '--add-data=feather.ico;.',     # Inclure l'icône dans l'exe
    '--clean',                      # Nettoyer les fichiers temporaires
    '--noconfirm',                  # Ne pas demander de confirmation
])

print("\n" + "="*60)
print(" Exécutable créé avec succès!")
print(" Emplacement: dist/Rotation90.exe")
print("="*60)
