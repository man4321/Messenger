from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
import webapp2
import json
from model import*


#backend


class Uplode(webapp2.RequestHandler):
    def post(self):
        request=json.loads(self.request.body)
        feeds=Feeds()
        print request.get('user_key')
        #feeds.user_key=ndb.Key(urlsafe=request.get('user_key'))

        feeds.post=request.get('post')
        feeds.put()
        def json_convert(self):
                d=[];
                for i in feeds:
                    d.append({
                        #'user_key':d.user_key,
                        'post':d.post
                        })
                self.response.out(json.dumps(d))
    def get(self):
        pass

class MainPage(webapp2.RequestHandler):
    feeds_per_page=10
    def get(self):
        #query=Feeds.query.fetch()   
        #print query
        cursor = Cursor(urlsafe=self.request.get('cursor'))
        feed, next_cursor, more = Feeds.query().fetch_page(
            self.feeds_per_page, start_cursor=cursor)

        d=[];
        for i in feed:
            d.append({
                'post':i.post,
                'post_time':str(i.post_time)

                })
        print d
        self.response.out.write({"more": more,"data":json.dumps(d), "curs":next_cursor.urlsafe()})
                
    def post(self):
        pass


class SignUp(webapp2.RequestHandler):
    def post(self):
        #print self
        request=json.loads(self.request.body)
        #print request
        user=User()

        user.firstname=request.get('firstname')
        user.lastname=request.get('lastname')
        user.username=request.get('username')
        user.password=request.get('password')
        user.email=request.get('email')
        
        query = User.query(User.email==user.email).get()
        if query is not None:
            self.response.out.write({"Error": "email is already exist!"})
        else:
            self.response.out.write("Done")
            user.put()
    def get(self):
        pass

class Login(webapp2.RequestHandler):
    def post(self):
        #print self
        request=json.loads(self.request.body)
        #print request
        user=User()
        user.email=request.get('email')
        user.password=request.get('password')
        data=User.query(User.email==user.email , User.password==user.password).get()
        if (data):
            self.response.out.write( "successfully login")
            def json_convert(self):
                d=[];
                for i in data:
                    d.append({
                        'firstname': d.firstname,
                        'lastname': d.lastname,
                        'username': d.username,
                        'password': d.password,
                        'email': d.email
                        })
                    x=json.dumps(d)
                    self.response.out(x)

        else:
            self.response.out.write({"Error": "Incorrect email or password"})

    def get(self):
        pass
class Messenger_R(webapp2.RequestHandler):
    messeges_per_page=10
    def get(self):
        #query=Feeds.query.fetch()   
        #print query
        cursor = Cursor(urlsafe=self.request.get('cursor'))
        messege, next_cursor, more = Sender.query().fetch_page(
            self.messeges_per_page, start_cursor=cursor)

        d=[];
        for i in messege:
            d.append({
                'content':i.content,
                'send_time':str(i.send_time)

                })
        print d
        self.response.out.write({"more": more,"data":json.dumps(d), "curs":next_cursor.urlsafe()})
                
    def post(self):
        pass

class Messenger(webapp2.RequestHandler):
    def post(self):
        request=json.loads(self.request.body)
        send=Sender()
        send.sender_key=ndb.Key(urlsafe=request.get('sender_key'))
        send.reciver_key=ndb.Key(urlsafe=request.get('reciver_key'))
        send.content=request.get('content')
        send.put()

        
       
    def get(self):
        pass
        
app=webapp2.WSGIApplication([
    ('/',Uplode),
    ('/main',MainPage),
    ('/sign',SignUp),
    ('/msg',Messenger),
    ('/login',Login),
    ('/reciver',Messenger_R)
    ],debug=True)


