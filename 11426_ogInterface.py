def build_ui(self):
    setup_gpio()

    try:
        with SMBus(1) as bus:
            bus.write_byte_data(MCP4441_I2C_ADDRESS, MCP4441_COMMAND_BYTE, 0xFF)  #蓝光的强度在这里调整！！！！
    except Exception as e:
        print(f"[Warning] MCP4441 I2C init failed: {e}")

    self.theme_cls.theme_style = "Light"
    self.theme_cls.primary_palette = "Green"

    screen = MDScreen(md_bg_color=(1, 1, 1, 1))
    layout = MDBoxLayout(orientation="horizontal")
    self.left_layout = MDFloatLayout(size_hint=(0.4, 1))
    self.right_layout = MDFloatLayout(size_hint=(0.6, 1))

    self.back_button = MDButton(
        MDButtonIcon(icon="home"),  # 设置图标为返回箭头
        MDButtonText(text="Home", font_style="Title"),
        style="elevated",
        pos_hint={"center_x": 2.2, "center_y": 0.95},  # 左上角位置
        size_hint=(0.25, 0.1),
        #on_release=self.switch_to_main_screen
        on_release=self.show_back_confirm_dialog
    )

    self.back_02_button = MDButton(
        MDButtonIcon(icon="arrow-left"),
        MDButtonText(text="Back", font_style="Title"),
        style="elevated",
        size_hint=(None, None), size=(dp(100), dp(40)),
        pos_hint={"x": 0.02, "top": 0.98},
        on_release=self.switch_to_pretest
    )
    screen.add_widget(self.back_02_button)

    stop_button = MDButton(
        MDButtonIcon(icon="timer-cancel"),
        MDButtonText(text="  Stop  ", font_style="Title"),
        style="elevated",
        pos_hint={"center_x": 0.5, "center_y": 0.65},  # 你也可以微调位置
        height="56dp",
        size_hint_x=0.6
    )
    stop_button.bind(on_press=self.show_stop_confirm_dialog)

    self.step3_button = MDButton(
        MDButtonIcon(icon="folder"),
        MDButtonText(text="Result", font_style="Title"),
        style="elevated",
        pos_hint={"center_x": 0.5, "center_y": 0.4},
        height="56dp",
        size_hint_x=0.6
    )

    # toggle_plot_button = MDButton(
    #     MDButtonIcon(icon="swap-horizontal"),
    #     MDButtonText(text="   Chart   ", font_style="Title"),
    #     style="elevated",
    #     pos_hint={"center_x": -0.33, "center_y": 0.2},  # 按钮位置可以根据需要调整 "center_x": -0.35
    #     height="56dp",
    #     size_hint_x=0.6
    # )

    # # 绑定按钮到 toggle_plot() 函数，用于切换显示的图表
    # toggle_plot_button.bind(
    #     on_press=self.toggle_plot,  # 原本的点击事件
    #     on_touch_down=self.start_touch_timer,  # 记录按下时间
    #     on_touch_up=self.check_long_press  # 计算按下时长
    #     )  


    self.actual_temperature_label = MDLabel(
        text="Current Temperature: -- °C",
        halign="center",
        pos_hint={"center_x": -0.4, "center_y": 0.1},
    )


    #这里应该要修改 0828——2025
    self.status_label = MDLabel(
        #text="Status: Waiting for action...", #这里可能要修改！！！！！！！！0828/2025
        halign="center",
        pos_hint={"center_x": 0.2, "center_y": 0.8},  #"center_y": 0.9 ("center_x": 0.4, "center_y": 0.85)
    )
    

    #可能要修改
    # self.remaining_time_label = MDLabel(
    #     text="Remaining: 60:00",   # 默认显示 60 分钟
    #     halign="center",
    #     pos_hint={"center_x": 0.2, "center_y": 0.9},  # 你可以调位置
    # )

    self.date_time_label = MDLabel(
        text="YYYY-MM-DD HH:MM:SS",
        halign="left",
        size_hint=(None, None),
        size=(dp(200), dp(40)),
        pos_hint={"x": -0.6, "y": 0},
    )

    logo = FitImage(
        source='/home/nero/NBUSA.jpg',
        size_hint=(None, None),
        size=(dp(233), dp(103)),  #size=(dp(133), dp(53))
        pos_hint={"right": 1.1, "bottom": 1},
    )

    #self.left_layout.add_widget(step1_button)
    self.left_layout.add_widget(stop_button)   # 新增 Stop 按钮
    #self.left_layout.add_widget(step2_button)
    self.left_layout.add_widget(self.step3_button)
    self.left_layout.add_widget(self.back_button)  # 添加返回按钮到左侧布局


    # ✅ status_label 创建完毕后，更新 ProcessFlowWidget
    self.process_flow.update_canvas()

    self.right_layout.add_widget(self.actual_temperature_label)
    self.right_layout.add_widget(self.status_label)
    self.right_layout.add_widget(self.remaining_time_label)  # ← 新增这一行
    self.right_layout.add_widget(self.date_time_label)
    self.right_layout.add_widget(logo)
    #self.right_layout.add_widget(toggle_plot_button) #可能要修改
    self.right_layout.add_widget(self.process_flow) #可能要修改！！！！！！

    layout.add_widget(self.left_layout)
    layout.add_widget(self.right_layout)

    screen.add_widget(layout)

    Clock.schedule_interval(self.update_actual_temperature, 0.5)
    Clock.schedule_interval(self.update_date_time, 1)
    Clock.schedule_interval(self.record_temperature, 1)  # 每隔1秒记录一次温度!!!!!!!!!!!!!!!!!!!!!!!!

    #step1_button.bind(on_press=self.step1_process)
    #step2_button.bind(on_press=self.start_step2)
    #step3_button.bind(on_press=self.step3_process)
    #self.step3_button.bind(on_release=self.go_to_report)
    self.step3_button.bind(on_release=self.open_report_with_result)


    return screen