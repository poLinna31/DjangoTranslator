from django.shortcuts import render
from googletrans import Translator
from asyncio import run
from .models import Language
from .models import TranslateHistory

async def _func(_txt, _lang):
    tr = await Translator().translate(_txt, dest=_lang)
    return tr.text

langs = {
    'ru' : 'Русский',
    'en' : 'Английский',
    'ar' : 'Арабский',
    'es' : 'Испанский',
    'de' : 'Немецкий'
}

def index(request):    
    src_lang = request.POST.get('src_lang', 'ru')    
    trans_lang = request.POST.get('trans_lang', 'en')
    src_text = request.POST.get('txt', '')
    trans_text = src_text
    translate_history = TranslateHistory.objects.all()
    
    if request.POST.get('swap_langs') is not None:               
        src_lang, trans_lang = trans_lang, src_lang

    if request.POST.get('trans_btn') is not None:
        trans_text = run(_func(src_text, trans_lang))
        if src_text != '':
            TranslateHistory.objects.create(src_value=src_text, trans_value=trans_text, src_lang=src_lang, trans_lang=trans_lang)
        
    if request.POST.get('hist_btn') is not None:
        t_h = TranslateHistory.objects.get(id=request.POST.get('hist_btn'))
        src_lang = t_h.src_lang
        trans_lang = t_h.trans_lang
        trans_text = t_h.trans_value
    
    return render(request, 'main/index.html', {
        'src_lang' : Language(langs[src_lang], src_lang),
        'langs' : [ Language(langs[l], l) for l in langs ] ,
        'trans_lang' : Language(langs[trans_lang], trans_lang),
        'src_text' : trans_text,
        'hist_obj' : (translate_history[len(translate_history)-1] if translate_history else None)
    })    

  
def get_translate_list(request):    
    translate_history = TranslateHistory.objects.all()    
    if request.POST.get('hist_btn') is not None:
        t_h = TranslateHistory.objects.get(id=request.POST.get('hist_btn'))
        src_lang = t_h.src_lang
        trans_lang = t_h.trans_lang
        src_text = t_h.trans_value
        return render(request, 'main/index.html', {
            'src_lang' : Language(langs[src_lang], src_lang),
            'langs' : [ Language(langs[l], l) for l in langs ] ,
            'trans_lang' : Language(langs[trans_lang], trans_lang),
            'src_text' : src_text,
            'hist_obj' : (translate_history[0] if translate_history else None)
        })        
    return render(request, 'main/translate_list.html', {
        'translate_history' : translate_history
    })

