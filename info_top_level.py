import customtkinter
import webbrowser







class App(customtkinter.CTkToplevel):

    APP_NAME = "VVO Info"
    WIDTH = 300   
    HEIGHT = 300
    
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
   
       

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        
        self.info_btn = customtkinter.CTkButton(master=self, corner_radius=1, height=30, width=250, border_spacing=5, text="Icons by Icons8",
                                                fg_color=("gray30"), text_color=("gray90"), hover_color=("red"), font=customtkinter.CTkFont(size=12, weight="bold"),
                                                    anchor="center", command=self.link_icon8)
        self.info_btn.pack(side='top', padx=10, anchor="n")
       
    def link_icon8(self):
        url = "https://icons8.ru/"
        webbrowser.open(url)

    def on_closing(self, event=0):
        self.destroy()

