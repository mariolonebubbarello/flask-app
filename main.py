import openai
import json
import jyserver.Flask as jsf
from flask import Flask, render_template, request, abort

openai.api_key = "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"
model_engine = 'text-davinci-003'
history = ''
words = 800

def chatgpt(answer):
    global history
    if len(history) + words > 4097:
        return 'limite della lunghezza della chat raggiunto. Riaggiornare la pagina e crearne una nuova'
    else:
        while True:
            try:
                #history.replace('\n', '')
                prompt = history + 'Io ti dico: ' + answer + '. '
                #prompt.replace('\n', ' ')

                completion = openai.Completion.create(
                    engine = model_engine,
                    prompt = prompt,
                    max_tokens = words,
                    stop = None,
                    temperature = 0.5
                )

                response = completion.choices[0].text

                accepted = False
                
                for char in response:
                    if char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?()/&%$£*àòèé^+':
                        accepted = True

                if response.isspace() == True or accepted == False:
                    pass
                else:
                    #response.replace('\n', ' ')
                    history = prompt
                    history = history + 'Tu hai detto: ' + response + '.'
                    response = response.replace('Tu hai detto:', '')
                    response = response.strip()
                    response = response.replace('\n', '<br>')
                    response = response.replace('\t', '&emsp;')

                    return response
            except Exception:
                pass

app = Flask(__name__, static_folder='static')
@jsf.use(app)

class App:
    def __init__(self):
        self.let = 0
    def login(self):
        self.input = self.js.document.getElementById("login")
        if self.input.value == 'ciao':
            self.js.console.log('ciao')
    def text(self, answer):
        self.response = chatgpt(answer)
        self.js.aiMessage(self.response)
        #self.js.document.getElementById('chat').innerHTML = self.js.document.getElementById('chat').innerHTML + self.response
    def refresh(self):
        global history
        history = ''
    

@app.route('/')
def index():
    file = open('data.json', 'r')
    data = json.load(file)
    text = json.dumps(data)
    file.close()
    file = open('data.json', 'w')
    file.write(text)
    file.close()
    return App.render(render_template('./login/index.html'))

@app.route('/chat', methods = ['POST', 'GET'])
def chat():
    if request.method == 'POST':
        file = open('data.json', 'r')
        data = json.load(file)
        text = json.dumps(data)
        file.close()
        password = request.form['password']
        user_agent = request.user_agent.string
        device_type = user_agent.split(')')
        device_type = device_type[0]
        device_type = device_type.split(';')
        device_type = device_type[-1]
        device_type = device_type.strip()
        #mac_address = uuid.getnode()
        #mac_address = ':'.join(['{:02x}'.format((mac_address >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])

        if password in data:
            if data[password] == '':
                file = open('data.json', 'w')
                data[password] = device_type
                file.write(json.dumps(data))
                file.close()
                return App.render(render_template('./chat/index.html'))
            else:
                if data[password] == device_type:
                    file = open('data.json', 'w')
                    file.write(text)
                    file.close()
                    return App.render(render_template('./chat/index.html'))
                else:
                    file = open('data.json', 'w')
                    file.write(text)
                    file.close()
                    abort(404)
        else:
            file = open('data.json', 'w')
            file.write(text)
            file.close()
            return abort(404)
            """
            enter = True

            for i in data:
                if data[i] == request.form['password']:
                    enter = False

            if enter == True:
                data.update({mac_address: request.form['password']})
                return App.render(render_template('./chat/index.html'))
            else:
                return abort(404)
            """
    else:
        file = open('data.json', 'r')
        data = json.load(file)
        text = json.dumps(data)
        file.close()
        file = open('data.json', 'w')
        file.write(text)
        file.close()
        return abort(404)
        
    

if __name__ == '__main__':
    app.run()