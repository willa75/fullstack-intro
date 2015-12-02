from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from restaurant import *

class webserverHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "Hello!"
				output += """<form method='POST' enctype='multipart/form-data'
					action='/hello'><h2>What would you like to say?</h2><input 
					name='message' type='text'><input type='submit' value='submit'>
					</form>"""
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += """&#161Hola!<a href='/hello'>Back to 
				Hello</a>"""
				output += """<form method='POST' enctype='multipart/form-data'
					action='/hello'><h2>What would you like to say?</h2><input 
					name='message' type='text'><input type='submit' value='submit'>
					</form>"""
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>List of Restuarants</h2><br><br>"
				restaurants = getRestaurants()
				for restaurant in restaurants:
					output += "<h2> %s </h2><br>" % restaurant.name
					output += """<a href='/restaurant/%s/edit'>Edit</a>
					<br>""" % restaurant.id
					output +="""<a href='/restaurant/%s/delete'>Delete</a><br>
					<br>"""% restaurant.id
				
				
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Create a New Restaurant</h1>"
				output += """<form method='POST' enctype='multipart/form-data'
				action='/restaurants/new'><h2>Make a New Restaurant</h2><input
				type='text' name='restaurant'><input type='submit' 
				value='submit'>"""
				output += "</br><a href='/restaurants'>Cancel</a>"
				
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
			if self.path.endswith("/edit"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				restaurantID = self.path.split("/")[2]
				name = getRestaurantName(restaurantID)

				output = ""
				output += "<html><body>"
				output += "<h1>Create a New Restaurant</h1>"
				output += """<form method='POST' enctype='multipart/form-data'
				action='/restaurant/%s/edit'><h2>Make a New Restaurant</h2><input
				type='text' value = '%s'name='restaurant'><input type='submit' 
				value='submit'>""" % (restaurantID , name)
				output += "</br><a href='/restaurants'>Cancel</a>"
				
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
			if self.path.endswith("/delete"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				restaurantID = self.path.split("/")[2]
				name = getRestaurantName(restaurantID)

				output = ""
				output += "<html><body>"
				output += "<h1>Are You Sure You Want to Delete %s</h1>"% name
				output += """<form method='POST' enctype='multipart/form-data'
				action='/restaurant/%s/delete'><input type='submit' 
				value='Confirm'>""" % restaurantID
				output += "<a href='/restaurants'>Cancel</a>"
				
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return
		except IOError:
			self.sned_error(404, "File Not Found %s" % self.path)

	def do_POST(self):
		if self.path.endswith("/restaurants/new"):
			try:
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('restaurant')

				addRestaurant(messagecontent[0])

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', 'restaurants')
				self.end_headers()

			except:
				pass
		if self.path.endswith("/edit"):
			try:
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('restaurant')
				
				restaurantID = self.path.split("/")[2]
				updateRestaurantName(messagecontent[0], restaurantID)

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', 'restaurants')
				self.end_headers()

			except:
				pass
		if self.path.endswith("/delete"):
			try:
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('restaurant')
				
				restaurantID = self.path.split("/")[2]
				deleteRestaurant( restaurantID )

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', 'restaurants')
				self.end_headers()

			except:
				pass

		else:
			try:
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')

				output = ""
				output += "<html><body>"
				output += "<h2> Okay, how about this: </h2>"
				output += "<h1> %s </h1>" % messagecontent[0]

				output += """<form method='POST' enctype='multipart/form-data'
					action='/hello'><h2>What would you like to say?</h2><input 
					name='message' type='text'><input type='submit' value='submit'>
					</form>"""
				output += "</body></html>"
				self.rfile.write(output)
				print output

			except:
				pass



def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()