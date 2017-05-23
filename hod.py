from flask import Flask, request, render_template, session, redirect, jsonify, make_response
from xml.dom import minidom

app = Flask("HOD Project")

prompts = {}
current_id = "0"

def preload_choices():
    doc = minidom.parse('data.xml')
    doc = doc.getElementsByTagName('prompts')[0]
    prompt_list = doc.getElementsByTagName("prompt")
    for element in prompt_list:
        t_dict = {}
        t_dict['text'] = element.getElementsByTagName("text")[0].firstChild.nodeValue
        t_dict['choices'] = []
        choices = element.getElementsByTagName("choice")

        for i in range(len(choices)):
            n_dict = {}
            n_dict['text'] = choices[i].firstChild.nodeValue
            n_dict['link'] = choices[i].getAttribute("link")
            n_dict['index'] = i
            t_dict['choices'].append(n_dict)

        prompts[element.getAttribute("id")] = t_dict
        print(t_dict)


@app.route("/")
def home():
    return redirect("/game")


@app.route("/game", methods=['GET', 'POST'])
def make_choice():
    global current_id
    prompt = prompts[current_id]

    if request.method == 'POST':
        id = int(request.form['choice'])
        current_id = prompt['choices'][id]['link']

    if current_id == "-1":
        return render_template('lose.html')

    prompt = prompts[current_id]

    return render_template("choice.html", prompt=prompt['text'], choices=prompt['choices'])

@app.route("/restart")
def restart():
    global current_id
    current_id = 0
    return redirect("/game")


preload_choices()
app.run(debug=True)
