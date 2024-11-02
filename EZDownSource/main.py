import os
import json
import subprocess
import tkinter as tk
import threading
from tkinter import simpledialog, filedialog, messagebox
import pandas as pd
from yt_dlp import YoutubeDL

Version = 'v2.1'
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
        if not self.download_path.get():
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
                        info_dict = ydl.extract_info(video_url, download=False)
                        video_id = info_dict.get("id", None)
                        downloaded_file = os.path.join(self.download_path.get(), f'{video_id}.mp3')

                        if os.path.exists(downloaded_file):
                            self.log(f'다운로드 스킵 : {idx+1:03}행 (파일 존재함)')
                            skip += 1
                            continue

                        ydl.extract_info(video_url, download=True)
                        self.log(f'다운로드 성공 : {idx+1:03}행')
                        success += 1

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
                        self.log(f'자르기 스킵 : {idx+1:03}행 (미사용)')
                        skip += 1
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
                        self.log(f'자르기 실패 : {idx+1:03}행 (공백 : {empty_list})')
                        fail += 1
                        continue

                    try:
                        info_dict = ydl.extract_info(row['Addr'], download=False)
                        video_id = info_dict.get("id", None)
                        downloaded_file = os.path.join(self.download_path.get(), f'{video_id}.mp3')

                        if os.path.exists(downloaded_file):
                            output_file = os.path.join(self.cut_path.get(), f'{idx+1-unused:03}.mp3')
                            command = [
                                'ffmpeg', '-y', '-i', downloaded_file,
                                '-ss', str(row['Start']), '-to', str(row['End']),
                                '-c', 'copy', output_file
                            ]
                            subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, check=True)
                            self.log(f'자르기 성공 : {idx+1:03}행 → {idx+1-unused:03}')
                            success += 1
                        else:
                            self.log(f'자르기 스킵 : {idx+1:03}행 (파일 없음)')
                            skip += 1
                            continue

                    except Exception as e:
                        self.log(f'자르기 실패 : {idx+1:03}행 ({e})')
                        fail += 1

            self.log(f'총 {musicNum}개 중 {success}개 성공, {fail}개 실패, {skip}개 (미사용 {unused}개)를 건너뛰었습니다.')
        
        thread = threading.Thread(target=cut)
        thread.start()
    
    def music_volume(self):
        """볼륨을 조절하는 함수"""
        # 경로 검사
        if not self.excel_path.get():
            messagebox.showerror("에러", "불러올 엑셀 파일을 선택해주세요.")
            return
        if not self.cut_path:
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
                messagebox.showerror("에러", f"엑셀 파일을 불러오는 중 오류가 발생했습니다. : ({e})")
                return

            musicNum = len(df)
            success = 0
            fail = 0
            skip = 0
            unused = 0
            for idx, row in df.iterrows():
                if pd.notna(row['미사용']):
                    self.log(f'볼륨 조절 스킵 : {idx+1:03}행 (미사용)')
                    skip += 1
                    unused += 1
                    continue

                filename = f'{idx+1-unused:03}.mp3'
                if not os.path.exists(os.path.join(self.cut_path.get(), filename)):
                    self.log(f'볼륨 조절 스킵 : {idx+1:03}행 ({filename} 파일 없음)')
                    skip += 1
                    continue

                command = ['mp3gain', '-c', '-r', '-d', str(vol), os.path.join(self.cut_path.get(), filename)]
                try:
                    subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW, check=True)
                    self.log(f'볼륨 조절 성공 : {idx+1:03}행 ({filename})')
                    success += 1

                except subprocess.CalledProcessError as e:
                    self.log(f'볼륨 조절 실패 : {idx+1:03}행 ({e})')
                    fail +=1
                    continue

            self.log(f'총 {musicNum}개 중 {success}개 성공, {fail}개 실패, {skip}개 (미사용 {unused}개)를 건너뛰었습니다.')
        
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
            for idx, row in df.iterrows():
                try:
                    if pd.notna(row['미사용']):
                        self.log(f'추출 스킵 : {idx+1:03}행 (미사용)')
                        unused += 1
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

                    self.log(f'추출 성공 : {idx+1:03} - {row["제목"]} ({idx+1-unused:03}.mp3)')
                    success += 1

                except Exception as e:
                    self.log(f'추출 실패 : {idx+1:03} - {row["제목"]} ({e})')
                    fail += 1
                    return
            
            with open('info.txt', 'w', encoding='utf-8') as outfile:
                outfile.write(f'const musicNumMax = {musicNum-unused};\n')
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

            self.log(f'총 {musicNum}개 중 {success}개 성공, {fail}개 실패, {unused}개를 미사용 했습니다.')
        
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