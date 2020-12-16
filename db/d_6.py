# 절차적코드는 누군가 import 해버리면 그즉시 수행이 되버려서 의도하지 않고 코드가 작동해 버린다
# 원하는 시점에 작동하게 모듈화 하고 싶다면 -> 함수, 클래스로 구성해야한다
import pymysql as my
# 함수의 리턴값


def db_selectLogin(uid, upw):
    conn = None
    row  = None
    try:
        # 차후 연결 정보를 일괄적으로 관리한다
        # 정보 변경시 다 고쳐야하는 문제, 요청이 올때마다 매번 접속하면
        # 느리다(응답이 느려질수 밖에 없다) => 개선
        conn = my.connect(host='localhost',
                          user='root',
                          password='12341234',
                          db='python_db',
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


# 게시판의 한개의 페이지를 구성하는 데이터를 조회하여 리턴한다
# 복수개의 데이터를 획득해서 리턴
# onePage_dataNum = 5
# 기본적으로 5개를 한페이지에서 보는 양으로 구성,정수값을 넣으라는 표시
def db_selectStockList(curPageId=1, onePage_dataNum=5):
    conn = None
    rows = None
    try:
        # 차후 연결 정보를 일괄적으로 관리한다
        # 정보 변경시 다 고쳐야하는 문제, 요청이 올때마다 매번 접속하면
        # 느리다(응답이 느려질수 밖에 없다) => 개선
        conn = my.connect(host='localhost',
                          user='root',
                          password='12341234',
                          db='python_db',
                          charset='utf8mb4',
                          cursorclass=my.cursors.DictCursor
                          )
        print('연결성공')

        with conn.cursor() as cursor:
            sql = '''  SELECT * FROM stocks order BY NAME ASC LIMIT %s,%s;  '''
            # 한 페이지에서 보여지는 데이터의 총수
            amt = onePage_dataNum
            # 데이터를 가저오는 row상의 시작위치
            startPage = (curPageId-1)*amt
            cursor.execute(sql, (startPage, amt))
            # 존재하는 회원 정보가 세팅되었을 것이다
            # 만약 회원정보가 없다면, None으로 리턴
            rows = cursor.fetchall()
            # 결과를 다 가저 오는것 fechall

    except Exception as e:
        print('예외발생', e)
    finally:
        if conn:
            conn.close()
    # 아이디 비번이 일치 > 데이터 리턴
    # 연결오류, 아이디비번 불일치 -> None
    return rows


def db_selectNameStock(keyword):
    conn = None
    rows = None
    try:
        # 차후 연결 정보를 일괄적으로 관리한다
        # 정보 변경시 다 고쳐야하는 문제, 요청이 올때마다 매번 접속하면
        # 느리다(응답이 느려질수 밖에 없다) => 개선
        conn = my.connect(host='localhost',
                          user='root',
                          password='12341234',
                          db='python_db',
                          charset='utf8mb4',
                          cursorclass=my.cursors.DictCursor
                          )
        print('연결성공')

        with conn.cursor() as cursor:
            # 파라미터를 무조건 execute()를 통해서 넣을 필요는 없다
            sql = '''  SELECT * FROM stocks WHERE name like '%{}%';  '''.format(
                keyword)
            cursor.execute(sql)
            rows = cursor.fetchall()

    except Exception as e:
        print('예외발생', e)
    finally:
        if conn:
            conn.close()
    # 아이디 비번이 일치 > 데이터 리턴
    # 연결오류, 아이디비번 불일치 -> None
    return rows

# 종목 코드를 넣어서 해당 종목 1개의 상세정보를 가져온다


def db_selectStockByCode(code):
    conn = None
    row = None
    try:
        conn = my.connect(host='localhost',
                          user='root',
                          password='12341234',
                          db='python_db',
                          charset='utf8mb4',
                          cursorclass=my.cursors.DictCursor
                          )
        print('연결성공')

        with conn.cursor() as cursor:
            sql = '''  SELECT * FROM stocks WHERE CODE= %s;  '''
            cursor.execute(sql, code)
            row = cursor.fetchone()

    except Exception as e:
        print('예외발생', e)
    finally:
        if conn:
            conn.close()
    # 아이디 비번이 일치 > 데이터 리턴
    # 연결오류, 아이디비번 불일치 -> None
    return row

# 코드와 일치하는 종목의 정보를 수정한다
# 성공하면 1, 실패하면 0


def db_updateStockInfo(code, indu, product):
    conn = None
    result = 0
    try:
        conn = my.connect(host='localhost',
                          user='root',
                          password='12341234',
                          db='python_db',
                          charset='utf8mb4',
                          cursorclass=my.cursors.DictCursor
                          )
        print('연결성공')

        with conn.cursor() as cursor:
            sql = '''  UPDATE
                        python_db.stocks
                        SET
                            indu=%s,
                            product=%s
                        where
                            `code`=%s;  '''
            print( sql.strip())
            cursor.execute(sql, ( indu, product, code))

        # 디비에 실제 반영을 수행
        conn.commit() # 커밋 -> 실반영 -> 성공/실패 여부를 알수 있다
        result = conn.affected_rows() # 영향을 받은수 => 0 or 1 <=

    except Exception as e:
        print('예외발생', e)
    finally:
        if conn:
            conn.close()
    # 아이디 비번이 일치 > 데이터 리턴
    # 연결오류, 아이디비번 불일치 -> None
    return result


if __name__ == "__main__":
    #print(db_selectStockByCode('309930'))
    if 0:
        print(db_selectStockList(1))
        print(db_selectStockList(2))
        print(db_selectStockList(3))
        print(db_selectStockList(1, 7))

    #단위 테스트, 개별함수를 직접 테스트 하기 위해서 삽입
    print( db_updateStockInfo('309930', '금융 지원 서비스업2', '기업인수합병2'))
    if 0:
        row = db_selectLogin('BDA', 1)
        print(row)
        print('-'*50)
        row = db_selectLogin('guest', 1234)
        print(row)
        print('-'*50)
        row = db_selectLogin('bua', 123)  # 비번이 다르다
        print(row)
