import os.path

from FileOperate import DropDuplicates, Rename
from FileOperate.Achieve import multithread_winrar_compress, multithread_winrar_uncompress

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
	# base_path = r'D:\Fenwick\Videos'
	# for dir in os.listdir(base_path):
		path = r"D:\Fenwick\Downloads"
		# path = os.path.join(base_path, dir)
		if os.path.isdir(path):
			# rename = Rename(path)
			# DropDuplicates.remove_duplicates(path, 1, 1)
			# # pre = os.path.basename(path)+'_'
			# rename.rename_by_sort(1, prefix='', fill_char='0', length=3)
			# rename.rename_by_num(1, '0', 1, 3)
			# rename.add_prefix_or_suffix('20', '', '')
			# rename.replace_character(')','')
			# rename.change_extension('.7z')
			
			# multithread_winrar_compress(path, 1, 64, 0)
			multithread_winrar_uncompress(path,2)
