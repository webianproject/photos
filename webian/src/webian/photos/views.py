from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers
from django.http import HttpRequest, HttpResponse
from photos.models import Photo


def index(request):
    """ Returns either an HTML or JSON representation of a list of photos
    depending on the Accept header of the HTTP request"""
    if best_match(['application/json', 'text/html'], request.META['HTTP_ACCEPT']) == 'application/json':
        print 'json'
        return HttpResponse(serializers.serialize("json", Photo.objects.all()[:9]))
    else:
        print 'html'
        photo_list = Photo.objects.all()[:9]
        return render_to_response('index.html', {'photo_list': photo_list} )

def detail(request, photo_id):
    p = get_object_or_404(Photo, pk=photo_id)
    return render_to_response('detail.html', {'photo': p})

def parse_mime_type(mime_type):
    parts = mime_type.split(";")
    params = dict([tuple([s.strip() for s in param.split("=")]) 
      for param in parts[1:] ])
    (type, subtype) = parts[0].split("/")
    return (type.strip(), subtype.strip(), params)

def parse_media_range(range): 
    (type, subtype, params) = parse_mime_type(range)
    if not params.has_key('q') or not params['q'] or \
            not float(params['q']) or float(params['q']) > 1 \
           or float(params['q']) < 0:
        params['q'] = '1'
    return (type, subtype, params)

def quality_parsed(mime_type, parsed_ranges): 
    """Find the best match for a given mime_type against a list of
       media_ranges that have already been parsed by
       parse_media_range(). Returns the 'q' quality parameter of the
       best match, 0 if no match was found. This function bahaves the
       same as quality() except that 'parsed_ranges' must be a list of
       parsed media ranges. See http://www.xml.com/pub/a/2005/06/08/restful.html"""

    best_fitness = -1; best_match = ""; best_fit_q = 0

    (target_type, target_subtype, target_params) = parse_media_range(mime_type)
    for (type, subtype, params) in parsed_ranges:
        param_matches = sum([1 for (key, value) in \
                target_params.iteritems() if key != 'q' and \
                params.has_key(key) and value == params[key]])
        if (type == target_type or type == '*') and (subtype == target_subtype or subtype == "*"):
            fitness = (type == target_type) and 100 or 0
            fitness += (subtype == target_subtype) and 10 or 0
            fitness += param_matches
            if fitness > best_fitness:
                best_fitness = fitness
                best_fit_q = params['q']
    return float(best_fit_q)

def best_match(supported, header): 
    """Takes a list of supported mime-types and finds the best match
    for all the media-ranges listed in header. The value of header
    must be a string that conforms to the format of the HTTP Accept:
    header. The value of 'supported' is a list of mime-types.
    
    >>> best_match(['application/xbel+xml', 'text/xml'],\                 
        'text/*;q=0.5,*/*; q=0.1')
    'text/xml'    """
    parsed_header = [parse_media_range(r) for r in header.split(",")]
    weighted_matches = [(quality_parsed(mime_type, parsed_header), mime_type) 
      for mime_type in supported]
    weighted_matches.sort()
    return weighted_matches[-1][0] and weighted_matches[-1][1] or ''


