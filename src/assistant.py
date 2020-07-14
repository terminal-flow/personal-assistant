import speech_recognition as sr
import wikipedia
import pyttsx3
import datetime
import os
import random
import subprocess

#startup
def startup():
    assistant_response('Personal assistant initialised')

    #hour = int(datetime.datetime.now().hour)

    #if hour >= 0 and hour < 12:
    #    assistant_response('Good Morning, how may I help')
    #elif hour >= 12 and hour < 18:
    #    assistant_response('Good Afternoon, how may I help')
    #else:
    #    assistant_response('Good Evening, how may I help')

#record audio and return audio as string
def record_audio():
    #record inputted audio
    r = sr.Recognizer() #create a recogniser object

    #open mic and start recording
    with sr.Microphone() as source:
        audio = r.listen(source)

    #recognise speech
    voice = ''
    try:
        voice = r.recognize_google(audio)
        print('You said: ' + voice)
    except sr.UnknownValueError:
        pass
    except sr.requestError as e:
        print('Error Results: ' + e)
    except:
        print('An error occured')
    return voice

#assistant response
def assistant_response(text):
    try:
        #convert text to speech
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice',voices[0].id)
        engine.say(text)
        engine.setProperty('rate',110)
        engine.runAndWait()
        engine.stop()
    except AssertionError:
        pass

#function for wake word
def wake_word(text):
    wake_words = 'Computer'
    wake_words = wake_words.lower()

    text = text.lower()

    #check for wake word
    if text.startswith(wake_words):
        return True
    #get current wake word
    elif text == 'request':
        return wake_words

    return False

#current date
def get_date():
    now = datetime.datetime.now()
    dayNum = str(now.day)
    monthNum = str(now.month)
    yearNum = str(now.year)
    weekName = str(datetime.datetime.today().strftime('%A'))
    monthName = str(datetime.datetime.today().strftime('%B'))

    today_date = 'It\'s ' + weekName + ', ' + dayNum + ' ' + monthName
    return today_date

def get_time():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute

    if minute < 10:
        minute = str(minute)
        minute = '0' + minute

    if hour >= 0 and hour < 12:
        ampm = 'AM'
    else:
        ampm = 'PM'

    if hour >= 13:
        hour = hour - 12

    minute = str(minute)
    hour = str(hour)

    full_time = 'It\'s ' + hour + ' ' + minute + ' ' + ampm
    return full_time

def greeting(text):
    greetings_in = ['hi', 'hello', 'hey', 'morning', 'afternoon', 'evening']

    greetings_out = ['hi', 'hello', 'hi there']

    praise = ['your welcome', 'no problem', 'any time']

    local_request = wake_word('request')
    name = [f'my name is {local_request}', 'i am your personal assistant']

    text_split = text.split()
    for i in range(len(text_split)):
        if text_split[i] in greetings_in:
            #failsafe for only returning for only greetings_in
            if len(text_split) == 1:
                return random.choice(greetings_out)

    if 'thank you' == text or 'cheers' == text or 'thanks' == text:
        return random.choice(praise)

    if ('what is your name' == text or 'what\'s your name' == text or
    'who are you' == text):
        return random.choice(name)

    #if no greeting
    return ''

#break word up into letters with pauses
def get_spelling(text):
    word_list = text.split()
    letter_r = ''

    for i in range(len(word_list)):
        if word_list[i].lower() == 'you' and word_list[i+1].lower() == 'spell':
            try:
                word_list[i+3]
            except IndexError:
                try:
                    spell_word = word_list[i+2]
                    for letter in spell_word:
                        letter_r = letter_r + '. ' + letter
                    return f'{spell_word} is spelled {letter_r}'
                except IndexError:
                    return ''
            return ''
        elif 'spell' in word_list[i+1]:
            return ''

#system commands
def system(command):
    from resources import system_short
    if command == 'system report':
        system_report = system_short.system_report()
        return system_report

    if command == 'mute':
        mute = system_short.mute()
        return mute

    if command == 'unmute':
        unmute = system_short.unmute()
        return unmute

    if command == 'increase volume':
        increase_volume = system_short.increase_volume()
        return increase_volume

    if command == 'decrease volume':
        decrease_volume = system_short.decrease_volume()
        return decrease_volume

    if command == 'sleep':
        sleep = system_short.sleep()
        return sleep

#get wikipedia search words
def get_wiki(text):
    word_list = text.split()

    for i in range(0, len(word_list)):
        if (word_list[i].lower() == 'search' and
        word_list[i+1].lower() == 'wikipedia' and word_list[i+2] == 'for'):
            word_list = str(word_list)
            extra, word_list = word_list.split('for')
            return word_list

#complete math equations
def get_math(text):
    from resources import maths_results
    maths_results = maths_results.math_results(text)
    return maths_results

#make new iNote
def get_inote(text):
    file = open('resources/notes/notes_content.txt', 'w')
    text = text.capitalize()
    file.write(text)
    file.close()

    subprocess.call(['osascript', 'resources/notes/make_inote.applescript'])

    file = open('resources/notes/notes_content.txt', 'w')
    file.write('')
    file.close()

    return 'note added'

#webbroswer commands
def get_site(text, terms= None):
    from resources import site_search
    if text == 'open youtube':
        get_youtube = site_search.get_youtube()
        return get_youtube
    elif text == 'search youtube':
        search_youtube = site_search.search_youtube(terms)
        return search_youtube
    elif text == 'open duckduckgo':
        get_duckduckgo = site_search.get_duckduckgo()
        return get_duckduckgo
    elif text == 'search browser':
        search_browser = site_search.search_browser(terms)
        return search_browser
    elif text == 'open google':
        get_google = site_search.get_google()
        return get_google
    elif text == 'search google':
        search_google = site_search.search_google(terms)
        return search_google
    elif text == 'open bing':
        get_bing = site_search.get_bing()
        return get_bing
    elif text == 'search bing':
        search_bing = site_search.search_bing(terms)
        return search_bing
    else:
        return ''

#search for and open application on system
def get_application(app):
    application_dir = os.listdir('/Applications')
    application_dir1 = os.listdir('/System/Applications')
    application_dir2 = os.listdir('/System/Applications/Utilities')
    for i in range(len(application_dir)):
        application_dir.append(application_dir[i].lower())

    for i in range(len(application_dir1)):
        application_dir.append(application_dir1[i].lower())

    try:
        for i in range(len(application_dir2)):
            application_dir.append(application_dir2[i].lower())
    except:
        pass

    if f'{app}.app' in application_dir and not app.startswith('.'):
        r = f'osascript -e \'tell application "{app}" to activate\''
        result = subprocess.check_output(r, shell= True)
        result = result.decode('UTF-8')

        return 'opening'
    return ''

def main_loop():
    startup()
    local_request = wake_word('request')
    while True:
        text = record_audio()
        text = str(text.lower())
        text_split = text.split()

        response = ''

        if wake_word(text) == True:
            #check for just wake word
            if local_request == text:
                audio_file = 'resources/accept.wav'
                subprocess.call(['afplay', audio_file])
                text = record_audio()
                text = str(text.lower())
                text_split = text.split()
            else:
                text = text.replace(f'{local_request} ', '')

            #check for greetings
            response = greeting(text)

            #check for math questions
            if response == '':
                response = get_math(text)

            if ('quit' == text or 'exit' == text or 'stop' == text):
                response = 'goodbye'
                assistant_response(response)
                exit()

            #check for date
            if (('what is the date' in text or 'what\'s the date' in text) and
            response == ''):
                response = get_date()

            #check for the time
            if (('what is the time' in text or 'what\'s the time' in text) and
            response == ''):
                response = get_time()

            #check spelling
            if 'how do you spell' in text and response == '':
                response = get_spelling(text)

            #system commands
            #system report
            if (('system report' == text or 'system status' == text)
            and response == ''):
                response = system('system report')

            #unmute
            if ('unmute' == text or 'stop mute' == text) and response == '':
                response = system('unmute')

            #mute
            if 'mute' == text and response == '':
                response = system('mute')

            #change volume
            if 'volume' in text and response == '':
                increase = ['volume up', 'increase volume',
                'increase the volume']
                decrease = ['volume down', 'decrease volume',
                'decrease the volume']

                for i in range(len(increase)):
                    if increase[i] in text:
                        response = system('increase volume')

                for i in range(len(decrease)):
                    if decrease[i] in text:
                        response = system('decrease volume')

            #sleep
            if 'sleep' == text and response == '':
                response = system('sleep')
                exit()

            #check wikipedia
            if 'search wikipedia' in text and response == '':
                info = get_wiki(text)
                try:
                    response = wikipedia.summary(info, sentences= 2)
                except ValueError:
                    pass # to little options
                except wikipedia.DisambiguationError:
                    pass # to many options

            #make a new iNote
            if 'make a note' in text and response == '':
                assistant_response('what is your note')
                text = record_audio()
                response = get_inote(text)

            #youtube
            if 'open youtube' in text and response == '':
                response = get_site('open youtube')

            if 'search youtube' in text and response == '':
                for i in range(len(text_split)):
                    if (text_split[i] == 'search' and text_split[i+1] == 'youtube'
                    and text_split[i+2] == 'for'):
                        terms = text_split[i+3:]
                        terms = '+'.join(terms)
                        response = get_site('search youtube', terms= terms)

            #search engines
            #duckduckgo (general)
            if (('open the internet' in text or 'open duckduckgo' in text)
            and response == ''):
                response = get_site('open duckduckgo')

            if (('search for' in text or 'search the internet for' in text)
            and response == ''):
                for i in range(len(text_split)):
                    if text_split[i] == 'search' and text_split[i+1] == 'for':
                        terms = text_split[i+2:]
                        terms = '+'.join(terms)
                        response = get_site('search browser', terms= terms)

            #google
            if 'open google' in text and response == '':
                response = get_site('open google')

            if 'search google for' in text and response == '':
                for i in range(len(text_split)):
                    if (text_split[i] == 'search' and text_split[i+1] == 'google'
                    and text_split[i+2] == 'for'):
                        terms = text_split[i+3:]
                        terms = '+'.join(terms)
                        response = get_site('search google', terms= terms)

            #bing
            if 'open bing' in text and response == '':
                response = get_site('open bing')

            if 'search bing for' in text and response == '':
                for i in range(len(text_split)):
                    if (text_split[i] == 'search' and text_split[i+1] == 'bing'
                    and text_split[i+2] == 'for'):
                        terms = text_split[i+3:]
                        terms = '+'.join(terms)
                        response = get_site('search bing', terms= terms)

            #open applications
            if 'open' in text and response == '':
                for i in range(len(text_split)):
                    if text_split[i] == 'open':
                        app = text_split[i+1:]
                        app = ' '.join(app)
                        response = get_application(app)


            #respond back using audio
            if response == '' or response == None:
                audio_file = 'resources/unsure.wav'
                subprocess.call(['afplay', audio_file])
            else:
                assistant_response(response)

main_loop()