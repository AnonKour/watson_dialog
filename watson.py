


import time
import json
import sys
import subprocess
sys.path.append('/home/nao/.local/lib/python2.7/site-packages/bluemix_sdk')
sys.path.append('/home/nao/pysolr-3.6.0')
from watson_developer_cloud import ConversationV1



#new watss_up@mail.com
#workspace= 6bea86f5-c2eb-4682-90f3-cf01bc4d6c8b
#"url": "https://gateway.watsonplatform.net/conversation/api",
#"username": "b9a24ee0-6367-4f16-becd-fb7101ff119f",
#"password": "1X2ZUQfT1sog"


class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self, False)
        self.tts = ALProxy('ALTextToSpeech')
        self.ttsStop = ALProxy('ALTextToSpeech', True) #Create another proxy as wait is blocking if audioout is remote


    def onLoad(self):
        #put initialization code here
        pass

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self,p):
        conversation = ConversationV1(
        ###your credentials#########################
        ###enter new username and password#####
        username='9920a179-8d33-4a24-99fd-128fd52093cb',
        password='Yii4rkIzXaRN',
        version='2016-09-20')
        return_val=0
        # replace with your own workspace_id
        workspace_id = '6bea86f5-c2eb-4682-90f3-cf01bc4d6c8b'

        response = conversation.message(workspace_id=workspace_id, message_input={
        'text': str(p)})

        #self.logger.error(str(response))
        output=response['output']
        text=str(output['text'])
        text=text[3:len(text)-2]

        #extracting greek phrase
        greek_ph=text.decode('unicode-escape')
        self.tts.say(u''.join(greek_ph).encode('utf-8').strip())

        #self.logger.error(greek_ph)
        #final_ans = nltk.word_tokenize(greek_ph)
        #print output['text']
        #print(u'\n'.join(final_ans))

        #print(json.dumps(final_ans, indent=2))
        #watson_input=self.getParameter("watson_input")
        #print(greek_ph)
        #self.tts.post.say(u' '.join(greek_ph))

        intent=response['intents']
        intent_category=intent[0]['intent']
        #self.logger.error(str(intent_category))


        intent_category_gr=intent_category.encode('utf-8') ##intents to greek utf-8

        if intent_category_gr=='κούνα_χέρι':
            entity=response['entities'] ##needs to be translate to utf-8?
            if entity:
                entity_value=entity[0]['value']
                #self.logger.error(type(value))
                entity_value_gr=entity_value.encode('utf-8') ## to greek using 'utf-8'
                if entity_value_gr=='αριστερο':
                    return_val=1
                if entity_value_gr=='δεξι':
                    return_val=2
                if entity_value_gr=='και τα δυο':
                    return_val=3
            else:
                return_val=0
        elif intent_category_gr=='σήκω':
            return_val=4
        elif intent_category_gr=='κάτσε':
            return_val=5
        elif intent_category_gr=='γεια':

            return_val=7
        elif intent_category_gr=='αντιο':

            return_val=8
        elif intent_category_gr=='κράτησε':
            return_val=6
        elif intent_category_gr=='τι_καιρό':
            entity=response['entities']
            if entity:
                entity_value=entity[0]['value']
                #self.logger.error(type(value))
                entity_value_gr=entity_value.encode('utf-8')##translate to greek using utf-8

                #if entity_value_gr=='καιρος':
                    return_val=0
                    #efoson diapistwsw oti to paron entity einai to cities
                    URL_THESS='http://www.accuweather.com/el/gr/thessaloniki/186405/weather-forecast/186405'
                    URL_ATHENS='http://www.accuweather.com/el/gr/athens/182536/weather-forecast/182536'
                    URL_YORK='http://www.accuweather.com/el/us/new-york-ny/10007/weather-forecast/349727'
                    URL_CHANIA='https://www.accuweather.com/el/gr/chania/182654/weather-forecast/182654'

                    #cmd=['wget -q -O- '+URL_ATHENS+' | awk -F\\\' \'/acm_RecentLocationsCarousel\.push/{print $12}\'| head -1']
                    to='στην' ##
                    return_val=0
                    city_name=entity[1]['value']
                    #self.logger.error(stdout)
                    city_name_gr=city_name.encode('utf-8')
                    if city_name_gr=='αθηνα':
                        cmd=['wget -q -O- '+URL_ATHENS+' | awk -F\\\' \'/acm_RecentLocationsCarousel\.push/{print $12}\'| head -1']
                        temp=subprocess.Popen( cmd, shell=True , stdout=subprocess.PIPE ).communicate()[0]
                        temp=temp[0:len(temp)]
                        cmd=['wget -q -O- '+URL_ATHENS+' | awk -F\\\' \'/acm_RecentLocationsCarousel\.push/{print $13}\'| head -1']
                        weather_stat=subprocess.Popen( cmd, shell=True , stdout=subprocess.PIPE ).communicate()[0]
                        weather_stat=weather_stat[9:len(weather_stat)-5]

                    elif city_name_gr=='θεσσαλονικη':
                        cmd=['wget -q -O- '+URL_THESS+' | awk -F\\\' \'/acm_RecentLocationsCarousel\.push/{print $12}\'| head -1']
                        temp=subprocess.Popen( cmd, shell=True , stdout=subprocess.PIPE ).communicate()[0]
                        temp=temp[0:len(temp)]
                        cmd=['wget -q -O- '+URL_THESS+' | awk -F\\\' \'/acm_RecentLocationsCarousel\.push/{print $13}\'| head -1']
                        weather_stat=subprocess.Popen( cmd, shell=True , stdout=subprocess.PIPE ).communicate()[0]
                        weather_stat=weather_stat[9:len(weather_stat)-5]
                    elif city_name_gr=='χανια':
                        to='στα'
                        cmd=['wget -q -O- '+URL_CHANIA+' | awk -F\\\' \'/acm_RecentLocationsCarousel\.push/{print $12}\'| head -1']
                        temp=subprocess.Popen( cmd, shell=True , stdout=subprocess.PIPE ).communicate()[0]
                        temp=temp[0:len(temp)]
                        cmd=['wget -q -O- '+URL_CHANIA+' | awk -F\\\' \'/acm_RecentLocationsCarousel\.push/{print $13}\'| head -1']
                        weather_stat=subprocess.Popen( cmd, shell=True , stdout=subprocess.PIPE ).communicate()[0]
                        weather_stat=weather_stat[9:len(weather_stat)-5]

                     self.tts.say('Ο καιρος  '+to+''+city_name_gr+' ειναι '+str(weather_stat) +' και η θερμοκρασια ειναι '+str(temp)+'c')
        elif intent_category_gr=='τι_μέρα':
            return_val=0
            date=time.ctime() ##get date
            self.tts.say('Σήμερα είναι'+date) ##
        #elif intent_category=='capabilities' or intent_category=='greetings' or intent_category=='Persons_info':
            #self.tts.say(u''.join(greek_ph).encode('utf-8').strip())
        #    return_val=0
        else:
            return_val=0

        #self.tts.say("Hello young Padawan")
        self.onStopped(return_val)
        pass

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
