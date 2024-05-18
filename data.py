class Data:
	def __init__(self, ui):
		self.ui = ui
		self._coins = 0
		self._health = 5
		self.ui.create_hearts(self._health)

		self.unlocked_level = 0
		self.current_level = 0