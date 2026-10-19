import jwt
from datetime import datetime, timedelta, timezone
#변수를 대문자로만 설정하면 바꾸지 않는 값
SECRET_KEY = "dslfjgkreobdgsregwdsbcxbilcjxkesfarglrwhklrejkedkgsljkldgslj"
ALGORITHM = "HS256"

payload={
    "sub" : "user01",
    "exp" : datetime.now(timezone.utc) + timedelta(minutes=30),  #유효시간 확인
}
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

print(token)

payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #토큰 풀기

print(payload)