# -*- coding: utf-8 -*-
#Библиотеки, които използват python и Kodi в тази приставка
import re
import sys
import os
import urllib
import urllib2
import xbmc, xbmcplugin,xbmcgui,xbmcaddon
import urlresolver
import base64

#Място за дефиниране на константи, които ще се използват няколкократно из отделните модули
__addon_id__= 'plugin.video.myonvideo'
__Addon = xbmcaddon.Addon(__addon_id__)
movico = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/Others-icon.png")
serico = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/serials-icon.png")
catalogue = base64.b64decode('aHR0cDovL215b252aWRlby5jb20vY2F0YWxvZ3VlLzE=')
movi = base64.b64decode('aHR0cDovL215b252aWRlby5jb20vY2F0ZWdvcnkvMzEvRmlsbWkvMQ==')
ser = base64.b64decode('aHR0cDovL215b252aWRlby5jb20vY2F0ZWdvcnkvMTkvU2VyaWFsaS8xLw==')
sernext = base64.b64decode('aHR0cDovL215b252aWRlby5jb20vY2F0ZWdvcnkvMTkvU2VyaWFsaS8xLw==')
search = base64.b64decode('aHR0cDovL215b252aWRlby5jb20vc2VhcmNoLnBocA==')
MUA = 'Mozilla/5.0 (Linux; Android 5.0.2; bg-bg; SAMSUNG GT-I9195 Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Version/1.0 Chrome/18.0.1025.308 Mobile Safari/535.19' #За симулиране на заявка от мобилно устройство
UA = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0' #За симулиране на заявка от  компютърен браузър


#Меню с директории в приставката
def CATEGORIES():
        addDir('Търсене',search,11,'DefaultFolder.png')
        addDir('Последно добавени',catalogue,1,movico)
        addDir('Филми',movi,2,movico)
        addDir('Сериали',ser,4,serico)
        #addDir('','',1,'')




#Разлистване видеата на първата подадена страница
def INDEXCATALOGUE(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        #print 'request page url:' + url
        data=response.read()
        response.close()

        #Начало на обхождането
        br = 0 #Брояч на видеата в страницата - 24 за този сайт
        match = re.compile('href=".+?online-(\d+).".+?src=(.+?) .+?<b>(.+?)</b></a>.+?</div>(.+?)\.').findall(data)
        for idmov,thumbnail,title,descr in match:
            movie = 'http://myonvideo.com/play:' + idmov
            addLink(title,movie,9,descr,thumbnail)
            br = br + 1
        if br >= 24: #тогава имаме следваща страница и конструираме нейния адрес
            getpage=re.compile('(.*)(\d+)').findall(url)
            for baseurl,page in getpage:
                newpage = int(page)+1
                url = baseurl + str(newpage)
                #print 'URL OF THE NEXT PAGE IS' + url
                thumbnail='DefaultFolder.png'
                addDir('следваща страница>>',url,1,thumbnail)

def INDEXMOVIEGENRES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        #print 'request page url:' + url
        data=response.read()
        response.close()
        #Начало на обхождането
        match = re.compile('<table.*(http.+?jpg).*\n.*\n.*\n.*\n<a href="(.+?)">.*<b>(.+?)</b></a>').findall(data)
        for thumbnail,url,title in match:
            addDir(title,url,3,thumbnail)


#Разлистване видеата на първата подадена страница
def INDEXMOVIES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        #print 'request page url:' + url
        data=response.read()
        response.close()

        #Начало на обхождането
        br = 0 #Брояч на видеата в страницата - 24 за този сайт
        match = re.compile('img src="http.+?-(\d+).jpg" alt="(.+?)"').findall(data)
        for idmov,title in match:
            movie = 'http://myonvideo.com/play:' + idmov
            thumbnail = 'http://myonvideo.com/image-' + idmov + '.jpg'
            descr = 'Липсва описание'
            addLink(title,movie,9,descr,thumbnail)
            br = br + 1
        if br == 40: #тогава имаме следваща страница и конструираме нейния адрес
            getpage=re.compile('</div><div class="pagination">\n<b>(.+?)</b><a href="(.+?)."').findall(data)
            for page,baseurl in getpage:
                newpage = int(page)+1
                url = baseurl + str(newpage)
                #print 'URL OF THE NEXT PAGE IS' + url
                thumbnail='DefaultFolder.png'
                addDir('следваща страница>>',url,6,thumbnail)

def INDEXSERIALS(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        #print 'request page url:' + url
        data=response.read()
        response.close()
        print 'tova e urlto' + url
        #Начало на обхождането
        br = 0
        match = re.compile('<table.*(http.+?jpg).*\n.*\n.*\n.*\n<a href="(.+?)">.*<b>(.+?)</b></a>').findall(data)
        for thumbnail,url,title in match:
            addDir(title,url,2,thumbnail)
            br = br + 1
        if br == 40: #тогава имаме следваща страница и конструираме нейния адрес
            getpage=re.compile('(.*)(\d+)').findall(url)
            for baseurl,page in getpage:
                newpage = int(page)+1
                newurl = sernext + 'Page/' + str(newpage)
                #print 'URL OF THE NEXT PAGE IS' + url
                thumbnail='DefaultFolder.png'
                addDir('следваща страница>>',newurl,5,thumbnail)

def INDEXSERPAGES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        #print 'request page url:' + url
        data=response.read()
        response.close()
        print 'tova e url' + url
        #Начало на обхождането
        br = 0
        match = re.compile('<table.*(http.+?jpg).*\n.*\n.*\n.*\n<a href="(.+?)">.*<b>(.+?)</b></a>').findall(data)
        for thumbnail,url,title in match:
            addDir(title,url,2,thumbnail)
            br = br + 1
        if br >= 38: #тогава имаме следваща страница и конструираме нейния адрес
            getpage=re.compile('div class="clear"></div>\n.*<div class="pagination">.*<<<.* <b>(\d+)</b> <a href="(.+?)/Page/\d+">\d+</a>').findall(data)
            for page,baseurl in getpage:
                newpage = int(page)+1
                url = baseurl + '/Page/' + str(newpage)
                #print 'URL OF THE NEXT PAGE IS' + url
                thumbnail='DefaultFolder.png'
                addDir('следваща страница>>',url,5,thumbnail)

def INDEXMOVPAGES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        #print 'request page url:' + url
        data=response.read()
        response.close()

        #Начало на обхождането
        br = 0 #Брояч на видеата в страницата - 24 за този сайт
        match = re.compile('img src="http.+?-(\d+).jpg" alt="(.+?)"').findall(data)
        for idmov,title in match:
            movie = 'http://myonvideo.com/play:' + idmov
            thumbnail = 'http://myonvideo.com/image-' + idmov + '.jpg'
            descr = 'Липсва описание'
            addLink(title,movie,9,descr,thumbnail)
            br = br + 1
        if br >= 38: #тогава имаме следваща страница и конструираме нейния адрес
            getpage=re.compile('</h2>.*\n.*<b>(.+?)</b><a href="(.+?)."').findall(data)
            for page,baseurl in getpage:
                newpage = int(page)+1
                url = baseurl + '/Page/' + str(newpage)
                #print 'URL OF THE NEXT PAGE IS' + url
                thumbnail='DefaultFolder.png'
                addDir('следваща страница>>',url,6,thumbnail)

def SHOW(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        #print 'request page url:' + url
        data=response.read()
        response.close()
        br = 0
        match = re.compile('<span class="bold">(.+?)</span>.*\n<iframe.*src="(.+?)"').findall(data)
        #matchi = re.compile('<link rel="image_src" href="(.+?)"').findall(data)
        for server,link in match:
         #for thumbnail in match:
          title = 'Сървър-' + server + name
          addLink2(name,link,10,iconimage,title)
          br = br + 1



#Зареждане на видео
def PLAY(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        url = urllib2.urlopen(req).geturl()
        print url
        li = xbmcgui.ListItem(iconImage=iconimage, thumbnailImage=iconimage, path=url)
        li.setInfo('video', { 'title': name })
        link = url
        try: stream_url = urlresolver.HostedMediaFile(link).resolve()
        except:
               deb('Link URL Was Not Resolved',link); deadNote("urlresolver.HostedMediaFile(link).resolve()","Failed to Resolve Playable URL."); return

        ##xbmc.Player().stop()
        play=xbmc.Player() ### xbmc.PLAYER_CORE_AUTO | xbmc.PLAYER_CORE_DVDPLAYER | xbmc.PLAYER_CORE_MPLAYER | xbmc.PLAYER_CORE_PAPLAYER
        try: _addon.resolve_url(url)
        except: t=''
        try: _addon.resolve_url(stream_url)
        except: t=''
        play.play(stream_url, li); xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=li)
        try: _addon.resolve_url(url)
        except: t=''
        try: _addon.resolve_url(stream_url)
        except: t=''

def SEARCH(url):
       keyb = xbmc.Keyboard('', 'Търсачка')
       keyb.doModal()
       searchText = ''
       if (keyb.isConfirmed()):
           searchText = urllib.quote_plus(keyb.getText())
           searchText=searchText.replace(' ','+')
           params = {'t':searchText, 'x':'26', 'y':'18'}
           req = urllib2.Request(url, urllib.urlencode(params))
           req.add_header('User-Agent', UA)
           response = urllib2.urlopen(req)
           #print 'request page url:' + url
           data=response.read()
           response.close()
           br = 0 #Брояч на видеата в страницата - 24 за този сайт
           match = re.compile('img src="http.+?-(\d+).jpg" alt="(.+?)"').findall(data)
           for idmov,title in match:
            movie = 'http://myonvideo.com/play:' + idmov
            thumbnail = 'http://myonvideo.com/image-' + idmov + '.jpg'
            descr = 'Липсва описание'
            addLink(title,movie,9,descr,thumbnail)
            br = br + 1
           if br == 40: #тогава имаме следваща страница и конструираме нейния адрес
            getpage=re.compile('</div><div class="pagination">\n<b>(.+?)</b><a href="(.+?)."').findall(data)
            for page,baseurl in getpage:
                newpage = int(page)+1
                url = baseurl + str(newpage)
                #print 'URL OF THE NEXT PAGE IS' + url
                thumbnail='DefaultFolder.png'
                addDir('следваща страница>>',url,6,thumbnail)



#Модул за добавяне на отделно заглавие и неговите атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addLink(name,url,mode,plot,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": plot } )
        liz.setProperty("IsPlayable" , "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink2(name,url,mode,iconimage,title):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(title, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty("IsPlayable" , "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok


#Модул за добавяне на отделна директория и нейните атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

#НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param







params=get_params()
url=None
name=None
iconimage=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        name=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass


#Списък на отделните подпрограми/модули в тази приставка - трябва напълно да отговаря на кода отгоре
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
    
elif mode==1:
        print ""+url
        INDEXCATALOGUE(url)

elif mode==2:
        print ""+url
        INDEXMOVIEGENRES(url)

elif mode==3:
        print ""+url
        INDEXMOVIES(url)

elif mode==4:
        print ""+url
        INDEXSERIALS(url)

elif mode==5:
        print ""+url
        INDEXSERPAGES(url)

elif mode==6:
        print ""+url
        INDEXMOVPAGES(url)

elif mode==9:
        print ""+url
        SHOW(url)

elif mode==10:
        print ""+url
        PLAY(url)

elif mode==11:
        print ""+url
        SEARCH(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
