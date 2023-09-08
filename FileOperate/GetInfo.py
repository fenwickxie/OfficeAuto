import os
import platform
from datetime import datetime


class GetInfo:
	def __init__(self, file_path):
		self.file_path = file_path
	
	def get_file_date(self):
		if platform.system() == 'Windows':
			create_time = os.path.getctime(self.file_path)
			modify_time = os.path.getmtime(self.file_path)
			infor = os.path.getatime(self.file_path)
		elif platform.system() == 'Linux' or platform.system() == 'Darwin':
			create_time = os.path.getctime(self.file_path)
			modify_time = os.path.getmtime(self.file_path)
		else:
			create_time = modify_time = None
		
		if create_time is not None:
			create_time_formatted = datetime.utcfromtimestamp(create_time).strftime('%Y%m%d')
			print(f'创建日期(YYMMDD): {create_time_formatted}')
		else:
			print('无法获取创建日期')
		
		if modify_time is not None:
			modify_time_formatted = datetime.utcfromtimestamp(modify_time).strftime('%Y%m%d')
			print(f'修改日期(YYMMDD): {modify_time_formatted}')
		else:
			print('无法获取修改日期')
	
	def get_movie_date(self):
		import subprocess
		import json
		
		if os.path.exists(self.file_path):
			# 使用ffprobe获取视频文件信息，包括创建媒体日期
			command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'format_tags=creation_time', '-of', 'default=nw=1:nk=1', file_path]
			result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
			
			if result.returncode == 0:
				# 解析ffprobe的输出，获取创建媒体日期
				output = result.stdout.strip()
				if output:
					create_time = output.strip()
					print(f'创建媒体日期: {create_time}')
				else:
					print('无法获取创建媒体日期')
			else:
				print('无法获取创建媒体日期')
		else:
			print('文件不存在')
	
	def get_image_creation_date(self):
		from PIL import Image
		from PIL.ExifTags import TAGS, GPSTAGS
		try:
			with Image.open(self.file_path) as img:
				exif_data = img._getexif()
				if exif_data is not None:
					for tag, value in exif_data.items():
						tag_name = TAGS.get(tag, tag)
						if tag_name == 'DateTimeOriginal':
							# 返回日期形式如 "2023:09:07 00:41:49"
							return value.replace(":", "").replace(" ", "_")
					return "拍摄日期未找到"
				else:
					return "没有 Exif 数据"
		except Exception as e:
			return f"发生错误: {str(e)}"


# 替换成你的图片文件路径
file_path = r"E:\Source\Pictures\20221217 The Chaser\1 (2).jpg"
getInfo = GetInfo(file_path)
result = getInfo.get_image_creation_date()
print(result)
