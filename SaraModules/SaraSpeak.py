#!/usr/bin/env python
# coding: utf-8

# In[5]:


from pygame import mixer
import tempfile
from gtts import gTTS
def __init__(self):
    mixer.init()
def SpeakChinese(sentence):
    mixer.init()
    with tempfile.NamedTemporaryFile(delete=True)as fp:
        tts=gTTS(text=sentence,lang='zh-TW')
        tts.save("{}.mp3".format(fp.name))
        mixer.music.load("{}.mp3".format(fp.name))
        mixer.music.play()





