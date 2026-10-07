<div align="center">

# TAGOBER

**얼굴 등록·인식과 사용자 기록 조회를 구현한 졸업작품 프로토타입**

![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![Express](https://img.shields.io/badge/Express-000000?style=flat-square&logo=express&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)

</div>

## 프로젝트 개요

TAGOBER는 웹에서 사용자 정보와 얼굴 이미지를 등록하고, 카메라 프레임에서 등록 사용자를 식별한 뒤 결과를 MySQL에 기록하는 프로토타입입니다.

이 저장소는 기존에 분리되어 있던 Express 웹 서버와 Flask 얼굴 인식 코드를 하나로 합친 통합 버전입니다.

## 구현 구성

```text
웹 브라우저
    │
    ▼
Express 서버 (`server.js`)
    ├── 정적 HTML 제공
    ├── 회원 정보 저장·로그인 확인
    ├── 세션에 사용자명 저장
    ├── 얼굴 이미지 업로드
    └── 사용자 정보·기록 조회
              │
              ├──────────────┐
              ▼              ▼
           MySQL       Flask 서버 (`model.py`)
                           ├── 등록 이미지에서 얼굴 검출
                           ├── 사용자별 LBPH 모델 생성
                           ├── 전송된 카메라 프레임 인식
                           └── 인식 결과를 payment 테이블에 기록
                                      ▲
                                      │
                              카메라 클라이언트
                                (`client.py`)
```

## 구현 내용

### 웹 서버

`server.js`는 Express로 작성되었습니다.

- `/`, `/login`, `/signup`, `/dashboard`에서 HTML 파일을 제공합니다.
- 회원가입 요청의 `username`, `password`, `name`, `email`, `phone`을 `signup` 테이블에 저장합니다.
- 로그인 시 `signup` 테이블에서 사용자를 조회하고 입력된 비밀번호를 비교합니다.
- 로그인한 사용자명은 `express-session`의 세션 값으로 보관합니다.
- 프로필 요청 시 회원 정보와 `faceregister.imagePath` 존재 여부를 조회합니다.
- 기록 요청 시 `payment` 테이블에서 현재 사용자의 기록을 읽어 HTML 테이블로 반환합니다.
- Multer로 업로드한 이미지를 `Page/Data/{username}/{username}.jpg`에 저장하고 해당 경로를 `faceregister` 테이블에 반영합니다.

### 얼굴 모델 생성

`model.py`는 Flask와 OpenCV로 작성되었습니다.

1. `faceregister` 테이블에서 사용자명과 등록 이미지 경로를 읽습니다.
2. Haar Cascade로 이미지 속 얼굴 영역을 검출합니다.
3. 검출된 얼굴로 사용자별 `LBPHFaceRecognizer` 객체를 학습합니다.
4. 생성된 모델은 사용자명을 키로 하는 `models` 딕셔너리에 보관합니다.
5. `/update` 요청을 받으면 지정된 사용자 한 명의 모델을 다시 생성합니다.

### 카메라 프레임 인식

`client.py`는 OpenCV로 카메라 프레임을 읽고 JPEG로 인코딩한 뒤, 직렬화하여 Flask의 `/video_feed`로 전송합니다.

Flask 서버는 다음 순서로 프레임을 처리합니다.

1. 전송된 프레임을 역직렬화하고 OpenCV 이미지로 복원합니다.
2. Haar Cascade로 얼굴을 검출하여 `200 × 200` 크기로 변환합니다.
3. 등록된 사용자별 LBPH 모델로 얼굴을 예측합니다.
4. 가장 낮은 confidence 값을 반환한 모델의 사용자명을 결과로 선택합니다.
5. 선택된 사용자명과 고정 요금 값 `1300`, 현재 Unix 시간을 `payment` 테이블에 기록합니다.
6. 인식한 사용자명을 직렬화하여 클라이언트에 반환합니다.

## 데이터 흐름

| 단계 | 입력 | 처리 | 저장 또는 출력 |
| --- | --- | --- | --- |
| 회원가입 | 사용자 정보 | Express가 MySQL INSERT 수행 | `signup` 테이블 |
| 로그인 | 아이디·비밀번호 | DB 조회 후 문자열 비교 | 세션 사용자명 |
| 얼굴 등록 | 이미지 파일 | Multer가 사용자별 경로에 저장 | `Page/Data`, `faceregister.imagePath` |
| 모델 생성 | 등록 이미지 | 얼굴 검출 후 사용자별 LBPH 학습 | 메모리의 `models` 객체 |
| 얼굴 인식 | 카메라 프레임 | 모든 사용자 모델의 confidence 비교 | 인식 사용자명 |
| 기록 조회 | 세션 사용자명 | `payment` 테이블 조회 | HTML 테이블 |

## 주요 파일

| 파일 | 역할 |
| --- | --- |
| `server.js` | 웹 페이지, 회원 처리, 이미지 업로드 및 기록 조회 |
| `model.py` | 얼굴 검출, LBPH 모델 학습 및 프레임 인식 |
| `client.py` | 카메라 프레임 수집과 Flask 서버 전송 |
| `Page/` | HTML 페이지와 등록 이미지 |
| `haarcascade_frontalface_default.xml` | OpenCV 얼굴 검출 분류기 |
| `dgw0601_model.yml` | 저장된 얼굴 인식 모델 파일 |

## 화면

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

## 제작

동의대학교 컴퓨터공학과 졸업작품으로 제작했습니다.
