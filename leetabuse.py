"""COMMAND : .leet , .ah"""

from telethon import events
import random, re
from uniborg.util import admin_cmd

MOHATIR = [
    "`Mohatir ki gaand me hook detected`",
    "`Mohatir ki aukat, padi Twitter se tatto pe laat.😂`",
    "`Autohost ki maa ki chut,`"
    "`Viper mod ki maa ka bhosda,`" 
   "`Mohatir ki maa ki sadeli fuddi,`" 
  "`Aur unke admins ki gaand me hathi ka loda`",
    "`Maaaaaaaaaaa ki chhuuuuuuuuuut mohatir Teri maa ki chut pe kutta mutna bhi pasand ni karega , behen ke laude Teri maa ki gaand me sabbal gayi thi jo uss raand ne tujhe hag Diya. 😤😤😤😤😤😤😤😤😤😤😤😤😡😡😡😡😡😡😡😡`",
    "`I bow to these people , for their decision.And Mohatir (Arshalan) you will be raped 😤😤😤😤😤😤😤😤`",
    "`Latest randikhana, 10rs me mohatir ki maa full night, 100rs me uski behen full night, 1000rs me muhatir khud lund chus lega`",
    "`Mohatir ki maaa chude sadko pe aur beti GB road pe`",
     "`Arshalan Beta , Tere to baap ki bhi khulle me gaand mar li , shant hoja aur ghar laut ja , warna me apni aukaat pe aya to ghar see uthwa dunga dono baap beton ko. Aur Teri behen aur ek bhai bhi Haina , unko bhi chor banane ka socha Hai Kya.?`",
      "`Mohtair Randi fir uchhal rahi Hai lagta Hai iss bar apni maa ki chudti hui photo public karwa ke maanga. 😂Baap ki gaand to marwa hi di laude ne`",
       "` Alag alag account se , apni maa chudwane aa jata hai, behenchod langde bohot hua tera me tera mazak ni udaya par bhsodike tu Hai issi layak bhagwan/Allah Kare ki Teri dusri taang ka bhi lund ban Jaye`",
        "`Mohatir ki maaa ka chut phat ke chaar ho gyi kal raat mere kutta aaya aur bola ki kaisi randi ko chodne bhej diya chut phat ke flower ho gya`",
      "`Jis jis autohost ke daaale ki aankh me kutte ke tatte lage Hain aur dimmag me suar ka guh bhara hua Hai unke liye.`", 
        "`Lol lol lol 😂😂😂Kitni gaand marwayega laude mohalund Tere baap ko aaj shaam phone karta hu.`",

]
LEET_STRINGS = [
     "`What the fuck, Abe suar ka mut pike nashe karta Hai Kya ? Ya baap ne illegally koi drugs IV see gaand me de diye?`",
   "`Dobara baap se bakchodi karega to gaand ka tabla bana ke lathh se baja dunga.`", 
   "`One more whore, shaking her ass to get fucked`",
  "`Listen , madarboard, tum jaise jhantu logon ki aukat nhi ki me tum jaise logon se hansi mazak karun.`", 
 "`Randwa panicked 😂😂😂😂`", 
  "`This is an example of what happens when you sell your brain for drugs 😂😂😂😂😂😂😂😂😂😂 `",
   "`  Aaa gya aur ek Chuddak raand ka 😂😂😂😂😂Jiski aur gaand me khaaj ho rahi Hai suno, Chor ke saath dene wala chor. Randi ke sath rehne wala dalla Kehlata Hai. Chahe wo koi aam insaan ho ya mantri 😒`",
   "`Teri ki maaa ka chut phat ke chaar ho gyi kal raat mere kutta aaya aur bola ki kaisi randi ko chodne bhej diya chut phat ke flower ho gya`",
  
]

# ===========================================
                          


@borg.on(admin_cmd("ah ?(.*)"))
async def _(event):
    if event.fwd_from:
         return
    bro = random.randint(0, len(MOHATIR) - 1)    
    input_str = event.pattern_match.group(1)
    reply_text = MOHATIR[bro]
    await event.edit(reply_text)



			  
			  
@borg.on(admin_cmd("leet ?(.*)"))
async def _(event):
    if event.fwd_from:
         return
    bro = random.randint(0, len(LEET_STRINGS) - 1)    
    input_str = event.pattern_match.group(1)
    reply_text = LEET_STRINGS[bro]
    await event.edit(reply_text)
			 