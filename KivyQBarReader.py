'''Kivymd screen with embeded camera for reading barcode and qrcode:
	
	Using QBarReader:
		1.Create an instance of QBarReader
			reader = QBarReader()
		2. Override the back method  with your own to navigate you to your desired screen when back button is pressed
			reader.back = #Your back method
		3. Add to root widget
			root.add_widget(reader)
			
	OR IN KV LANGUAGE
	root:
		QBarReader:
			back:#Your back method
			
Note: Save button saves a pickled version of the scanned data to qrbardata.dat file which can be read. Also the scanned data is present as result property of QBarReader(You can access with instance.results)
'''

import cv2
from kivy.lang import Builder
from kivymd.toast import toast
from kivymd.app import MDApp
from kivy.uix.camera import Camera
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty


def decode(img):
	image = cv2.imread(img)
	if qrcode_reader.detect(image)[0]:
		decodedText, points, _ = qrcode_reader.	detectAndDecode(image)
	elif barcode_reader.detect(image)[0]:
		ok,decodedText,*_ = barcode_reader.detectAndDecode(image)
	else:
		decodedText = 'No data found'
	return decodedText
	
qrcode_reader = cv2.QRCodeDetector()
barcode_reader = cv2.barcode_BarcodeDetector()

Builder.load_string('''
<QBarReader>:
	title:'Scanning ...'
	camera:camera
	Scanner:
		id:camera
		size_hint:None,None
		size:1500,1500
	MDGridLayout:
		rows:1
		padding:20,20,20,20
		pos_hint:{'center_x':.5,'center_y':0.05}
		size_hint:.5,.17
		#width:150
		spacing:5
		MDIconButton:
			icon:'chevron-left'
			user_font_size:'80sp'
			theme_text_color:'Custom'
			text_color:1,1,1,1
			on_press:root.back('back')
		MDIconButton:
			icon:'record'
			user_font_size:'80sp'
			theme_text_color:'Custom'
			text_color:1,0,0,1
			on_press:root.scan(camera)
		MDIconButton:		
			icon:'content-save-outline'
			user_font_size:'80sp'
			theme_text_color:'Custom'
			text_color:1,1,1,1
			on_press:root.save()
	
<Scanner>:
	size_hint:None,None
	keep_ratio:True
	allow_stretch:True
	pos_hint:{'center_x':.5,'center_y':.5}
	canvas.before:
        PushMatrix
        Rotate:
            angle: -90
            origin: self.center
    canvas.after:
        PopMatrix''')
    
###Reader screen
class QBarReader(MDScreen):
	results = b''
	camera = ObjectProperty()
	
	def scan(self,scanner):
		self.results = b''
		scanner.export_to_png('image.png')
		self.results = decode('image.png')
		toast(str(self.results))		
	
	def save(self):
		import pickle
		with open('qrbardata.dat', 'wb') as file:
			pickle.dump(self.results, file)
		toast('Data saved ...')
		
	def back(self,screen_name):
		self.parent.current = screen_name

###Main camera widget		
class Scanner(Camera):
	pass		

####Test####
kv = '''
ScreenManager:
	QBarReader:
		back:lambda *args:None
	Screen:
		name:'back'
'''
class test(MDApp):
	def build(self):	
		return Builder.load_string(kv)
				
test().run()
