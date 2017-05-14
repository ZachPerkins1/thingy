from flask import Flask, request, render_template, session, redirect, jsonify, make_response
from xml.dom import minidom

app = Flask("HOD Project")

prompts = []
current_id = 0

def preload_choices():
    doc = minidom.parse('data.xml')
    doc = doc.getElementsByTagName('prompts')[0]
    prompt_list = doc.getElementsByTagName("prompt")
    for element in prompt_list:
        t_dict = {}
        t_dict['text'] = element.getElementsByTagName("text")[0].firstChild.nodeValue
        choices = element.getElementsByTagName("choice")
        t_di
 ct['choice_a'] = choices[0].firstChild.nodeValue
        t_dict['choice_a_link'] = int(choices[0].getAttribute("link"))
        t_dict['choice_b'] = choices[1].firstChild.nodeValue
        t_dict['choice_b_link'] = int(choices[1].getAttribute("link"))

        prompts.append(t_dict)
        print(t_dict)

@app.route("/")
def home():
    return redirect("/game")


@app.route("/game", methods=['GET', 'POST'])
def make_choice():
    global current_id
    prompt = prompts[current_id]
    print prompt['choice_a_link']
    print prompt['choice_b_link']
    if request.method == 'POST':
        id = int(request.form['choice'])
        if id == 0:
            current_id = prompt['choice_a_link']
            print "a"
        else:
            current_id = prompt['choice_b_link']
            print "b"

    if current_id == -1:
        return render_template('lose.html')

    prompt = prompts[current_id]

    return render_template("choice.html", prompt=prompt['text'], choice_a=prompt['choice_a'], choice_b=prompt['choice_b'])

@app.route("/restart")
def restart():
    global current_id
    current_id = 0
    return redirect("/game")


preload_choices()
app.run(debug=True)
