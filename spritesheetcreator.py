from windows import *
import tkFileDialog
import Image
import ImageTk

title = 'Sprite Sheet Creator'

class SpriteSheetCreatorWindow(DefaultDialog):
    def __init__(self, *args, **kws):
        self.__image = kws.pop('image')
        DefaultDialog.__init__(self, *args, **kws)

    def body(self, master):
        self.canvas = ExtendedCanvas(master, bd=0, highlightthickness=0, bg='black')
        self.canvas.pack(expand='yes', fill='both')
        self.canvas.bind('<1>', self.__switch_color, '+')
        self.__photo = ImageTk.PhotoImage(self.__image)
        self.__imagedraw = ImageDraw(self.canvas, 0, 0, self.__photo, anchor='nw')
        self.canvas.width = self.__photo.width()
        self.canvas.height = self.__photo.height()

    def __switch_color(self, event):
        if self.canvas['bg'] == 'black':
            self.canvas['bg'] = 'white'
        else:
            self.canvas['bg'] = 'black'

    def apply(self):
        fn = tkFileDialog.asksaveasfilename()
        if fn:
        	self.__image.save(fn, 'PNG')

def init(ide):
    pass

def execute(ide):
    # SpriteSheetCreatorWindow(ide)
    images = tkFileDialog.askopenfilenames(parent=ide,
        filetypes=[('Image Files', '.' + ' .'.join(ide.__class__.SUPPORTED_IMAGE_TYPES))])
    if images:
        images = [Image.open(i) for i in images]
        width, height = images[0].size
        final_image = Image.new(
                    "RGBA",
                    (
                        width*len(images),
                        height
                    )
        )
        for i in range(len(images)):
            final_image.paste(images[i],
                (
                    i*width,
                    0
                )
            )
        SpriteSheetCreatorWindow(ide, image=final_image)