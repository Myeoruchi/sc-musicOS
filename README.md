# 스타크래프트 노래 맞히기 유즈맵 오픈소스

Create by Myeoruchi (Heaven)

Thanks to Avlos (갈대)

## 주의사항
- DO NOT USE **euddraft 0.10.0.1**

## 특징
### 기능
- 다른 사람에게 내가 친 정답이 보이지 않으므로, **모두가 정답**을 맞힐 수 있습니다.
- **정답자와 비정답자간**에 채팅을 분리할 수 있는 **채팅 분리** 기능이 있습니다.
- **정답 리스트 2개**를 운용할 수 있어 **줄임말 정답** 같은 것을 On/Off 가능합니다.
- **2초 듣고 맞히기** 기능을 제공하며, **개인별로 적용**됩니다.
- 정답 입력 시에 **띄어쓰기와 대소문자**에 영향받지 않습니다.
- 힌트 공개 여부에 따라 **점수가 차등 지급**됩니다.
- 스킵의 종류로 강제 스킵, 못맞힌 사람의 만장일치 스킵 투표, 다 맞힌 후 과반수 스킵 투표가 있습니다.
- 모두가 맞혔을 경우에 자동으로 스킵해주는 **자동 스킵 기능**을 On/Off 가능합니다.

### 단점
- 채팅 분리 매커니즘에 의해 채팅 로그가 대부분 남지 않습니다.
- 가끔씩 채팅(정답)이 씹히는 경우가 있습니다.

## 편의 기능
전용 툴이 있으면 편할 것 같아 새로 만들었습니다.

툴의 이름은 EZDown이며 곡 다운로드, 구간 자르기, 볼륨 조절 등 다양한 기능을 수행합니다.

## 사용 방법

### EZDown 사용법
- EZDown 폴더의 엑셀 파일을 수정하여 양식에 맞게 정리하세요. (열의 이름을 바꾸어선 안됩니다.)
- EZDown 폴더의 EZDown 파일을 실행시켜 경로를 지정해주세요.
    - 기본적으로 디렉토리 구조에 맞게 상대적으로 설정되어 있으니 **그냥 작업하는걸 권장**합니다.
    - 음원 다운로드는 엑셀에 있는 주소로 유튜브에서 음원을 다운로드합니다.
    - 음원 볼륨 조절 및 자르기는 다운로드 한 음원을 바탕으로 볼륨 조절 및 자르기를 수행합니다.
    - 정보 추출은 엑셀 정보를 바탕으로 맵에 들어갈 정보를 musicInfo.eps 파일로 생성합니다.
        - 단, 엑셀 경로를 기반으로 하고 있으므로, 가급적 디렉토리 구조를 바꾸지 말아주세요.

### 힌트 시간 조절 / 점수 조절 / 제작자 이름 수정 / 리더보드 멘트 수정
- Map 폴더 내에 build.eds 파일을 메모장으로 수정하여 주석을 바탕으로 수정하시면 됩니다.

### 오프닝 및 엔딩 수정
- Map/src 폴더 내 opening.eps 및 main.eps 내에 있는 오프닝이나 엔딩 멘트 수정하시면 됩니다.

### 빌드 방법
- Map 폴더 내 build.eds 파일을 euddraft에 끌어다 놓거나 euddraft를 연결하여 실행하면 됩니다.
