from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.clock import Clock
from kivy.utils import platform

Window.clearcolor = (0.025, 0.025, 0.035, 1)


class GlassPanel(BoxLayout):
    bg_color = ListProperty([0.055, 0.055, 0.075, 0.96])
    radius = NumericProperty(24)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = dp(14)
        self.spacing = dp(10)
        with self.canvas.before:
            self._color = Color(*self.bg_color)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size,
                                          radius=[(self.radius, self.radius)] * 4)
        self.bind(pos=self._sync, size=self._sync, bg_color=self._sync_color)

    def _sync(self, *_):
        self._rect.pos = self.pos
        self._rect.size = self.size

    def _sync_color(self, *_):
        self._color.rgba = self.bg_color


class Island(Widget):
    island_color = ListProperty([0.02, 0.02, 0.025, 1])
    island_width = NumericProperty(dp(210))
    island_height = NumericProperty(dp(48))
    title = StringProperty("CART3R")
    subtitle = StringProperty("Dynamic Island")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (self.island_width, self.island_height)
        with self.canvas:
            self.shadow_color = Color(0.9, 0.08, 0.16, 0.20)
            self.shadow = RoundedRectangle(pos=self.pos, size=self.size,
                                           radius=[(30, 30)] * 4)
            self.fill_color = Color(*self.island_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size,
                                         radius=[(30, 30)] * 4)
            Color(1, 0.12, 0.22, 0.9)
            self.dot = RoundedRectangle(pos=(self.x + dp(14), self.center_y - dp(4)),
                                        size=(dp(8), dp(8)), radius=[(8, 8)] * 4)
        self.bind(pos=self._sync, size=self._sync, island_color=self._color_sync)

    def _sync(self, *_):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.shadow.pos = (self.x - dp(2), self.y - dp(2))
        self.shadow.size = (self.width + dp(4), self.height + dp(4))
        self.dot.pos = (self.x + dp(14), self.center_y - dp(4))

    def _color_sync(self, *_):
        self.fill_color.rgba = self.island_color

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._drag_offset = (self.x - touch.x, self.y - touch.y)
            self._dragging = True
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if getattr(self, "_dragging", False):
            nx = touch.x + self._drag_offset[0]
            ny = touch.y + self._drag_offset[1]
            self.pos = (max(0, min(Window.width - self.width, nx)),
                        max(0, min(Window.height - self.height, ny)))
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if getattr(self, "_dragging", False):
            self._dragging = False
            return True
        return super().on_touch_up(touch)


class DynamicIslandApp(App):
    def build(self):
        self.title = "CART3R Dynamic Island"
        self.root = FloatLayout()

        self.bg = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        self.root.add_widget(self.bg)

        header = BoxLayout(size_hint_y=None, height=dp(48))
        header.add_widget(Label(text="[b]CART3R[/b]  [color=ff334f]DYNAMIC ISLAND[/color]",
                                markup=True, font_size="18sp", halign="left"))
        menu_btn = self.make_button("KONTROL", self.open_control, width=dp(100))
        header.add_widget(menu_btn)
        self.bg.add_widget(header)

        self.island = Island()
        self.island.pos = (Window.width / 2 - dp(105), Window.height - dp(130))
        self.root.add_widget(self.island)

        intro = GlassPanel(orientation="vertical", size_hint_y=None, height=dp(180))
        intro.add_widget(Label(text="[b]Kişisel Dynamic Island[/b]", markup=True,
                               font_size="20sp", color=(1, 1, 1, 1)))
        intro.add_widget(Label(text="Siyah hapı parmağınla sürükleyerek taşı. "
                                    "Ayarlar bölümünden boyutunu ve rengini değiştir.",
                               font_size="14sp", color=(0.72, 0.72, 0.78, 1),
                               halign="center", valign="middle"))
        self.bg.add_widget(intro)

        self.bg.add_widget(self.make_button("GÖRÜNÜMÜ ÖZELLEŞTİR", self.open_settings, height=dp(52)))
        self.bg.add_widget(self.make_button("KONTROL MERKEZİNİ AÇ", self.open_control, height=dp(52)))
        self.bg.add_widget(self.make_button("SİSTEM WI-FI AYARLARI", self.open_wifi, height=dp(52)))

        note = Label(text="PROTOTİP • Uygulama içi görünüm • Sistem genelinde overlay değildir",
                     font_size="10sp", color=(0.55, 0.55, 0.60, 1),
                     size_hint_y=None, height=dp(28))
        self.bg.add_widget(note)
        return self.root

    def make_button(self, text, callback, width=None, height=dp(46)):
        b = Button(text=text, size_hint=(None, None) if width else (1, None),
                   width=width or 0, height=height, background_normal="",
                   background_color=(0.30, 0.035, 0.075, 1),
                   color=(1, 1, 1, 1), bold=True)
        b.bind(on_release=lambda *_: callback())
        return b

    def make_popup(self, title, content, height=dp(430)):
        pop = Popup(title=title, content=content, size_hint=(0.92, None),
                    height=height, separator_color=(0.95, 0.12, 0.25, 1),
                    background_color=(0.045, 0.045, 0.06, 1))
        pop.open()
        return pop

    def open_settings(self):
        panel = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(12))
        panel.add_widget(Label(text="Ada genişliği", size_hint_y=None, height=dp(25)))
        width_slider = Slider(min=140, max=320, value=self.island.width)
        panel.add_widget(width_slider)
        panel.add_widget(Label(text="Ada yüksekliği", size_hint_y=None, height=dp(25)))
        height_slider = Slider(min=36, max=90, value=self.island.height)
        panel.add_widget(height_slider)
        panel.add_widget(Label(text="Yatay konum", size_hint_y=None, height=dp(25)))
        x_slider = Slider(min=0, max=max(1, Window.width - self.island.width),
                          value=self.island.x)
        panel.add_widget(x_slider)
        panel.add_widget(Label(text="Dikey konum", size_hint_y=None, height=dp(25)))
        y_slider = Slider(min=0, max=max(1, Window.height - self.island.height),
                          value=self.island.y)
        panel.add_widget(y_slider)
        panel.add_widget(Label(text="Ada rengi", size_hint_y=None, height=dp(25)))
        colors = GridLayout(cols=3, spacing=dp(8), size_hint_y=None, height=dp(48))
        palette = [
            ("Kırmızı", [0.02, 0.02, 0.025, 1]),
            ("Bordo", [0.16, 0.015, 0.04, 1]),
            ("Mor", [0.08, 0.025, 0.16, 1]),
            ("Mavi", [0.015, 0.045, 0.12, 1]),
            ("Yeşil", [0.01, 0.10, 0.07, 1]),
            ("Gri", [0.12, 0.12, 0.14, 1]),
        ]
        for name, color in palette:
            btn = Button(text=name, background_normal="", background_color=color)
            btn.bind(on_release=lambda _, c=color: setattr(self.island, "island_color", c))
            colors.add_widget(btn)
        panel.add_widget(colors)

        def apply(*_):
            self.island.size = (dp(width_slider.value), dp(height_slider.value))
            self.island.pos = (x_slider.value, y_slider.value)
            x_slider.max = max(1, Window.width - self.island.width)
            y_slider.max = max(1, Window.height - self.island.height)

        for slider in (width_slider, height_slider, x_slider, y_slider):
            slider.bind(value=apply)
        panel.add_widget(self.make_button("KAPAT", lambda: popup.dismiss()))
        popup = self.make_popup("GÖRÜNÜM AYARLARI", panel, dp(610))

    def open_control(self):
        panel = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))
        panel.add_widget(Label(text="[b]Hızlı Kontroller[/b]", markup=True,
                               font_size="20sp", size_hint_y=None, height=dp(40)))
        grid = GridLayout(cols=2, spacing=dp(10))
        actions = [
            ("Wi-Fi ayarları", self.open_wifi),
            ("Bluetooth ayarları", self.open_bluetooth),
            ("Ses ayarları", self.open_sound),
            ("Ekran ayarları", self.open_display),
        ]
        for title, fn in actions:
            grid.add_widget(self.make_button(title, fn, height=dp(64)))
        panel.add_widget(grid)
        panel.add_widget(Label(text="Bu kısayollar Android'in kendi ayar ekranlarını açar. "
                                    "Uygulama sistem anahtarlarını gizlice değiştirmez.",
                               font_size="12sp", color=(0.72, 0.72, 0.78, 1)))
        panel.add_widget(self.make_button("KAPAT", lambda: popup.dismiss()))
        popup = self.make_popup("CART3R CONTROL CENTER", panel, dp(350))

    def launch_android_settings(self, action):
        if platform != "android":
            self.show_message("Android gerekli", "Bu kısayol yalnızca Android cihazda çalışır.")
            return
        try:
            from jnius import autoclass
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Intent = autoclass("android.content.Intent")
            activity = PythonActivity.mActivity
            intent = Intent(action)
            activity.startActivity(intent)
        except Exception as exc:
            self.show_message("Ayarlar açılamadı", str(exc))

    def open_wifi(self):
        self.launch_android_settings("android.settings.WIFI_SETTINGS")

    def open_bluetooth(self):
        self.launch_android_settings("android.settings.BLUETOOTH_SETTINGS")

    def open_sound(self):
        self.launch_android_settings("android.settings.SOUND_SETTINGS")

    def open_display(self):
        self.launch_android_settings("android.settings.DISPLAY_SETTINGS")

    def show_message(self, title, message):
        box = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        box.add_widget(Label(text=message))
        box.add_widget(self.make_button("TAMAM", lambda: pop.dismiss()))
        pop = Popup(title=title, content=box, size_hint=(0.85, None), height=dp(220))
        pop.open()


if __name__ == "__main__":
    DynamicIslandApp().run()