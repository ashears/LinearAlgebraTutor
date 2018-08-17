'''
CIS 422
Project 2: Linear Algebra Visualizer

Filename: main.py

Description:

By: Andrew Cvitanovich, Ashton Shears, Adrian Scheuerell and Marc Lee

Modified On: 5/12/2018
'''

from flask import Flask, render_template, request, url_for, make_response, redirect
import json
import jinja2
import os
import re
import copy



application = Flask(__name__)
application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
##Global Variables##
nav_list = [{"Topic":"Fundamentals","Items":[
        {"Name":"Linear Equations","URL":"linearequation","Complete":False,"Current":False},
        {"Name":"Intro to Matrices", "URL":"matrices_basics","Complete":False,"Current":False},
        {"Name":"Intro to Vectors", "URL":"/vector_intro","Complete":False,"Current":False},
        ]},
        {"Topic":"Matrices","Items":[
        {"Name":"Matrix Operations", "URL":"/matrix_operations","Complete":False,"Current":False},
        {"Name":"Reduced Row-Echelon Form", "URL":"/rref","Complete":False,"Current":False},
        {"Name":"Matrix Multiplication", "URL":"/matrix_mult","Complete":False,"Current":False},
        {"Name":"Determinants of Matrices", "URL":"/determinants","Complete":False,"Current":False},
        {"Name":"Inverting Matrices","URL":"/matrix_inverse","Complete":False,"Current":False},
        {"Name":"Transpose of a Matrix", "URL":"/matrix_transpose","Complete":False,"Current":False},
        ]},
        {"Topic":"Vectors","Items":[
        {"Name":"Vector Operations","URL":"/vector_operations","Complete":False,"Current":False},
        {"Name":"Linear Combinations and Span","URL":"/linear_combo","Complete":False,"Current":False},

        {"Name":"Inner products of Vectors", "URL":"/inner_products","Complete":False,"Current":False},
        {"Name":"Orthogonality","URL":"/orthogonal_vectors","Complete":False,"Current":False},
        ]},
        {"Topic":"Eigenvalues","Items":[
            {"Name":"Eigenvalues","URL":"/eigenvalues","Complete":False,"Current":False},
            {"Name":"Characteristic Equation", "URL":"/char_eqn","Complete":False,"Current":False},
        ]},
        {"Topic":"Vector Spaces","Items":[
            {"Name":"Intro to Vector Spaces","URL":"/vector_spaces","Complete":False,"Current":False},
            {"Name":"Subspaces", "URL":"/subspaces","Complete":False,"Current":False},
        ]},
        {"Topic":"Transformations","Items":[
            {"Name":"Linear Transformations","URL":"/linear_transformations","Complete":False,"Current":False},
            {"Name":"Injection and Surjection","URL":"/inject_surject","Complete":False,"Current":False},
            {"Name":"Bonus: 2D Graphics","URL":"/2D_graphics","Complete":False,"Current":False},
    ]}]

##Global variable so that we don't need to type out the same nav list for every topic
##END GLOBAL VARS###


##routes to modules are constructed as follows:
##@app.route("<url you linked to in nav_list>")
##def function_name()"
######page = {"Description": "<this info will go in description section>", "Resources": "", "Visualization" : ""}
######nav = nav_list
######head = {"Greeting": ""}
######return render_template("moduletemplate.html")

# INITIALIZE FLASK ROUTINES
@application.route("/")
@application.route("/index.html")
def hello():
    page = {"Description": "Welcome to LinearAlgebraTutor!", "Resources": "", "Visualization" : ""}
    #showing user progression index page as well
    nav = copy.deepcopy(nav_list)
    checking_topics(nav)
    #when point data is not in cookie data, it add point
    if request.cookies.get("point") == None:
        resp = make_response(redirect(url_for('hello')))
        resp.set_cookie('point', '0')
        point = request.cookies.get('point')
        return resp
    else:
        point = request.cookies.get('point')

    head = {"Points": point}

    return render_template("index.html", page=page,nav=nav,head=head)


@application.route("/help")
def help():
    #showing user progression data on helping page as well
    nav = copy.deepcopy(nav_list)
    checking_topics(nav)
    if request.cookies.get("point") == None:
        resp = make_response(redirect(url_for('hello')))
        resp.set_cookie('point', '0')
        point = request.cookies.get('point')
        return resp
    else:
        point = request.cookies.get('point')

    head = {"Points": point}
    return render_template("help.html",nav=nav,head=head)


@application.route("/linearequation", methods=['GET', 'POST'])
def linear_equation_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('linear_equation_module'))) #redirect to current page to update cookie.
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    prev_point = request.cookies.get('point') #getting point data from cookie
    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error handling block
            if request.form.getlist('test1') == ['a', 'b', 'e', 'f'] and request.form['test2'] == "c":
                #If all answers are correct
                resp = make_response(redirect(url_for('linear_equation_module'))) #redirect to current page. To update cookie
                resp.set_cookie("linequation", "OK") #add progression data to cookie
                resp.set_cookie("point", str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "One or more answers are incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("linequation"):
        nav[0]["Items"][0]["Complete"] = True #adding check mark on left panel
        result_text = "Correct, You earned 100 points"
    else:
        nav[0]["Items"][0]["Complete"] = False

    page = {"Description":
    '''
    <p>
    <h3>Linear Equations</h3>
            We begin our study of linear algebra with a fundamental concept, linear equations.
            <br><i>Definition:</i> A linear equation is an equation written of the form:<br>
            $$ax_1 + bx_2 = y$$
            $$ay_1 + by_2 + cy_3 = z$$
            where a,b,c are constants, or with numbers:<br>
            $$2x_1 + 7x_2 = 5$$
            Notice how for each term of the linear equation there is only one variable. So,
            $$x_1x_2 + 5x_3 = 17$$ is not a linear equation but $$x_1 + 2 = -x_2$$ is a linear equation, because it can be rewritten as:
            $$x_1 + x_2 = -2$$


            <h3>Systems of Linear Equations</h3>
            A system of linear equations is simply multiple linear equations considered in the same scope. This is an example system of linear equation with four given linear equations:<br>
            $$x_1 + x_2 + x_3 = 5$$
            $$5x_1 + 0x_2 + 6x_3 = 12$$
            $$12x_1 + 4x_2 + x_3 = 1$$
            $$0x_1 + x_2 + 0x_3 = 1$$
            It can be seen that for the above system of linear equations, there could be some: $$x_1, x_2, x_3$$
            where all the equations are satisfied as true. This is called the solution set.<br>
           <h3>Solution Set</h3>
            A solution set to a system of linear equations is a set of values to where the system holds true.<br>
            <b>Example</b>
            $$3x_1 - x_2 = 8$$
            $$-5x_1 + 10x_2 = -5$$
            $$\\text{A solution set for this system is } (x_1 = 3, x_2 = 1)$$
            </p>''',

            "Resources": '''<p>
            Textbook:<br>
            <a href="http://linear.ups.edu/html/section-SSLE.html">A First Course in Linear Algebra: Systems of Linear Equations</a>
            
            </p>
            ''',

            "Visualization": ''' <p>
            <b>Try it now! 1:</b><br>
            Which ones are linear equations?<br>
            <form action="" name="test1" method="post" onsubmit="">
            $$A: x_1 + x_2 - 5x_3 + 12x_4 = -2$$
            $$B: 5x = 12$$
            $$C: 3x_1x_2 + x_3 + 4x_4 = 12 $$
            $$D: 5 + 3 + 9 = 12$$
            $$E: 19 - x = 15$$
            $$F: x_2 = 15$$
            <input type="checkbox" name="test1" id="A" value="a"> A
            <input type="checkbox" name="test1" id="B" value="b"> B
            <input type="checkbox" name="test1" id="C" value="c"> C
            <input type="checkbox" name="test1" id="A" value="d"> D
            <input type="checkbox" name="test1" id="B" value="e"> E
            <input type="checkbox" name="test1" id="C" value="f"> F<br>

            <b>Try it now! 2:</b> <br>
            What is the solution to this system of linear equations?
            $$x_1 - 2x_2 = 10$$
            $$3x_1 + x_2 = -5$$
            <input type="radio" name="test2" id="A" value="a">(20,5)<br>
            <input type="radio" name="test2" id="B" value="b">(-1,-1)<br>
            <input type="radio" name="test2" id="C" value="c">(0,-5)<br>


            <input type="submit" value="Submit">
            </form>
            </p>''' + "<b>" + result_text + "</b>"}
    nav[0]['Items'][0]['Current'] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/matrices_basics", methods=['GET','POST'])
def matrices_basics_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('matrices_basics_module'))) #redirect to current page to update cookie
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    prev_point = request.cookies.get('point') #getting point data from cookie
    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error handling block
            if request.form.getlist('test1') == ['a', 'b', 'c'] and request.form.getlist('test2') == ['a', 'c']:
                #If all answers are correct
                resp = make_response(redirect(url_for('matrices_basics_module'))) #redirect to current page. To update cookie
                resp.set_cookie("basic_matrix", "OK") #add progression data to cookie
                resp.set_cookie("point", str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "One or more answers are incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("basic_matrix"):
        nav[0]["Items"][1]["Complete"] = True #adding checkmark on left panel
        result_text = "Correct, you earned 100 points"
    else:
        nav[0]["Items"][1]["Complete"] = False

    page = {"Description": '''

            <p>
            <h3>Matrices</h3>
            In the previous module, <a href ="{{ url_for('linearequation') }}">Linear Equations</a>, we explained the basics of linear equations. An efficient way to represent systems of linear equations is with matrices. We can represent each linear equation from the system as a row in a matrix, and then do operations on the matrix that allow us to interpret the system in many ways. For example, this system of linear equations:<br>
            $$x_1 + 2x_2 + 3x_3 = 5$$
            $$4x_1+ 0x_2 - x_3 = 15$$
            $$6x_1 +12x_2+ 5x_3 = -4$$
            can be represented by the following 3x3 <i>coefficient matrix</i> and 3x1 matrix(also known as a <a href="">vector</a> with 3 elements).<br>
            $$
            \\begin{bmatrix} 1 & 2 & 3 \\\\
                            4 & 0 & -1 \\\\
                            6 & 12 & 5 \\\\
            \\end{bmatrix}
            \\begin{bmatrix} x_1\\\\
                    x_2\\\\
                    x_3\\\\
            \\end{bmatrix}
            =
            \\begin{bmatrix} 5 \\\\
                            15 \\\\
                            -4 \\\\
            \\end{bmatrix}
            \\quad
            $$
            or as the augmented matrix:</br>
            $$
            \\left[\\begin{array}{rrr|r}
                1 & 2 & 3 & 5\\\\
                4 & 0 & -1 & 15\\\\
                6 & 12 & 5 & -4\\\\
                \\end{array}\\right]
            $$



            <p>
            <br>You may be wondering, what does putting these linear equations into matrices allow us to do?
            One common use is to find a solution to the system of equations, by converting the matrix to the form below:
            $$
            \\left[\\begin{array}{rrr|r}
                1 & 0 & 0 & 2\\\\
                0 & 1 & 0 & 5\\\\
                0 & 0 & 1 & 3\\\\
                \\end{array}\\right]

            $$
            <br>which shows that the solution to this system is: $$(x_1 = 2, x_2 = 5, x_3 = 3)$$.
            <br>We call the form of this matrix <a href="/rref">Reduced Row-Echelon Form</a>
            </p>


            ''',

            "Resources": '''<p>
            Textbook<br>
            <a href="http://linear.ups.edu/html/section-RREF.html">A First Course in Linear Algebra: Matrices</a>

            </p>
            ''',

            "Visualization": '''<p>
            <b>Try it now! 1:</b><br>
            Which of the following are matrices?
            $$
            A = \\begin{bmatrix} 3 \\\\
                    3\\\\
                    3\\\\

            \\end{bmatrix}
            ,B = \\begin{bmatrix} 1/2 & -1\\\\
                                    7 & 4\\\\
                                    3 & 1/2\\\\
            \\end{bmatrix}
            ,C = \\begin{bmatrix} 1 & 0 & 0\\\\
                                    0 & 1 & 1\\\\
                                    1 & 1 & 1\\\\
            \\end{bmatrix}
            $$
            <form action="" method="post" name="test1">
            <input type="checkbox" name="test1" id="A" value="a"> A
            <input type="checkbox" name="test1" id="B" value="b"> B
            <input type="checkbox" name="test1" id="C" value="c"> C<br>

            <b>Try it now! 2:</b>
            Which matrices represents the following system of equations?
            $$2x_1 + 4x_2 = 3$$
            $$4x_1 -x_3 = 5$$
            $$x_1 + x_2 + x_3 = 10 $$

            $$A: \\begin{bmatrix} 2 & 4 & 0 \\\\ 4 & 0 & -1 \\\\ 1 & 1 & 1 \\\\ \\end{bmatrix}
            \\begin{bmatrix} x_1 \\\\ x_2\\\\ x_3\\\\ \\end{bmatrix}
            =
            \\begin{bmatrix} 3\\\\5\\\\10\\\\ \\end{bmatrix}
            $$

            $$
            B: \\begin{bmatrix} 2 & 4 \\\\ 4 & -1\\\\ 1 & 1 \\\\ \\end{bmatrix}
            \\begin{bmatrix} x_1 \\\\ x_2\\\\ x_3\\\\ \\end{bmatrix}
            =
            \\begin{bmatrix} 3\\\\5\\\\10\\\\ \\end{bmatrix}
            $$

            $$C:
                \\left[\\begin{array}{rrr|r}
                    2 & 4 & 0 & 3\\\\
                    4 & 0 & -1 & 5\\\\
                    1 & 1 & 1 & 10\\\\
                    \\end{array}\\right]

                $$
                <input type="checkbox" name="test2" id="A" value="a"> A
                <input type="checkbox" name="test2" id="B" value="b"> B
                <input type="checkbox" name="test2" id="C" value="c"> C<br>
                <input type="submit" value="Submit">
                </form>

                </p>''' + "<b>" + result_text + "</b>"}
    nav[0]['Items'][1]['Current'] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/matrix_operations", methods=['GET','POST'])
def matrix_operations_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('matrix_operations_module'))) #redirect to current pageto update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    prev_point = request.cookies.get('point') #getting point data from cookie
    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try:
            #error handling block
            if request.form['x1'] == "12" and request.form['y1'] == "16" and request.form['x2'] == "0" and request.form['y2'] == "15":
                #If all answers are correct
                resp = make_response(redirect(url_for('matrix_operations_module'))) #redirect to current page. To update cookie
                resp.set_cookie("matrix_ops", "OK") #add progression data to cookie
                resp.set_cookie('point', str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "Your answer is incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("matrix_ops"):
        nav[1]["Items"][0]["Complete"] = True #adding check mark
        result_text = "Correct, you earned 100 points"
    else:
        nav[1]["Items"][0]["Complete"] = False

    page = {"Description":
        '''
        <p>
        <h3>Matrix Operations</h3>
        In the previous section, <a href="/matrices_basics">Intro to Matrices and Vectors</a>, we provided a brief description of what matrices are.</br>
        Now, we will explain when matrices are equal and two key operations that can be done to matricies, namely Matrix Addition and Matrix Scalar Multiplication</br>

            <h3>Matrix Equality:</h3>


            Two Matrices are considered  <i>equal</i> when for every corresponding element of the matrix they have the same value.
            <br>For example,
            $$
            A =
            \\begin{bmatrix} 1 & 2 & 3 \\\\
                            4 & 5 & 6 \\\\
            \\end{bmatrix}
            \\quad
            B =
            \\begin{bmatrix} 1 & 2 & 3 \\\\
                            4 & 5 & 6 \\\\
            \\end{bmatrix}
            $$

            are equivalent matrices, which can be expressed by A = B.
            <br> The matrices,

            $$
            C =
            \\begin{bmatrix} 1 & 2 & 3 \\\\
                            4 & 5 & 6 \\\\
            \\end{bmatrix}
            \\quad
            D =
            \\begin{bmatrix} 4 & 5 & 6 \\\\
                            1 & 2 & 3 \\\\
            \\end{bmatrix}
            $$

            are not equivalent matrices,
            <br> and

            $$
            E =
            \\begin{bmatrix} 1 & 3 & 5 \\\\
                            7 & 9 & 11 \\\\
            \\end{bmatrix}
            \\quad
            F =
            \\begin{bmatrix} 1 & 3 & 5 & 7 & 9 & 11
            \\end{bmatrix}
            $$

            are not equivalent matrices.

            <h3>Matrix Addition</h3>
        This operation takes two Matrices <i>with the same number of rows and columns</i>, A and B, and returns a matrix [A + B]</br>
        All that needs to be done is add together each corresponding element of the two matrices. This can be seen in the following example:

                $$
                A =
                \\begin{bmatrix} 1 & 2 & 3 \\\\
                                4 & 5 & 6 \\\\
                \\end{bmatrix}
                \\quad
                B =
                \\begin{bmatrix} 4 & 5 & 6 \\\\
                            6 & 5 & 4 \\\\
            \\end{bmatrix}
            $$
            $$
            A+B =
            \\begin{bmatrix} (1+4) & (2+5) & (3+6) \\\\
                            (4+6) & (5+5) & (6+4) \\\\
            \\end{bmatrix}
            $$

            $$
            A+B =
            \\begin{bmatrix} 5 & 7 & 9 \\\\
                            10 & 10 & 10 \\\\
            \\end{bmatrix}
            $$

    <h3>Matrix Scalar Multiplication</h3>
    This operations takes a scalar (a number) and a Matrix, and then returns a Matrix.
    </br>For each element of the matrix, multiply that by the scalar. This can be seen in the following example:
    $$
    5A = 5\\begin{bmatrix} 1 & 2 & 3 \\\\
                            4 & 5 & 6 \\\\
            \\end{bmatrix}
            \\quad
            = \\begin{bmatrix} 5 & 10 & 15 \\\\
                            20 & 25 & 30 \\\\
            \\end{bmatrix}
            \\quad

    $$
            </p>


    </p>
            ''', "Resources": 
                '''
                Textbook:<br>
                <a href="http://linear.ups.edu/html/section-MO.html">A First Course in Linear Algebra: Matrix Operations</a>
                ''', "Visualization":
                '''
                <p>
                <b>Try it Now! 1:</b> For the following equation, two matrices are being added to each other.
                <br>What is the value of x? What is the value of y?
                $$
                \\begin{bmatrix} 1 & 2 & 3 \\\\
                            3 & 2 & 1 \\\\
                \\end{bmatrix}
                +
                \\begin{bmatrix} 5 & 10 & 15 \\\\
                            13 & -11 & 13 \\\\
                \\end{bmatrix}
                =
                \\begin{bmatrix} 6 & x & 18 \\\\
                            y & -9 & 14 \\\\
                \\end{bmatrix}
                $$
                <form name="trynow1" form action="/matrix_operations" form method='post'>
                x = <input type="text" name="x1" size="2" maxlength="3">
                y = <input type="text" name="y1" size="2" maxlength="3">
                <br>

                <b>Try it Now! 2:</b> For the following equation, a matrix is being multiplied by a scalar.
                <br>What is the value of x? What is the value of y?
                $$
                5 *
                \\begin{bmatrix} -1 & 0 & 2 \\\\
                            3 & -2 & -4 \\\\
                            5 & -5 & 5 \\\\
                \\end{bmatrix}
                =
                \\begin{bmatrix} -5 & x & 10 \\\\
                            y & -10 & -20 \\\\
                            25 & -25 & 25 \\\\
                \\end{bmatrix}
                $$
                x = <input type="text" name="x2" size="2" maxlength="3">
                y = <input type="text" name="y2" size="2" maxlength="3">
                <br><input type="submit" value="Submit">
                </form>


                </p>
                ''' + "<b>" + result_text + "</b>"}
    nav[1]['Items'][0]['Current'] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/rref", methods=['GET', 'POST'])
def rref_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('rref_module'))) #redirect to current page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    prev_point = request.cookies.get('point') #getting point data from cookie
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error handling blcok
            if request.form.getlist('test1') == ["a"] and request.form['test2'] == "3":
                #If all answers are correct
                resp = make_response(redirect(url_for('rref_module'))) #redirect to current page. To update cookie
                resp.set_cookie("rref", "OK") #add progression data to cookie
                resp.set_cookie("point", str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "One or more answers are incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("rref"):
        nav[1]["Items"][1]["Complete"] = True #make checkmark on leftpanel 
        result_text = "Correct, you earned 100 points"
    else:
        nav[1]["Items"][1]["Complete"] = False

    page = {"Description":
            '''
            <p>
            <h3>Echelon Form</h3>
            A matrix is in echelon form when it has the three properties:
            <ol>
            <li>Each leading entry of a row is in a column to the right of the leading entry of the row above it****</li>
            <li>All entries in a column below a leading entry are zeros.</li>
            <li>All nonzero rows are above any rows of all zeros.</li>
            </ol>
            Thus, A is in echelon form, while B and C and D are not in echelon form.
            $$
            A =
            \\left[\\begin{array}{rrr|r}
                1 & 2 & 2 & -1\\\\
                0 & -2 & 5 & 2\\\\
                0 & 0 & 3 & -4\\\\
                \\end{array}\\right]
            ,B =
            \\left[\\begin{array}{rrr|r}
                1 & 0 & 0 & 3\\\\
                0 & 1 & 0 & 2\\\\
                0 & 0 & 1 & -4\\\\
                \\end{array}\\right]
            $$
            $$
            ,C =
            \\left[\\begin{array}{rrr|r}
                1 & 0 & 0 & 3\\\\
                0 & 1 & 0 & 2\\\\
                0 & 0 & 1 & -4\\\\
                \\end{array}\\right]
            ,D =
            \\left[\\begin{array}{rrr|r}
                1 & 0 & 0 & 3\\\\
                0 & 1 & 0 & 2\\\\
                0 & 0 & 1 & -4\\\\
                \\end{array}\\right]
            $$

            <h3>Reduced Row-Echelon Form</h3>
            Reduced row-echelon form will prove to be more useful. In order to be in this form, it has the requirements for echelon form, and also two more requirements:
            <ol>
            <li>The leading entrry in each nonzero row is 1</li>
            <li>Each leading 1 is the only nonzero entry in its column</li>
            </ol>
            Thus, while<br>
            Previously we have showed that matrices can be used to represent systems of linear equations. We briefly mentioned that with the matrix form we are able to solve the system of equations. Converting the matrix into <i>Reduced Row-Echelon Form</i> allows us an effective way to find this solution. <br>
            Below is an example of a matrix in reduced row-echelon form:

            $$
            \\left[\\begin{array}{rrr|r}
                1 & 0 & 0 & 3\\\\
                0 & 1 & 0 & 2\\\\
                0 & 0 & 1 & -4\\\\
                \\end{array}\\right]
            $$
            This reduced matrix shows us that,
            $$(x_1 = 3, x_2 = 2, x_3 = -4)$$
            is a solution to the linear system associated with that reduced matrix.

            <br>You may be wondering, "how can I make a matrix into Reduced Row-Echelon Form.<br>
            To achieve this, we use <i>row operations</i>.<br>

            <h3>Row Operations</h3>

            We have three row operations that are used:<br>
            <ol>
            <li>Swap two rows in the matrix</li>
            <li>Multiply each entry of a single row</li>
            <li>Multiply each entry of a row by some quantity, and add these values to the same entries in the same columns of a second row. Leave the first row the same but replace the second row with the new values </li>
            </ol>

            <b>Example 1</b><br>
            Put the following matrix A in row reduced echelon form. What is the solution set?
            $$
            A =
            \\left[\\begin{array}{rrr|r}
                1 & 2 & -3 & -4\\\\
                -1 & 1 & 0 & 1\\\\
                -2 & -4 & 1 & -22\\\\
                \\end{array}\\right]
            $$
            <i>Step 1</i>: Add row 1 to row 2. This yields the matrix:
            $$
            A =
            \\left[\\begin{array}{rrr|r}
                1 & 2 & -3 & -4\\\\
                0 & 3 & -3 & -3\\\\
                -2 & -4 & 1 & -22\\\\
                \\end{array}\\right]
            $$
            <i>Step 2</i>: Multiply row 2 by 1/3. This yields the following matrix:
            $$
            A =
            \\left[\\begin{array}{rrr|r}
                1 & 2 & -3 & -4\\\\
                0 & 1 & -1 & -1\\\\
                -2 & -4 & 1 & -22\\\\
                \\end{array}\\right]
            $$
            <i>Step 3</i>: Add 2 * row 1 to row 3. This yields the matrix:
            $$
            A =
            \\left[\\begin{array}{rrr|r}
                1 & 2 & -3 & -4\\\\
                0 & 1 & -1 & -1\\\\
                0 & 0 & -5 & -30\\\\
                \\end{array}\\right]
            $$
            <i>Step 4</i>: Multiply row 3 by -1/5. This yields the matrix:
            $$
            A =
            \\left[\\begin{array}{rrr|r}
                1 & 2 & -3 & -4\\\\
                0 & 1 & -1 & -1\\\\
                0 & 0 & 1 & 6\\\\
                \\end{array}\\right]
            $$
            <i>Step 5</i>: Add row 3 to row 2. This yields the matrix:
            $$
            A =
            \\left[\\begin{array}{rrr|r}
                1 & 2 & -3 & -4\\\\
                0 & 1 & 0 & 5\\\\
                0 & 0 & 1 & 6\\\\
                \\end{array}\\right]
            $$
            <i>Step 6</i>: Add -2 * row 2 to row 1. This yields the matrix:
            $$
            A =
            \\left[\\begin{array}{rrr|r}
                1 & 0 & -3 & -14\\\\
                0 & 1 & 0 & 5\\\\
                0 & 0 & 1 & 6\\\\
                \\end{array}\\right]
            $$
            <i>Step 7</i>: Add 3 * row 3 to row 1. This yields the matrix, in reduced row-echelon form:
            $$
            A =
            \\left[\\begin{array}{rrr|r}
                1 & 0 & 0 & 4\\\\
                0 & 1 & 0 & 5\\\\
                0 & 0 & 1 & 6\\\\
                \\end{array}\\right]
            $$
            It can now be seen that $$(x_1 = 4, x_2 = 5, x_3 = 6)$$ is a solution to the system of linear equations represented by matrix A.
            </p>
            ''', "Resources":
            '''
            Textbook:<br>
            <a href="http://linear.ups.edu/html/section-RREF.html">A First Course in Linear Algebra: RREF</a>
            ''',"Visualization" :
            '''
            <p>
            <b>Try it now! 1:</b>
            Which matrix is in row-reduced echelon form?<br>
            $$
            A =
            \\left[\\begin{array}{rrr|r}
                1 & 0 & 0 & -4\\\\
                0 & 1 & 0 & 1\\\\
                0 & 0 & 0 & 0\\\\
                \\end{array}\\right]
            ,B =
            \\left[\\begin{array}{rrr|r}
                1 & 2 & -3 & -4\\\\
                -1 & 1 & 0 & 1\\\\
                -2 & -4 & 1 & -22\\\\
                \\end{array}\\right]
            ,C =
            \\left[\\begin{array}{rrr|r}
                1 & 2 & -3 & -4\\\\
                -1 & 1 & 0 & 1\\\\
                -2 & -4 & 1 & -22\\\\
                \\end{array}\\right]
            $$
            <form action="" name="test1" method="post" onsubmit="">
            <input type="checkbox" name="test1" id="A" value="a"> A
            <input type="checkbox" name="test1" id="B" value="b"> B
            <input type="checkbox" name="test1" id="C" value="c"> C<br>

            <b>Try it now! 2:</b><br>
            What is the solution to the system of linear equations associated with A?
            $$
            A =
            \\left[\\begin{array}{rr|r}
                2 & 1 & -4\\\\
                0 & 2 & 4\\\\
                \\end{array}\\right]
            $$
            $$1:(x_1 = -4, x_2 = 4)$$
            $$2:(x_1 = 2, x_2 = 3)$$
            $$3:(x_1 = -3, x_2 = 2)$$
            $$4:(x_1 = -2, x_2 = 3)$$

            <input type="radio" name="test2" id="1" value="1"> 1
            <input type="radio" name="test2" id="2" value="2"> 2
            <input type="radio" name="test2" id="3" value="3"> 3
            <input type="radio" name="test2" id="4" value="4"> 4<br>
            </p>
            <input type="submit" value="Submit">
            </form>


            </p>
            ''' + "<b>" + result_text + "</b>"}
    nav[1]['Items'][1]['Current'] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/matrix_inverse", methods=['GET', 'POST'])
def matrix_inverse_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('matrix_inverse_module'))) #redirect to current page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    prev_point = request.cookies.get('point') #getting point data from cookie
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error handling block
            if request.form['test1'] == "e" and request.form['test2'] == "j" and request.form['test3'] == "none":
                #If all answers are correct
                resp = make_response(redirect(url_for("matrix_inverse_module"))) #redirect to current page. To update cookie
                resp.set_cookie("inverse", "OK") #add progression data to cookie
                resp.set_cookie("point", str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "One or more answers are incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("inverse"):
        nav[1]["Items"][4]["Complete"] = True #make checkmark on leftpanel
        result_text = "Correct, you earned 100 points"
    else:
        nav[1]["Items"][4]["Complete"] = False

    page = {"Description":
            '''
            <h3>Inverse of numbers</h3>
            When considering numbers, the inverse of a number is that number to the -1 power. That is, the inverse of 5 is 1/5. This can we written as:
            $$ 5^{-1} = 1/5$$
            With numbers, a number multiplied by it's inverse is always 1. Thus:
            $$3^{-1}*3 = 1 $$
            The inverse of matrices function somewhat similarly.
            <h3>Inverse of Matrices</h3>
            A matrix A with n row's and column's is called <b>invertible</b> if there is a matrix C with the same number of rows and column's such that A*C = I, where I is the <a href="">identity matrix</a>
            <h3>Getting the Inverse of 2x2 Matrices</h3>
            We have a simple formula for computing the inverse of 2x2 matrices. The next section will explain how to invert larger matrices.
            $$
            \\text{If we have a matrix F =}
            \\begin{bmatrix} a & b\\\\
                            c & d\\\\
            \\end{bmatrix}
            $$
            We know that if ad - bc = 0, F is not invertible. Otherwise,
            $$
            F^{-1} = \\frac{1}{ad - bc}
            \\begin{bmatrix} d & -b\\\\
                            -c & a\\\\
            \\end{bmatrix}
            \\quad
            $$
            <h3>Getting inverse of any invertible square matrix</h3>
            In order to find the inverse of a general square matrix, we have an effective algorithm:
            $$
            \\text{1. Augment matrix with identity matrix:}
            \\begin{bmatrix} A & I\\\\
            \\end{bmatrix}
            $$
            $$
            \\text{2. Row reduce the matrix until is is in the form:}
            \\begin{bmatrix} I & A'\\\\
                    \\end{bmatrix}
            $$
            $$
            A' \\text{ is A inverted, or } A^{-1}
            $$
            <br><b>Example 1</b><br>
            $$
            \\text{Find the inverse of the matrix C =}
            \\begin{bmatrix} 1 & 0 & -1 \\\\
                            1 & 1 & 1 \\\\
                            0 & 1 & 1 \\\\
            \\end{bmatrix}
            $$
            <b>Solution:</b>
            $$
            \\text{1. Start by augmenting C with the identity matrix}
            $$
            $$
            \\begin{bmatrix} C & I\\\\
            \\end{bmatrix}
            =
            \\begin{bmatrix} 1 & 0 & -1 & 1 & 0 & 0\\\\
                            1 & 1 & 1 & 0 & 1 & 0\\\\
                            0 & 1 & 1 & 0 & 0 & 1\\\\
            \\end{bmatrix}
            $$
            $$\\text{2. Row reduce the matrix until it is in the form:} \\begin{bmatrix} I & A'\\\\ \\end{bmatrix}$$
            $$\\begin{bmatrix} I & A' \\\\ \\end{bmatrix} =
            \\begin{bmatrix} 1 & 0 & 0 & 0 & 1 & -1 \\\\ 0 & 1 & 0 & 1 & -1 & 2 \\\\ 0 & 0 & 1 & -1 & 1 & -1 \\\\ \\end{bmatrix}$$
            $$\\text{Inverse of A = } A^{-1} = \\begin{bmatrix} 0 & 1 & -1 \\\\ 1 & -1 & 2 \\\\ -1 & 1 & -1 \\\\ \\end{bmatrix}$$

            While this is an effective way to find the inverse, not every matrix is invertible.
            <h3>Determining matrix invertibility</h3>
            If the <a href="/determinants">determinant</a> of A is 0, then there is no possible inverse of A.
            ''', "Resources": 
            '''
            Textbook:<br>
            <a href="http://linear.ups.edu/html/section-MISLE.html">A First Course in Linear Algebra: Matrix Inverse</a><br>
            Video:<br>
            <a href="https://www.khanacademy.org/math/precalculus/precalc-matrices/intro-to-matrix-inverses/v/inverse-matrix-part-1">Khan Academy: Matrix Inverse</a>
            ''', "Visualization" :
            '''
            <p>
            <b>Try it now! 1:</b><br>
            Which matrix is the inverse of matrix A?
            $$A = \\begin{bmatrix} -2 & 1 \\\\ 5 & -5 \\\\ \\end{bmatrix}$$
            $$B = \\begin{bmatrix} -2/5 & 1/5 \\\\ 1 & -1 \\\\ \\end{bmatrix},
            C = \\begin{bmatrix} -5 & -1 \\\\ -5 & -2 \\\\ \\end{bmatrix}$$

            $$D = \\begin{bmatrix} 1 & 2/5 \\\\ 1 & 1/5 \\\\ \\end{bmatrix},
            E = \\begin{bmatrix} -1 & -1/5 \\\\ -1 & -2/5 \\\\ \\end{bmatrix}
            $$
            <form name="trynow1" action="/matrix_inverse" method="post" onsubmit="">

            <input type="radio" name="test1" id="B" value="b"> B
            <input type="radio" name="test1" id="C" value="c"> C
            <input type="radio" name="test1" id="D" value="d"> D
            <input type="radio" name="test1" id="E" value="e"> E<br>


            <b>Try it now! 2:</b><br>
            Which matrix is the inverse of matrix F?
            $$F = \\begin{bmatrix} 1 & 2 & 1 \\\\ -2 & -1 & 1 \\\\ 3 & 6 & -3 \\\\ \\end{bmatrix}$$
            $$G = \\begin{bmatrix} -1/6 & -2/3 & 1/6 \\\\ 1/6 & -1/3 & -1/6 \\\\ 1/2 & 0 & 1/6 \\\\ \\end{bmatrix}
            ,H = \\begin{bmatrix} 1/6 & 2/3 & -1/6 \\\\ -1/6 & 1/3 & -1/6 \\\\ -1/2 & 0 & 1/6 \\\\ \\end{bmatrix}$$
            $$I = \\begin{bmatrix} 1/6 & 2/3 & 1/6 \\\\ -1/6 & 1/3 & 1/6 \\\\ 1/2 & 0 & -1/6 \\\\ \\end{bmatrix}
            ,J = \\begin{bmatrix} 1/6 & -2/3 & -1/6 \\\\ 1/6 & 1/3 & 1/6 \\\\ 1/2 & 0 & -1/6 \\\\ \\end{bmatrix}$$

            <input type="radio" name="test2" id="G" value="g"> G
            <input type="radio" name="test2" id="H" value="h"> H
            <input type="radio" name="test2" id="I" value="i"> I
            <input type="radio" name="test2" id="J" value="j"> J
            <input type="radio" name="test2" id="none" value="none">Matrix F is not invertible<br>


            <b>Try it now! 3:</b><br>
            Which matrix is the inverse of matrix Q?
            $$Q = \\begin{bmatrix} 1 & 2 & 3 \\\\ 4 & 5 & 6 \\\\ 7 & 8 & 9 \\\\ \\end{bmatrix}$$
            $$P = \\begin{bmatrix} 9 & -2 & 3 \\\\ -6 & 5 & -4 \\\\ 7 & -8 & 1 \\\\ \\end{bmatrix},
            R = \\begin{bmatrix} 1/5 & 2 & 3 \\\\ 4 & 1 & 6 \\\\ 7 & 7 & 9/5 \\\\ \\end{bmatrix}$$
            $$S = \\begin{bmatrix} 9/8 & 1 & 7/8 \\\\ 6/8 & 5/8 & 4/8 \\\\ 3/8 & 2/8 & 1/8 \\\\ \\end{bmatrix}
            ,T = \\begin{bmatrix} 1/4 & 2/4 & 3/4 \\\\ 4/4 & 5/4 & 6/4 \\\\ 7/4 & 8/4 & 9/4 \\\\ \\end{bmatrix}
            $$

            <input type="radio" name="test3" id="P" value="p"> B
            <input type="radio" name="test3" id="R" value="r"> C
            <input type="radio" name="test3" id="S" value="s"> D
            <input type="radio" name="test3" id="T" value="t"> T
            <input type="radio" name="test3" id="None" value="none"> Matrix Q is not invertible<br>
            <input type="submit" value="Submit">
            </form>

            </p>
            ''' + "<b>" + result_text + "</b>"}
    nav[1]['Items'][4]['Current'] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/vector_intro", methods=['GET', 'POST'])
def intro_to_vectors_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('intro_to_vectors_module'))) #redirect to current page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    prev_point = request.cookies.get('point') #getting point data from cookie
    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error handling block
            if request.form.getlist('test1') == ['a', 'c', 'd']:
                #If all answers are correct
                resp = make_response(redirect(url_for("intro_to_vectors_module"))) #redirect to current page. To update cookie
                resp.set_cookie("intro_vector", "OK") #add progression data to cookie
                resp.set_cookie("point", str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "Your answer is incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("intro_vector"):
        nav[0]["Items"][2]["Complete"] = True #make checkmark
        result_text = "Correct, you earned 100 points"
    else:
        nav[0]["Items"][2]["Complete"] = False


    page = {"Description":
            '''
            <h3>Defining Vectors</h3>
            In linear algebra, we consider a vector to be a 1-dimensional array of numbers.
            <br>For example both a and b below are vectors,

            $$
            A =
            \\begin{bmatrix} -2\\\\
                            3\\\\
                            9\\\\
            \\end{bmatrix}

            B =
            \\begin{bmatrix} -1 & 3\\\\
            \\end{bmatrix}
            $$

            We can also consider vector A to be a matrix with 3 rows and 1 column, and vector B as a matrix with 1 row and 2 columns.
            ''', "Resources": 
            '''
            Textbook:<br>
            <a href="http://linear.ups.edu/html/section-VO.html">A First Course in Linear Algebra: Vectors</a>
            ''', "Visualization" :
            '''
            <p>
            Which of the following are vectors?<br>
            $$
            A = \\begin{bmatrix} -2\\\\
                    1\\\\
                    0\\\\
                    \\end{bmatrix}
            ,B = \\begin{bmatrix} 5 & 3 & -2\\\\
                                1 & -2 & 4\\\\
                               \\end{bmatrix}
            ,C = \\begin{bmatrix} 1 & 7 & 5 & -2\\\\
                    \\end{bmatrix}
            ,D = \\begin{bmatrix} 1/2\\\\
                                -1/2\\\\
                                \\end{bmatrix}
            $$
            <form name="trynow1" action="/vector_intro" method="post" onsubmit="">

            <input type="checkbox" name="test1" id="A" value="a"> A
            <input type="checkbox" name="test1" id="B" value="b"> B
            <input type="checkbox" name="test1" id="C" value="c"> C
            <input type="checkbox" name="test1" id="A" value="d"> D<br>
            <input type="submit" value="Submit">
            </form>

            </p>
            ''' + "<b>" + result_text + "</b>"}
    nav[0]['Items'][2]['Current'] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/vector_operations", methods=['GET', 'POST'])
def vector_operations_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('vector_operations_module'))) #redirect to current page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    prev_point = request.cookies.get('point') #getting point data from cookie
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error handling block
            if request.form.getlist('test1') == ['h'] and request.form['test2'] == "y":
                #If all answers are correct
                resp = make_response(redirect(url_for("vector_operations_module"))) #redirect to current page. To update cookie
                resp.set_cookie("operations", "OK") #add progression data to cookie
                resp.set_cookie('point', str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "One or more answers are incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("operations"):
        nav[2]["Items"][0]["Complete"] = True #make checkmark
        result_text = "Correct, you earned 100 points"
    else:
        nav[2]["Items"][0]["Complete"] = False

    page = {"Description":
            '''
            <h3>Vector Addition</h3>
            We are able to add two vectors together. This has a very similar implementation to matrix addition, that is, we simply add the corresponding elements together. This can be seen in the following example:
            <br><b>Example 1</b>
            $$A = \\begin{bmatrix} 5\\\\
                                    -1\\\\
                                    0\\\\
            \\end{bmatrix}
            ,B = \\begin{bmatrix} 3\\\\
                                1\\\\
                                -2\\\\
            \\end{bmatrix}
            ,A+B = \\begin{bmatrix} 8\\\\
                                    0\\\\
                                    -2\\\\
            \\end{bmatrix}
            $$
            <h3>Vector Scalar Multiplication</h3>
            Another operations we can do on vectors is multiply them by a scalar. For each element of the vector, we multiply it by the scalar. This can be seen in the following example:
            <br><b>Example 2</b>
            $$A = \\begin{bmatrix} 2\\\\
                                    -2\\\\
                                    1\\\\
                                    0\\\\
            \\end{bmatrix}
            , 3A = \\begin{bmatrix} 6\\\\
                                    -6\\\\
                                    3\\\\
                                    0\\\\
            \\end{bmatrix}
            $$
            ''', "Resources":
            '''
            <br>Textbook:
            <br><a href="http://linear.ups.edu/html/section-VO.html">A First Course in Linear Algebra:Vector Operations</a>
            '''
            , "Visualization" :
            '''
            <p>
            <b>Try it now! 1:</b><br>
            Which vector is the result to A and B being added to each other?<br>
            $$
            A = \\begin{bmatrix} 3\\\\
                                12\\\\
                                1\\\\
                                -3\\\\
            \\end{bmatrix}
            ,B = \\begin{bmatrix} 1\\\\
                                  2\\\\
                                  3\\\\
                                  4\\\\
            \\end{bmatrix}
            $$
            $$
            F = \\begin{bmatrix} 3\\\\
                                12\\\\
                                1\\\\
                                -3\\\\
            \\end{bmatrix}
            ,G = \\begin{bmatrix} 3\\\\
                                  24\\\\
                                  3\\\\
                                  -12\\\\
            \\end{bmatrix}
            ,H = \\begin{bmatrix} 4\\\\
                                  14\\\\
                                  4\\\\
                                  1\\\\
            \\end{bmatrix}
            ,I = \\begin{bmatrix} 2\\\\
                                  10\\\\
                                  -2\\\\
                                  -7\\\\
            \\end{bmatrix}
            $$

            <b>Answer:</b>
            <form name="trynow1" action="/vector_operations" method="post" onsubmit="">

            <input type="checkbox" name="test1" id="F" value="f"> F
            <input type="checkbox" name="test1" id="G" value="g"> G
            <input type="checkbox" name="test1" id="H" value="h"> H
            <input type="checkbox" name="test1" id="I" value="i"> I<br>

            <b>Try it now! 2:</b><br>
            Which vector is the result of -2 * A?
            $$A = \\begin{bmatrix} -2\\\\
                                   1\\\\
                                   0\\\\
                                   4\\\\
            \\end{bmatrix}
            $$
            $$
            W = \\begin{bmatrix} -4\\\\
                                 2\\\\
                                 0\\\\
                                 8\\\\
            \\end{bmatrix}
            X = \\begin{bmatrix} -4 \\\\ -1 \\\\ -2 \\\\ 2 \\\\ \\end{bmatrix}
            ,Y = \\begin{bmatrix} 4 \\\\ -2 \\\\ 0 \\\\ -8 \\\\ \\end{bmatrix}
            ,Z = \\begin{bmatrix} 4 \\\\ 1 \\\\ 2 \\\\ -2 \\\\ \\end{bmatrix}
            $$

            <input type="radio" name="test2" id="W" value="w"> W
            <input type="radio" name="test2" id="X" value="x"> X
            <input type="radio" name="test2" id="Y" value="y"> Y
            <input type="radio" name="test2" id="Z" value="z"> Z<br>
            <input type="submit" value="Submit">
            </form>

            </p>
            ''' + "<b>" + result_text + "</b>"}
    nav[2]["Items"][0]["Current"] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/matrix_transpose", methods=['GET', 'POST'])
def matrix_transpose_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('matrix_transpose_module'))) #redirect to current page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    prev_point = request.cookies.get('point') #getting point data from cookie
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error handling block
            if request.form['test1'] == "d" and request.form.getlist('test2') == ['w', 'y']:
                #If all answers are correct
                resp = make_response(redirect(url_for("matrix_transpose_module"))) #redirect to current page. To update cookie
                resp.set_cookie("transpose", "OK") #add progression data to cookie
                resp.set_cookie('point', str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "Your answer is incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("transpose"):
        nav[1]["Items"][5]["Complete"] = True #make check mark
        result_text = "Correct, you earned 100 points"

    else:
        nav[1]["Items"][5]["Complete"] = False

    page = {"Description":
            '''
            <p>
            <h3>Getting the Tranpose of a Matrix</h3>
            Another useful option that gets done on matrices is getting the transpose of a matrix. To do this, we swap the rows and columns. This can be seen in the following example:<br>
            <b>Example 1:</b>
            $$
        \\text{A common notation for the transpose of a matrix A is } A^T
            $$
            $$A = \\begin{bmatrix} 5 & 2 & 3\\\\
                    1 & -1 & -2\\\\
                    0 & 5 & 4\\\\
                    11 & 8 & -9 \\\\
            \\end{bmatrix}
            ,A^T = \\begin{bmatrix} 5 & 1 & 0 & 11\\\\
                                    2 & -1 & 5 & 8\\\\
                                    3 & -2 & 4 & -9\\\\
            \\end{bmatrix}
            $$
            <h3>Symmetric Matrices</h3>
            We consider a matrix to be symmetric if it's transpose is equal to the original matrix. That is,
            $$A^T = A$$
            For a matrix to be symmetric it must be square. <br>
            <b>Example 2:</b><br>
            The following 3 matrices all are symmetric matrices.
            $$\\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\\\ \\end{bmatrix},
            \\begin{bmatrix} 1 & 2 & 3 \\\\ 2 & 4 & 2 \\\\ 3 & 2 & 1 \\\\ \\end{bmatrix}
            ,\\begin{bmatrix} -2 & 9 & 5 & 1 \\\\ 9 & 6 & -2 & 0 \\\\ 5 & -2 & 8 & 4 \\\\ 1 & 0 & 4 & 2 \\\\ \\end{bmatrix}
            $$
            </p>
            ''', "Resources": 
            '''
            Video:<br>
            <a href="https://www.khanacademy.org/math/linear-algebra/matrix-transformations/matrix-transpose/v/linear-algebra-transpose-of-a-matrix">Khan Academy: Matrix Transpose</a>
            ''', "Visualization" :
            '''
            <p>
            <b>Try it now! 1:</b><br>
            Which of the following matrices is the transpose of A?
            $$
            A = \\begin{bmatrix} 7 & 4 & 3 \\\\ 2 & -2 & 0 \\\\ \\end{bmatrix}
            $$
            $$
            B = \\begin{bmatrix} 2 & -2 & 0 \\\\ 7 & 4 & 3 \\\\ \\end{bmatrix},
            C = \\begin{bmatrix} 2 & 7 \\\\ -2 & 4 \\\\ 0 & 3 \\\\ \\end{bmatrix}
            $$
            $$
            D = \\begin{bmatrix} 7 & 2 \\\\ 4 & -2 \\\\ 3 & 0 \\\\ \\end{bmatrix}
            ,E = \\begin{bmatrix} 7 & 4 & 3 \\\\ 2 & -2 & 0 \\\\ \\end{bmatrix}
            $$

            <form name="trynow1" action="/matrix_transpose" method="post" onsubmit="">

            <input type="radio" name="test1" id="B" value="b"> B
            <input type="radio" name="test1" id="C" value="c"> C
            <input type="radio" name="test1" id="D" value="d"> D
            <input type="radio" name="test1" id="E" value="e"> E<br>

            <b>Try it now! 2:</b>
            Which of the following matrices are symmetric?
            $$
            W = \\begin{bmatrix} 2 & 3 \\\\ 3 & 1 \\\\ \\end{bmatrix},
            X = \\begin{bmatrix} 1 & 3 \\\\ 1 & 3 \\\\ \\end{bmatrix},
            Y = \\begin{bmatrix} -1 & 0 & 5 \\\\ 0 & 3 & -2 \\\\ 5 & -2 & -2 \\\\ \\end{bmatrix},
            Z = \\begin{bmatrix} -2 & 1 & 3 \\\\ 8 & 4 & 1 \\\\ 3 & 8 & 9 \\\\ \\end{bmatrix}
            $$


            <input type="checkbox" name="test2" id="W" value="w"> W
            <input type="checkbox" name="test2" id="X" value="x"> X
            <input type="checkbox" name="test2" id="Y" value="y"> Y
            <input type="checkbox" name="test2" id="Z" value="z"> Z<br>
            <input type="submit" value="Submit">
            </form>


            </p>
            ''' + "<b>" + result_text + "</b>"}
    nav[1]['Items'][5]['Current'] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/eigenvalues", methods=['GET', 'POST'])
def into_to_eigen__module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('into_to_eigen__module'))) #redirect to current page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    prev_point = request.cookies.get('point') #getting point data from cookie
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error handling block
            if request.form.getlist('test1') == ['b', 'd']:
                #If all answers are correct
                resp = make_response(redirect(url_for("into_to_eigen__module"))) #redirect to current page. To update cookie 
                resp.set_cookie("eigen", "OK") #add progression data to cookie
                resp.set_cookie('point', str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "Your answer is incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("eigen"):
        nav[3]["Items"][0]["Complete"] = True #make checkmark 
        result_text = "Correct, you earned 100 points"
    else:
        nav[3]["Items"][0]["Complete"] = False

    page = {"Description":
            '''
            <p>
            <h3>Eigenvectors and Eigenvalues</h3>
            <b>Definition</b><br>
            An eigenvector is a vector that when multiplied by a square matrix yields a scalar multiplied by the eigenvector. This can be written as:
            $$Ax = \lambda x$$
            $$\\text{Where A is a square matrix, x is the eigenvector, and } \lambda \\text{ is the scalar described above, called an eigenvalue.}$$
            <b>Example 1:</b>
            $$\\text{Are either } \\begin{bmatrix} 0\\\\
                                                    1\\\\
            \\end{bmatrix}
            \\text{ or } \\begin{bmatrix} 1\\\\
                                        4/9\\\\
            \\end{bmatrix}
            \\text{ eigenvectors of } \\begin{bmatrix} 10 & 0\\\\
                                                        4 & 1\\\\
            \\end{bmatrix} \\text{?}$$
            <b>Solution:</b><br>
            Yes, both are.
            $$\\begin{bmatrix} 10 & 0\\\\ 4 & 1\\\\ \\end{bmatrix}
            \\begin{bmatrix} 0\\\\ 1\\\\ \\end{bmatrix}
            =
            1\\begin{bmatrix} 0\\\\ 1\\\\ \\end{bmatrix}
            $$
            $$
            \\begin{bmatrix} 10 & 0\\\\ 4 & 1\\\\ \\end{bmatrix}
            \\begin{bmatrix} 1\\\\ 4/9\\\\ \\end{bmatrix}
            =
            10
            \\begin{bmatrix} 1\\\\ 4/9\\\\ \\end{bmatrix}
            $$
            So we have explained <i>what</i> eigenvectors and eigenvalues are, but <i>how</i> can we find them? We use a special equation, called the <a href="/char_eqn"><i>characteristic equation</i></a>.
            </p>
            ''', "Resources": 
            '''
            Textbook:<br>
            <a href="http://linear.ups.edu/html/section-EE.html">A First Course in Linear Algebra: Eigenvectors and Eigenvalues</a>
            <br>Video:<br>
            <a href="https://www.khanacademy.org/math/linear-algebra/alternate-bases/eigen-everything/v/linear-algebra-introduction-to-eigenvalues-and-eigenvectors">Khan Academy: Eigenvalues and Eigenvectors</a>
            ''', "Visualization" :
            '''
            <p>
            <b>Try it now! 1:</b><br>
            Which of the following vectors are eigenvectors of matrix A?
            $$A= \\begin{bmatrix} 5 & 1 \\\\ -2 & 2 \\\\ \\end{bmatrix}$$
            $$v_1 = \\begin{bmatrix} 1 \\\\ 1\\\\ \\end{bmatrix}
            ,v_2 = \\begin{bmatrix} 1 \\\\ -1 \\\\ \\end{bmatrix}
            ,v_3 = \\begin{bmatrix} 2 \\\\  1 \\\\ \\end{bmatrix}
            ,v_4 = \\begin{bmatrix} 1 \\\\ -2 \\\\ \\end{bmatrix}
            $$

            <form name="trynow1" action="/eigenvalues" method="post" onsubmit="">

            <input type="checkbox" name="test1" id="A" value="a"> A
            <input type="checkbox" name="test1" id="B" value="b"> B
            <input type="checkbox" name="test1" id="C" value="c"> C
            <input type="checkbox" name="test1" id="A" value="d"> D<br>
            <input type="submit" value="Submit">
            </form>

            </p>
            ''' + "<b>" + result_text + "</b>"}
    nav[3]['Items'][0]['Current'] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/char_eqn", methods=['GET', 'POST'])
def char_eqn_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('char_eqn_module'))) #redirect to current page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    prev_point = request.cookies.get('point') #getting point data from cookie
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error handling block
            if request.form.getlist('test1') == ['a', 'c']:
                #If all answers are correct
                resp = make_response(redirect(url_for('char_eqn_module'))) #redirect to current page. To update cookie
                resp.set_cookie("char_eqn", "OK") #add progression data to cookie
                resp.set_cookie('point', str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "Your answer is incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("char_eqn"):
        nav[3]["Items"][1]["Complete"] = True #make checkmark
        result_text = "Correct, you earned 100 points"
    else:
        nav[3]["Items"][1]["Complete"] = False

    page = {"Description":
            '''
            <p>
            <h3>The Characteristic Equation</h3>
            In order to find the eigenvalues and eigenvectors of a matrix, we use the <i>Characteristic Equation</i>.<br>
            This equation is simple; take the determinant of the matrix with lambda begin subtracted from each diagonal value. This can be seen in the following example.
            <br><b>Example:</b><br>
            What are the eigenvalues of matrix A?
            $$ A = \\begin{bmatrix} 4 & 1\\\\ 2 & 5\\\\  \\end{bmatrix}$$
            $$ det\\begin{bmatrix} 4 - \\lambda & 1\\\\ 2 & 5 - \\lambda \\\\  \\end{bmatrix}$$
            $$=(4-\\lambda)(5-\\lambda) - (1)(2) = 20 + \\lambda^2 - 4\\lambda - 5\\lambda - 2$$
            $$=\\lambda^2 -9\\lambda + 18 $$
            $$=(\\lambda - 6)(\\lambda -3) $$
            From here we are able to see that the eigenvalues are 6 and 3.<br>
            </p>
            ''', "Resources": 
            '''
            Textbook:<br>
            <a href="http://linear.ups.edu/html/section-EE.html">A First Course in Linear Algebra: Eigenvectors and Eigenvalues</a>
            <br>Video:<br>
            <a href="https://www.khanacademy.org/math/linear-algebra/alternate-bases/eigen-everything/v/linear-algebra-introduction-to-eigenvalues-and-eigenvectors">Khan Academy: Eigenvectors and Eigenvalues</a>
            ''', "Visualization" :
            '''
            <p>
            <b>Try it now! 1:</b><br>
            What are the eigenvalues of matrix Z?
            $$ Z = \\begin{bmatrix} 4 & 3 \\\\ 1 & 6 \\\\ \\end{bmatrix}$$
            <form name="trynow1" action="/char_eqn" method="post" onsubmit="">

            <input type="checkbox" name="test1" id="A" value="a"> 7
            <input type="checkbox" name="test1" id="B" value="b"> 5
            <input type="checkbox" name="test1" id="C" value="c"> 3
            <input type="checkbox" name="test1" id="D" value="d"> 1<br>
            <input type="submit" value="Submit">
            </form>

            </p>
            ''' + "<b>" + result_text + "</b>"}
    nav[3]["Items"][1]["Current"] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/matrix_mult", methods=['GET', 'POST'])
def matrix_mult_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('matrix_mult_module'))) #redirect to current page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    prev_point = request.cookies.get('point') #getting point data from cookie
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error handling block
            if request.form['test1'] == "e" and request.form['test2'] == 'none':
                #If all answers are correct
                resp = make_response(redirect(url_for('matrix_mult_module'))) #redirect to current page. To update cookie
                resp.set_cookie('mult', "OK") #add progression data to cookie
                resp.set_cookie('point', str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "One or more answers are incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("mult"):
        nav[1]["Items"][2]["Complete"] = True #make checkmark 
        result_text = "Correct, you earned 100 points"
    else:
        nav[1]["Items"][2]["Complete"] = False

    page = {"Description":
            '''
            <p>
            <h3>Matrix Multiplication</h3>
            Matrix multiplication is quite different than number multiplication.<br>
            One way that we like to think about it is that
            <br>Examine the following matrix multiplication equation:
            $$A=\\begin{bmatrix} a_{11} & a_{12} \\\\ a_{21} & a_{22} \\\\ \\end{bmatrix}
            ,B = \\begin{bmatrix} b_{11} & b_{12} \\\\ b_{21} & b_{22} \\\\ \\end{bmatrix}
            $$
            $$AB = \\begin{bmatrix} (a_{11}b_{11} + a_{12}b_{12}) & (a_{11}b_{21} + a_{12}b_{22}) \\\\
                                    (a_{21}b_{11} + a_{22}b_{12}) & (a_{21}b_{21} + a_{22}b_{22}) \\\\
                                    \\end{bmatrix}$$

            We can see that the topleft most element is simply the <a href="/inner_product">inner product</a> of the row of A and the column of B, and the rest of the elements in the new matrix follow this pattern.

            <br>It may be obvious now that for this process to work, the number of columns in the left matrix must equal the number of rows in the right matrix. That is,
            $$X = \\begin{bmatrix} 5 & 1 & 2 \\\\ -1 & 4 & 3 \\\\ -2 & 0 & 9 \\\\ \\end{bmatrix}
            ,Y = \\begin{bmatrix} 1 & 4 & 2 \\\\ -2 & -2 & 2 \\\\ \\end{bmatrix}
            $$
            XY is not a valid matrix multiplication, because matrix X has 3 columns and matrix Y has 2 rows.<br>
            <b>Example:</b><br>
            $$\\text{What is the result of matrix Q multiplied by matrix S?}$$
            $$Q = \\begin{bmatrix} 1 & 3 & -3 \\\\ 2 & 5 & -2 \\\\ \\end{bmatrix}
            ,S = \\begin{bmatrix} 3 & 4 & 1 & 0 \\\\ 2 & 0 & -1 & 1 \\\\ 1 & -2 & 3 & 0 \\\\ \\end{bmatrix}$$
            <b>Answer:</b>
            $$QS = \\begin{bmatrix} (3*1 + 3*2 + 1*-3) & (1*4 + 3*0 + -3*-2) & (1*1 + 3*-1 + -3*3) & (1*0 + 3*1 + -3*0) \\\\
                    (2*3 + 5*2 + -2*1) & (2*4 + 5*0 + -2*-2) & (2*1 + 5*-1 + -2*3) & (2*0 + 5*1 + -2*0) \\\\ \\end{bmatrix}
                    $$
            $$QS = \\begin{bmatrix} (3 + 6 -3) & (4 + 0 + 6) & (1 - 3 - 6) & (0+3 + 0) \\\\ (6 + 10 -2) & (8 + 0 + 4) & (2 - 5 - 6) & (0 + 5 + 0) \\\\ \\end{bmatrix}$$
            $$QS = \\begin{bmatrix} 6 & 10 & -11 & 3 \\\\ 14 & 12 & -9 & 5 \\\\ \\end{bmatrix}$$

            </p>
            ''', "Resources": 
            '''
            Textbook:<br>
            <a href="http://linear.ups.edu/html/section-MM.html">A First Course in Linear Algebra: Matrix Multiplication</a>
            <br>Video:<br>
            <a href="https://www.khanacademy.org/math/linear-algebra/matrix-transformations/modal/v/linear-algebra-matrix-product-examples">Khan Academy: Matrix Product examples</a>

            ''', "Visualization" :
            '''
            <p>
            <b>Try it now! 1:</b><br>
            What matrix is the result of A*B?
            $$A = \\begin{bmatrix} 1 & 2 \\\\ -2 & -1 \\\\ \\end{bmatrix}
            ,B = \\begin{bmatrix} 1 & 1 \\\\ 3 & -3 \\\\ \\end{bmatrix}$$
            $$C = \\begin{bmatrix} -7 & -5 \\\\ 5 & -1 \\\\ \\end{bmatrix},
            D = \\begin{bmatrix} 7 & 5 \\\\ 5 & 1 \\\\ \\end{bmatrix},
            E = \\begin{bmatrix} 7 & -5 \\\\ -5 & 1 \\\\ \\end{bmatrix}
            ,F = \\begin{bmatrix} -7 & 5 \\\\ 5 & -1 \\\\ \\end{bmatrix}$$
            <form name="trynow1" action="/matrix_mult" method="post" onsubmit="">

            <input type="radio" name="test1" id="C" value="c"> C
            <input type="radio" name="test1" id="D" value="d"> D
            <input type="radio" name="test1" id="E" value="e"> E
            <input type="radio" name="test1" id="F" value="f"> F
            <input type="radio" name="test1" id="none" value="none">Not possible<br>

            <b>Try it now! 2:</b><br>
            What matrix is the result of X*Y?
            $$X = \\begin{bmatrix} 1 & 2 & 1 \\\\ -2 & -1  & 1\\\\ \\end{bmatrix}
            ,Y = \\begin{bmatrix} 1 & 1 \\\\ 3 & -3 \\\\ \\end{bmatrix}$$
            $$L = \\begin{bmatrix} -7 & -5 \\\\ 5 & -1 \\\\ \\end{bmatrix},
            M = \\begin{bmatrix} 7 & 5 \\\\ 5 & 1 \\\\ \\end{bmatrix},
            N = \\begin{bmatrix} 7 & -5 \\\\ -5 & 1 \\\\ \\end{bmatrix}
            ,O = \\begin{bmatrix} -7 & 5 \\\\ 5 & -1 \\\\ \\end{bmatrix}$$
            <input type="radio" name="test2" id="L" value="l"> L
            <input type="radio" name="test2" id="M" value="m"> M
            <input type="radio" name="test2" id="N" value="n"> N
            <input type="radio" name="test2" id="O" value="o"> O
            <input type="radio" name="test2" id="none" value="none">Not possible<br>
            <input type="submit" value="Submit">
            </form>

            </p>
            ''' + "<b>" + result_text + "</b>"}
    nav[1]["Items"][2]["Current"] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)


@application.route("/determinants", methods=['GET', 'POST'])
def determinants_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('determinants_module'))) #redirect to current page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    prev_point = request.cookies.get('point') #getting point data from cookie
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error handling block
            if request.form.getlist('test1') == ["a"]:
                #If all answers are correct
                resp = make_response(redirect(url_for("determinants_module"))) #redirect to current page. To update cookie
                resp.set_cookie("determinant", "OK") #add progression data to cookie
                resp.set_cookie('point', str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "Your answer is incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("determinant"):
        nav[1]["Items"][3]["Complete"] = True #make checkmark
        result_text = "Correct, you earned 100 points"

    else:
        nav[1]["Items"][3]["Complete"] = False


    page = {"Description":
            '''
            <p>

            <h3>Determinant of 2x2 Matrices</h3>
            We start our discussion on how to get the determinant of a 2x2 matrix. This is because getting the determinant of a 2x2 matrix is quite easy.
            <br><b>Example 1</b><br>
            What is the determinant of matrix A?
            $$A =  \\begin{bmatrix} a & b \\\\ c & d \\\\ \\end{bmatrix}$$
            <b>Answer:</b>
            $$ detA = ad - bc$$
            <b>Example 2:</b><br>
            What is the determinant of matrix B?
            $$B = \\begin{bmatrix} 4 & 5 \\\\ 1 & 3\\\\ \\end{bmatrix}$$
            <b>Answer:</b>
            $$detB = (4)(3) - (5)(1) = 12 - 5 = 7$$
            <h3>Determinant of NxN matrices</h3>
            There are multiple methods for getting the determinant of any size square matrix.
            They are all rather in-depth, so we chose to include video links to explain this topic, listed in the resources section.


            </p>
            ''', "Resources":
            '''
            <p>
            Textbook:
           <a href="http://linear.ups.edu/html/section-DM.html">A First Course in Linear Algebra: Determinants</a>
           <br>Khan Academy:
            <a href="https://www.khanacademy.org/math/linear-algebra/matrix-transformations/inverse-of-matrices/v/linear-algebra-nxn-determinant">NxN Determinants</a>
            </p>
            ''', "Visualization" :
            '''
            <p>
            <b>Try it now! 1:</b><br>
            What is the determinant of matrix A?
            $$A = \\begin{bmatrix} 4 & 1 \\\\ 2 & -5 \\\\ \\end{bmatrix}$$
            <form name="trynow1" action="/determinants" method="post" onsubmit="">

            <input type="checkbox" name="test1" id="A" value="a"> -22<br>
            <input type="checkbox" name="test1" id="B" value="b"> -20<br>
            <input type="checkbox" name="test1" id="C" value="c"> 14<br>
            <input type="checkbox" name="test1" id="A" value="d"> 13<br>
            <input type="submit" value="Submit">
            </form>

            </p>
            ''' + "<b>" + result_text + "</b>"}
    nav[1]["Items"][3]["Current"] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/inner_products", methods=['GET', 'POST'])
def inner_product_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('inner_product_module'))) #redirect to curret page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    prev_point = request.cookies.get('point') #getting point data from cookie
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method (checking answers)
    if request.method == 'POST':
        try: #error handling block
            if request.form['test1'] == "d" and request.form['test2'] == "d":
                #If all answers are correct
                resp = make_response(redirect(url_for("inner_product_module"))) #redirect to current page. To update cookie
                resp.set_cookie("inner", "OK") #add progression data to cookie
                resp.set_cookie("point", str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "Your answer is incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("inner"):
        nav[2]["Items"][2]["Complete"] = True #make checkmark
        result_text = "Correct, you earned 100 points"
    else:
        nav[2]["Items"][2]["Complete"] = False

    page = {"Description":
            '''
            <p>
            <h3>Inner products of vectors</h3>
            For two vectors, u and v, the inner product is the <a href="">transpose</a> of u multiplied by vector v, using <a href="">matrix multiplication.</a><br>
            This can be seen below:<br>
            $$u * v = u^Tv$$
            This will result in a 1x1 matrix, a single value. This can be seen because we know that the result of matrix multiplication is a matrix with the number of rows from the left matrix and the number of columns from the right matrix. <br>

            Another common term for inner product is dot product.<br>
            <b>Example 1:</b><br>
            What is the inner product of vectors x and z?
            $$ x = \\begin{bmatrix} 5 \\\\ 4 \\\\ 3\\\\ \\end{bmatrix},
            u = \\begin{bmatrix} 2 \\\\ 1 \\\\ 0 \\\\ \\end{bmatrix}$$
            <b>Answer:</b>
            $$ x*z = x^Tz$$
            $$= \\begin{bmatrix} 5 & 4 & 3 \\\\ \\end{bmatrix} \\begin{bmatrix} 2 \\\\ 1\\\\ 0\\\\ \\end{bmatrix}$$
            $$= (5)(2) + (4)(1) + (3)(0) = 14$$
            </p>
            ''', "Resources": 
            '''
            Textbook:<br>
            <a href="http://linear.ups.edu/html/section-O.html">A First Course in Linear Algebra: Orthogonalization</a>
            Video:<br>
            <a href="https://www.khanacademy.org/math/linear-algebra/vectors-and-spaces/dot-cross-products/v/vector-dot-product-and-vector-length">Khan Academy: Dot Product</a>
            ''', "Visualization" :
            '''
            <p>
            <b>Try it now! 1:</b><br>
            What is the result of v*x?
            $$v = \\begin{bmatrix} 1 \\\\ 2 \\\\ 3 \\\\ \\end{bmatrix}
            ,x = \\begin{bmatrix} -2 \\\\ 1 \\\\ -2 \\\\ \\end{bmatrix}$$

            <form name="trynow1" action="/inner_products" method="post" onsubmit="">

            <input type="radio" name="test1" id="A" value="a"> 4<br>
            <input type="radio" name="test1" id="B" value="b"> -4<br>
            <input type="radio" name="test1" id="C" value="c"> 6<br>
            <input type="radio" name="test1" id="A" value="d"> -6<br>

            <b>Try it now! 2:</b><br>
            What is the result of z*y?
            $$z = \\begin{bmatrix} 10 \\\\ 2 \\\\ 5 \\\\ -2 \\\\ \\end{bmatrix}
            ,y = \\begin{bmatrix} -4 \\\\ 12 \\\\ -2 \\\\ 0 \\\\ \\end{bmatrix}$$


            <input type="radio" name="test2" id="A" value="a"> 24<br>
            <input type="radio" name="test2" id="B" value="b"> -24<br>
            <input type="radio" name="test2" id="C" value="c"> 26<br>
            <input type="radio" name="test2" id="A" value="d"> -26<br>
            <input type="submit" value="Submit">
            </form>

            </p>
            ''' + "<b>" + result_text + "</b>"}
    nav[2]["Items"][2]["Current"] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/orthogonal_vectors", methods=['GET', 'POST'])
def orth_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('orth_module'))) #redirect to current page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    prev_point = request.cookies.get('point') #getting point data from cookie
    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error handling block
            if request.form.getlist('test1') == ['a', 'd'] and request.form['test2'] == 'o':
                #If all answers are correct
                resp = make_response(redirect(url_for("orth_module"))) #redirect to current page. To update cookie
                resp.set_cookie("orth", "OK") #add progression data to cookie
                resp.set_cookie('point', str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "Your answer is incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("orth"):
        nav[2]["Items"][3]["Complete"] = True #make checkmark
        result_text = "Correct, you earned 100 points"
    else:
        nav[2]["Items"][3]["Complete"] = False

    page = {"Description":
            '''
            <p>
            <h3>Orthogonal Vectors</h3>
            We define two vectors to be orthogonal to each other if the inner product of the two vectors equals zero. That is, vectors u and v are orthogonal if:
            $$ u \\cdot v = 0$$
            We say that a set of vectors are orthogonal if for each vector in the set, the inner product of all other vectors in the set equals 0.
            <h3>Orthonormal Vectors</h3>
            We say that two vectors are orthonormal is they are orthogonal, and also unit vectors. <br>
            A unit vector is a vector with <i>length</i> 1.<br>
            <b>Definition:</b><br>
            The length of a vector is the square root of the inner product of itself, shown below:
            $$ \\text{Length of v = ||v|| = } \\sqrt{v \\cdot v}$$
            In order to make the orthogonal vectors orthonormal, we <i>normalize</i> the vectors.
            <br><b>Definition:</b><br>
            To normalize a vector, making it a unit vector which has length 1, we divide the vector by its length. That is:
            $$ \\text{Unit vector of v = } \\frac{1}{||v||}v$$
            We say that a set of vectors is an orthonormal set it is an orthogonal set and each vector is a unit vector.
            </p>
            ''', "Resources": 
            '''
            Textbook:<br>
            <a href="http://linear.ups.edu/html/section-O.html">A First Course in Linear Algebra: Orthogonalization</a>
            ''', "Visualization" :
            '''
            <p>
            <b>Try it now! 1:</b><br>
            $$\\text{Which vectors are orthogonal to } \\begin{bmatrix} 3 \\\\ 2 \\\\ -2 \\\\ \\end{bmatrix}$$
            $$a = \\begin{bmatrix} 0 \\\\ 1\\\\ 1\\\\ \\end{bmatrix}
            ,b = \\begin{bmatrix} 4 \\\\ 1 \\\\ -2 \\\\ \\end{bmatrix}
            ,c = \\begin{bmatrix} -3 \\\\ -2 \\\\ 2 \\\\ \\end{bmatrix}
            ,d = \\begin{bmatrix} 2 \\\\ 0 \\\\ 3 \\\\ \\end{bmatrix}$$

            <form name="trynow1" action="/orthogonal_vectors" method="post" onsubmit="">

            <input type="checkbox" name="test1" id="A" value="a">A
            <input type="checkbox" name="test1" id="B" value="b">B
            <input type="checkbox" name="test1" id="C" value="c">C
            <input type="checkbox" name="test1" id="A" value="d">D<br>

            <b>Try it now! 2:</b><br>
            $$\\text{Let x = }\\begin{bmatrix} 4 \\\\ 0 \\\\ -3 \\\\ \\end{bmatrix}$$
            $$\\text{Which vector is a unit vector in the same direction as x?}$$
            $$l = \\begin{bmatrix} 4/25 \\\\ 0 \\\\ -3/25 \\\\ \\end{bmatrix},
            m = \\begin{bmatrix} 4 \\\\ 0 \\\\ 3 \\\\ \\end{bmatrix},
            n = \\begin{bmatrix} 9 \\\\ 5 \\\\ 2 \\\\ \\end{bmatrix},
            o = \\begin{bmatrix} 4/5 \\\\ 0 \\\\ -3/5 \\\\ \\end{bmatrix}$$


            <input type="radio" name="test2" id="L" value="l"> l<br>
            <input type="radio" name="test2" id="M" value="m"> m<br>
            <input type="radio" name="test2" id="N" value="n"> n<br>
            <input type="radio" name="test2" id="O" value="o"> o<br>
            <input type="submit" value="Submit">
            </form>

            </p>
            ''' + "<b>" + result_text + "</b>"}
    nav[2]['Items'][3]['Current'] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/linear_combo", methods=['GET', 'POST'])
def span_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('span_module'))) #redirect to current page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    prev_point = request.cookies.get('point') #getting point data from cookie
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error handling block
            if request.form['test1'] == 'w':
                #If all answers are correct
                resp = make_response(redirect(url_for('span_module'))) #redirect to current page. To update cookie
                resp.set_cookie('span', "OK") #add progression data to cookie
                resp.set_cookie('point', str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "Your answer is incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question." 
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("span"):
        nav[2]["Items"][1]["Complete"] = True #make checkmark
        result_text = "Correct, you earned 100 points"
    else:
        nav[2]["Items"][1]["Complete"] = False

    page = {"Description":
            '''
            <p>
            <h3>Linear Combinations of Vectors</h3>
            A linear combination is as it sounds, a combination of vectors that become a new vector. <br>
            For instance, with the following vectors:
            $$a = \\begin{bmatrix} 6 \\\\ 10 \\\\ \\end{bmatrix}
            b = \\begin{bmatrix} 0 \\\\ 2 \\\\ \\end{bmatrix}
            c = \\begin{bmatrix} 2 \\\\ 2 \\\\ \\end{bmatrix}
            $$
            We can say that a is a linear combination of vectors b and c, because
            $$\\begin{bmatrix} 6 \\\\ 10 \\\\ \\end{bmatrix}
             = 2\\begin{bmatrix} 0 \\\\ 2 \\\\ \\end{bmatrix}
            + 3\\begin{bmatrix} 2 \\\\ 2 \\\\ \\end{bmatrix}
            $$
            From the previous example we can see that their could be an infinite amount of linear combinations, thus we need terminology to express the entire set of linear combinations between vectors.
            <h3>Spanning Sets</h3>
            A spanning set is the entire list of linear combinations over a set of vectors. Another way to describe spanning sets:
            The spanning set of a set of vectors: $$v_1,v_2,...,v_n$$
            is the list of all possible ways to write:
            $$c_1v_1+c_2v_2+...+c_nv_n$$
            $$\\text{where } c_1,...,c_n \\text{ are scalars.}$$
            How can we find this spanning set?
            </p>
            ''', "Resources":
            '''
            Textbook:<br>
            <a href="http://linear.ups.edu/html/section-LC.html">A First Course in Linear Algebra: Linear Combinations</a>
            <br>Video:<br>
            <a href="https://www.khanacademy.org/math/linear-algebra/vectors-and-spaces/linear-combinations/v/linear-combinations-and-span">Khan Academy: Linear Combinations</a>
            ''', "Visualization" :
            '''
            <p>
            <b>Try it now! 1:</b><br>
            Which vector is a linear combination of vectors a and b?
            $$a = \\begin{bmatrix} 3 \\\\ -2 \\\\ \\end{bmatrix},
            b = \\begin{bmatrix} -4 \\\\ 1 \\\\ \\end{bmatrix}
            $$
            $$
            w = \\begin{bmatrix} 0 \\\\ 5 \\\\ \\end{bmatrix},
            x = \\begin{bmatrix} 5 \\\\ 0 \\\\ \\end{bmatrix},
            y = \\begin{bmatrix} 1 \\\\ 5 \\\\ \\end{bmatrix},
            z = \\begin{bmatrix} 5 \\\\ 1 \\\\ \\end{bmatrix}
            $$

            <form name="trynow1" action="/linear_combo" method="post" onsubmit="">

            <input type="radio" name="test1" id="W" value="w"> w
            <input type="radio" name="test1" id="X" value="x"> x
            <input type="radio" name="test1" id="Y" value="y"> y
            <input type="radio" name="test1" id="Z" value="z"> z<br>
            <input type="submit" value="Submit">
            </form>

            </p>
            ''' + "<b>" + result_text + "</b>"}
    nav[2]["Items"][1]["Current"] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/vector_spaces", methods=['GET', 'POST'])
def vector_spaces_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('vector_spaces_module'))) #redirect to current page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    prev_point = request.cookies.get('point') #getting point data from cookie
    checking_topics(nav) #checking all the topics' cookie data

    if request.method == 'POST':
        try: #error handling block
            if request.form['ans0'] == "no" and request.form['ans1'] == "yes" and request.form['ans2'] == "yes":
                #If all answers are correct
                resp = make_response(redirect(url_for('vector_spaces_module'))) #redirect to current page. To update cookie
                resp.set_cookie("vector_space", "OK") #add progression data to cookie
                resp.set_cookie("point", str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "One or more answers are incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("vector_space"):
        nav[4]["Items"][0]["Complete"] = True #make checkmark
        result_text = "Correct, you earned 100 points"
    else:
        nav[4]["Items"][0]["Complete"] = False

    page = {"Description":

        '''

        <h3>What Is A Vector Space?</h3>

        <p>Vector spaces are sets, or collections, of vectors satisfying a group
        of 10 rules when we perform the operations of addition and subtraction
        on them. This is a powerful concept because a vector space can be
        generalized to include much more than simply 2-dimensional arrows in
        a plane. For any collection of vectors \(u,v,w \\in V \\text{ and  }
        \\ c,d \\in \\mathbb{R}\) these rules are:</p><br>
        <ol>
        <li> \( u + v \in V \\ \) (Additive Closure)</li>
        <li> \( u + v = v + u \\ \) (Commutativity)</li>
        <li> \( u + (v + w) = (u + v) + w \\ \) (Associativity)</li>
        <li> \( 0 \\in V \\ \) when \( \\ 0 + u = u \) (Existence of a Zero)</li>
        <li> \(u + (-u) = 0 \\ \) for every \( \\ u \) (Additive Inverse)</li>
        <li> \(cu \\in V \) (Scalar Closure)</li>
        <li> \( c(u+v) = cu + cv \) (Scalar Multiplicative Associativity)</li>
        <li> \( (c+d)u = cu + du \) (Distributivity Across Scalar Addition)</li>
        <li> \( c(du) = (cd)u \) (Associativity of Scalar Multiplication)</li>
        <li> \( 1u = u \) (Existence of One) </li>
        </ol>

        <p>Note that some sources will list these rules in a different order.
        This list is not a ranking. All of the rules must be satisfied for a
        collection of vectors to be considered a vector space.</p>

        <h3>What are some examples of vector spaces?</h3>

        <p>You may be wondering what is the motivation for categorizing vectors
        in this way. Actually, vector spaces show up all over the place.
        In fact, some vector spaces may not resemble our traditional
        conceptions of vectors. The idea of a vector is much more general
        than a 2-dimensional arrow.</p>

        <p>When we reason about the elements of a vector space we are really
        considering any object that is an element of a space with the
        properties described above. For example, the set of all 2-dimensional
        vectors is actually a vector space, and so is the set of all
        3-dimensional vectors, but so is the set of all 2x2 matrices!
        Granted, a 2x2 matrix does not match our traditional notions of what a
        vector is, but the set of all 2x2 matrices,
        denoted as \(\mathbb{M}_2\), does obey the rules above.</p>

        <p>In fact, the general concept of a vector space can include any
        sort of mathematical object that follows the above rules. Even sets
        of polynomials can be vector spaces! For example, \(\mathbb{P}_2\),
        which is the set of all polynomials of degree 2, forms a vector space.
        We can add polynomials of degree 2 together and they are still
        in \(\mathbb{P}_2\). For example, take \( a = 1 + x^2 \) and
        \( b = 2 + 3x + 4x^2 \). Then if \( c = a + b \),
        \( c = 3 + 3x + 5x^2 \), which is also in \(\mathbb{P}_2\). You should
        prove to yourself that these polynomial "vectors" in \( \mathbb{P}_2 \ \)
        also satisfy all the other rules above.
        </p>

        <p>Other types of functions can be elements of a vector space.
        In fact, the set of all real valued continuous functions \(F\) is
        a vector space. You should verify this for yourself by considering
        the 10 rules and how they apply to functions of this type.</p>


        ''',
        "Resources": '''
        <a href="http://www.physics.miami.edu/%7Enearing/mathmethods/vector_spaces.pdf">http://www.physics.miami.edu/%7Enearing/mathmethods/vector_spaces.pdf</a><br>
        <a href="http://linear.ups.edu/html/section-VS.html">http://linear.ups.edu/html/section-VS.html</a><br>
        <a href="https://en.wikipedia.org/wiki/Vector_space">https://en.wikipedia.org/wiki/Vector_space</a><br>
        <a href="http://mathworld.wolfram.com/VectorSpace.html">http://mathworld.wolfram.com/VectorSpace.html</a><br>
        ''',
        "Visualization": '''
                <p>

                <form name="trynow1" form action="/vector_spaces" form method='post'>

                Is the set of all 2D vectors with only <em> positive </em>
                values a vector space? That is,
                \( V = \{ \\begin{bmatrix} x \\\\ y \\end{bmatrix} \\
                 | \\ x,y \ge 0 \} \) <br>

                <input type="radio" name="ans0" value="yes"> Yes<br>
                <input type="radio" name="ans0" value="no"> No<br>

                <br>How about the set of all line segments on the real line?<br>

                <input type="radio" name="ans1" value="yes"> Yes<br>
                <input type="radio" name="ans1" value="no"> No<br>

                <br>How about the set of all complex numbers, \( \\mathbb{C} \)? <br>

                <input type="radio" name="ans2" value="yes"> Yes<br>
                <input type="radio" name="ans2" value="no"> No<br>

                <br><input type="submit" value="Submit">
                </form>


                </p>
        ''' + "<b>" + result_text + "</b>"}
    nav[4]["Items"][0]["Current"] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/subspaces", methods=['GET', 'POST'])
def subspaces_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('subspaces_module'))) #redirect to current page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    prev_point = request.cookies.get('point') #getting point data from cookie
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error catching block
            if request.form['ans0'] == "no" and request.form['ans1'] == 'yes':
                #If all answers are correct
                resp = make_response(redirect(url_for('subspaces_module'))) #redirect to current page. To update cookie
                resp.set_cookie("subspace", "OK") #add progression data to cookie
                resp.set_cookie('point', str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "One or more answers are incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("subspace"):
        nav[4]["Items"][1]["Complete"] = True #make checkmark
        result_text = "Correct, you earned 100 points"
    else:
        nav[4]["Items"][1]["Complete"] = False

    page = {"Description":
    '''
    <h3>What is a subspace?</h3>

    <p>A vector space that is contained inside of some other vector space is known as a subspace.
    So whenever a vector space is a subspace we have a vector space that is also part of another larger vector space!</p>

    <p>A simple example of this is the set of all coordinate vectors in the Cartesian plane, or
    \( \\ (x,y) \) in \( \\mathbb{R}^2 \) where \(x = y\). It is easy to verify that this set,
    which we shall call \( V \), is a vector space. Furthermore, \( V \in \\mathbb{R}^2 \),
    which is also a vector space, so \( V \) is a <em>subspace</em> of \( \\mathbb{R}^2 \)!</p>

    <p>Consider also any subset of vectors that "live" in the plane \( z = 0 \) in \( \\mathbb{R}^2 \).
    This includes 3-dimensional elements like <br>
    \( \\begin{bmatrix} 3 \\\\ 4 \\\\ 0 \\end{bmatrix} \) and
    \( \\begin{bmatrix} 7 \\\\ -10 \\\\ 0 \\end{bmatrix} \) but not
    \( \\begin{bmatrix} 7 \\\\ -10 \\\\ 1 \\end{bmatrix} \). <br>
    All vectors in \( W \) exist in the plane \( z = 0 \) and \( W \) is a
    vector space because it satisfies the 10 rules we have already gone over.
    Also, since \( W \in \\mathbb{R}^3 \) and \( \\mathbb{R}^3 \) is a vector space,
    \( W \) is a subspace of \( \\mathbb{R}^3 \).</p>

    <p>Can you think of any other examples of subspaces? How about \( \mathbb{P}_2 \)?
    Is this polynomial vector space a subspace of anything?
    Try the problems in the quiz section!</p>

    ''',
    "Resources":
    '''
            <a href="http://www.physics.miami.edu/%7Enearing/mathmethods/vector_spaces.pdf">http://www.physics.miami.edu/%7Enearing/mathmethods/vector_spaces.pdf</a><br>
            <a href="http://linear.ups.edu/html/section-VS.html">http://linear.ups.edu/html/section-VS.html</a><br>
            <a href="https://en.wikipedia.org/wiki/Vector_space">https://en.wikipedia.org/wiki/Vector_space</a><br>
            <a href="http://mathworld.wolfram.com/VectorSpace.html">http://mathworld.wolfram.com/VectorSpace.html</a><br>
    ''',
    "Visualization":
    '''

                    <p>
                    <form name="trynow1" form action="" form method='post'>
                    How about the plane \(z = 1\) in \(\\mathbb{R}^3\)? Do
                    the vectors in this plane form a subspace of \( \\mathbb{R}^3\)?
                    [HINT: Think about "Scalar Closure".] <br>

                    <input type="radio" name="ans0" value="yes"> Yes<br>
                    <input type="radio" name="ans0" value="no"> No<br>

                    <br>Are the 2D real diagonal matrices
                    a subspace of \( \\mathbb{M}_2 \)?
                    These are of the form
                    \( \\begin{bmatrix} a & 0 \\\\ 0 & b \\end{bmatrix} \)
                    where \( a,b \in \\mathbb{R} \) <br>

                    (Answer should be yes) <br>
                    <input type="radio" name="ans1" value="yes"> Yes<br>
                    <input type="radio" name="ans1" value="no"> No<br>


                    <br><input type="submit" value="Submit">
                    </form>


                    </p>
    ''' + "<b>" + result_text + "</b>"}
    nav[4]["Items"][1]["Current"] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/linear_transformations", methods=['GET', 'POST'])
def linear_transformations_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('linear_transformations_module'))) #redirect to current page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    prev_point = request.cookies.get('point') #getting point data from cookie
    checking_topics(nav)#checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error handling block 
            #If all answers are correct
            if request.form['ans0'] == "no" and request.form['ans1'] == 'c':
                resp = make_response(redirect(url_for('linear_transformations_module'))) #redirect to current page. To update cookie
                resp.set_cookie("Ltransform", "OK") #add progression data to cookie
                resp.set_cookie('point', str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "One or more answers are incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("Ltransform"):
        nav[5]["Items"][0]["Complete"] = True #make checkmark
        result_text = "Correct, you earned 100 points"
    else:
        nav[5]["Items"][0]["Complete"] = False

    page = {"Description":
    '''
    <h3>What is a Linear Transformation?</h3>
    <p>We have discussed the very basics of vector spaces. But how might we
    take elements from one vector space and <em>transfer</em> them into some
    other vector space? Usually in mathematics, when we wish to map an object
    from one space to another space we use a function. Functions are exactly
    what we need to map elements of a vector space into another vector space.</p>

    <p>A <em>linear transformation</em> is any functional mapping between vector
    spaces with the following properties: <br><br>
    <em> For a linear transformation \( \\ T : U \\rightarrow V \) </em>
    <ol>
    <li> \( T(a + b) = T(a) + T(b)\) for all \(a,b \in U\) </li>
    <li> \( T(ma) = mT(a) \) for all \(a \in U\) and \(m \in \mathbb{C}\)
    (Where \( \mathbb{C} \) is the complex numbers )</li>
    </ol>
    You may be surprised to see complex numbers in here. We have not
    discussed them much, but vector spaces of complex numbers exist, so we need
    to account for that in our definition. Basically this definition states that
    any functional mapping between vector spaces must satisfy the 2 conditions
    above.</p>

    <h3>Examples</h3>
    <ul>
    <li>
    The identity transformation. A function that maps a vector space into itself!
    </li>
    <li>
    We can transform vectors in \( \\mathbb{R}^2 \) into vectors in
    \(\\mathbb{R}^3\). For example, let:
    $$ T = f(x,y) = \\begin{bmatrix} x \\\\ y - x \\\\ y \\end{bmatrix} $$
    where vectors in \( V = \\mathbb{R}^2 \) are represented as:
    $$ \\begin{bmatrix} x \\\\ y \\end{bmatrix} $$
    and vectors in \( W = \\mathbb{R}^3 \) are represented as:
    $$ \\begin{bmatrix} x \\\\ y \\\\ z \\end{bmatrix} .$$
    Then the transformation \( T : V \\rightarrow W \) is a linear transformation.
    You should choose some arbitrary 2D vectors and try
    this yourself to verify that the transformation follows both rules above.

    </li>
    <li>
    The projection of a 2D vector (vectors in \( \\mathbb{R}^2)\) onto the
    y-axis! In this case we have a function \( T : U \\rightarrow V \) where:<br>
    \(U = \) vectors in \(\\mathbb{R}\)<br>
    \(V = \) all vectors in \(\\mathbb{R}\) of the form
    $$ \\begin{bmatrix} 0 \\\\ y \\end{bmatrix}$$ where \(y \in \\mathbb{R} \)<br>
    and \(T = \\begin{bmatrix} 0 & 0 \\\\ 0 & 1 \\end{bmatrix}\)<br>
    You should verify for yourself that \(T\) does indeed project all 2D vectors
    onto the y-axis. Can you think of how to project all 2D vectors onto the
    x-axis? We will discuss projections more when we go over other 2D matrix
    transformations in the bonus module about 2D graphics!
    </li>

    ''',
    "Resources":
    '''

                <a href="http://linear.ups.edu/html/section-LT.html">http://linear.ups.edu/html/section-LT.html</a><br>
                <a href="https://en.wikipedia.org/wiki/Linear_map">https://en.wikipedia.org/wiki/Linear_map</a><br>

    ''',
    "Visualization":
    '''

    <p>
    <form name="trynow1" form action="" form method='post'>
    Let \( Q = \\mathbb{R}^2 \), \( W = \\mathbb{R} \), and define a function
     \( f : Q \\rightarrow W \) where \( f(x,y) = xy \). Thus, this function takes
      vectors in \( \\mathbb{R}^2 \) and maps them to scalars in \( \\mathbb{R} \).
       Is this a linear transformation?<br>

    <input type="radio" name="ans0" value="yes"> Yes<br>
    <input type="radio" name="ans0" value="no"> No<br>

    <br> Which of these functions maps vectors in \( \\mathbb{R}^2 \) onto the
     plane \( z = 0 \) in \( \\mathbb{R}^3 \)? <br>

    <input type="radio" name="ans1" value="a"> \( f(x,y) =
    \\begin{bmatrix} x \\\\ 0 \\\\ 0 \\end{bmatrix} \) <br>
    <input type="radio" name="ans1" value="b"> \( f(x,y) =
    \\begin{bmatrix} x \\\\ y \\\\ 1 \\end{bmatrix} \) <br>
    <input type="radio" name="ans1" value="c">  \( f(x,y) =
    \\begin{bmatrix} x \\\\ y \\\\ 0 \\end{bmatrix} \) <br>
    <input type="radio" name="ans1" value="d"> \( f(x,y) =
    \\begin{bmatrix} y \\\\ x \\\\ 0 \\end{bmatrix} \) <br>


    <br><input type="submit" value="Submit">
    </form>


    </p>
    ''' + "<b>" + result_text + "</b>"}
    nav[5]["Items"][0]["Current"] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/inject_surject", methods=['GET', 'POST'])
def inject_surject_module():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('inject_surject_module'))) #redirect to current page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    prev_point = request.cookies.get('point') #getting point data from cookie
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error catching block
            #If all answers are correct
            if request.form['ans0'] == "yes" and request.form['ans1'] == "yes" and request.form["ans2"] == "d":
                resp = make_response(redirect(url_for('inject_surject_module'))) #redirect to current page. To update cookie
                resp.set_cookie('inject', 'OK') #add progression data to cookie
                resp.set_cookie('point', str(int(prev_point) + 100)) #add 100 points and update cookie data
                return resp
            else:
                result_text = "One or more answers are incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("inject"):
        nav[5]["Items"][1]["Complete"] = True #make checkmark
        result_text = "Correct, you earned 100 points"
    else:
        nav[5]["Items"][1]["Complete"] = False

    page = {"Description":
    '''
    <p>Injection and surjection are very useful concepts in the mathematics of
    functional mappings. Since linear transformations are
    a type of functional mapping it is useful to understand these concepts.</p>

    <p>An injective mapping, often called a <em>one-to-one</em> mapping means
    very much what you might think "one-to-one" means. A linear transformation
    \( T : U \\rightarrow V \) is <em>injective</em> if for every mapping
    \(T(x) = T(y) \) we have \( x = y \). That is, getting the same result from
    applying \( T \) implies that the inputs must have been the same, otherwise
    a linear transformation is not injective. For example, the function
    \( f(x) = x^2 \) is a linear transformation of elements of \( \\mathbb{R} \)
    into \( \\mathbb{P}_2 \) but \( f \) is not injective! We can see this
    immediately by comparing \( x = -5 \) with \( x = 5 \). \( f(-5) = f(5) \)
    even though \( -5 \) and \( 5 \) are not equal!</p>

    <p>A mapping \( T : U \\rightarrow V \) is <em>surjective</em> if for every
    \( v \in V \) there exists a \( u \in U \) where \( T(u) = v \). In other words,
    all elements of \( V \) must be mapped to by an element of \( U \). In simple terms,
    the mapping \( T \) must fully "cover" the entire vector space \( U \). Perhaps
    this is why surjective mappings are often called "onto" mappings! </p>


    ''',
    "Resources":
    '''
                <a href="http://linear.ups.edu/html/section-LT.html">http://linear.ups.edu/html/section-LT.html</a><br>
                <a href="https://en.wikipedia.org/wiki/Linear_map">https://en.wikipedia.org/wiki/Linear_map</a><br>

    ''',
    "Visualization":
    '''

            <p>
            <form name="trynow1" form action="" form method='post'>
            Consider vectors in \( \\mathbb{R}^2 \). Is the identity mapping
            \( T = \\begin{bmatrix} 1 \\\\ 1 \\end{bmatrix} \) surjective?<br>

            <input type="radio" name="ans0" value="yes"> Yes<br>
            <input type="radio" name="ans0" value="no"> No<br>

            Is the identity mapping injective?<br>

            <input type="radio" name="ans1" value="yes"> Yes<br>
            <input type="radio" name="ans1" value="no"> No<br>

            Recall the projection of vectors in \( \\mathbb{R}^2 \) onto the
            y-axis. Is this surjective? Is it injective?<br>

            <input type="radio" name="ans2" value="a"> Both <br>
            <input type="radio" name="ans2" value="b"> Injective only <br>
            <input type="radio" name="ans2" value="c"> Surjective Only <br>
            <input type="radio" name="ans2" value="d"> Neither <br>

            <br><input type="submit" value="Submit">
            </form>


            </p>

    ''' + "<b>" + result_text + "</b>"}
    nav[5]["Items"][1]["Current"] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

@application.route("/2D_graphics", methods=['GET', 'POST'])
def two_dimensional():
    # If point is not on cookie data, it would add it to cookie
    if request.cookies.get('point') == None:
        resp = make_response(redirect(url_for('two_dimensional'))) #redirect to current page to update cookie data
        resp.set_cookie('point', '0') #Since the point is none, set it as 0
        return resp

    nav = copy.deepcopy(nav_list) #deep copying nav_list to not make duplicate
    prev_point = request.cookies.get('point') #getting point data from cookie
    checking_topics(nav) #checking all the topics' cookie data

    #quiz method
    if request.method == 'POST':
        try: #error catching block
            if request.form['ans0'] == "d" and request.form['ans2'] == "a":
                #If all answers are correct
                resp = make_response(redirect(url_for('two_dimensional'))) #redirect to current page. To update cookie
                resp.set_cookie("twodim", "OK") #add progression data to cookie
                resp.set_cookie('point', str(int(prev_point) + 100))   #add 100 points and update cookie data
                return resp
            else:
                result_text = "One or more answers are incorrect" #If user answerd wrong, return this statement
        except:
            result_text = "Please answer each question."
    else:
        result_text = ""

    #If cookie id is in cookie data, leave check mark on left panel
    if check_cookie("twodim"):
        nav[5]["Items"][2]["Complete"] = True #make checkmark
        result_text = "Correct, you earned 100 points"
    else:
        nav[5]["Items"][2]["Complete"] = False

    page = {"Description":
    '''
    <p>Linear transformations are very useful in computer graphics, particularly for modifying the
    appearance of an image.</p>

    Say we have an image of our favorite college mascot:
    <img src="
    ''' +
    url_for('static', filename='img0.png')
    + '''
    " alt="Stretched">

    <p>We might wish to <b>stretch</b> the image. Stretching in the
    y-axis is accomplished with using the matrix:</p>
    $$ \\begin{bmatrix} k & 0 \\\\ 0 & 1 \\end{bmatrix} $$

    <img src="
    ''' +
    url_for('static', filename='img2.png')
    + '''
    " alt="Stretched">

    Where \( k \) is a value greater than one. This is known as the stretch factor.
    Similarly we can <b>stretch</b> along the x-axis with:
    $$ \\begin{bmatrix} 1 & 0 \\\\ 0 & k \\end{bmatrix} $$

    <img src="
    ''' +
    url_for('static', filename='img1.png')
    + '''
    " alt="Stretched">

    <b>Squeezing</b> is accomplished using a reciprocal of \( k \), like so:
    $$ \\begin{bmatrix} 1 & 0 \\\\ 0 & 1/k \\end{bmatrix} $$

    <img src="
    ''' +
    url_for('static', filename='img3.png')
    + '''
    " alt="Stretched">


    While <b>reflections</b> about the x or y axes are achieved with negative values:
    $$ \\begin{bmatrix} -1 & 0 \\\\ 0 & 1 \\end{bmatrix} $$

    <img src="
    ''' +
    url_for('static', filename='img4.png')
    + '''
    " alt="Stretched">

    And <b>rotations</b> are accomplished using sines and cosines:
    $$ \\begin{bmatrix} \cos(\\theta) & \sin(\\theta) \\\\ -\sin(\\theta) & \cos(\\theta) \\end{bmatrix} $$

    <img src="
    ''' +
    url_for('static', filename='img5.png')
    + '''
    " alt="Stretched">

    We can also <b>shear</b> an image, which is a kind of sideways squashing transformation:
    $$ \\begin{bmatrix} 1 & k \\\\ 0 & 1 \\end{bmatrix} $$

    <img src="
    ''' +
    url_for('static', filename='img6.png')
    + '''
    " alt="Stretched">

    In this case k is known as the "shear factor".

    This is just a brief introduction to the many ways matrix transformations are
    used in computer graphics. We have not even discussed the 3D transformations!



    ''',
    "Resources":
    '''

                    <a href="https://en.wikipedia.org/wiki/Affine_transformation">https://en.wikipedia.org/wiki/Affine_transformation</a><br>

    ''',
    "Visualization":
    '''

                <p>
                <form name="trynow1" form action="" form method='post'>
                Consider the matrix:
                $$ \\begin{bmatrix} 0 & 1 \\\\ 1 & 0 \\end{bmatrix} $$
                How will this matrix transform an image?<br>

                <input type="radio" name="ans0" value="a"> Same Image <br>
                <input type="radio" name="ans0" value="b"> Reflection about the x-axis <br>
                <input type="radio" name="ans0" value="c"> Shear to the right <br>
                <input type="radio" name="ans0" value="d"> Reflection about y=x <br>

                Which of these matrices will rotate an image counterclockwise by
                90 degrees?<br>

                <input type="radio" name="ans2" value="a">
                $$ \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix} $$ <br>
                <input type="radio" name="ans2" value="b">
                $$ \\begin{bmatrix} -1 & 0 \\\\ 0 & -1 \\end{bmatrix} $$ <br>
                <input type="radio" name="ans2" value="c">
                $$ \\begin{bmatrix} 0 & -1 \\\\ -1 & 0 \\end{bmatrix} $$ <br>
                <input type="radio" name="ans2" value="d">
                $$ \\begin{bmatrix} 0 & 1 \\\\ -1 & 0 \\end{bmatrix} $$ <br>

                <br><input type="submit" value="Submit">
                </form>


                </p>
    ''' + "<b>" + result_text + "</b>"}

    nav[5]["Items"][2]["Current"] = True #make selected topic bold on left panel
    head = {"Points": request.cookies.get('point')} #prints out points on top
    return render_template("moduletemplate.html", page=page,nav=nav,head=head)

def check_cookie(id):
    '''
    Input
        id: cookie id (string type)
    Output
        boolean
        If the id is in cookies, it return True
        otherwise, return False
    '''
    if request.cookies.get(id) == "OK":
        return True
    else:
        return False

def checking_topics(nav):
    '''
    This is helping function for saving user progression
    Input
        nav: navigation menu (dictionary or list)
    Output:
        None

    Checking all the topic's cookie id to leave check mark even though user choose different topics
    '''
    id_list = ['twodim', 'inject', 'Ltransform', 'subspace', 'vector_space',
    'span', 'orth', 'inner', 'determinant', 'mult', 'char_eqn', 'eigen', 'transpose',
    'operations', 'intro_vector', 'inverse', 'rref', 'matrix_ops', 'basic_matrix',
    'linequation']
    result = []

    for i in id_list:
        if request.cookies.get(i) == "OK":
            result.append(i)

    if "linequation" in result: nav[0]["Items"][0]["Complete"] = True

    if "basic_matrix" in result: nav[0]["Items"][1]["Complete"] = True

    if "intro_vector" in result: nav[0]["Items"][2]["Complete"] = True

    if "matrix_ops" in result: nav[1]["Items"][0]["Complete"] = True

    if "rref" in result: nav[1]["Items"][1]["Complete"] = True

    if "mult" in result: nav[1]["Items"][2]["Complete"] = True

    if "determinant" in result: nav[1]["Items"][3]["Complete"] = True

    if "inverse" in result: nav[1]["Items"][4]["Complete"] = True

    if "transpose" in result: nav[1]["Items"][5]["Complete"] = True

    if "operations" in result: nav[2]["Items"][0]["Complete"] = True

    if "span" in result: nav[2]["Items"][1]["Complete"] = True

    if "inner" in result: nav[2]["Items"][2]["Complete"] = True

    if "orth" in result: nav[2]["Items"][3]["Complete"] = True

    if "eigen" in result: nav[3]["Items"][0]["Complete"] = True

    if "char_eqn" in result: nav[3]["Items"][1]["Complete"] = True

    if "vector_space" in result: nav[4]["Items"][0]["Complete"] = True

    if "subspace" in result: nav[4]["Items"][1]["Complete"] = True

    if "Ltransform" in result: nav[5]["Items"][0]["Complete"] = True

    if "inject" in result: nav[5]["Items"][1]["Complete"] = True

    if "twodim" in result: nav[5]["Items"][2]["Complete"] = True



if __name__ == "__main__":
    application.run(host='0.0.0.0')
