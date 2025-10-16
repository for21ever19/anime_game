from PIL import Image, ImageDraw, ImageFont
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRAME_DIR = os.path.join(BASE_DIR, 'Anime_frame')
IMAGES_DIR = os.path.join(BASE_DIR, 'images_processed') # Предполагаю, что картинки в папке 'images'
FONTS_DIR = os.path.join(BASE_DIR, 'fonts')
QUESTIONS_DIR = os.path.join(BASE_DIR, 'questions')

rarity_frames = {
    'S': os.path.join(FRAME_DIR, 'S.Rank.png'),
    'A': os.path.join(FRAME_DIR, 'A.Rank.png'),
    'B': os.path.join(FRAME_DIR, 'B.Rank.png'),
    'C': os.path.join(FRAME_DIR, 'C.Rank.png')
}

def create_card_image(card_data, images_dir, fonts_dir):
    char_filename = card_data['image_path']
    scale = 2

    char_path = os.path.join(images_dir, char_filename) # <--- ИЗМЕНЕНИЕ
    card_width, card_height = 250, 387
    final_card = Image.open(char_path).convert("RGBA").resize((card_width * scale, card_height * scale), Image.Resampling.LANCZOS)
    rarity_key = card_data['rarity']
    frame_path = rarity_frames[rarity_key]
    frame_image = Image.open(frame_path).convert("RGBA").resize((card_width * scale, card_height * scale), Image.Resampling.LANCZOS)

    final_card.paste(frame_image, (0, 0), frame_image)
    
    overlay_height = 80
    overlay = Image.new('RGBA', (card_width * scale, overlay_height * scale), (0, 0, 0, 128))
    final_card.paste(overlay, (0, (card_height - overlay_height) * scale), overlay)
    
    
    draw = ImageDraw.Draw(final_card)
    bebas_font_path = os.path.join(fonts_dir, "BebasNeue.ttf") # <--- ИЗМЕНЕНИЕ
    name_font = ImageFont.truetype(bebas_font_path, 36 * scale)

    roboto_font_path = os.path.join(fonts_dir, "Roboto-Regular.ttf") # <--- ИЗМЕНЕНИЕ
    anime_font = ImageFont.truetype(roboto_font_path, 20 * scale)

    draw.text((15 * scale, 310 * scale), card_data['name'], font=name_font, fill='white')
    draw.text((15 * scale, 350 * scale), card_data['anime'], font=anime_font, fill='white')
    
    rarity_font = ImageFont.truetype(bebas_font_path, 39 * scale) # <--- ИЗМЕНЕНИЕ
    circle_center_x = 33 * scale
    circle_center_y = 22 * scale
    rarity_text = card_data['rarity']
    bbox = draw.textbbox((0, 0), rarity_text, font=rarity_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = circle_center_x - (text_width / 2)
    text_y = circle_center_y - (text_height / 2)
    draw.text((text_x, text_y), rarity_text, font=rarity_font, fill='white')


    final_card = final_card.resize((card_width, card_height), Image.Resampling.LANCZOS)
    
    return final_card


if __name__ == "__main__":
    
    test_card = {
        'rarity': 'A',
        'image_path': 'askeladd2.png',
    'name': 'Askeladd',            
    'anime': 'Vinland Saga'   

    }
    result_image = create_card_image(test_card, images_dir=IMAGES_DIR, fonts_dir=FONTS_DIR) 
    result_image.show()


  