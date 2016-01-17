from django.shortcuts import render
import non_rel

import time


# Create your views here.


from django.http import HttpResponse


def index(request):

    library = "xcite/mtd - mikethedrummer/wav loops/09"
    #cursor = non_rel.db.disco_a.find().sort('insert_time', non_rel.pymongo.DESCENDING).limit(1)
    #cursor = non_rel.db.disco_a.find().distinct('library')
    cursor = non_rel.db.disco_a.find({'library':library})
   

    for d in cursor:
	print d

    return HttpResponse("Hello, world. You're at the polls index.")
