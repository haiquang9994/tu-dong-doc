# pages/views.py
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from http import HTTPStatus
from django.views.decorators.csrf import csrf_exempt
import json
from gtts import gTTS
import re
import base64
import hashlib
from pydub import AudioSegment

class HttpResponseMethodNotAllowed(HttpResponse):
    status_code = HTTPStatus.METHOD_NOT_ALLOWED

def homePageView(request):
    context = {
        "first_name": "Anjaneyulu",
        "last_name": "Batta",
        "address": "Hyderabad, India"
    }
    template_name = "home2.html"
    return render(request, template_name, context)

def aboutPageView(request):
    context = {
        "name": "Nguyễn Hải Quang",
        "email": "haiquang9994@gmail.com"
    }
    template_name = "about.html"
    return render(request, template_name, context)

def md5(text):
    m = hashlib.md5()
    m.update(text.encode())
    return m.hexdigest()

@csrf_exempt
def textToSpeech(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data['text']
        text = re.sub(r'\.', '. ', text)
        text = re.sub(r'\.\ \ ', '. ', text)
        text = re.sub(r'\.\ +\"', '."', text)
        rows = [r for r in re.compile("\.(\ )|\-").split(text.strip()) if (r != '' and r != None and r.strip() != "")]
        final_text = '. '.join(rows).strip()
        output = gTTS(final_text, lang="vi", slow=False)
        filename = 'mp3/' + md5(text) + '.mp3'
        output.save(filename)
        sound = AudioSegment.from_mp3(filename)
        faster_sound = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * 1.2)})
        faster_sound.export(filename, format="mp3")
        response_data = {}
        response_data['text'] = final_text
        response_data['base64'] = str(GlobalToBase64(filename))
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseMethodNotAllowed()

def GlobalToBase64(file):
    with open(file, 'rb') as fileObj:
        image_data = fileObj.read()
        base64_data = base64.b64encode(image_data)
        return base64_data.decode()

@csrf_exempt
def uploadFilePageView(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        text = ''
        for line in uploaded_file:
            text = text + line.decode()
        return HttpResponse(text)
    else:
        return HttpResponseMethodNotAllowed()
