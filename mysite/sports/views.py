from django.http import HttpResponse
from models import Place, Entry
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404

#def 500raised(request):
#	render_to_response('places/500.html', {"blank":blank})

class infoData():
	def __init__(self, time, crowd):
		self.time = time
		if crowd == 0:
			self.crowd = "Post-Apocalyptic (1)"
		elif crowd == 1:
			self.crowd = "Sparse (2)"
		elif crowd == 2:
			self.crowd = "Spacious (3)"
		elif crowd == 3:
			self.crowd = "Comfortable (4)"
		elif crowd == 4:
			self.crowd = "Full (5)"
		elif crowd == 5:
			self.crowd = "Packed (6)"
		elif crowd > 5:
			self.crowd = "Livestock Pen (7)"
		else:
			self.crowd = "Sorry, not enough data."

def main(request):
	c = {"blank":"blank"}
	return render_to_response ('places/main.html',c, context_instance=RequestContext(request))	


def index(request, method):
	if method == "al":
		list_of_places = Place.objects.all().order_by('name')
	elif method == "crd_up":
		list_of_places = Place.objects.all().order_by('average_crowd', 'name')
	elif method == "crd_dn":
		list_of_places = Place.objects.all().order_by('-average_crowd', 'name')
	else:
		list_of_places = ["INVALID URL, SORRY"]
	#return HttpResponse(len(list_of_places))
	final_list = []
	for list_item in list_of_places:
		list_item = list_item.name.replace(" ","_")
		final_list.append(list_item)
	return render_to_response ('places/index.html', {"places":final_list})

def getinfo (request):
	c = {"blank":"blank"}
	return render_to_response ('places/getInfo.html',{"blank":'blank'}, context_instance=RequestContext(request))

def update():
	return null

def dispinfo (request, place_name):
	entry_times = [[],[],[],[],[],[]]
	data = [0,0,0,0,0,0]	
	times = [0,0,0,0,0,0]
	counts = [0,0,0,0,0,0]
	place_name = place_name.replace(" ","_")
	found = False
	if (request.POST):
		a = get_object_or_404(Place, name=place_name)
		"""b=findstring(place_name)
		if b == "Non existent entry":
			raise Http404
		else:
			a = b"""
		#a = get_object_or_404(Place, 'name'=place_name)
		#return HttpResponse(request.POST['comments'])
		time = request.POST['time']
		crowd = request.POST['crowded']
		if (request.POST['details']):
			details = request.POST['details']
			a.details = details
		if (request.POST['comments']):
			comments = request.POST['comments']
			a.entry_set.create(crowd_level = crowd, time = time, comment = comments)
		else:
			a.entry_set.create(crowd_level = crowd, time = time, comment = 'none')
		a.save()
		a.average_crowd()


	for thing in Place.objects.all():
		if place_name == thing.name.replace(" ","_"):
			place = thing
			found = True
	'''place_name = place_name.replace("_"," ")
	place_name = place_name.capitalize()'''	
	place_name = place_name.replace(" ","_")
	a = Place.objects.get(name__iexact=place_name)
	place = a
	if not place:
		raise Http404
	entries = a.entry_set.all()
	for entry in entries:
		entry_times[entry.time].append(entry.crowd_level)
		counts[entry.time] += 1
	
	for i in xrange(6):
		if counts[i] > 0:
			times[i] = int(sum(entry_times[i])/counts[i])
		else:
			times[i] = -1
	
	data[0] = infoData("Early Morning", times[0])
	data[1] = infoData("Late Morning", times[1])
	data[2] = infoData("Mid Day", times[2])
	data[3] = infoData("Afternoon", times[3])
	data[4] = infoData("Evening", times[4])
	data[5] = infoData("Midnight", times[5])

	return render_to_response ('places/placeInfo.html', {"place":place.name, 'data':data, 'entries':place.entry_set.all()})
		#return HttpResponse(str(times[2]) + str(counts[2]) + str(sum(entry_times[2])) + str(sum(entry_times[0])/counts[2]) + str(testSum) + str(entry_times[2][0]) + place.name)
def createentry(request):
	return render_to_response ('places/createpage.html', {"blank":"blank"}, context_instance=RequestContext(request))

def createentrycontinue(request):
	title = request.POST['title'].replace(" ", "_")
	location = request.POST['location']
	comments = request.POST['details']
	p = Place(name = title, location=location, details=comments)
	p.save()
	return render_to_response('places/createpagecontinue.html', {"placename": p.name}, context_instance=RequestContext(request))
	#return HttpResponse (p.name)

def findstring (term):
	places = Place.objects.all()	
	for place in places:
		place.name = place.name.replace(' ','_')
		if place.name == term:
			return place
	return "Non existent entry"

def editentry (request, place_name):
	a = get_object_or_404(Place, name=place_name)
	return render_to_response('places/wereyouhere.html', {'placeinfo':a}, context_instance=RequestContext(request))

def results (request):
	term = request.POST['term']
	hits = search(term)
	if len(hits) < 1:
		error_message = True
	else:
		error_message = False
	return render_to_response ('places/results.html', {"hits": hits, 'error_message': error_message}, context_instance=RequestContext(request))
		

def search(term):
	term = term.capitalize()
	hits = []
	places = Place.objects.all()
	termLength = len(term)
	spaces = False
	if term.find(' ') is not -1:
		spaces = True

	if spaces is False:
		for place in places:
			place.name = place.name.replace(' ','_').capitalize()
			if place.name.find(term) is not -1:
				hits.append(place.name)
			else:
				for entry in place.entry_set.all():
					if entry.comment.find(term) is not -1:
						hits.append(place.name)


	else:
		termPart1 = term[:term.find(' ')]
		termPart2 = term[term.find(' ')+1:]
		hits.append(search(termPart1))
		hits.append(search(termPart2))
	

	return hits
