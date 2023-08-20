import io
import ffmpeg
import json
import requests
from PIL import Image
import numpy as np
import pyttsx4
from moviepy.editor import *
 # ceci est les import langchain pour gerer la gestion avec les prompts et memoire
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import SerpAPIWrapper
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
import os
import time
import pyrebase
import json
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager as CM
import threading 
from elevenlabs import generate, play, save
from elevenlabs import set_api_key
set_api_key("")

def startGenerateVideo(message, cara, mood , audience, idtitle):
    endpoint = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": "Bearer "}
    api_key = "sk-"
    os.environ['OPENAI_API_KEY'] = "sk-"

    question1a_template = PromptTemplate(
        input_variables = ['message' , 'cara' , 'mood', 'audience'],   
        template="Write an original story of 500 characters, with a captivating plot and an unexpected conclusion. The story should really convey the following message: {message}. The story should include the following character traits: {cara},  and have a marked mood: {mood}. Do not include the words of the mood in the text of the story. the target audience is : {audience} but you do not  include the word of the audience in the story but keep in mind that the target audience.  You need to finish your sentence with a conclusion of your sentence.")


    listhistoire_template = PromptTemplate(
        input_variables = ['histoire'], 
        template = "Based on the provided story, suggest 10 consecutive action ideas. For each action idea, ensure to include specific aspects about the design, characteristics of the story, and other relevant details. Reiterate these essential details for every action idea. Present them in a numbered list: {histoire}.")

    

    img_template = PromptTemplate(
        input_variables = ['listhistoire', 'numberidea'], 
        template = "You are an expert in prompt creation and imagery for books. Based on the provided story, can you craft a concise prompt for a single situation to generate a text-to-image representation of the story's beginning? Use only common nouns, and provide detailed descriptions of physical appearances and geography. From the following list of ideas: {listhistoire}, use only the {numberidea}th idea.")

   
    question1_memory = ConversationBufferMemory(input_key="message" ,  memory_key='chat_history' )
    histoire_memory = ConversationBufferMemory(input_key='histoire', memory_key='chat_history')
    listhistoire_memory = ConversationBufferMemory(input_key='histoire', memory_key='chat_history')
    img_memory = ConversationBufferMemory(input_key='listhistoire', memory_key='chat_history')

    llm = OpenAI(temperature=0.9) 
    question1a_chain = LLMChain(llm=llm, prompt=question1a_template, verbose=True, output_key='histoire', memory=question1_memory)
   
    listhistoire_chain = LLMChain(llm=llm, prompt=listhistoire_template, verbose=True, output_key='listhistoire', memory=histoire_memory)
    img_chain = LLMChain(llm=llm, prompt=img_template, verbose=True, output_key='img_description', memory=img_memory)


    message = str(message)
    cara = str(cara)
    mood = str(mood)
    audience = str(audience)
    histoire = question1a_chain.run(message=""+message, cara=""+cara, mood=""+mood, audience=""+audience)
    print(histoire)

    listhistoire = listhistoire_chain.run(histoire)
    
    
    img_descriptions = []

    for i in range(10):
        valuee = str(i + 1)
        img_description = img_chain.run(listhistoire=listhistoire, numberidea=valuee)
        img_descriptions.append(img_description)
        print(f"img{i + 1} : {img_description}")
        

    payloads = []
    
    for description in img_descriptions:
        valX =  {"inputs": ""+description}
        payloads.append(valX)
    print("Payload : done")
    responses = []
    for payload in payloads:
        responses.append(requests.post(endpoint, headers=headers, json=payload))
    print("Response : done")

    ii = 0
    for response in responses:
        if(response is not None ):
            img = Image.open(io.BytesIO(response.content))
            varText = "myimage"+str(ii)+".npy"
            np.save(varText, np.asarray(img))
            varText2 =  "img"+str(ii)+".png"
            img.save(varText2, 'PNG')
        print("Now in : " + str(ii))
        ii = ii + 1
        

  



    # engine = pyttsx4.init()

    # rate = engine.getProperty('rate')   # getting details of current speaking rate
    # print (rate)                        #printing current voice rate
    # engine.setProperty('rate', 125)     # setting up new voice rate
    # voices = engine.getProperty('voices')

    # volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    # print (volume)                          #printing current volume level
    # engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
    # voices = engine.getProperty('voices')       #getting details of current voice
    #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    # engine.setProperty('voice', voices[38].id)   #changing index, changes voices. 1 for female

    
    # We can use file extension as mp3 and wav, both will work
    # engine.save_to_file(histoire, 'speech.mp3')
    
    audio = generate(
        text=histoire,
        voice="Bella",
        model='eleven_monolingual_v1'
        )
    
    save(audio,'speech.mp3')

    # play(audio)
    # Wait until above command is not finished.
    # engine.runAndWait()

    img_1 = ImageClip("img1.png")
    img_2 = ImageClip("img2.png")
    img_3 = ImageClip("img3.png")
    img_4 = ImageClip("img4.png")
    img_5 = ImageClip("img5.png")
    img_6 = ImageClip("img6.png")
    img_7 = ImageClip("img7.png")
    img_8 = ImageClip("img8.png")
    img_9 = ImageClip("img9.png")
    img_10 = ImageClip("img10.png")


    audio = AudioFileClip("speech.mp3")

    dureemp = ffmpeg.probe('speech.mp3')['format']['duration']
    timing = float(dureemp) / 10.0
    print(dureemp)
    print(timing)

    list_of_image = {
        img_1.set_duration(timing),
        img_2.set_duration(timing),
        img_3.set_duration(timing),
        img_4.set_duration(timing),
        img_5.set_duration(timing),
        img_6.set_duration(timing),
        img_7.set_duration(timing),
        img_8.set_duration(timing),
        img_9.set_duration(timing),
        img_10.set_duration(timing),
   

    }


    final_video = concatenate_videoclips(list_of_image , method="compose")
    final_video.audio = audio.subclip(0, final_video.duration)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    titleF = idtitle+".mp4"
    final_video.write_videofile(titleF, fps=30)
    
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()

    # Chemin du fichier vidéo sur votre machine
    local_video_path = idtitle+".mp4"

    # Chemin où vous souhaitez stocker le fichier vidéo dans Firebase Storage
    firebase_storage_path = "videos/"+idtitle+".mp4"

    # Télécharger la vidéo
    storage.child(firebase_storage_path).put(local_video_path)

    download_url = storage.child(firebase_storage_path).get_url(None)

    print(f"Video uploaded to {firebase_storage_path} in Firebase Storage.")
    print(f"Download URL: {download_url}")
    print("id : " + idtitle)
    idtitle = int(idtitle)-1
    db.child("Dialogue").child(idtitle).update({"url": download_url})
    
    



config = {
       #config
    }

firebase = pyrebase.initialize_app(config)
db = firebase.database()



def check_new_values():
    last_known_data = db.child("Dialogue").get().val()
    while True:
        time.sleep(3)  # Attendre 3 secondes
        current_data = db.child("Dialogue").get().val()
        print("noc : "+ str(current_data))
        print("-")
        print("no l : "+  str(last_known_data))
        print("-")
        number_of_fields = len(current_data)  # Ligne ajoutée pour récupérer le nombre de champs

        print("Nombre de champs : " + str(number_of_fields))  # Afficher le nombre de champs
        print("-")


        if current_data != last_known_data:
            current_data.pop(0)
            last_known_data.pop(0)

            formatted_datac = ', '.join(map(str, current_data))
            formatted_datal = ', '.join(map(str, last_known_data))
            
            print("GO")
            if isinstance(current_data, dict) and isinstance(last_known_data, dict):
                new_entries = set(current_data.keys()) - set(last_known_data.keys())
            else:
                # Convertir directement en ensemble si ce sont des listes
                new_entries = set(formatted_datac) - set(formatted_datal)
                
            print("okk")
            print("okk")
            print("newentire : " + str(new_entries))
            print("okk22 : " + formatted_datac)

            value_text = formatted_datac[number_of_fields]
            print("ok23 : " + value_text)  # Affiche: bn

            value_id = formatted_datac[number_of_fields]

            print("ok22" + value_id)  # Affiche: bss
            formatted_datac = "["+formatted_datac+"]"
            # Remplacer les simples quotes par des doubles quotes pour le format JSON
            formatted_datac = formatted_datac.replace("'", '"')

            # Convertir le string en liste de dictionnaires
            data_list = json.loads(formatted_datac)
            print(len(data_list))
            # Récupérer la dernière valeur de 'text'
            last_message_value = data_list[((len(data_list)-1))]['message']
            last_cara_value = data_list[((len(data_list)-1))]['cara']
            last_mood_value = data_list[((len(data_list)-1))]['mood']
            last_audience_value = data_list[((len(data_list)-1))]['audience']

            print(last_message_value)
            startGenerateVideo(str(last_message_value), str(last_cara_value), str(last_mood_value), str(last_audience_value), str(number_of_fields))
         
            last_known_data = current_data
            last_known_data = db.child("Dialogue").get().val()



# Démarrer le thread pour vérifier les nouvelles valeurs
threading.Thread(target=check_new_values).start()
