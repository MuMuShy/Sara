import speech_recognition as sr
def Listen():
    print('sara is listening...')
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio=r.listen(source)
    data=""
    #開始語音辨識
    try:
        data=r.recognize_google(audio,language='zh-TW')
        print("you said"+data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return data