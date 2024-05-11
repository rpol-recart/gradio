import gradio as gr
from gradio_calendar import Calendar
import datetime
import json


class AppState():
    def __init__(self):
        self.state_dict={}
        self.current_date=self.set_start_date()
        self.selected_megurement_time=None
        self.megurement_time_values=[]
        self.setup_current_value=None
        self.setup_slider_value=2.2
        self.chat_history=[]
        self.selected_graphs=[]
        self.current_pot="2602"
        self.data=None
        self.app_init_states()
        pass
    def app_init_states(self):
        self.state_dict=self.load_states()
        self.init_new_window()
        #self.data=self.load_data()
        pass
    def init_new_window(self):
        strdate=self.date_to_str(self.current_date)
        if strdate not in self.state_dict.keys():
            self.state_dict[strdate]={}
        if self.current_pot not in self.state_dict[strdate].keys():    
            self.state_dict[strdate][self.current_pot]={}
        if self.selected_megurement_time not in self.state_dict[strdate][self.current_pot].keys():
            self.state_dict[strdate][self.current_pot][self.selected_megurement_time]={'chat':[]}
        
        self.chat_history=self.state_dict[strdate][self.current_pot][self.selected_megurement_time]['chat']    

    def set_start_date(self):
        return datetime.datetime.now().date()
    def date_to_str(self,dt):
        return dt.strftime('%d-%m-%Y')
    def update_states(self):
        strdate=self.date_to_str(self.current_date)
        self.state_dict[strdate][self.current_pot][self.selected_megurement_time]['chat']=self.chat_history

        pass
    def get_chat_history(self):
        strdate=self.date_to_str(self.current_date)
        if strdate in self.state_dict.keys():
            self.state_dict[strdate][self.current_pot][self.selected_megurement_time]
    def load_states(self):
        with open('app_states.json','r') as f:
            self.state_dict=json.load(f)
        return self.state_dict
    def save_states(self):
        with open('app_states.json','w') as f:
            json.dump(self.state_dict,f)
        pass
    def change_calendar(self,cal):
        self.current_date=cal
        self.init_new_window()
        ddupdate=['one','two','three']
        chat_history=self.chat_history
        return  gr.Dropdown(choices=ddupdate,multiselect=True, interactive=True),chat_history
    
    def new_message(self,chat_history):
        self.chat_history=chat_history
        self.update_states()
        self.save_states()
    def change_setup(self,setup_value):
        pass
    def change_pot(self,value):
        self.current_pot=value
        self.init_new_window()
        chat_history=self.chat_history
        self.megurement_time_values=self.load_meagurements_times(self.current_date,self.current_pot)
        return gr.Dropdown(choices=self.megurement_time_values,multiselect=False, interactive=True),chat_history
    def change_mg(self,value):
        self.selected_megurement_time=value
        self.init_new_window()
        chat_history=self.chat_history
        return chat_history

    def load_meagurements_times(self, current_date,current_pot):
        return ['test1','test2','test3']
    
astate=AppState()


def updatedd(cal):
    ddupdate=['one','two','three']
    return  gr.Dropdown(choices=ddupdate,multiselect=True, interactive=True)

def respond(message, chat_history):
        print(chat_history)
        print(rad1.value)
        chat_history.append((message,None))
        astate.new_message(chat_history)
        gr.Warning('message here')
        return "", chat_history

def prev(dt):
    return dt-datetime.timedelta(days=1)
def next(dt):
    return dt+datetime.timedelta(days=1)

with gr.Blocks() as demo:
    with gr.Row():
        
        cal1 = Calendar(type="datetime", label="Выбрать дату", info="Click the calendar icon to bring up the calendar.")
        with gr.Column():
            btn5=gr.Button('Предыдущий')
            btn6=gr.Button('Следующий')
        rad1=gr.Radio(["2602", "2605"], value=astate.current_pot, label="Ванна", info="Для какой ванны производятся измерения")
        drop3 = gr.Dropdown(["a", "b", "c"],value="a",interactive=True, label="Замеры в течении дня")
    with gr.Row():
        with gr.Column(scale=2, min_width=300):
            ddown1 = gr.Dropdown([None],multiselect=True,label="Графики")
            rad2=gr.Radio(["Увеличить", "Уменьшить", "Не менять"], label="Ванна", info="Подача глинозема")
            slider2=gr.Slider(-20, 20, value=4,step=0.1, interactive=True, label="Уставка , текущее значение 2", info="Выбрать значения от -20 до 20")
            inbtw = gr.Button("Сохранить",variant='primary')
            chatbot = gr.Chatbot()
            text5 = gr.Textbox(label="Сообщение")
            with gr.Row():
                btn1=gr.Button('Отправить',variant='primary')
                btn2=gr.Button('Редактировать')
        with gr.Column(scale=4, min_width=600):
            with gr.Tab("График"):
                output = gr.Plot(label='main')                         
                btn = gr.Button("Go")
                
            with gr.Tab("Данные"):
                btn7 = gr.Button("Go")
            with gr.Tab("Сравнение"):
                drdown2=gr.Dropdown(["a", "b", "c"],value="a",interactive=True, label="Замер для сравнения")
                drdown3 = gr.Dropdown([2,3,4,5],multiselect=True,label="Графики текущего измерения")
                drdown4 = gr.Dropdown([2,3,4,5],multiselect=True,label="Графики сравнительного измерения")
                btn8 = gr.Button("Вывести")
                comparition_plot = gr.Plot(label='main') 
                
            with gr.Tab("Детально"):
                btn9 = gr.Button("Go")    

        cal1.change(astate.change_calendar,inputs=cal1,outputs=[ddown1,chatbot])
        btn1.click(respond,inputs=[text5,chatbot],outputs=[text5,chatbot])
        btn5.click(prev,inputs=cal1,outputs=cal1)
        btn6.click(next,inputs=cal1,outputs=cal1)
        rad1.change(astate.change_pot,inputs=rad1,outputs=[drop3,chatbot])
        drop3.change(astate.change_mg,inputs=drop3,outputs=chatbot)

demo.launch(auth=('a','a'))
