from PIL import ImageTk, Image, ImageDraw, ImageFont

rarity_frames = {
    'S': 'Anime_frame/S.Rank.png', 
    'A': 'Anime_frame/A.Rank.png',
    'B': 'Anime_frame/B.Rank.png',
    'C': 'Anime_frame/C.Rank.png'
}

def create_card_image(card_data):
    char_filename = card_data['image_path']
    scale = 2
    char_path = f"images_processed/{char_filename}"
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
    name_font = ImageFont.truetype("Fonts/BebasNeue.ttf", 36 * scale)
    anime_font = ImageFont.truetype("Fonts/Roboto-Regular.ttf", 20 * scale)
    draw.text((15 * scale, 310 * scale), card_data['name'], font=name_font, fill='white')
    draw.text((15 * scale, 350 * scale), card_data['anime'], font=anime_font, fill='white')
    
    rarity_font = ImageFont.truetype("fonts/BebasNeue.ttf", 39 * scale)
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
    result_image = create_card_image(test_card) 
    result_image.show()


  