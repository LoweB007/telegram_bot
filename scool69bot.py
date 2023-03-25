#
#  cd Documents/scool69bot/
# python3 runpyschool69bot.py
import xml.etree.ElementTree as ET
import datetime
import telebot
import time
bot = telebot.TeleBot('')# scool
#bot = telebot.TeleBot('') #
tree = ET.parse('/home/pi/Documents/scool69bot/raspisanie.xml')
tree2 = ET.parse('/home/pi/Documents/scool69bot/homework2.xml')
treead = ET.parse('/home/pi/Documents/scool69bot/admins.xml')
root = tree.getroot()
root2 = tree2.getroot()
treead = ET.parse('/home/pi/Documents/scool69bot/admins.xml')
rootad = treead.getroot()
menulvl = ''
selectedlesson =''
selectedDay =''
lessons =[]
weekDays = ["???????????","???????","?????","???????","???????","???????","???????????"]
for e in root.findall(".//lesson"):
    lessons.append(str(e.attrib)[11:-2])
lessons = list(set(lessons))
keyboard4 = telebot.types.ReplyKeyboardMarkup()
for i in lessons:
    keyboard4.row(i)
keyboard1 = telebot.types.ReplyKeyboardMarkup()
for i in weekDays:
    keyboard1.row(i)
keyboard2 = telebot.types.ReplyKeyboardMarkup()
keyboard2.row('?????????????', '?????????', '???????', '?????????', '?????????')
keyboard3 = telebot.types.ReplyKeyboardMarkup()
keyboard3.row('??')
keyboard3.row('?????')
keyboard3.row('???????? ??')
keyboard5 = telebot.types.ReplyKeyboardMarkup()
keyboard5.row('??')
keyboard5.row('?????')
keyboard6 = telebot.types.ReplyKeyboardMarkup()
keyboard6.row('??')
keyboard6.row('???')
@bot.message_handler(commands=['start'])
@bot.message_handler(content_types=['text'])
def start_message(message):
    global menulvl
    if message.text.lower() == '/start':
        bot.send_message(message.chat.id, '??????,'+message.from_user.first_name+'?????? ???????', reply_markup=ifadmin(message.chat.id,keyboard3,keyboard5))
        menulvl = ''
        bot.send_message(1468282620, message.chat.id, reply_markup=ifadmin(message.chat.id,keyboard3,keyboard5))
    if message.text.lower() == '?????':
        menulvl = '?????'
        bot.send_message(message.chat.id, '?????? ????', reply_markup=keyboard1)
    elif message.text.lower() == '??':
        menulvl = '??'        
        bot.send_message(message.chat.id, '?????? ????', reply_markup=keyboard4)
    elif message.text.lower() == '???????? ??':
        admin = ifadmin(message.chat.id,True,False)
        print(admin)
        if admin == True:
            menulvl = '???????? ?? ??????????'        
            bot.send_message(message.chat.id, '?????? ????', reply_markup=keyboard4)
    else:    
        menulvl = menu(message.text.lower(),message,menulvl)


def menu(messagetext,message,menulvl):
    global selectedDay
    global selectedlesson
    menulvl_temp = menulvl
    if menulvl == '?????':
        menulvl_temp = printDay(message.text.lower(),message,menulvl)
    elif menulvl == '??':
        menulvl_temp = readHomework(message.text.lower(),message,menulvl)

    elif menulvl == '???????? ?? ??????????':
#             ????? ??? ?? ??????? ????? ???????????? ??
        selectedDay = findDays(message.text.lower(),message)
        selectedlesson = message.text.lower()
        Hw1 = root2.findall('./day'+ selectedDay +'/*[@name="'+selectedlesson+'"]')
        print(Hw1)
        if selectedDay == '':
            print(1)
            return menulvl_temp
        elif Hw1==[]:
            print(2)
            
            
            bot.send_message(message.chat.id, '?? ????? ???????? ??: '+selectedDay)
            menulvl_temp = '???????? ?? ?????'
            #menulvl_temp = writeHomework(selectedDay,selectedlesson,message.text.lower(),message)
        else:
            try:
                lastdz = readHomework(message.text.lower(),message,menulvl)
                menulvl_temp = '??????'
                bot.send_message(message.chat.id,'?????? ?????????????',reply_markup=keyboard6)
            except:
                menulvl_temp = '???????? ?? ?????'
    elif menulvl_temp == '??????':
        if message.text.lower() == '??':
            bot.send_message(message.chat.id, '?? ????? ???????? ??: '+selectedDay)
            menulvl_temp = '???????? ?? ?????'
        elif message.text.lower() == '???':
            bot.send_message(message.chat.id,'??????,????????? ??????',reply_markup=ifadmin(message.chat.id,keyboard3,keyboard5))
            return menulvl_temp
    elif menulvl == '???????? ?? ?????':
        menulvl_temp = writeHomework(selectedDay,selectedlesson,message.text.lower(),message)
    return menulvl_temp


def printDay(dayName, message, menulvl):
        for e in root.findall(".//*[@name='"+dayName+"']"):
            for lesson in e:
                bot.send_message(message.chat.id,str(lesson.attrib)[11:-2],reply_markup=ifadmin(message.chat.id,keyboard3,keyboard5))
        return ''


def readHomework(lesson,message,menulvl):
        data = findDays(lesson,message)
        fulldata = printFullDays(lesson,message)
        if data == '':
            return ''
        else:
            Hw = root2.findall('./day'+ data +'/*[@name="'+lesson+'"]')
            for e in root2.findall('./day'+ data +'/*[@name="'+lesson+'"]'):

                bot.send_message(message.chat.id,e.text+" ??  " + fulldata+"  ???????? ?????????????:  "+getAuthor(e), reply_markup=ifadmin(message.chat.id,keyboard3,keyboard5))
                
            if Hw == []:
                bot.send_message(message.chat.id,"?? ????????", reply_markup=ifadmin(message.chat.id,keyboard3,keyboard5))
            return ''


def findDays(lesson,message):
    now = datetime.datetime.now()
    tomorrow = now.isoweekday()+1
    numDay = []
    for e in root.findall(".//*[@lname='"+lesson+"']/.."):
        delta = weekDays.index(str(e.attrib)[10:-2])+1 - tomorrow
        if delta >=0:
            numDay.append(delta)
        else:
            numDay.append(7+delta)
    if numDay == []:
        print(message)
        bot.send_message(message.chat.id,"???? "+lesson+" ?? ??????", reply_markup=ifadmin(message.chat.id,keyboard3,keyboard5))
        return ''
    else:
        nearDay = min(numDay)+1
        delta = datetime.timedelta(days=nearDay)
        nearLessonDate = now+delta
        return (f'{nearLessonDate.day}{nearLessonDate.month}{nearLessonDate.year}')


def printFullDays(lesson,message):
    now = datetime.datetime.now()
    tomorrow = now.isoweekday()+1
    numDay = []
    for e in root.findall(".//*[@lname='"+lesson+"']/.."):
        delta = weekDays.index(str(e.attrib)[10:-2])+1 - tomorrow
        if delta >=0:
            numDay.append(delta)
        else:
            numDay.append(7+delta)
    if numDay == []:
        print(message)
        bot.send_message(message.chat.id,"???? "+lesson+" ?? ??????", reply_markup=ifadmin(message.chat.id,keyboard3,keyboard5))
        return ''
    else:
        nearDay = min(numDay)+1
        delta = datetime.timedelta(days=nearDay)
        nearLessonDate = now+delta
        return (f'{nearLessonDate.day}.{nearLessonDate.month}.{nearLessonDate.year}')


def writeHomework(day,lesson,dzText,message):
    print("write")
    if root2.find("./day"+ day)==None:
        new_day = ET.SubElement(root2.find("."), 'day'+day)
    else:
        new_day = root2.find("./day"+ day)
    if root2.find('./day'+ day +'/*[@name="'+lesson+'"]')==None:
        newlesson = ET.SubElement(new_day, 'lesson')
        newlesson.text = dzText
        newlesson.attrib['name'] = lesson # must be str; cannot be an int
        newlesson.attrib['author'] = message.from_user.first_name # must be str; cannot be an int
        print(newlesson)
    else:
        newhomework = root2.find('./day'+ day +'/*[@name="'+lesson+'"]')
        newhomework.text = dzText

    tree2.write('/home/pi/Documents/scool69bot/homework2.xml')
    bot.send_message(message.chat.id,'????????',reply_markup=ifadmin(message.chat.id,keyboard3,keyboard5))
    return ''


def ifadmin(chatid,admin,noadmin):
    admins = rootad.findall(".//admin")
    for adm in admins:
        if str(chatid) == str(adm.text):
            return admin   
    return noadmin


def getAuthor(e):
    print(e.get('author'))
#     try:
    author = str(e.get('author'))
    if author == 'None':
        return '?????? ???????????? ??????)'
    else:
        return author
#     except:
#         return '?????? ???????????? ??????)'


def main():
    try:
        bot.polling(none_stop=True)
    except: 
        print(datetime.datetime.now())
        time.sleep(5)


if __name__=='__main__':
   main()