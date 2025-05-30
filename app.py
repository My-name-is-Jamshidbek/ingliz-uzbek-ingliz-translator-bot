import os
from datetime import datetime
from aiogram import types
from aiogram.types import InputFile

from loader import dp
from config import ADMIN_ID
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from states import User,Reklama_audio,Reklama_fayl as Reklama_file,Reklama_gif,Reklama_video,Reklama_photo
from loader import bot
from aiogram.dispatcher import FSMContext
from replybuttons import keyboard_kontakt, keyboard_admin_menu_1,keyboard_admin_rozibolish,keyboard_user_menu_1
from inlinebuttons import keyboard_admin_menu_2
from baza import baseadd, basereturnlen, basereturnids
from translator import translator_text, photo_text, speach_text, word_audio
import time
#start
@dp.message_handler(CommandStart())
async def start(message:types.Message):
    if str(message.from_user.id) == str(ADMIN_ID):
        await message.answer('salomadmin botga hush kelibsiz!', reply_markup=keyboard_admin_menu_1, )
    else:
        await message.answer(f"Salom {message.from_user.full_name} botga hush kelibsiz!\nBot ishlashi uchun "
                             f"kontaktingizni ulashing!!",reply_markup=keyboard_kontakt)
        await User.user_contact.set()


#royxatdan otish
@dp.message_handler(state=User.user_contact,content_types=types.ContentType.CONTACT)
async def sendcontact(message:types.Message,state:FSMContext):
    try:
        ba = message.values
        full_name = message.contact.full_name#str(ba['contact']["first_name"]+ba['contact']["last_name"])
        user_id = message.from_user.id#str(ba['contact']["user_id"])
        tel_number = message.contact.phone_number#str(ba['contact']['phone_number'])
        baseadd(user_id,full_name,user_id,tel_number)
        await state.finish()
        await bot.send_message(user_id,text='Text, Voice, Photo jo\'natishingiz mumkin',
                               reply_markup=keyboard_user_menu_1)
    except:
        await state.finish()
        await bot.send_message(user_id, text='Text, Voice, Photo jo\'natishingiz mumkin',
                               reply_markup=keyboard_user_menu_1)


#reklama
#foto

@dp.message_handler(state=Reklama_photo.reklama_fayl_nomi,content_types=types.ContentType.PHOTO)
async def Reklama_photo_fayl_nomi(message:types.input_media.InputMediaPhoto,state:FSMContext):
    ba = message.values
    msgid = message.values["message_id"]
    userid = ba['from']['id']
    msg = await bot.send_message(userid,text='Qabul qilindi izohni kiritishingiz mumkin:')
    await Reklama_photo.reklama_text_matni.set()
    await state.update_data(reklama_fayl_nomi=str(ba['photo'][-1]["file_id"]),d2=msgid,d3=msg.message_id)

@dp.message_handler(state=Reklama_photo.reklama_text_matni,content_types=types.ContentType.TEXT)
async def Reklama_photo_text_matni(message:types.Message,state:FSMContext):
    ba = message.text
    msgid = message.message_id
    userid = message.from_user.id
    msg = await bot.send_message(userid,text=str('Reklama barcha foydalanauvchilarga yuboriladi. \nFoydalanuvchilar soni:'+str(basereturnlen())),reply_markup=keyboard_admin_rozibolish)
    await Reklama_photo.reklama_berish.set()
    await state.update_data(reklama_text_matni=ba,d4=msgid,d5=msg.message_id)

@dp.message_handler(state=Reklama_photo.reklama_berish,content_types=types.ContentType.TEXT)
async def Reklama_photo_berish(message:types.Message,state:FSMContext):
    ba = message.text
    msgid = message.message_id
    if str(message.from_user.id) == str(ADMIN_ID):
        if ba == 'Tasdiqlash':
            data = await state.get_data()
            rfn = data.get('reklama_fayl_nomi')
            text = data.get('reklama_text_matni')
            d1=data.get('d1')
            d2=data.get('d2')
            d3=data.get('d3')
            d4=data.get('d4')
            d5=data.get('d5')
            for id in (d1,d2,d3,d4,d5,msgid):
                try:await bot.delete_message(chat_id=message.from_user.id,message_id=id)
                except:pass
            await state.finish()
            b = basereturnids()
            yuborildi = 0
            xatoliklar = 0
            for user_id in b:
                try:
                    await bot.send_photo(chat_id=user_id, photo=rfn, caption=text)
                    yuborildi += 1
                except:
                    xatoliklar += 1
            await message.answer(f"yuborildi: {yuborildi}\nxatoliklar: {xatoliklar}",reply_markup=keyboard_admin_menu_1)
        else:
            await message.answer('Reklama bekor qilindi!')
    else:
        await message.answer('admin @mal_un')


#video

@dp.message_handler(state=Reklama_video.reklama_fayl_nomi,content_types=types.ContentType.VIDEO)
async def Reklama_video_fayl_nomi(message:types.Message,state:FSMContext):
    name = message.video.file_id
    ba = message.message_id
    userid = message.from_user.id
    msg = await bot.send_message(userid,text='Qabul qilindi izohni kiritishingiz mumkin:')
    await Reklama_video.reklama_text_matni.set()
    await state.update_data(reklama_fayl_nomi=name,d2=ba,d3=msg.message_id)

@dp.message_handler(state=Reklama_video.reklama_text_matni,content_types=types.ContentType.TEXT)
async def Reklama_video_text_matni(message:types.Message,state:FSMContext):
    ba = message.text
    msgid = message.message_id
    userid = message.from_user.id
    msg = await bot.send_message(userid,text=str('Reklama barcha foydalanauvchilarga yuboriladi. \nFoydalanuvchilar soni:'+str(basereturnlen())),reply_markup=keyboard_admin_rozibolish)
    await Reklama_video.reklama_berish.set()
    await state.update_data(reklama_text_matni=ba,d4=msgid,d5=msg.message_id)

@dp.message_handler(state=Reklama_video.reklama_berish,content_types=types.ContentType.TEXT)
async def Reklama_video_berish(message:types.Message,state:FSMContext):
    ba = message.text
    msgid = message.message_id
    if str(message.from_user.id) == str(ADMIN_ID):
        if ba == 'Tasdiqlash':
            data = await state.get_data()
            rfn = data.get('reklama_fayl_nomi')
            text = data.get('reklama_text_matni')
            d1=data.get('d1')
            d2=data.get('d2')
            d3=data.get('d3')
            d4=data.get('d4')
            d5=data.get('d5')
            for id in (d1,d2,d3,d4,d5,msgid):
                try:await bot.delete_message(chat_id=message.from_user.id,message_id=id)
                except:pass
            await state.finish()
            b = basereturnids()
            yuborildi = 0
            xatoliklar = 0
            for user_id in b:
                try:
                    await bot.send_video(chat_id=user_id, video=rfn, caption=text)
                    yuborildi += 1
                except:
                    xatoliklar += 1
            await message.answer(f"yuborildi: {yuborildi}\nxatoliklar: {xatoliklar}",reply_markup=keyboard_admin_menu_1)
        else:
            await message.answer('Reklama bekor qilindi!')
    else:
        await message.answer('admin @mal_un')

#gif

@dp.message_handler(state=Reklama_gif.reklama_fayl_nomi,content_types=types.ContentType.ANIMATION)
async def Reklama_gif_fayl_nomi(message:types.Message,state:FSMContext):
    ba = message.animation.file_id
    msgid = message.message_id
    userid = message.from_user.id
    msg = await bot.send_message(userid,text='Qabul qilindi izohni kiritishingiz mumkin:')
    await Reklama_gif.reklama_text_matni.set()
    await state.update_data(reklama_fayl_nomi=str(ba),d2=msgid,d3=msg.message_id)

@dp.message_handler(state=Reklama_gif.reklama_text_matni,content_types=types.ContentType.TEXT)
async def Reklama_gif_text_matni(message:types.Message,state:FSMContext):
    ba = message.text
    msgid = message.message_id
    userid = message.from_user.id
    msg = await bot.send_message(userid,text=str('Reklama barcha foydalanauvchilarga yuboriladi. \nFoydalanuvchilar soni:'+str(basereturnlen())),reply_markup=keyboard_admin_rozibolish)
    await Reklama_gif.reklama_berish.set()
    await state.update_data(reklama_text_matni=ba,d4=msgid,d5=msg.message_id)

@dp.message_handler(state=Reklama_gif.reklama_berish,content_types=types.ContentType.TEXT)
async def Reklama_gif_berish(message:types.Message,state:FSMContext):
    ba = message.text
    msgid = message.message_id
    if str(message.from_user.id) == str(ADMIN_ID):
        if ba == 'Tasdiqlash':
            data = await state.get_data()
            rfn = data.get('reklama_fayl_nomi')
            text = data.get('reklama_text_matni')
            d1=data.get('d1')
            d2=data.get('d2')
            d3=data.get('d3')
            d4=data.get('d4')
            d5=data.get('d5')
            for id in (d1,d2,d3,d4,d5,msgid):
                try:await bot.delete_message(chat_id=message.from_user.id,message_id=id)
                except:pass
            await state.finish()
            b = basereturnids()
            yuborildi = 0
            xatoliklar = 0
            for user_id in b:
                try:
                    await bot.send_animation(chat_id=user_id, animation=rfn, caption=text)
                    yuborildi += 1
                except:
                    xatoliklar += 1
            await message.answer(f"yuborildi: {yuborildi}\nxatoliklar: {xatoliklar}",reply_markup=keyboard_admin_menu_1)
        else:
            await message.answer('Reklama bekor qilindi!')
    else:
        await message.answer('admin @mal_un')

#yordam
@dp.message_handler(CommandHelp())
async def els(message:types.Message):
    await message.answer(f"Salom bu tarjimon bot bu bot @mal_un tomonidan yaratilgan botdan foydalanish uchun shunchaki matnni jonatish kifoya!\nAgar matn ingliz tilida bo\'lsa uni ozbaek tiliga agar matn o'zbek tilida bo\'lsa ingliz tiliga tarjima qiladi.")

#admin menu 2 reklama
@dp.callback_query_handler(text_contains='reklama_')
async def reklama(call: types.callback_query,state:FSMContext):
    try:
        if call.data and call.data.startswith("reklama_foto"):
            msg = await call.message.answer('Reklama rasmini kiritishingiz mumkin:')
            await Reklama_photo.reklama_fayl_nomi.set()
            await state.update_data(d1=msg.id)
        elif call.data and call.data.startswith("reklama_audio"):
            msg = await call.message.answer('Reklama audiosini kiritishingiz mumkin:')
            await Reklama_audio.reklama_fayl_nomi.set()
            await state.update_data(d1=msg.id)
        elif call.data and call.data.startswith("reklama_gif"):
            msg = await call.message.answer('Reklama gifini kiritishingiz mumkin:')
            await Reklama_gif.reklama_fayl_nomi.set()
            await state.update_data(d1=msg.id)
        elif call.data and call.data.startswith("reklama_video"):
            msg = await call.message.answer('Reklama videosini kiritishingiz mumkin:')
            await Reklama_video.reklama_fayl_nomi.set()
            await state.update_data(d1=msg.id)
        elif call.data and call.data.startswith("reklama_fayl"):
            msg = await call.message.answer('Reklama faylini kiritishingiz mumkin:')
            await Reklama_file.reklama_fayl_nomi.set()
            await state.update_data(d1=msg.id)
    except:pass



#qolgan matnlar
@dp.message_handler(content_types=[types.ContentType.TEXT, types.ContentType.PHOTO, types.ContentType.VOICE])
async def els(m:types.Message):
    text = False
    try:
        if m.voice:
            file_id = m.voice.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            await bot.download_file(file_path, "data/voices/"+str(file_id)+".mp3")
            time.sleep(5)
            text = speach_text("data/voices/"+str(file_id)+".mp3",m.from_user.id)
        elif m.text:
            if str(m.from_user.id) == str(ADMIN_ID) and m.text == 'Reklama berish':
                await m.answer('salomadmin botga hush kelibsiz!', reply_markup=keyboard_admin_menu_2, )
            elif m.text == 'Reklama berish':
                await m.answer('admin @mal_un')
            elif m.text == '👨‍💻Dasturchi malumoti👨‍💻':
                month = 12
                day = 29
                year = 2003
                year_now = datetime.now().year
                month_now = datetime.now().month
                day_now = datetime.now().day
                datetime_now = datetime.strptime(f"{year_now}/{month_now}/{day_now}", '%Y/%m/%d')  # datetime.now()
                datetime_ = datetime.strptime(f"{year}/{month}/{day}", '%Y/%m/%d')
                old = datetime_now-datetime_
                await m.answer(text=f"ism: Jamshidbek\n"
                                    f"familiya: Ollanazarov\n"
                                    f"yoshi: {old.days // 365} yil {old.days % 365} kun.\n"
                                    f"ma\'lumoti: Tugallanmagan oliy\n"
                                    f"username: @mal_un\n"
                                    f"o\'qish joyi:TATU\n"
                                    f"Telegram tarmog\'idagi loyihalar:\n"
                                    f"@Uz_Translate_En_Bot\n"
                                    f"@talk_mate_bot\n"
                                    f"@UBTUITCurriculumBot\n"
                                    f"@tarjimon_ingliz_uzbek_ingliz_bot\n"
                                    f"@download_youtube_download_bot\n"
                                    f"@ramazon_vaqtlari_uzb_bot\n"
                                    f"@WIKI_SEARCH_UZ_MAL_BOT\n"
                                    f"@IMLO_TEST_UZB_BOT")
            else:
                text = m.text
        elif m.photo:
            file_id = m.photo[0].file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            await bot.download_file(file_path, "data/photos/" + str(file_id) + ".jpg")
            time.sleep(5)
            text = photo_text("data/photos/" + str(file_id) + ".jpg")
    except Exception as e:
        print(e)
        text = "Message not found!!"
    if text:
        text = translator_text(text)
        if 'uz_en' == text['type']:
            try:
                voice1 = word_audio(text['text'], t=1)
                voice = InputFile(voice1)
                await m.reply_voice(voice=voice, caption=text['text'])
            except Exception as e:
                await m.reply(text['text'], reply_markup=keyboard_user_menu_1)
                print(e)
        else:
            try:
                voice1 = word_audio(m.text, t=0)
                voice = InputFile(voice1)
                await m.reply_voice(voice=voice, caption=text['text'])
            except Exception as e:
                await m.reply(text['text'], reply_markup=keyboard_user_menu_1)
                print(e)
        os.remove(voice1)