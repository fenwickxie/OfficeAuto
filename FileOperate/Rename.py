import os
import re
from tools import calculate_time


class Rename:
	def __init__(self, path):
		"""
		:param path: path of files
		"""
		self.path = path
	
	def rename_by_sort(self, start: int, prefix: str = '', fill_char: str = '0', length: int = 3):
		"""
		:param start: start of the name
		:param prefix: char of prefix
		:param fill_char: char of filling before filename，default ‘0’
		:param length: length of filename，default 3
		:return: None
		"""
		# 列出目录下所有文件
		filenames = os.listdir(self.path)
		
		# 按照文件名排序
		filenames.sort(key=str.lower)
		
		# 遍历文件并重命名
		for index, filename in enumerate(filenames):
			if os.path.isfile(os.path.join(self.path, filename)):
				# 构造新文件名
				new_filename_no_extension = prefix + "{:{fill_char}>{length}}".format(start + index, fill_char=fill_char, length=length)
				extension = filename.split('.')[-1].lower()
				new_filename = '{}.{}'.format(new_filename_no_extension, extension)
				# 拼接路径和文件名
				src = os.path.join(self.path, filename)
				dst = os.path.join(self.path, new_filename)
				# 重命名文件
				os.rename(src, dst)
	
	@calculate_time
	def rename_by_num(self, num_loc: int = 0, fill_char: str = '0', start: int = 0, length: int = 3):
		"""
		:param start: start of name
		:param num_loc: 根据字符串中的第几组连续数字进行排序，default 0
		:param fill_char: char of filling before filename，default ‘0’
		:param length: length of filename，default 3
		:return: None
		"""
		# 列出目录下所有文件
		filenames = os.listdir(self.path)
		filenames = [file for file in filenames if os.path.isfile(os.path.join(self.path,file))]
		# 按照文件名中的数字排序
		try:
			filenames.sort(key=lambda l: int(re.findall('\d+', l)[num_loc]))  # 找出字符串中的第一组连续数字并依据其整形进行排序
		except Exception as e:
			print(e)
		# 遍历文件并重命名
		for index, filename in enumerate(filenames):
			# 构造新文件名
			new_filename_no_extension = "{:{fill_char}>{length}}".format(index + start, fill_char=fill_char, length=length)
			extension = filename.split('.')[-1].lower()
			new_filename = '{}.{}'.format(new_filename_no_extension, extension)
			# 拼接路径和文件名
			src = os.path.join(self.path, filename)
			dst = os.path.join(self.path, new_filename)
			# 重命名文件
			os.rename(src, dst)
		return self
	
	@calculate_time
	def rename_by_size(self):
		"""
		:param self.self.self.self.self.path:
		:return:
		"""
		
		# 列出目录下所有文件
		files = os.listdir(self.path)
		
		# 获取文件大小并按照文件大小排序
		files.sort(key=lambda x: os.path.getsize(os.path.join(self.path, x)))
		
		# 初始化计数器
		count = 1
		
		# 遍历文件并重命名
		for file in files:
			__filename, extension = os.path.splitext(file)
			
			new_name = str(count) + extension
			
			# 如果新文件名已存在，则在文件名后面添加数字
			j = 1
			while os.path.exists(os.path.join(self.path, new_name)):
				# 构造新文件名
				new_name = f'{count}_{j}.{extension[1:]}'
				j += 1
			# 拼接路径和文件名
			src = os.path.join(self.path, file)
			dst = os.path.join(self.path, new_name)
			# 重命名文件
			os.rename(src, dst)
			# 计数器加一
			count += 1
		return self
	
	@calculate_time
	def rename_by_type(self):
		"""
		:return:
		"""
		# 遍历目录
		for root, dirs, files in os.walk(self.path):
			# 获取文件列表，并排序
			files = sorted(files, key=str.lower)
			
			# 遍历文件
			for i, file in enumerate(files):
				# 获取文件类型和路径
				file_type = file.split('.')[-1].lower()
				file_path = os.path.join(root, file)
				
				# 获取文件名前缀和新文件名
				prefix = file_type
				new_file_name = f'{prefix}_{i + 1}.{file_type}'
				
				# 如果新文件名已存在，则在文件名后面添加数字
				j = 1
				while os.path.exists(os.path.join(root, new_file_name)):
					new_file_name = f'{prefix}_{i + 1}_{j}.{file_type}'
					j += 1
				
				# 重命名文件
				os.rename(file_path, os.path.join(root, new_file_name))
		return self
	
	def add_prefix_or_suffix(self, prefix: str = '', suffix: str = '', separator: str = ''):
		"""
		add prefix or suffix into filename
		:param prefix: string of prefix
		:param suffix: string of suffix
		:param separator: string of separator
		:return: None
		"""
		
		# 列出目录下所有文件
		filenames = os.listdir(self.path)
		
		# 按照文件名排序
		filenames.sort(key=str.lower)
		
		# 遍历文件并重命名
		for index, filename in enumerate(filenames):
			# 构造新文件名
			filename_no_extension, extension = os.path.splitext(filename)
			
			if prefix != '' and suffix == '':
				new_filename_no_extension = prefix + separator + filename_no_extension
			elif prefix == '' and suffix != '':
				new_filename_no_extension = filename_no_extension + separator + suffix
			elif prefix != '' and suffix != '':
				new_filename_no_extension = prefix + separator + filename_no_extension + separator + suffix
			else:
				raise TypeError('未指定前缀和后缀')
			new_filename = new_filename_no_extension + extension
			# 拼接路径和文件名
			src = os.path.join(self.path, filename)
			dst = os.path.join(self.path, new_filename)
			# 重命名文件
			os.rename(src, dst)
		return self
	
	def change_extension(self, new_extension: str):
		"""
		:param new_extension: new extension to change
		:return: self
		"""
		# 列出目录下所有文件
		filenames = os.listdir(self.path)
		
		# 按照文件名排序
		filenames.sort(key=str.lower)
		
		# 遍历文件并重命名
		for index, filename in enumerate(filenames):
			src_path = os.path.join(self.path, filename)
			if os.path.isfile(src_path):
				# 构造新文件名
				filename_no_extension, extension = os.path.splitext(filename)
				
				if new_extension[0] == '.':
					filename_with_new_extension = filename_no_extension + new_extension.lower()
				else:
					filename_with_new_extension = filename_no_extension + '.' + new_extension.lower()
				
				# 拼接路径和文件名
				dst_path = os.path.join(self.path, filename_with_new_extension)
				# 重命名文件
				os.rename(src_path, dst_path)
		return self
	
	def replace_character(self, character_old: str, character_new, include_dir: bool = False):
		"""
		:param character_new:
		:param include_dir:
		:param character_old:
		:return:
		"""
		# 列出目录下所有文件
		filenames = os.listdir(self.path)
		
		# 按照文件名排序
		filenames.sort(key=str.lower)
		
		# 遍历文件并重命名
		for index, filename in enumerate(filenames):
			src_path = os.path.join(self.path, filename)
			if os.path.isfile(src_path):
				# 构造新文件名
				filename_no_extension, extension = os.path.splitext(filename)
				if character_old is not None:
					filename_replaced = filename_no_extension.replace(character_old, character_new) + extension.lower()
				# 拼接路径和文件名
				dst_path = os.path.join(self.path, filename_replaced)
				# 重命名文件
				os.rename(src_path, dst_path)
			elif include_dir:
				if character_old is not None:
					filename_replaced = filename.replace(character_old, character_new)
				# 拼接路径和文件夹名
				dst_path = os.path.join(self.path, filename_replaced)
				# 重命名文件夹
				os.rename(src_path, dst_path)
		return self
