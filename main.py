from utils.models import *
from utils.gql_utils import *

app.add_url_rule(
    '/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

#index route
@app.route('/', methods=['GET'])
def home():
    user=current_user()
    role=''
    username=''
    if user:
        role=user['role']
        username=user['username']
    return render_template('index.html',role=role,username=username)

#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_login(username, password):
            return redirect(url_for('home'))
    if 'message' in session:warning=session['message']
    else:warning=''
    return render_template('login.html',warning=warning)

#view2 you can add your own views
@app.route('/view2', methods=['GET', 'POST'])
@login_required
def view2():
    return render_template('view2.html')
#detail about a person in the db you can remove or expand it
@app.route('/persons/<user>', methods=['GET', 'POST'])
@login_required
def person_detail(user):
    user=Person.query.filter_by(username=user).first()
    return render_template('details.html',result=user)



#graphql api query endpoint
#use this same for all your queries once defined in gql utils
#if you can manage all the js bull**** of course
@app.route('/query', methods=['POST'])
def handle_query():
    query = request.get_json()['query']
    result = schema.execute(query)
    if result.errors:
        return jsonify({"error": str(result.errors[0])})
    return jsonify({"result": result.data})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)