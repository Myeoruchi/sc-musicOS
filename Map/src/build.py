from eudplib import *
import os
import pathlib

from main import settings
settings: dict[str]

def set_property():
	chkt = GetChkTokenized()	
	SPRP = bytearray(chkt.getsection("SPRP"))
	FORC = bytearray(chkt.getsection("FORC"))

	SPRP[0:2] = i2b2(GetStringIndex(settings['title']))
	SPRP[2:4] = i2b2(GetStringIndex(settings['description']))
	FORC[8:10] = i2b2(GetStringIndex(settings['force1']))
	FORC[10:12] = i2b2(GetStringIndex(settings['force2']))

	chkt.setsection("SPRP", SPRP)
	chkt.setsection("FORC", FORC)

def build():
	global maker, leaderboard, hint1, ansAllow, forceTwoSec, hintTime, scoreMax, scoreDiff, segCount
	maker = EPD(Db(settings['maker']))
	leaderboard = settings['leaderboard']
	hint1 = EPD(Db(settings['hint1_name']))
	ansAllow = EPD(Db(settings['answer_allow']))
	forceTwoSec = True if settings['two_second'] == 'True' else False
	hintTime = EUDArray([int(settings['hint1_open']), int(settings['hint2_open'])])
	scoreMax = int(settings['score_max'])
	scoreDiff = int(settings['score_diff'])

	trimpath = settings['trimpath']
	with open(f'{os.path.join(trimpath, "info.txt")}', 'r', encoding='utf-8') as f:
		musicNum = f.readline()
		assert musicNum != 'fail', "EZDown을 이용해 실패없이 음원을 잘라주세요."
		musicNum = int(musicNum)
		op = f.readline()
		end = f.readline()
		if op: op = int(op)
		if end: end = int(end)
	
	segment_count = []
	for idx in range(musicNum):
		file_path = trimpath + f'/{idx+1:03}'
		segment_count.append(len(os.listdir(file_path)))
		for seg_idx in range(segment_count[-1]):
			MPQAddFile(f'{idx}-{seg_idx}', pathlib.Path(f'{file_path}/{seg_idx:03}.ogg').read_bytes())
	
	if op:
		file_path = trimpath + '/OP'
		segment_count.append(len(os.listdir(file_path)))
		for seg_idx in range(segment_count[-1]):
			MPQAddFile(f'{musicNum}-{seg_idx}', pathlib.Path(f'{file_path}/{seg_idx:03}.ogg').read_bytes())
	
	if end:
		file_path = trimpath + '/ED'
		segment_count.append(len(os.listdir(file_path)))
		for seg_idx in range(segment_count[-1]):
			MPQAddFile(f'{musicNum+1}-{seg_idx}', pathlib.Path(f'{file_path}/{seg_idx:03}.ogg').read_bytes())
	segCount = EUDArray(segment_count)

	for name in ['opening1', 'opening2', 'click', 'skip', 'correct']:
		if name:
			MPQAddFile(f'{name}', pathlib.Path(f'./effect/{settings[name]}').read_bytes())

set_property()
build()