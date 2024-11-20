import os
import time
import json
import base64
import subprocess
import tkinter as tk
import threading
from tkinter import simpledialog, filedialog, messagebox, PhotoImage
import pandas as pd
from yt_dlp import YoutubeDL
from urllib.parse import urlparse, parse_qs

SEGMENT_DURATION = 2.28
VERSION = 'v2.3'
settings_file = 'settings.json'

icon_base64 = "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"
icon_data = base64.b64decode(icon_base64)

class App:
    def __init__(self, root):
        self.root = root
        
        #타이틀
        self.root.title(f"EZDown {VERSION}")

        #창 크기 고정
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # 경로 넣을 Frame 생성
        self.path_frame = tk.Frame(root)
        self.path_frame.grid(row=0, column=0, rowspan=3, columnspan=3, pady=10, sticky="w")

        # 경로 앞 텍스트
        self.text_filepath = tk.Label(self.path_frame, text="엑셀 파일 경로")
        self.text_filepath.grid(row=0, column=0, padx=10, pady=10)

        # 엑셀 경로를 표시할 Entry 위젯
        self.excel_path = tk.Entry(self.path_frame, width=50,relief="solid")
        self.excel_path.grid(row=0, column=1, padx=10, pady=10)

        # 파일 경로 지정 버튼
        self.button_browse = tk.Button(self.path_frame, text="파일 선택", command=lambda: self.browse_path(0, self.excel_path))
        self.button_browse.grid(row=0, column=2, padx=10, pady=10)

        # 경로 앞 텍스트
        self.text_filepath = tk.Label(self.path_frame, text="원본 음원 저장 경로")
        self.text_filepath.grid(row=1, column=0, padx=10, pady=10)

        # 엑셀 경로를 표시할 Entry 위젯
        self.download_path = tk.Entry(self.path_frame, width=50, relief="solid")
        self.download_path.grid(row=1, column=1, padx=10, pady=10)

        # 파일 경로 지정 버튼
        self.button_browse = tk.Button(self.path_frame, text="폴더 선택", command=lambda: self.browse_path(1, self.download_path))
        self.button_browse.grid(row=1, column=2, padx=10, pady=10)

        # 경로 앞 텍스트
        self.text_filepath = tk.Label(self.path_frame, text="자른 음원 저장 경로")
        self.text_filepath.grid(row=2, column=0, padx=10, pady=10)

        # 엑셀 경로를 표시할 Entry 위젯
        self.cut_path = tk.Entry(self.path_frame, width=50, relief="solid")
        self.cut_path.grid(row=2, column=1, padx=10, pady=10)

        # 파일 경로 지정 버튼
        self.button_browse = tk.Button(self.path_frame, text="폴더 선택", command=lambda: self.browse_path(2, self.cut_path))
        self.button_browse.grid(row=2, column=2, padx=10, pady=10)

        # 버튼을 넣을 Frame을 생성
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=3, column=0, columnspan=3, pady=10)

        # 음원 다운로드 버튼
        self.button_download = tk.Button(self.button_frame, text="음원 다운로드", width=15, command=self.music_download)
        self.button_download.grid(row=3, column=0, padx=10, pady=10)

        # 음원 자르기
        self.button_cut = tk.Button(self.button_frame, text="음원 볼륨 조절 및 자르기", width=20, command=self.music_cut)
        self.button_cut.grid(row=3, column=1, padx=10, pady=10)

        # 정보 추출 버튼
        self.button_extract = tk.Button(self.button_frame, text="정보 추출", width=15, command=self.extract_info)
        self.button_extract.grid(row=3, column=2, padx=10, pady=10)

        # 로그창
        self.log_text = tk.Text(root, height=10, wrap=tk.WORD, state="disabled")
        self.log_text.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # 스크롤바 생성
        self.yscrollbar = tk.Scrollbar(root, orient="vertical", command=self.log_text.yview)
        self.yscrollbar.grid(row=4, column=4, sticky='ns')

        # 스크롤바 연결
        self.log_text.config(yscrollcommand=self.yscrollbar.set)

        # 행과 열의 가중치 설정 (상대적 크기 조정을 위해 필요)
        root.grid_rowconfigure(4, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # 경로 불러오기
        if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    path = json.load(f)
                    try:
                        self.excel_path.insert(0, path['0'])
                        self.excel_path.xview(tk.END)
                    except:
                        pass

                    try:
                        self.download_path.insert(0, path['1'])
                        self.download_path.xview(tk.END)
                    except:
                        pass
                    
                    try:
                        self.cut_path.insert(0, path['2'])
                        self.cut_path.xview(tk.END)
                    except:
                        pass
    
    def extract_video_id(self, url):
            if 'youtu.be' in url:
                parsed_url = urlparse(url)
                video_id = parsed_url.path.strip('/')
                return video_id if len(video_id) == 11 else None
            
            elif 'youtube.com' in url:
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)
                video_id = query_params.get('v', [None])[0]
                return video_id if len(video_id) == 11 else None
            
            return None

    def browse_path(self, folder, path):
        if folder:
            selectpath = filedialog.askdirectory()
        else:
            selectpath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])

        if selectpath:
            path.delete(0, tk.END)  # 기존 경로 삭제
            path.insert(0, selectpath)  # 경로 삽입
            path.xview(tk.END) # 끝으로 스크롤

            settings = {}
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
            settings[f'{folder}'] = selectpath
            with open(settings_file, 'w') as f:
                json.dump(settings, f)

    def music_download(self):
        """음원을 다운로드 하는 함수"""
        # 경로 검사
        if not self.excel_path.get():
            messagebox.showerror("에러", "불러올 엑셀 파일을 선택해주세요.")
            return
        if not self.download_path.get():
            messagebox.showerror("에러", "원본 음원 저장 경로를 선택해주세요.")
            return
        os.makedirs(self.download_path.get(), exist_ok=True)

        sleep = simpledialog.askfloat("간격 설정기", "차단을 막기 위한 다운로드 간격 설정입니다.\n초 단위이므로 적당히 경험에 따라 조절해주세요.", parent=root)
        if sleep == None:
            self.log("다운로드 작업 취소")
            return
        
        def download():
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.download_path.get(), '%(id)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
                'postprocessor_args': [
                    '-b:a', '320k',
                    '-ar', '44100',
                    '-ac', '2',
                ],
                'audio-quality': 0,
                'extractaudio': True,
            }
            
            # 엑셀 파일 열기
            try:
                df = pd.read_excel(self.excel_path.get())
            except Exception as e:
                messagebox.showerror("에러", f"엑셀 파일을 불러오는 중 오류가 발생했습니다. ({e})")
                return

            musicNum = len(df)
            success = 0
            fail = 0
            skip = 0
            unused = 0
            with YoutubeDL(ydl_opts) as ydl:
                for idx, row in df.iterrows():
                    if pd.notna(row['미사용']):
                        self.log(f'다운로드 스킵 : {idx+1:03}행 (미사용)')
                        skip += 1
                        unused += 1
                        continue

                    video_url = row['Addr']
                    if pd.isna(video_url):
                        self.log(f'다운로드 실패 : {idx+1:03}행 (Addr 비어있음)')
                        fail += 1
                        continue
                    
                    try:
                        video_id = self.extract_video_id(video_url)
                        if video_id:
                            downloaded_file = os.path.join(self.download_path.get(), f'{video_id}.mp3')
                        else:
                            downloaded_file = video_url

                        if os.path.exists(downloaded_file):
                            self.log(f'다운로드 스킵 : {idx+1:03}행 (파일 존재함)')
                            skip += 1
                            continue

                        ydl.extract_info(video_url, download=True)
                        self.log(f'다운로드 성공 : {idx+1:03}행')
                        success += 1

                        time.sleep(sleep)

                    except Exception as e:
                        self.log(f'다운로드 실패 : {idx+1:03}행 ({e})')
                        fail += 1

            self.log(f'총 {musicNum}개 중 {success}개 성공, {fail}개 실패, {skip}개 (미사용 {unused}개)를 건너뛰었습니다.')
        
        thread = threading.Thread(target=download)
        thread.start()

    def music_cut(self):
        """음원을 자르는 함수"""
        # 경로 검사
        if not self.excel_path.get():
            messagebox.showerror("에러", "불러올 엑셀 파일을 선택해주세요.")
            return
        if not self.download_path.get():
            messagebox.showerror("에러", "원본 음원 저장 경로를 선택해주세요.")
            return
        if not self.cut_path.get():
            messagebox.showerror("에러", "자른 음원 저장 경로를 선택해주세요.")
            return
        os.makedirs(self.download_path.get(), exist_ok=True)
        os.makedirs(self.cut_path.get(), exist_ok=True)

        vol = simpledialog.askfloat("볼륨 설정기", "설정할 볼륨을 입력하세요.\n추천값 : 93.0±", parent=root)
        if not vol:
            self.log("볼륨 조절 / 자르기 작업 취소")
            return
        vol -= 89.0

        quality = simpledialog.askfloat("음질 설정기", "설정할 음질을 입력하세요. (1~10, 추천 값 : 4)\n클수록 음질이 높아집니다.", parent=root)
        if not quality:
            self.log("볼륨 조절 / 자르기 작업 취소")
            return

        def cut():
            # 엑셀 파일 열기
            try:
                df = pd.read_excel(self.excel_path.get())
            except Exception as e:
                messagebox.showerror("에러", f"엑셀 파일을 불러오는 중 오류가 발생했습니다. ({e})")
                return

            subprocess.run(f'del /s /f /q "{self.cut_path.get()}"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW, check=True)

            musicNum = len(df)
            success = 0
            fail = 0
            unused = 0
            op = 0
            end = 0
            for idx, row in df.iterrows():
                if pd.notna(row['미사용']):
                    self.log(f'볼륨 조절 / 자르기 스킵 : {idx+1:03}행 (미사용)')
                    unused += 1
                    continue

                empty = []
                if pd.isna(row['Addr']):
                    empty.append('Addr')
                if pd.isna(row['Start']):
                    empty.append('Start')
                if pd.isna(row['End']):
                    empty.append('End')

                if empty:
                    empty_list = ', '.join(empty)
                    self.log(f'볼륨 조절 / 자르기 실패 : {idx+1:03}행 (공백 : {empty_list})')
                    fail += 1
                    continue

                try:
                    video_id = self.extract_video_id(row['Addr'])
                    if video_id:
                        downloaded_file = os.path.join(self.download_path.get(), f'{video_id}.mp3')
                    else:
                        downloaded_file = row['Addr']

                    if os.path.exists(downloaded_file):
                        if pd.notna(row['오프닝/엔딩']):
                            if row['오프닝/엔딩'] == '오프닝':
                                path = self.cut_path.get() + '/OP'
                                op += 1
                            else:
                                path = self.cut_path.get() + '/ED'
                                end += 1
                        else:
                            path = self.cut_path.get() + f'/{idx+1-unused-op-end:03}'
                        os.makedirs(path, exist_ok=True)
                        output_file = path + '/cut.mp3'

                        command = [
                            'ffmpeg',
                            '-ss', str(row['Start']),
                            '-to', str(row['End']),
                            '-i', downloaded_file,
                            '-reset_timestamps', '1',
                            '-c:a', 'libmp3lame',
                            '-q:a', '0',
                            '-ar', '44100',
                            '-ac', '2',
                            '-b:a', '320k',
                            output_file
                        ]
                        subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, check=True)

                        command = ['mp3gain', '-c', '-r', '-d', str(vol), output_file]
                        subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, check=True)
                        
                        command = [
                            'ffmpeg',
                            '-i', output_file,
                            '-f', 'segment',
                            '-segment_time', str(SEGMENT_DURATION),
                            '-reset_timestamps', '1',
                            '-c:a', 'libvorbis',
                            '-q:a', str(quality),
                            path + '/%03d.ogg'
                        ]
                        subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, check=True)

                        self.log(f'볼륨 조절 / 자르기 성공 : {idx+1:03}행')
                        success += 1
                    else:
                        self.log(f'볼륨 조절 / 자르기 실패 : {idx+1:03}행 (파일 없음)')
                        fail += 1
                        continue

                except Exception as e:
                    self.log(f'볼륨 조절 / 자르기 실패 : {idx+1:03}행 ({e})')
                    fail += 1

            subprocess.run(f'del /s /f /q "{self.cut_path.get()}\\*.mp3"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW, check=True)

            with open(f'{self.cut_path.get()}/info.txt', 'w', encoding='utf-8') as f:
                if fail:
                    f.write('fail')
                else:
                    f.write(f'{musicNum-unused-op-end}\n{op}\n{end}')
            self.log(f'총 {musicNum}개 중 {success}개 성공, {fail}개 실패, {unused}개 미사용 했습니다.')
            self.log(f'{op+end}개의 곡이 오프닝/엔딩 곡으로 사용됐습니다.')
        
        thread = threading.Thread(target=cut)
        thread.start()

    def extract_info(self):
        """맵에 들어갈 정보를 파일로 출력하는 함수"""
        # 경로 검사
        if not self.excel_path.get():
            messagebox.showerror("에러", "불러올 엑셀 파일을 선택해주세요.")
            return

        def extract():            
            # 엑셀 파일 열기
            try:
                df = pd.read_excel(self.excel_path.get())
            except Exception as e:
                messagebox.showerror("에러", f"엑셀 파일을 불러오는 중 오류가 발생했습니다. : ({e})")
                return

            CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
            musicNum = len(df)
            categoryNum = 0
            categoryInclude = []
            categoryName = []
            categoryIndex = []
            hint = 'const hintArr1 = ['
            chosung = 'const hintArr2 = ['
            artist = 'const artArr = ['
            answer_list = 'const ansArr = ['
            answer_count = 'const indexArr = ['
            music_length = 'const lenArr = ['

            def extract_chosung(text):
                result = []
                for char in text:
                    if '가' <= char <= '힣':  # 한글 유니코드 범위 안에 있는 경우
                        char_code = ord(char) - 0xAC00
                        chosung_index = char_code // (21 * 28)
                        result.append(CHOSUNG_LIST[chosung_index])
                    else:
                        result.append(char)  # 한글이 아닌 경우 그대로 추가
                return ''.join(result)

            musicNum = len(df)
            success = 0
            fail = 0
            unused = 0
            opend = 0
            for idx, row in df.iterrows():
                try:
                    if pd.notna(row['미사용']):
                        self.log(f'추출 스킵 : {idx+1:03}행 (미사용)')
                        unused += 1
                        continue
                    
                    if pd.notna(row['오프닝/엔딩']):
                        self.log(f'추출 스킵 : {idx+1:03}행 (오프닝/엔딩)')
                        opend += 1
                        continue
                    
                    empty = []
                    if pd.isna(row['범주']):
                        empty.append('범주')
                    if pd.isna(row['힌트1']):
                        empty.append('힌트1')
                    if pd.isna(row['가수']):
                        empty.append('가수')
                    if pd.isna(row['제목']):
                        empty.append('제목')
                    if pd.isna(row['Start']):
                        empty.append('Start')
                    if pd.isna(row['End']):
                        empty.append('End')
                    if pd.isna(row['정답 리스트1']):
                        empty.append('정답 리스트1')
                    
                    if empty:
                        empty_list = ', '.join(empty)
                        self.log(f'추출 실패 : {idx+1:03}행 (공백 : {empty_list})')
                        
                    if row['범주'] in categoryName:
                        index = categoryName.index(row['범주'])
                        categoryIndex.append(index)
                        categoryInclude[index] += 1
                    else:
                        categoryName.append(row['범주'])
                        categoryIndex.append(categoryNum)
                        categoryInclude.append(1)
                        categoryNum += 1

                    hint += f'EPD(Db("{row["힌트1"]}")), '
                    artist += f'EPD(Db("{row["가수"]} - {row["제목"]}")), '

                    count = 0
                    answers = row['정답 리스트1'].split(',')  # ,로 구분된 정답 분리
                    count += len(answers)

                    if pd.notna(row['정답 리스트2']):
                        answers += row['정답 리스트2'].split(',')
                    count += len(answers) << 0x8
                        
                    answer_db_format = ', '.join([f'Db("{answer.strip()}")' for answer in answers])
                    answer_list += f'[{answer_db_format}], '

                    first_answer = answers[0].strip()
                    cho = extract_chosung(first_answer)
                    chosung += f'EPD(Db("{cho}")), '

                    answer_count += f'{count}, '
                    music_length += f'{int(row["End"] - row["Start"])}, '

                    self.log(f'추출 성공 : {idx+1:03}행')
                    success += 1

                except Exception as e:
                    self.log(f'추출 실패 : {idx+1:03}행 ({e})')
                    fail += 1
                    return

            with open(f'{os.path.dirname(self.excel_path.get())}/src/musicInfo.eps', 'w', encoding='utf-8') as outfile:
                outfile.write(f'const musicNumMax = {musicNum-unused-opend};\n')
                outfile.write(f'const categoryNum = {categoryNum};\n')

                outfile.write('const categoryActive = EUDArray(categoryNum);\n') 

                outfile.write('const categoryInclude = [')
                for i in range(len(categoryInclude)-1):
                    outfile.write(f'{categoryInclude[i]}, ')
                outfile.write(f'{categoryInclude[-1]}];\n')

                outfile.write('const categoryName = [')
                for i in range(len(categoryName)-1):
                    outfile.write(f'EPD(Db("{categoryName[i]}")), ')
                outfile.write(f'EPD(Db("{categoryName[-1]}"))];\n')

                outfile.write('const categoryIndex = [')
                for i in range(len(categoryIndex)-1):
                    outfile.write(f'{categoryIndex[i]}, ')
                outfile.write(f'{categoryIndex[-1]}];\n')
                
                outfile.write(f'{music_length[:-2]}];\n')
                outfile.write(f'{answer_count[:-2]}];\n')
                outfile.write(f'{answer_list[:-2]}];\n')
                outfile.write(f'{artist[:-2]}];\n')
                outfile.write(f'{hint[:-2]}];\n')
                outfile.write(f'{chosung[:-2]}];\n')

            self.log(f'총 {musicNum}개 중 {success}개 성공, {fail}개 실패, 미사용 {unused}개, 오프닝/엔딩 {opend}개를 스킵했습니다.')
        
        thread = threading.Thread(target=extract)
        thread.start()
    
    def log(self, message):
        """로그 메시지를 출력하는 함수"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state="normal")  # Text 위젯을 수정 가능 상태로 변경
        self.log_text.insert(tk.END, message + "\n")  # 메시지 삽입
        self.log_text.yview(tk.END)  # 자동으로 최신 로그로 스크롤
        self.log_text.config(state="disabled")  # 수정 불가능 상태로 설정

# Tkinter 윈도우 실행
if __name__ == "__main__":
    root = tk.Tk()
    icon_image = PhotoImage(data=icon_data)
    root.iconphoto(True, icon_image)
    app = App(root)
    root.mainloop()