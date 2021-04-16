from flask import Flask, redirect, render_template, url_for, request, session
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from flask_wtf import FlaskForm
from wtforms import SelectField

# TOLERANCE = 30
# END_ANSWERS= ['1','2','3','4']

app = Flask(__name__)
app.config['SECRET_KEY'] = 'leroyJenkins'
#@app.route('/')
#def index():
#    return render_template('index.html')

# Where to input the angle differential
@app.route('/', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        variance_input = request.form['variance']
        session['tolerance'] = variance_input

        return redirect(url_for('visualize'))
    return render_template('user_input.html')
    

# The Plot Page
@app.route('/visualize', methods=['GET', 'POST'])
def visualize():
    TOLERANCE = int(session['tolerance'])
    
    base_angle = random.randint(40,150 - 3 * TOLERANCE)
    
    test_angles = [base_angle,
                   base_angle + 1 * TOLERANCE,
                   base_angle + 2 * TOLERANCE,
                   base_angle + 3 * TOLERANCE]
    
    random.shuffle(test_angles)

    temp = np.argsort(test_angles)
    answers = np.empty_like(temp)
    answers[temp] = np.arange(len(test_angles)) + 1
    answers = list(answers)

    print()
    session['answer1'] = str(answers[0])
    session['answer2'] = str(answers[1])
    session['answer3'] = str(answers[2])
    session['answer4'] = str(answers[3])

    buf = test(test_angles)
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    form = Form()
    
    return render_template('game_play.html', form=form, plots = data)

@app.route('/results', methods=['GET', 'POST'])
def results():

    if request.method == 'POST':
        userAnswers = request.form

        smallest = userAnswers['smallest']
        second_smallest = userAnswers['second_smallest']
        third_smallest = userAnswers['third_smallest']
        largest = userAnswers['largest']
        userAnswers = [smallest, second_smallest, third_smallest, largest]

        print('Users answers:', userAnswers)
        END_ANSWERS = [session['answer1'], session['answer2'], session['answer3'], session['answer4']] 
        print('Correct Answers:', END_ANSWERS)

        if userAnswers == END_ANSWERS:
            return f'<h1>Correct!</h1>'
        else:
            return f'<h1>Wrong!<br>{END_ANSWERS[0]}</h1><br><h1>{END_ANSWERS[1]}</h1><br><h1>{END_ANSWERS[2]}</h1><br><h1>{END_ANSWERS[3]}</h1>'
    else:
        return f'<h1>Loading</h1>'

def test(angles):
    # unpack and create angles
    angle1, angle2, angle3, angle4 = angles
    
    # calculate the end points
    def findEndPoints(angle):
        length1 = random.randint(3, 5)
        length2 = random.randint(3, 5)
        
        randTheta = random.randint(0, 360)
        theta1 = 0 + randTheta
        theta2 = angle + randTheta
        
        x = 5 + random.randint(-2,2)
        y = 5 + random.randint(-2,2)
        
        endx1 = x + length1 * math.cos(math.radians(theta1))
        endy1 = y + length1 * math.sin(math.radians(theta1))
        
        endx2 = x + length2 * math.cos(math.radians(theta2))
        endy2 = y + length2 * math.sin(math.radians(theta2))
        
        return (x, y, endx1, endy1, endx2, endy2)
       
    # Plot the points
    fig, axs = plt.subplots(2, 2)
    
    x, y, endx1, endy1, endx2, endy2 = findEndPoints(angle1)
    axs[0, 0].plot([x, endx1], [y, endy1], 'k')
    axs[0, 0].plot([x, endx2], [y, endy2], 'k')
    axs[0, 0].set_title('Angle 1')
    
    x, y, endx1, endy1, endx2, endy2 = findEndPoints(angle2)
    axs[0, 1].plot([x, endx1], [y, endy1], 'k')
    axs[0, 1].plot([x, endx2], [y, endy2], 'k')
    axs[0, 1].set_title('Angle 2')
    
    x, y, endx1, endy1, endx2, endy2 = findEndPoints(angle3)
    axs[1, 0].plot([x, endx1], [y, endy1], 'k')
    axs[1, 0].plot([x, endx2], [y, endy2], 'k')
    axs[1, 0].set_title('Angle 3')
    
    x, y, endx1, endy1, endx2, endy2 = findEndPoints(angle4)
    axs[1, 1].plot([x, endx1], [y, endy1], 'k')
    axs[1, 1].plot([x, endx2], [y, endy2], 'k')
    axs[1, 1].set_title('Angle 4')
    
    # Hide labels and axis
    for ax in axs.flat:
        ax.axis('off')
        ax.label_outer()
        ax.set_aspect('equal', adjustable='box')
        ax.set_ylim([0, 10])   # set the bounds to be 10, 10
        ax.set_xlim([0, 10])
        
    # plt.show(block=False)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    return buf

class Form(FlaskForm):
    smallest = SelectField('smallest', choices=[('1'), ('2'), ('3'), ('4')], default = 1)
    second_smallest = SelectField('secondsmallest', choices=[('1'), ('2'), ('3'), ('4')], default = 2)
    third_smallest = SelectField('thirdsmallest', choices=[('1'), ('2'), ('3'), ('4')], default = 3)
    largest = SelectField('largest', choices=[('1'), ('2'), ('3'), ('4')], default = 4)


if __name__ == "__main__":
    app.run(debug=True)


