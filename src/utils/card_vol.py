from PIL import Image, ImageDraw, ImageFont
import asyncio

async def draw_card(id):
    back = Image.open('../photos_vol/background.png')
    try:
        vol_photo = Image.open(f'../photos_vol/tg{id}.png')
        vol_photo = vol_photo.resize((200, 200))
    except:
        vol_photo = Image.open(f'../photos_vol/tg0.png')
        vol_photo = vol_photo.resize((200, 200))

    # mask = Image.open('../photos_vol/mask.png')
    # mask = mask.resize((100, 100))

    back.paste(vol_photo, (400, 100))

    font = ImageFont.truetype('../photos_vol/ofont.ru_Arial.ttf', size=28)
    text = "Сергей Орешкин\nРанг:..."

    draw_text = ImageDraw.Draw(back)

    draw_text.text(xy=(back.width / 2, 350),
              text=text, fill=(255, 255, 255), font=font,
              anchor='mm')
    back.show()


asyncio.run(draw_card(1))