from pathlib import Path


class PathTools:
	def __init__(self, filename=None):
		self.filename = filename

	@property
	def get_current_folder_full(self):
		return 'Path(__file__).absolute().parent'

	@property
	def get_current_file_full(self):
		return 'Path(__file__).absolute()'

	@property
	def eval_script_path(self):
		file = Path(self.filename).name
		return f'Path(__file__).absolute().parent.joinpath("{file}")'

	@property
	def get_real_path(self):
		return 'Path(__file__).parent.resolve()'
