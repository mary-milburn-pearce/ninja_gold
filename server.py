from flask import Flask, render_template, request, redirect, session
import datetime, random 
from constant import DEFAULT_TRIES_TO_WIN, DEFAULT_GOLDS_TO_WIN

app = Flask(__name__)  
app.secret_key = 'opus'

@app.route('/')         
def index():
    if 'gold' not in session:
        return redirect('/reset')
    return render_template("index.html")


gold_dict = {
    'farm' : {'min_amt' : 10, 'max_amt' : 20},
    'cave' : {'min_amt' : 5, 'max_amt' : 10},
    'house' : {'min_amt' : 2, 'max_amt' : 5},
    'casino' : {'min_amt' : -50, 'max_amt' : 50}
}

@app.route('/process', methods=['POST'])         
def process_money():
    source=request.form['source']
    min_gold=gold_dict[source]['min_amt']
    max_gold=gold_dict[source]['max_amt']
    newVal=random.randint(min_gold, max_gold)
    if newVal >= 0:
        message_color='green'
        actStr=f"Earned {newVal} golds from the {source} " \
            + datetime.datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
    else:
        message_color='red'
        actStr=f"Lost {(0-newVal)} golds to the {source} " \
            + datetime.datetime.now().strftime("%B %d, %Y %I:%M:%S %p")
    session['gold']+=newVal
    session['tries-left']=int(session['tries-left'])-1
    session['activities'].append( {'color' : message_color, 'message' : actStr} )
    if session['gold']>=session['win-points']:
        session['win-status']='Won'
    elif session['tries-left']<=0:
        session['win-status']='Lost'
    else:
        session['win-status']=''
    return redirect('/')

@app.route('/reset', methods=['POST', 'GET'])
def process_reset():
    print(request.form)
    if request.method=='GET' or request.form['win-points']=="":
        win_points=DEFAULT_GOLDS_TO_WIN
    else:
        win_points=int(request.form['win-points'])
    if request.method=='GET' or request.form['win-tries']=="":
        win_tries=DEFAULT_TRIES_TO_WIN
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