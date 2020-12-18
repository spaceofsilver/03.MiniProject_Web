from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask import jsonify
from db.d_6 import *
from flask_socketio import SocketIO

app = Flask(__name__)
# 세션처리 #
app.secret_key = 'sakccsdcocjk2sdjkdskcj'
# [2] 시크릿키 지정 (환경변수) #
app.config['SECRET_KEY'] = '12341234' #  비밀번호
# [3] SocketIO 생성시 Flask 객체를 래핑
socketio = SocketIO( app, cors_allowed_origins="*", async_mode='threading' )

# < 회원가입 &  로그인 & 로그아웃 > ----------------------------------------------------------------------------------------------------------------------------------------------

# 회원가입 #
@app.route('/signup', methods=['GET','POST'] )
def signup():    
    if request.method == 'GET': # 화면 처리 담당
        return render_template('signup.html')
    else:
        uid      = request.form.get('uid')
        upw      = request.form.get('upw')
        name     = request.form.get('name')
        gender   = request.form.get('gender')
        address  = request.form.get('address')
        # print(gender)
        user = db_signupUsers(uid, upw, name, gender, address)
        if user:
            return render_template('alert2.html')
        else:        
            return redirect( url_for('home') )   


# 로그인 #
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        res = make_response( render_template('login.html') )
        res.set_cookie('uid', '게스트')
        return res
    else:    
        uid = request.form.get('uid')
        upw = request.form.get('upw')
        user = db_selectLogin( uid, upw )
        print(user)
        if user:
            session['uid'] = user['uid'] 
            session['upw'] = user['upw'] 
            session['name'] = user['name'] 
            return redirect('/indexlogin')
            pass
        else:
            # 4. 안되면 팝업
            return '''
                    <script>
                        alert('아이디 비번을 확인하세요');
                        history.back();
                    </script>
                    '''

# 로그아웃
@app.route('/logout')
def logout():
    # 세션제거
    if 'uid' in session:
        session.pop('uid', None )
    if 'top_name' in session:
        session.pop('top_name', None )
    if 'pants_name' in session:
        session.pop('pants_name', None )
    if 'acc_name' in session:
        session.pop('acc_name', None )
    return redirect( url_for( 'home' )) 

# < // 회원가입 & 로그인 & 로그아웃 > -------------------------------------------------------------------------------------------------------------------------------

# < 로그인 전 > ---------------------------------------------------------------------------------------------------------------------------------------------------

# 로그인 전 '메인화면'
@app.route('/')
def home():    
    return render_template('index.html', name='사용자명')

# 로그인 전 '상의'
@app.route('/top')
def top():
    return render_template('top.html')

# 로그인 전 상의 > 세부 정보
@app.route('/top_buy', methods=['POST','GET'])
def top_buy():
    return render_template('top_buy.html')

# 로그인 전 '악세사리'
@app.route('/acc')
def acc():
    return render_template('acc.html')

# 로그인 전 악세사리 > 세부 정보
@app.route('/acc_buy', methods=['POST','GET'])
def acc_buy():
    return render_template('acc_buy.html')

# 로그인 전 '바지'
@app.route('/pants' , methods=['POST','GET'])
def pants():
    return render_template('pants.html')

# 로그인 전 바지 > 세부 정보  
@app.route('/pants_buy', methods=['POST','GET'])
def pants_buy():
    return render_template('pants_buy.html')

# < // 로그인 전 >---------------------------------------------------------------------------------------------------------------------------------------------------

## 고객센터(홈, 공지사항, 이벤트, 질문하기로 구성) => 이미지 첨부는 시간상 따로 안했음. 추후 가능하면 할것임.
@app.route('/notice')
def notice():
    return render_template('notice.html')

@app.route('/event')
def event():
    return render_template('event.html')



# < 로그인 후 > --------------------------------------------------------------------------------------------------------------------------

# 로그인 후의 '메인 화면'
@app.route('/indexlogin')
def indexlogin():   
    return render_template('indexlogin.html', name='사용자명')

# 로그인 후 메뉴에 등장하는 '마이 페이지'
@app.route('/my_page')
def my_page():    
    return render_template('my_page.html')


# 로그인 후 '상의' 카테고리
@app.route('/new_top')
def new_top():    
    return render_template('new_top.html')

# 로그인 후 상의 > 세부 정보
@app.route('/new_top_buy',methods=['POST','GET'])
def new_top_buy():    
    top_name               = request.form.get('option1')
    top_size               = request.form.get('option2')
    top_amt                = request.form.get('option3')
    session['top_name']    = top_name
    session['top_size']    = top_size
    session['top_amt']     = top_amt
    return render_template('new_top_buy.html')


# 로그인 후 '악세사리' 카테고리   
@app.route('/new_acc_buy',methods=['POST','GET'])
def new_acc_buy():    
    acc_name               = request.form.get('option1')
    acc_size               = request.form.get('option2')
    acc_amt                = request.form.get('option3')
    user                   = db_selectLogin( session['uid'], session['upw'] )
    session['acc_name']    = acc_name
    session['acc_size']    = acc_size
    session['acc_amt']     = acc_amt
    return render_template('new_acc_buy.html')

# 로그인 후 '악세사리' > 세부 정보
@app.route('/new_acc' , methods=['POST','GET'])
def new_acc():
    return render_template('new_acc.html')

# 로그인 후 '하의' 카테고리
@app.route('/new_pants')
def new_pants():    
    return render_template('new_pants.html')

# 로그인 후 '하의' > 세부 정보
@app.route('/new_pants_buy',methods=['POST','GET'])
def new_pants_buy():    
    pants_name               = request.form.get('option1')
    pants_size               = request.form.get('option2')
    pants_amt                = request.form.get('option3')
    session['pants_name']    = pants_name
    session['pants_size']    = pants_size
    session['pants_amt']     = pants_amt
    return render_template('new_pants_buy.html')

# ------------------------------------------------------------------
## after 고객센터 
@app.route('/new_notice')
def new_notice():
    return render_template('new_notice.html')

@app.route('/new_event')
def new_event():
    return render_template('new_event.html')

## notice 내부에 있는 사이트로 메뉴바에 추가 안함.
@app.route('/new_chat')
def new_chat():
    return render_template('new_chat.html')

@app.route('/new_chat2')
def new_chat2():
    return render_template('new_chat2.html')

## notice 내부에 있는 사이트로 메뉴바에 추가 안함.
@app.route('/upload_new_chat')
def upload_new_chat():
    return render_template('upload_new_chat.html')

# ------------------------------------------------------------------

@app.route('/new_upload', methods=['GET','POST'])
def new_upload(): 
    if request.method == 'GET':
        return render_template('new_upload.html', name='사용자명')
    else:
        # 파일 업로드 처리하는 부분
        f = request.files['file']
        
        #print(os.path.abspath(__file__))
        #print(os.path.dirname(os.path.abspath(__file__)))
        #print(os.getcwd())
        # 경로를 os에 상관없이 자동으로 계산해준다
        dir = os.path.dirname(os.path.abspath(__file__))
        #print(dir + '/static/upload/' + f.filename )
        f.save(dir + '/static/upload/' + f.filename)
        return '''
            <img src='static/upload/%s'/>
        ''' %f.filename



if __name__ == '__main__': 
    app.run(debug=True)  

