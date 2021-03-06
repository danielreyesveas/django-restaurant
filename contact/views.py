from django.shortcuts import render
from django.http import JsonResponse
from .forms import ContactForm
from .utils import api_response
import time
import json
from .constants import contact_template_slug, newsletter_template_slug, email_sender_url, email_sender_api_key
import urllib3

def contact(request):
    form = ContactForm

    context = {'form': form}
    return render(request, 'contact/contact.html', context)

def send_email(request):
    json_response = {'success': False}

    http = urllib3.PoolManager()

    data = json.loads(request.body.decode("utf-8"))

    if('subject' not in data): 
        json_response['msg'] = 'El campo \'subject\' no puede estar vacío' 
        return api_response(json_response)
    elif('email' not in data): 
        json_response['msg'] = 'El campo \'email\' no puede estar vacío' 
        return api_response(json_response)
    elif('content' not in data): 
        json_response['msg'] = 'El campo \'content\' no puede estar vacío' 
        return api_response(json_response)

    name = data['name']
    email = data['email']
    subject = data['subject']
    content = data['content']

    attempt_num = 0
    while attempt_num < 1:       
        body = {'name': name, 'from': email, 'subject': subject, 'content': content, 'template_slug': contact_template_slug, 'type': 'contact'}
        headers = {'Content-Type': 'application/json', 'api-key': email_sender_api_key}
        response = http.request(
            'POST',
            email_sender_url,
            body=json.dumps(body),
            headers=headers
        )
        if response.status == 200:
            data = json.loads(response.data.decode('utf-8'))
            return JsonResponse(data)
        else:
            attempt_num += 1
            time.sleep(5) 
    
    json_response["msg"] = "Hubo un problema con la solicitud."

    return JsonResponse(json_response)

def subscribe_newsletter(request):
    json_response = {'success': False}
    
    http = urllib3.PoolManager()

    data = json.loads(request.body.decode("utf-8"))

    if('email' not in data): 
        json_response['msg'] = 'El campo \'email\' no puede estar vacío' 
        return api_response(json_response)
   
    email = data['email']    
   
    attempt_num = 0
    while attempt_num < 1:       
        body = {'from': email, 'template_slug': newsletter_template_slug, 'type': 'newsletter'}
        headers = {'Content-Type': 'application/json', 'api-key': email_sender_api_key}
        response = http.request(
            'POST',
            email_sender_url,
            body=json.dumps(body),
            headers=headers
        )
        if response.status == 200:
            data = json.loads(response.data.decode('utf-8'))
            return JsonResponse(data)
        else:
            attempt_num += 1
            time.sleep(5) 

    json_response["msg"] = "Hubo un problema con la solicitud."

    return JsonResponse(json_response)