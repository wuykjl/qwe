import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from jnius import autoclass
from android.runnable import run_on_ui_thread

WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.kivy.android.PythonActivity').mActivity

class Wv(Widget):
    def __init__(self, **kwargs):
        super(Wv, self).__init__(**kwargs)
        Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args):
        webview = WebView(activity)
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setBuiltInZoomControls(True)
        settings.setDisplayZoomControls(False)
        
        webview.setWebViewClient(WebViewClient())
        
        # 强制加载 index.html (脚本会自动将用户文件重命名为此)
        path = "file://" + os.path.dirname(os.path.abspath(__file__)) + "/index.html"
        webview.loadUrl(path)
        activity.setContentView(webview)

class ServiceApp(App):
    def build(self):
        return Wv()

if __name__ == '__main__':
    ServiceApp().run()