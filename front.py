import requests
'''

This Script is created to be a front-end for Quran-Exams-api

'''
class App :


    def __init__(self) :
        self.token = None
        self.main_url = 'https://quran-exam-api.dis-store.website/'
        
        actions = [self.Login, self.Register ,self.Profile, self.CreateSession]
        user_action = ['1 - login ', '2 - register ', '3 - profile','4 - Enter Questions', '5 - Quit']

        while True :
            for i in user_action :
                print(i)
            u = int(input('CHOOSE >')) - 1
            if u == 4 : 
                break
            else:
                actions[u]()



    def Profile (self) : 
        profile_url = self.main_url
        req = self.MakeRequest('get',profile_url)
        
        self.leaders = req['leaders']
        self.user_info = req['user']

        print(f'[+] Welcome {self.user_info["username"]}')


    def CreateSession (self) : 
        if self.token : 
            session_url = self.main_url + 'session/'
            data = {}

            req = self.MakeRequest('post',session_url,data=data)
            session = req['session']
            self.QuestionSession(session)

    def QuestionSession (self, session) : 
        q_url = self.main_url + f'q/{session}/'
        data = {}
        req = self.MakeRequest('get',q_url)
        
        question_text = req['session']['text']
        choices = req['session']['choices']

        print('[?] Answer Question')
        print(question_text)
        for i in range(0,len(choices)) :
            print(f'{i + 1} ) ',choices[i]) 

        user_answer = int(input('Please Choice The Answer Number : ')) - 1

        data = {
            'user_answer' : choices[user_answer],
            'uuid' : session
        }

        req = self.MakeRequest('post',q_url,data=data)
        
        for key, val in req.items() : 
            print(f'{key} -> {val}')



    def Login (self) : 

        login_url = self.main_url + 'auth/login/'
        email = input('Email : ')
        password = input('Password : ')

        data = {
            'email' : email,
            'password' : password,
        }

        req = self.MakeRequest('post',login_url,data=data)
        self.token = req['token']
        
    def Register (self) : 
        register_url = self.main_url + 'auth/register/'
        username = input('Username : ')
        email = input('Email : ')
        password = input('Password : ')

        data = {
            'username' : username,
            'email' : email,
            'password' : password,
        }

        req = self.MakeRequest('post',register_url,data=data)
        self.token = req['token']


    def MakeRequest(self, method, url,**kwargs) : 

        headers = {}

        if self.token is not None :
            headers['Authorization'] = f'token {self.token}'
        
        if method == "post" : 
            data = kwargs['data']
            req = requests.post(url,headers=headers,data=data)
        else : 
            req = requests.get(url,headers=headers)

        json_file = req.json()

        if req.status_code == 400 :
            print('[!] ERROR')
            for key,val in json_file.items() :
                print(f'{key} : {val}')
        else :
            return json_file
    

if __name__ == '__main__' : 
    App()

