import tkinter as tk
import psutil


class Monitor(tk.Frame):
    def __init__(self, master=None, max_row=6, **kw):
        super().__init__(master, **kw)
        # 布局
        self.grid(sticky='wesn')
        # 关闭按钮
        close_button = tk.Button(self, text="", command=self.quit, bg="#FF8888", fg="#FF8888", width=1, height=0, bd=0, highlightthickness=0, relief='flat')
        close_button.place(x=self.winfo_x(), y=self.winfo_y())
        # 背景
        self.configure(bg="#AAEEFF")

        self.last_io_counters = psutil.net_io_counters()
        self.widgets = []
        self.create_widgets(max_row)
        self.after(500, self.update_values)

    def create_widgets(self, max_row):
        fields = ['CPU使用率', 'CPU频率', '内存使用率', '硬盘使用率', '上传速度', '下载速度']
        for i in range(min(len(fields), max_row)):
            label = tk.Label(self, text=fields[i], font=('Times', 10), bg='#AAEEFF')
            label.grid(row=i, column=0, padx=20, pady=10, sticky='w')
            widget = tk.Label(self, text='', font=('Arial', 10), width=10, bg='#AAEEFF')
            widget.grid(row=i, column=1, padx=20, pady=10, sticky='e')
            self.widgets.append(widget)

    def update_values(self):
        # CPU使用率
        cpu_percent = psutil.cpu_percent()
        # CPU频率
        cpu_current = psutil.cpu_freq().current
        # Memory使用率
        memory_percent = psutil.virtual_memory().percent
        # Disk使用率
        disk_percent = psutil.disk_usage('/').percent
        # 上传速度、下载速度
        io_counters = psutil.net_io_counters()
        up_speed = (io_counters.bytes_sent - self.last_io_counters.bytes_sent) / 1024 / 1024
        down_speed = (io_counters.bytes_recv - self.last_io_counters.bytes_recv) / 1024 / 1024
        self.last_io_counters = io_counters

        values = [f'{cpu_percent:.1f}%',
                  f'{cpu_current:.1f}',
                  f'{memory_percent:.1f}%',
                  f'{disk_percent:.1f}%',
                  f'{up_speed:.3f} MB/s',
                  f'{down_speed:.3f} MB/s']

        for i, value in enumerate(values):
            self.widgets[i]['text'] = value

        self.after(500, self.update_values)


if __name__ == '__main__':
    root = tk.Tk()
    root.wm_attributes('-topmost', True)   # 处于最顶部
    root.attributes("-alpha", 0.8)  # 透明度
    root.overrideredirect(True) # 没有工具栏
    root.resizable(False, False)
    root.title('监控')
    app = Monitor(root, max_row=6)
    app.mainloop()