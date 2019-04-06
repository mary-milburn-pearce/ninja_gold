from flask import Flask, render_template, request, redirect, session
import datetime, random

app = Flask(__name__)  
app.secret_key = 'opus'

@app.route('/')         
def index():
    return render_template("index.html")

@app.route('/process', methods=['POST'])         
def process_money():
    # print(request.form)
    # # if 'gold' not in session:
    # #     return redirect('/reset')
    message_color='green'
    if request.form['source']=='farm':
        newVal=random.randint(10, 20)
        actStr=f"Earned {newVal} golds from the farm " \
            + datetime.datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
    elif request.form['source']=='cave':
        newVal=random.randint(5, 10)
        actStr=f"Earned {newVal} golds from the cave " \
            + datetime.datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
    elif request.form['source']=='house':
        newVal=random.randint(2, 5)
        actStr=f"Earned {newVal} golds from the house " \
            + datetime.datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
    elif request.form['source']=='casino':
        newVal=random.randint(-50, 50)
        if newVal >= 0:
            actStr=f"Earned {newVal} golds from the casino " \
                + datetime.datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
        else:
            message_color='red'
            actStr=f"Lost {(0-newVal)} golds to the casino " \
                + datetime.datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
    session['gold']+=newVal
    session['activities'].append( {'color' : message_color, 'message' : actStr} )
    if session['gold']>=session['win-points']:
        session['win-status']='Won'
    elif session['tries-left']==0:
        session['win-status']='Lost'
    else:
        session['tries-left']=int(session['tries-left'])-1
        session['win-status']=''
    return redirect('/')

@app.route('/reset', methods=['POST', 'GET'])
def process_reset():
    print(request.form)
    if request.form['win-points']=='':
        win_points=100
    else:
        win_points=int(request.form['win-points'])
    if request.form['win-tries']=="":
        win_tries=10
    else:
        win_tries=int(request.form['win-tries'])
    session.clear
    session['gold']=0
    session['activities']=[]
    session['win-points']=win_points
    session['win-tries']=win_tries
    session['tries-left']=win_tries
    session['win-status']=''
    return redirect('/')

if __name__=="__main__":   
    app.run(debug=True)    