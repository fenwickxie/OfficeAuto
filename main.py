import os.path

from FileOperate import DropDuplicates, Rename
from FileOperate.Achieve import multithread_winrar_compress

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
	path = r"C:\Users\fy.xie\Desktop\temp\test"
	rename = Rename(path)
	# DropDuplicates.remove_duplicates(path, 1, 1)
	# # pre = os.path.basename(path)+'_'
	# rename.rename_by_sort(path, 1, prefix='', fill_char='0', length=3)
	# rename.add_prefix_or_suffix(path, '[铃木美咲Misaki Suzuki]', '', ' ')
	# multithread_winrar_compress(path, 27, 64, 2)
	rename.change_extension('.txt')
