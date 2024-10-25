import os
import io
import json
import subprocess
import tkinter as tk
import threading
from tkinter import simpledialog, filedialog, messagebox
import pandas as pd
from yt_dlp import YoutubeDL
from pydub import AudioSegment

Version = 'v2.0'
settings_file = 'settings.json'

class App:
    def __init__(self, root):
        self.root = root
        
        #타이틀
        self.root.title(f"EZDown {Version}")

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
        self.button_frame.grid(row=3, column=0, columnspan=4, pady=10)

        # 음원 다운로드 버튼
        self.button_download = tk.Button(self.button_frame, text="음원 다운로드", width=15, command=self.music_download)
        self.button_download.grid(row=3, column=0, padx=10, pady=10)

        # 음원 자르기
        self.button_cut = tk.Button(self.button_frame, text="음원 자르기", width=15, command=self.music_cut)
        self.button_cut.grid(row=3, column=1, padx=10, pady=10)

        # 볼륨 조절
        self.button_volume = tk.Button(self.button_frame, text="볼륨 조절", width=15, command=self.music_volume)
        self.button_volume.grid(row=3, column=2, padx=10, pady=10)

        # 정보 추출 버튼
        self.button_extract = tk.Button(self.button_frame, text="정보 추출", width=15, command=self.extract_info)
        self.button_extract.grid(row=3, column=3, padx=10, pady=10)

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
        elif not self.download_path.get():
            messagebox.showerror("에러", "원본 음원 저장 경로를 선택해주세요.")
            return
        
        if not os.path.exists(self.download_path.get()):
            os.makedirs(self.download_path.get())

        def download():
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.download_path.get(), '%(id)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
            }
            
            # 엑셀 파일 열기
            try:
                df = pd.read_excel(self.excel_path.get())
            except Exception as e:
                messagebox.showerror("에러", f"엑셀 파일을 불러오는 중 오류가 발생했습니다. : {e}")
                return

            musicNum = len(df)
            success = 0
            fail = 0
            skip = 0
            with YoutubeDL(ydl_opts) as ydl:
                for idx, row in df.iterrows():
                    video_url = row['Addr']
                    try:
                        info_dict = ydl.extract_info(video_url, download=False)
                        video_id = info_dict.get("id", None)
                        downloaded_file = os.path.join(self.download_path.get(), f'{video_id}.mp3')

                        if os.path.exists(downloaded_file):
                            self.log(f'다운로드 스킵 : {idx+1:03} - {row["제목"]}')
                            skip += 1
                            continue

                        ydl.extract_info(video_url, download=True)
                        self.log(f'다운로드 성공 : {idx+1:03} - {row["제목"]}')
                        success += 1

                    except Exception as e:
                        self.log(f'다운로드 실패 : {idx+1:03} - {row["제목"]} ({e})')
                        fail += 1

            self.log(f'총 {musicNum}개 중 {success}개 성공, {fail}개 실패, {skip}개를 건너뛰었습니다.')
        
        thread = threading.Thread(target=download)
        thread.start()

    def music_cut(self):
        """음원을 자르는 함수"""
        # 경로 검사
        if not self.excel_path.get():
            messagebox.showerror("에러", "불러올 엑셀 파일을 선택해주세요.")
            return
        elif not self.download_path.get():
            messagebox.showerror("에러", "원본 음원 저장 경로를 선택해주세요.")
            return
        elif not self.cut_path.get():
            messagebox.showerror("에러", "자른 음원 저장 경로를 선택해주세요.")
            return
        
        if not os.path.exists(self.download_path.get()):
            os.makedirs(self.download_path.get())
        if not os.path.exists(self.cut_path.get()):
            os.makedirs(self.cut_path.get())

        def cut():
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.download_path.get(), '%(id)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
            }
            
            # 엑셀 파일 열기
            try:
                df = pd.read_excel(self.excel_path.get())
            except Exception as e:
                messagebox.showerror("에러", f"엑셀 파일을 불러오는 중 오류가 발생했습니다. : {e}")
                return

            musicNum = len(df)
            success = 0
            fail = 0
            skip = 0
            with YoutubeDL(ydl_opts) as ydl:
                for idx, row in df.iterrows():
                    video_url = row['Addr']
                    try:
                        info_dict = ydl.extract_info(video_url, download=False)
                        video_id = info_dict.get("id", None)
                        downloaded_file = os.path.join(self.download_path.get(), f'{video_id}.mp3')

                        if os.path.exists(downloaded_file):
                            start_time = row['Start'] * 1000
                            end_time = row['End'] * 1000
                            # 파일을 메모리로 읽어서 처리
                            with open(downloaded_file, 'rb') as f:
                                audio_data = f.read()
                            # 오디오 파일을 메모리에서 불러와서 지정된 구간을 잘라내기
                            audio = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
                            trimmed_audio = audio[start_time:end_time]
                            # 잘라낸 오디오를 순서대로 저장
                            filename = f'{idx+1:03}.mp3'
                            trimmed_audio.export(os.path.join(self.cut_path.get(), filename), format="mp3", bitrate="320k")
                            self.log(f'자르기 성공 : {idx+1:03} - {row["제목"]}')
                            success += 1
                        else:
                            self.log(f'음원 파일 없음 (스킵) : {idx+1:03} - {row["제목"]}')
                            skip += 1
                            continue

                    except Exception as e:
                        self.log(f'자르기 실패 : {idx+1:03} - {row["제목"]} ({e})')
                        fail += 1

            self.log(f'총 {musicNum}개 중 {success}개 성공, {fail}개 실패, {skip}개를 건너뛰었습니다.')
        
        thread = threading.Thread(target=cut)
        thread.start()
    
    def music_volume(self):
        """볼륨을 조절하는 함수"""
        # 경로 검사
        if not self.excel_path.get():
            messagebox.showerror("에러", "불러올 엑셀 파일을 선택해주세요.")
            return
        elif not self.cut_path:
            messagebox.showerror("에러", "자른 음원 저장 경로를 선택해주세요.")
            return

        if not os.path.exists(self.cut_path.get()):
            os.makedirs(self.cut_path.get())

        vol = simpledialog.askfloat("볼륨 설정기", "설정할 볼륨을 입력하세요.\n추천값 : 93.0±", parent=root)
        if not vol:
            self.log("볼륨 조절 작업 취소")
            return
        vol -= 89.0

        def volume():    
            # 엑셀 파일 열기
            try:
                df = pd.read_excel(self.excel_path.get())
            except Exception as e:
                messagebox.showerror("에러", f"엑셀 파일을 불러오는 중 오류가 발생했습니다. : {e}")
                return

            musicNum = len(df)
            success = 0
            fail = 0
            skip = 0
            for idx, row in df.iterrows():
                filename = f'{idx+1:03}.mp3'
                if not os.path.exists(os.path.join(self.cut_path.get(), filename)):
                    self.log(f'음원 파일 없음 (스킵) : {idx+1:03} - {row["제목"]}')
                    skip += 1
                    continue
                command = ['mp3gain', '-c', '-r', '-d', str(vol), os.path.join(self.cut_path.get(), filename)]
                try:
                    subprocess.run(command, check=True)
                    self.log(f'볼륨 조절 성공 : {idx+1:03} - {row["제목"]}')
                    success += 1
                except subprocess.CalledProcessError as e:
                    self.log(f'볼륨 조절 실패 : {idx+1:03} - {row["제목"]}')
                    fail +=1
                    continue

            self.log(f'총 {musicNum}개 중 {success}개 성공, {fail}개 실패, {skip}개를 건너뛰었습니다.')
        
        thread = threading.Thread(target=volume)
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
                messagebox.showerror("에러", f"엑셀 파일을 불러오는 중 오류가 발생했습니다. : {e}")
                return

            CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
            musicNum = len(df)
            genreNum = 0
            genreInclude = []
            genreName = []
            genreIndex = []
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

            for idx, row in df.iterrows():
                try:
                    if row["장르 구분"] in genreName:
                        index = genreName.index(row["장르 구분"])
                        genreIndex.append(index)
                        genreInclude[index] += 1
                    else:
                        genreName.append(row["장르 구분"])
                        genreIndex.append(genreNum)
                        genreInclude.append(1)
                        genreNum += 1

                    # 힌트, 가수와 제목, 정답 리스트, 정답 개수 데이터를 파일에 즉시 추가
                    hint += f'EPD(Db("{row["힌트1"]}")), '
                    artist += f'EPD(Db("{row["가수"]} - {row["제목"]}")), '

                    # 정답 리스트 처리
                    answers = row['정답 리스트'].split(',')  # ,로 구분된 정답 분리
                    answer_db_format = ', '.join([f'Db("{answer.strip()}")' for answer in answers])
                    answer_list += f'[{answer_db_format}], '

                    # 정답 리스트에서 첫 번째 정답의 초성만 추출하여 파일에 저장
                    first_answer = answers[0].strip()
                    cho = extract_chosung(first_answer)
                    chosung += f'EPD(Db("{cho}")), '

                    # 정답 개수 처리
                    answer_count += f'{len(answers)}, '

                    # 음악 길이 저장
                    music_length += f'{int(row["End"] - row["Start"])}, '

                except Exception as e:
                    self.log(f'추출 실패 : ({e})')
                    return
            
            with open('info.txt', 'w', encoding='utf-8') as outfile:
                outfile.write(f'const musicNumMax = {musicNum};\n')
                outfile.write(f'const genreNum = {genreNum};\n')

                outfile.write('const genreActive = EUDArray(genreNum);\n') 

                outfile.write('const genreInclude = [')
                for i in range(len(genreInclude)-1):
                    outfile.write(f'{genreInclude[i]}, ')
                outfile.write(f'{genreInclude[-1]}];\n')

                outfile.write('const genreName = [')
                for i in range(len(genreName)-1):
                    outfile.write(f'EPD(Db("{genreName[i]}")), ')
                outfile.write(f'EPD(Db("{genreName[-1]}"))];\n')

                outfile.write('const genreIndex = [')
                for i in range(len(genreIndex)-1):
                    outfile.write(f'{genreIndex[i]}, ')
                outfile.write(f'{genreIndex[-1]}];\n')
                
                outfile.write(f'{music_length[:-2]}];\n')
                outfile.write(f'{answer_count[:-2]}];\n')
                outfile.write(f'{answer_list[:-2]}];\n')
                outfile.write(f'{artist[:-2]}];\n')
                outfile.write(f'{hint[:-2]}];\n')
                outfile.write(f'{chosung[:-2]}];\n')

            self.log(f'추출에 성공했습니다.')
        
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
    app = App(root)
    root.mainloop()