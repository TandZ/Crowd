from django.db import models

class Place(models.Model):
	name = models.CharField(max_length = 200)
	location = models.CharField(max_length = 200)
	details = models.CharField (max_length = 300)
	average_crowd = models.IntegerField()
	entries = []
	def __unicode__(self):
		return self.name

	def average_crowd(self):
		entries = self.entry_set.all()
		self.average_crowd = 0
		averages = [0,0,0,0,0,0]
		counts = [0,0,0,0,0,0]
		for entry in entries:
			averages[entry.time] = averages[entry.time] + entry.crowd_level
			counts[entry.time] += 1
		
		zeroes = [False,False,False,False,False,False]

		for i in xrange(6):
			if counts[i] > 0:
				averages[i] = averages[i] / counts[i]
			else:
				averages[i] = 0
				zeroes[i] = True
		
		final_count = 0
		for i in xrange(6):
			if zeroes[i] == False:
				self.average_crowd = self.average_crowd + averages[i]
				final_count = final_count + 1
		
		if final_count > 0:
			self.average_crowd = self.average_crowd / final_count
		else:
			final_count = 0
		
		return self.average_crowd
				

class Entry(models.Model):
	place = models.ForeignKey(Place)
	crowd_level = models.IntegerField()
	comment = models.CharField(max_length = 500)
	time = models.IntegerField()
	def __unicode__(self):
		return self.comment
