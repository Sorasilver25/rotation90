"""
Script pour créer une icône plume élégante et moderne pour l'application
"""
from PIL import Image, ImageDraw
import math

def create_feather_icon():
    """Crée une belle icône de plume avec dégradés et détails"""
    # Créer plusieurs tailles pour l'icône .ico
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = []
    
    for size in sizes:
        # Créer une image avec transparence
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        w, h = size
        scale = w / 256
        
        # Palette de couleurs moderne et élégante (turquoise/cyan vibrant)
        colors = [
            (0, 200, 255, 255),      # Cyan brillant
            (30, 144, 255, 255),     # Bleu profond
            (70, 130, 220, 255),     # Bleu moyen
            (100, 180, 255, 255),    # Bleu clair
            (20, 120, 200, 255),     # Bleu foncé
        ]
        
        stem_color = (10, 60, 120, 255)  # Bleu très foncé pour la tige
        
        # Centre et dimensions
        center_x = w * 0.5
        center_y = h * 0.5
        
        # Dessiner l'ombre légère pour donner du volume
        shadow_offset = max(int(3 * scale), 1)
        
        # Créer une forme de plume plus organique
        # Points de contrôle pour la forme de la plume
        top_x = center_x + w * 0.05
        top_y = h * 0.08
        bottom_x = center_x - w * 0.15
        bottom_y = h * 0.92
        
        # Dessiner les barbes de plume avec effet de dégradé
        num_barbs = max(int(25 * scale), 8)
        
        for i in range(num_barbs):
            progress = i / num_barbs
            
            # Position sur la tige
            y_pos = top_y + (bottom_y - top_y) * progress
            x_stem = top_x + (bottom_x - top_x) * progress
            
            # Longueur variable des barbes (forme ovoïde)
            barb_factor = math.sin(progress * math.pi)
            
            # Côté gauche (barbes longues)
            left_length = w * 0.38 * barb_factor
            x_left = x_stem - left_length
            y_left = y_pos + h * 0.02 * barb_factor
            
            # Couleur variable selon la position
            color_idx = int(progress * (len(colors) - 1))
            barb_color = colors[color_idx]
            
            # Largeur des barbes
            barb_width = max(int(4 * scale * barb_factor), 1)
            
            # Dessiner les barbes gauches (avec courbure)
            draw.line(
                [(x_stem, y_pos), (x_left, y_left)],
                fill=barb_color,
                width=barb_width
            )
            
            # Ajouter des barbes secondaires pour plus de détail
            if i % 2 == 0 and scale > 0.3:
                sub_x = x_stem - left_length * 0.6
                sub_y = y_pos + h * 0.01 * barb_factor
                draw.line(
                    [(x_stem, y_pos), (sub_x, sub_y)],
                    fill=(barb_color[0], barb_color[1], barb_color[2], 180),
                    width=max(barb_width - 1, 1)
                )
            
            # Côté droit (barbes plus courtes)
            right_length = w * 0.25 * barb_factor
            x_right = x_stem + right_length
            y_right = y_pos + h * 0.015 * barb_factor
            
            barb_width_right = max(int(3 * scale * barb_factor), 1)
            
            draw.line(
                [(x_stem, y_pos), (x_right, y_right)],
                fill=barb_color,
                width=barb_width_right
            )
        
        # Dessiner la tige centrale (rachis) avec épaisseur variable
        stem_width_top = max(int(5 * scale), 2)
        stem_width_bottom = max(int(3 * scale), 1)
        
        # Tige en plusieurs segments pour effet de largeur variable
        segments = max(int(20 * scale), 5)
        for i in range(segments):
            progress = i / segments
            y1 = top_y + (bottom_y - top_y) * progress
            x1 = top_x + (bottom_x - top_x) * progress
            y2 = top_y + (bottom_y - top_y) * (progress + 1/segments)
            x2 = top_x + (bottom_x - top_x) * (progress + 1/segments)
            
            width = stem_width_top + (stem_width_bottom - stem_width_top) * progress
            
            draw.line(
                [(x1, y1), (x2, y2)],
                fill=stem_color,
                width=int(width)
            )
        
        # Pointe de la plume (calamus) - forme pointue élégante
        tip_size = max(int(16 * scale), 4)
        tip_points = [
            (top_x, top_y - tip_size * 0.3),
            (top_x - tip_size * 0.4, top_y + tip_size * 0.5),
            (top_x, top_y),
            (top_x + tip_size * 0.4, top_y + tip_size * 0.5),
        ]
        
        draw.polygon(tip_points, fill=stem_color)
        
        # Ajouter un petit cercle brillant pour donner du style
        if scale >= 0.5:
            shine_x = top_x + w * 0.15
            shine_y = top_y + h * 0.2
            shine_radius = max(int(8 * scale), 2)
            draw.ellipse(
                [
                    (shine_x - shine_radius, shine_y - shine_radius),
                    (shine_x + shine_radius, shine_y + shine_radius)
                ],
                fill=(255, 255, 255, 120)
            )
        
        images.append(img)
    
    # Sauvegarder en .ico (multi-tailles)
    images[0].save(
        'feather.ico',
        format='ICO',
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:]
    )
    
    # Sauvegarder aussi en PNG pour utilisation dans l'app
    images[0].save('feather.png', format='PNG')
    
    print("✅ Icône plume élégante créée avec succès!")
    print("   📁 feather.ico (pour l'exécutable)")
    print("   📁 feather.png (pour l'application)")

if __name__ == "__main__":
    create_feather_icon()
