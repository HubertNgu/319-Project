
class ValueCounter(object):

	def __init__(self):
		self.count = dict()

	def update(self, key, value):
		if key not in self.count:
			self.count[key] = value
		else:
			self.count[key] = self.count[key] + value

	def get(self, key):
		if key in self.count:
			return self.count[key]
		else:
			return 0

	def items(self):
		return self.count.items()