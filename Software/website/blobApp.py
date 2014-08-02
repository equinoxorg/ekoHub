from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import main
import webapp2

# create upload URL in the blobstore
upload_url = blobstore.create_upload_url('/upload')


class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('<html><body>')
		self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
		self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit"
    name="submit" value="Submit"> </form></body></html>""")

# saves uploaded content as a blob
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
    blob_info = upload_files[0]
    self.redirect('/serve/%s' % blob_info.key())


 # when this application is running the other isn't 
app = webapp2.WSGIApplication([( '/uploadBlob' , MainPage ),
								('/upload', UploadHandler)],
                                debug = True)
