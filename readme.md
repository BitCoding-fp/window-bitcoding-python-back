## 2024-06-02

윈도우 최적화 된 코드입니다!   
윈도우 로컬 환경에서 실행시킬 시 환경설정을 해당 방법으로 진행해주세요. 

### [수정]

```
services/rag.py
```

기존의 JSONLoader와 jq를 사용하는 방식에서   
pandas를 사용하는 방식으로 변경 - jq 윈도우 호환 불가능

<br/>


## [윈도우 설치 방법]
- 윈도우에서 호환되지 않는 라이브러리를 수동 설치로 분리하였습니다. 

### 1. 자동 설치
- condafoge : python=3.10 기준
```
pip install -r requirementswin.txt
```


### 2. 수동 설치
- 자동 설치 실행 후 powershell에서 실행해주세요

```
# conda 설치
# conda install -c conda-forge aws-c-auth aws-c-cal aws-c-common aws-c-compression aws-c-event-stream aws-c-http aws-c-io aws-c-mqtt aws-c-s3 aws-c-sdkutils aws-checksums aws-crt-cpp aws-sdk-cpp bzip2 c-ares lz4-c openjpeg re2 snappy zeromq zstd


# pip 설치
# pip install aiohttp==3.9.3 aiosignal==1.2.0 beautifulsoup4==4.12.2


# abseil-cpp 빌드 및 설치
# git clone https://github.com/abseil/abseil-cpp.git
# cd abseil-cpp
# mkdir build
# cd build
# cmake ..
# cmake --build . --config Release
# cmake --install . --config Release

# vcpkg 빌드 및 설치
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat

# vcpkg 환경변수 설정
setx PATH "%PATH%;C:\path\to\vcpkg"


# arrow-cpp 빌드 및 설치
# git clone https://github.com/apache/arrow.git
# cd arrow/cpp
# mkdir build
# cd build
# cmake ..
# cmake --build . --config Release
# cmake --install . --config Release


# ORC 빌드 및 설치
# git clone https://github.com/apache/orc.git
# cd orc
# mkdir build
# cd build
# cmake ..
# cmake --build . --config Release
# cmake --install . --config Release


# 설치 후 bson호환성 오류 해결 - 일부 삭제 후 재설치
# pip uninstall bson
# pip install pymongo

```
