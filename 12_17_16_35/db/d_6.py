import pymysql as my

# 로그인 함수
def db_selectLogin(uid, upw):
    conn = None
    row  = None
    try:
        conn = my.connect(host='localhost',
                          user='root',
                          password='12341234',
                          db='mini_project',
                          charset='utf8mb4',
                          cursorclass=my.cursors.DictCursor
                          )
        print('연결성공')

        with conn.cursor() as cursor:
            sql = '''  SELECT * FROM users WHERE uid=%s AND upw = %s;  '''
            cursor.execute(sql, (uid, upw))
            # 존재하는 회원 정보가 세팅되었을 것이다
            # 만약 회원정보가 없다면, None으로 리턴
            row = cursor.fetchone()

    except Exception as e:
        print('예외발생', e)
    finally:
        if conn:
            conn.close()
    # 아이디 비번이 일치 > 데이터 리턴
    # 연결오류, 아이디비번 불일치 -> None
    return row

# 회원가입 함수
def db_signupUsers(uid, upw, name, gender, address):
    conn   = None
    result = 0
    try:
        conn = my.connect(host='localhost',
                          user='root',
                          password='12341234',
                          db='mini_project',
                          charset='utf8mb4',
                          cursorclass=my.cursors.DictCursor
                          )
        print('연결성공')

        with conn.cursor() as cursor:
            # 파라미터를 무조건 execute()를 통해서 넣을 필요는 없다
            sql = '''  INSERT INTO users (uid, upw, name, gender, address) VALUES (%s, %s, %s, %s, %s);  '''
            cursor.execute(sql, (uid, upw, name, gender, address))

            conn.commit() # 커밋 -> 실반영 -> 성공/실패 여부를 알수 있다
            result = conn.affected_rows() # 영향을 받은수 => 0 or 1 <=

    except Exception as e:
        print('예외발생', e)
    finally:
        if conn:
            conn.close()

    return result

# 상품 넣기 함수
def db_insertProduct(top_name, top_size, uid, upw,):
    result = None   
    conn = None   
    try:
        conn = my.connect(  host    ='localhost',   
                            user    ='root',        
                            password='12341234',
                            db      ='mini_project',
                            charset ='utf8mb4',
                            cursorclass=my.cursors.DictCursor
                        )
        # ----------------------------------
        with conn.cursor() as cursor:    
            sql = '''
            UPDATE users SET cart_pro= %s, cart_size= %s 
            WHERE  uid=%s AND upw=%s;'''
            cursor.execute(sql, (top_name, top_size, uid,upw) )
            # DB에 실제 반영 (! 중요 ) -> 커밋
            conn.commit()
            # 실반영이 되면 성공 실패 여부를 알 수 있다.
            result = conn.affected_rows()
        # ----------------------------------
    except Exception as e:  
        print('예외발생' , e)
    finally:
        if conn:
            conn.close()
    return result



# 단위 테스트
# if __name__ == "__main__":

