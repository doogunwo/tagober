<div align="center">

# TAGOBER

**얼굴 인식 기반 승차 인증 및 이용 내역 관리 시스템**

Node.js 웹 서버와 Python 얼굴 인식 서버를 하나로 구성한 졸업작품 프로젝트입니다.

![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![Express](https://img.shields.io/badge/Express-000000?style=flat-square&logo=express&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)

</div>

## 프로젝트 소개

TAGOBER는 사용자의 얼굴을 등록하고, 얼굴 인식 결과를 이용해 승차 기록과 요금을 관리하는 시스템입니다. 웹 서비스는 회원가입, 로그인, 얼굴 등록, 프로필 및 이용 내역 조회를 담당하며, Python 서버는 얼굴 모델 학습과 영상 프레임 인식을 처리합니다.

기존에 분리되어 있던 Node.js 서버와 Flask 얼굴 인식 서버를 하나의 저장소로 통합한 버전입니다.

## 주요 기능

- 회원가입 및 세션 기반 로그인
- 사용자 얼굴 이미지 등록
- 등록된 얼굴을 이용한 사용자 식별
- 얼굴 인식 모델 재학습
- 승차 기록 및 요금 저장
- 사용자 프로필과 이용 내역 조회

## 시스템 구성

```text
Web browser
    │
    ▼
Node.js / Express :3000
    ├── 회원가입 및 로그인
    ├── 얼굴 이미지 업로드
    ├── 프로필·승차 기록 조회
    └── 모델 업데이트 요청
              │
              ▼
Python / Flask :5000
    ├── OpenCV 얼굴 검출·인식
    ├── 얼굴 모델 학습
    └── 인식 결과 및 결제 기록 처리
              │
              ▼
            MySQL
```

## 기술 스택

| 구분 | 기술 |
| --- | --- |
| Web server | Node.js, Express, EJS |
| AI server | Python, Flask |
| Computer vision | OpenCV, NumPy |
| Database | MySQL |
| File upload | Multer |
| Session | express-session |
| HTTP communication | Axios, Requests |

## 프로젝트 구조

```text
tagober/
├── Page/                            # 웹 페이지 및 등록 이미지
├── server.js                        # Express 웹 서버
├── model.py                         # Flask 얼굴 인식 서버
├── client.py                        # 영상 전송 클라이언트
├── haarcascade_frontalface_default.xml
├── dgw0601_model.yml                # 얼굴 인식 모델
├── package.json                     # Node.js 의존성
├── package-lock.json
├── requirements.txt                 # Python 의존성
└── README.md
```

## 실행 방법

### 1. 저장소 복제

```bash
git clone https://github.com/doogunwo/tagober.git
cd tagober
```

### 2. 의존성 설치

Node.js 패키지를 설치합니다.

```bash
npm install
```

Python 가상환경을 만든 뒤 필요한 패키지를 설치합니다.

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. 환경 설정

현재 데이터베이스 접속 정보와 서버 주소는 `server.js`, `model.py`, `client.py`에 직접 설정되어 있습니다. 실행 환경에 맞게 다음 값을 수정해야 합니다.

- MySQL 호스트, 포트, 사용자, 비밀번호 및 데이터베이스
- Express 서버 주소
- Flask 얼굴 인식 서버 주소
- 카메라 또는 영상 입력 설정

### 4. 서버 실행

얼굴 인식 서버를 먼저 실행합니다.

```bash
python model.py
```

별도 터미널에서 웹 서버를 실행합니다.

```bash
node server.js
```

웹 서버는 기본적으로 `http://localhost:3000`에서 실행됩니다. 현재 Flask 서버의 호스트 주소는 `model.py`에 지정되어 있으므로 실행 환경에 맞게 변경해야 합니다.

## 주요 엔드포인트

### Express 서버

| Method | Endpoint | 설명 |
| --- | --- | --- |
| `GET` | `/` | 메인 화면 |
| `GET` | `/login` | 로그인 화면 |
| `GET` | `/signup` | 회원가입 화면 |
| `GET` | `/dashboard` | 대시보드 |
| `GET` | `/profile` | 사용자 프로필 |
| `GET` | `/record` | 승차 기록 |
| `GET` | `/face` | 얼굴 등록 화면 |
| `POST` | `/signup` | 회원 등록 |
| `POST` | `/login` | 로그인 처리 |
| `POST` | `/upload` | 얼굴 이미지 업로드 및 모델 업데이트 요청 |

### Flask 서버

| Method | Endpoint | 설명 |
| --- | --- | --- |
| `POST` | `/start` | 얼굴 인식 시작 |
| `POST` | `/update` | 등록 이미지 기반 모델 재학습 |
| `POST` | `/video_feed` | 영상 프레임 얼굴 인식 |

## 화면 미리보기

<table>
  <tr>
    <td><img src="https://github.com/doogunwo/Tagober_server/assets/87505243/39e99b47-8f77-48b9-85e7-66c1d625e12a" alt="TAGOBER 화면 1"></td>
    <td><img src="https://github.com/doogunwo/Tagober_server/assets/87505243/6fc936bd-6f6f-4c45-92eb-a3b67861ab6f" alt="TAGOBER 화면 2"></td>
  </tr>
  <tr>
    <td><img src="https://github.com/doogunwo/Tagober_server/assets/87505243/8e1b0f98-0762-4966-a71b-d87304aa7aeb" alt="TAGOBER 화면 3"></td>
    <td><img src="https://github.com/doogunwo/Tagober_server/assets/87505243/5acc722e-862a-425e-a098-f1498b76981f" alt="TAGOBER 화면 4"></td>
  </tr>
  <tr>
    <td><img src="https://github.com/doogunwo/Tagober_server/assets/87505243/50d6864e-f2b8-4a9a-9998-64982fe0017d" alt="TAGOBER 화면 5"></td>
    <td><img src="https://github.com/doogunwo/Tagober_server/assets/87505243/b0652b4a-fd49-4835-bf8f-6421d3ecc17f" alt="TAGOBER 화면 6"></td>
  </tr>
</table>

## 참고

이 저장소는 동의대학교 컴퓨터공학과 졸업작품으로 제작되었습니다.
