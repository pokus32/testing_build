import asyncio
from loguru import logger
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import StringProperty, DictProperty, ObjectProperty, BooleanProperty, ListProperty
from pathlib import Path
from datetime import datetime
import time
import base64
from PIL import Image as PIL_Image
from io import BytesIO

from kivy.uix.image import Image
from functools import partial

row1_color = (0.62,1,0.75, 1)
row2_color = (0.7, 0.7, 0.7, 1)
norm_color = [1,1,1,1]
error_color = [0.99,0.82,1,1]


class SinglePPAP(BoxLayout):
    """ """
    ppap_id       = StringProperty()
    ppap_id_name  = StringProperty()
    aplay_button  = ObjectProperty()


class PPAPsList(GridLayout):
    """ """
    ppaps_layout    = ObjectProperty()
    cancel_button   = ObjectProperty()


def show_image(file_name, dt=None, title=None):
    logger.info('')
    if not Path(file_name).is_file():
        return 1
    content = BoxLayout(orientation='vertical')
    content.add_widget(Image(source=file_name))
    close_button = Button(text='Kapat', size_hint=(None,None), size=(55,30))
    button_layout = StackLayout(size_hint_y=None, orientation='rl-tb')
    button_layout.bind(minimum_height=button_layout.setter('height'))
    button_layout.add_widget(close_button)
    content.add_widget(button_layout)
    if title is None: title = '' 
    pop_wind = Popup(title = title,
                      content = content, 
                      size_hint =(None, None), size =(480, 500),title_color = [1,0,0,1],title_size = 20)
    close_button.bind(on_release=pop_wind.dismiss)
    pop_wind.open()

class ImageButton(Image):
    logger.info('')
    removable = BooleanProperty()
    removable = False
    def on_touch_down(self, touch):
        if touch.is_double_tap and self.collide_point(*touch.pos) and self.removable:
            Clock.unschedule(show_image)
            file = Path(self.source)
            try:
                file.unlink()
            except OSError as e:
                print("Error: %s : %s" % (file, e.strerror))
            if len(self.parent.children)<2:
                rt_wdgt = ''
                for wdgt in self.walk_reverse():
                    if wdgt.ids.get('media_row'):
                        wdgt.ids.get('media_row').height = 30
                        break
            self.parent.remove_widget(self)
        elif touch.is_touch and self.collide_point(*touch.pos):
            Clock.unschedule(show_image)
            Clock.schedule_once(partial(show_image, self.source), 1)


class MediaScreen(BoxLayout):
    """ """
    image1 = ObjectProperty()
    ok_button = ObjectProperty()
    shot_button = ObjectProperty()
    esc_but = ObjectProperty()

    def __init__(self,parent,**kwargs):
        logger.info('')
        super(MediaScreen, self).__init__(**kwargs)
        self.my_parent = parent
        
        return

        self.capture = cv2.VideoCapture(0)
        self.capture.set(3, 640)
        self.capture.set(4, 480)
        # self.my_parent.media_pop.bind(on_dismiss=self.on_exit)
        Clock.schedule_interval(self.update_image, 1.0/20)
        self.ok_button.bind(on_release = self.save_media)
        self.esc_but.bind(on_release = self.esc_media)

    def update_image(self,arg):
        """

        :param arg: 

        """
        ret, self.frame = self.capture.read()
        if ret:
            # try:
            buf1 = cv2.flip(self.frame, 0)
            buf = buf1.tostring()
            texture1 = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.image1.texture = texture1

    def esc_media(self,arg=None):
        """

        :param arg:  (Default value = None)

        """
        Clock.unschedule(self.update_image)
        self.capture.release()
        arg.disabled = True
        self.my_parent.media_pop.dismiss()

    def save_media(self,arg=None):
        """

        :param arg:  (Default value = None)

        """
        arg.disabled = True ## otkluchaju knopku
        Clock.unschedule(self.update_image)
        self.capture.release()
        self.my_parent.media_pop.dismiss()
        file_name = str(self.my_parent.new_id) + '_' + str(int(time.time())) + '.jpg'
        cv2.imwrite(file_name, self.frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        im_bttn = ImageButton(source=file_name,size_hint=(None,None),size=(120,80))
        im_bttn.removable = True
        self.my_parent.ids.media_row.height = 90
        self.my_parent.ids.thumbnails.add_widget(im_bttn)
        

class OneRequestRow(GridLayout):

    def __init__(self, **kwargs):
        logger.info('')
        super(OneRequestRow, self).__init__(**kwargs)


class ReqLayout(BoxLayout):
    """ """
    i_unit = ObjectProperty()
    i_quantity = ObjectProperty()

    new_id = StringProperty()
    item_type = StringProperty()
    item_type = 'Sarf'
    department = StringProperty()
    consumer_department = StringProperty()
    measure_methods = DictProperty()
    cur_date = datetime.now().strftime('%d.%m.%y')
    
    def __init__(self,**kwargs):
        logger.info('')
        super(ReqLayout, self).__init__(**kwargs)
        self.controller = App.get_running_app().request_controller
        self.get_id()
        Clock.schedule_once(self.make_table, 1)

    def set_department(self, inst):
        logger.info('')
        if inst.state == 'down':## neobhodima proverka sostoyanoya
            self.department = inst.text
        else:
            self.department = ''

    def set_cons_department(self, inst):
        logger.info('')
        if inst.state == 'down':## neobhodima proverka sostoyanoya
            self.consumer_department = inst.text
        else:
            self.consumer_department = ''

    def set_measure_methods(self, inst):
        logger.info('')
        if inst.state == 'down':## neobhodima proverka sostoyanoya
            self.measure_methods.update({inst.mes_id:inst.text})
        else:
            self.measure_methods.pop(inst.mes_id)

    def on_new_id(self, *args):
        logger.info('')
        if 'eo_doc_n' in self.ids:
            self.ids.eo_doc_n.text = str(self.new_id)
            self.cur_date = datetime.now().strftime('%d.%m.%y')
            # self.ids.current_date.text = ' ' + self.cur_date

    def get_id(self):
        logger.info('')
        coro = asyncio.ensure_future(self.__get_id())
        asyncio.gather(coro, return_exceptions=False)

    async def __get_id(self):
        self.new_id = await self.controller.get_last_out_n()

    def save_info(self, arg=None):
        logger.info('')
        coro = asyncio.ensure_future(self.__save_info())
        asyncio.gather(coro, return_exceptions=False)

    async def __save_info(self, arg=None):
        logger.info('')
        if self.ids.i_staff.text != '' and\
                self.ids.i_request.text != '' and\
                self.ids.i_quantity.text != '' and\
                self.ids.i_porpose.text != '' and\
                self.department != '' and\
                len(self.measure_methods) != 0 and\
                self.consumer_department != '':
            media = {}
            file_mask = str(self.new_id) + '_*.jpg'
            for f in Path.cwd().glob(file_mask):
                with open(f, "rb") as img_file:
                    img_string = base64.b64encode(img_file.read())
                    media.update({f.name.split('.')[0]: img_string})
            quantity = float(self.i_quantity.text)
            unit = self.i_unit.text.strip()
            data_dict = {
                'date':self.cur_date,
                'doc_n':self.new_id,
                'department':self.department,
                'staff':self.ids.i_staff.text.strip(),
                'request':self.ids.i_request.text.strip(),
                'purpose':self.ids.i_porpose.text.strip(),
                "quantity" : quantity,
                "unit" : unit,
                'marka':self.ids.i_marka.text.strip(),
                'supplier':self.ids.i_supplier.text.strip(),
                'consumer_department':self.consumer_department,
                'measure_methods':dict(self.measure_methods),
                'item_type': self.item_type,
                'note':self.ids.i_note.text.strip(),
                'media': media,
                'satisfied':''
            }
            if hasattr(self.ids.i_porpose, 'ppap_id'):
                data_dict.update({'ppap_id': self.ids.i_porpose.ppap_id})
            await self.controller.insert_request_data(data_dict)
            self.ids.i_staff.background_color = norm_color
            self.ids.i_request.background_color = norm_color
            self.ids.i_quantity.background_color = norm_color
            self.ids.i_porpose.background_color = norm_color
            ##udalyau tolko i_quantity.text i_unit.text dannie chtob ne zapisalos povtorno
            self.ids.i_quantity.text = ''
            self.ids.i_unit.text = ''
            self.__clear_thumbnails()
            await self.__get_id() ## noviy id tolko posle sohraneniya dokumenta
        else:
            self.ids.i_staff.background_color = \
            self.ids.i_request.background_color = \
            self.ids.i_quantity.background_color = \
            self.ids.i_porpose.background_color = error_color
        await self.__make_table()

    def make_table(self, arg=None):
        logger.info('')
        coro = asyncio.ensure_future(self.__make_table())
        asyncio.gather(coro, return_exceptions=False)

    async def __make_table(self):
        logger.trace('')
        self.inside_layout = GridLayout(cols=1, padding = 1, spacing=1, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        self.inside_layout.bind(minimum_height=self.inside_layout.setter('height'),minimum_width=self.inside_layout.setter('width'))
        self.ids.query_scroll_layout.clear_widgets()
        self.ids.query_scroll_layout.add_widget(self.inside_layout)
        jj = 1
        return
        for ii in await self.controller.get_staff_requests():
            tmp_obj = OneRequestRow()
            if jj == 1:
                tmp_obj.clr = row1_color
                jj = 2
            else:
                tmp_obj.clr = row2_color
                jj = 1

            ##cod nije soderjot preobrozovanie str(...)
            ##t.k. mogut popastsa chisla v tekstovih polyah
            tmp_obj.doc_n =         tmp_obj.doc_n.replace("_repl_doc_n", str(int(ii.get('doc_n'))))
            tmp_obj.department =    tmp_obj.department.replace("_repl_department", str(ii.get('department')))
            tmp_obj.staff =         tmp_obj.staff.replace("_repl_staff", str(ii.get('staff')))
            tmp_obj.doc_date =      tmp_obj.doc_date.replace("_repl_doc_date", str(ii.get('date')))
            tmp_obj.request =       tmp_obj.request.replace("_repl_request", str(ii.get('request')))
            tmp_obj.quantity =      tmp_obj.quantity.replace("_repl_quantity", str(ii.get('quantity')))
            tmp_obj.marka =         tmp_obj.marka.replace("_repl_marka", str(ii.get('marka')))
            tmp_obj.purpose =       tmp_obj.purpose.replace("_repl_purpose", str(ii.get('purpose')))
            tmp_obj.supplier =      tmp_obj.supplier.replace("_repl_supplier", str(ii.get('supplier')))
            control_methods = ' '.join(map(str, \
                    list(ii.get('measure_methods').values())))
            tmp_obj.contrl_methods = tmp_obj.contrl_methods.replace("_repl_contrl_methods", control_methods)
            tmp_obj.cons_dep =      tmp_obj.cons_dep.replace("_repl_cons_dep", \
                                      str(ii.get('consumer_department')))
            tmp_obj.note =          tmp_obj.note.replace("_repl_note", str(ii.get('note')))

            media = ii.get('media',{})
            if media:
                for img_key in media:
                    im = PIL_Image.open(BytesIO(base64.b64decode(media[img_key])))
                    file_name = img_key + '.jpg'
                    im.save(file_name)
                    tmp_obj.thumbnails.height = 99
                    tmp_obj.thumbnails.add_widget(ImageButton(source=file_name,size_hint=(None,None),size=(121,81)))
            else:
                tmp_obj.remove_widget(tmp_obj.thumbnails_layout)
            self.inside_layout.add_widget(tmp_obj)

    def __clear_thumbnails(self):
        logger.info('')
        self.ids.thumbnails.clear_widgets()
        self.ids.media_row.height = 30

    def clear_form(self):
        logger.info('')
        self.ids.i_staff.text = ''
        self.ids.i_request.text = ''
        self.ids.i_porpose.text = ''
        self.ids.i_quantity.text = ''
        self.ids.i_unit.text = ''
        self.ids.i_marka.text = ''
        self.ids.i_note.text = ''
        self.ids.i_supplier.text = ''
        self.ids.row_mat_button.state = 'normal'
        for ii in self.ids.departmant_group.children:
            ii.state = 'normal'
        for ii in self.ids.contr_method_group.children:
            ii.state = 'normal'
        for ii in self.ids.cons_department_group.children:
            ii.state = 'normal'
        ## TODO make all image operation in a kivy.cache 
        # for f in Path.cwd().glob('*_*.jpg'):
        #     try:
        #         f.unlink()
        #     except OSError as e:
        #         print("Error: %s : %s" % (f, e.strerror))

        self.__clear_thumbnails()
        self.make_table()

    def set_item_type(self, inst):
        logger.info('')
        task_coro = asyncio.ensure_future(self.__set_item_type(inst))
        asyncio.gather(task_coro, return_exceptions=False)

    async def __set_item_type(self, inst):
        logger.info('')
        if inst.state == 'down':
            self.item_type = inst.text
            await self.controller.show_ppaps_list(SinglePPAP, PPAPsList, self.__aplay_ppap_data)
            self.ids.i_porpose.readonly = True
            self.ids.i_request.readonly = True
            self.ids.i_marka.readonly = True
        else:
            self.item_type = 'Sarf'
            self.ids.i_porpose.readonly = False
            self.ids.i_request.readonly = False
            self.ids.i_marka.readonly = False
            self.ids.i_porpose.text = ''
            self.ids.i_request.text = ''
            self.ids.i_marka.text = ''
    
    def __aplay_ppap_data(self, ppap_id, ppap_name, material_name, material_dim):
        logger.info('')
        self.ids.i_porpose.text = ppap_id + '/' + ppap_name
        self.ids.i_porpose.ppap_id = ppap_id
        self.ids.i_request.text = f'{material_name} / {material_dim}'
        self.ids.i_marka.text = material_name

    def  insert_media(self):
        logger.info('')
        if len(self.ids.thumbnails.children) > 3:

            return 1 #!!!!!!!!!!!!!!!!!!!!!!

        m_screen = MediaScreen(self)
        self.media_pop = Popup(title = '---',
                      content = m_screen, 
                      size_hint =(None, None), 
                      size =("480dp", "500dp"),
                      title_color = [1,0,0,1],
                      title_size = "20dp",
                      auto_dismiss=True)
        self.media_pop.open()
