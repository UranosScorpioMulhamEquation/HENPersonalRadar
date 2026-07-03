import flet as ft
import uuid
from datetime import date

# ==================== Main Application ====================
def main(page: ft.Page):
    page.title = "HENRadar"
    page.padding = 20
    # إعدادات النافذة التالية مفيدة للويندوز ولن تؤثر سلباً على الموبايل
    page.window_width = 600
    page.window_height = 600

    # 1. دوال الحماية المخصصة للموبايل
    def get_device_id():
        # التحقق مما إذا كان الجهاز يمتلك معرفاً مسبقاً في الذاكرة
        if page.client_storage.contains_key("device_id"):
            return page.client_storage.get("device_id")
        else:
            # توليد معرف جديد وحفظه ليكون ثابتاً لهذا الموبايل
            new_id = uuid.uuid4().hex[:8].upper()
            page.client_storage.set("device_id", new_id)
            return new_id

    def generate_password(mid):
        digits = ''.join(filter(str.isdigit, str(mid)))
        num = int(digits[:8]) if digits else int(str(mid).encode().hex(), 16)
        return str(round(abs(num / 2 * 3.14)))[:6]

    # 2. التطبيق الأساسي
    def load_main_app():
        page.controls.clear()

        def run_engine(birth_date):
            homo_k, eris_k, neptune_k, tolerance = 6.18, 9.3, 10.77, 0.3
            data = []
            for i in range(1, 85):
                h = abs((i/homo_k)-round(i/homo_k))
                e = abs((i/eris_k)-round(i/eris_k))
                n = abs((i/neptune_k)-round(i/neptune_k))
                status = "CRITICAL" if (h <= tolerance and e <= tolerance and n <= tolerance) else "Normal"
                
                d = birth_date.day + int(e * 30)
                m = birth_date.month + int(h * 12)
                y = birth_date.year + i
                while d > 30: d -= 30; m += 1
                while m > 12: m -= 12; y += 1
                data.append(f"{y}-{m:02d}-{d:02d} : {status}")
            return data

        def on_generate(e):
            results_col.controls.clear()
            try:
                y, m, d = map(int, birth_input.value.strip().split('-'))
                birth_date = date(y, m, d)
                res = run_engine(birth_date)
                for line in res:
                    results_col.controls.append(ft.Text(line, size=14))
            except:
                results_col.controls.append(ft.Text("Error: Use format YYYY-MM-DD"))
            page.update()

        birth_input = ft.TextField(label="Paste Birth Date YYYY-MM-DD", value="1981-04-17")
        results_col = ft.Column(spacing=5)
        
        scroll_box = ft.Container(
            content=ft.Column([results_col], scroll=ft.ScrollMode.AUTO),
            height=400,
            expand=True,
        )

        page.add(
            ft.Text("HENRadar - Analysis Engine v2.0", size=30, weight="bold"),
            birth_input,
            ft.ElevatedButton("Generate", on_click=on_generate),
            scroll_box
        )
        page.update()

    # ==================== 3. Authentication Flow ====================
    # التحقق من حالة التفعيل من خلال ذاكرة Flet الداخلية
    if page.client_storage.get("is_activated"):
        load_main_app()
    else:
        mid = get_device_id()
        
        def on_activate(e):
            pwd = activation_input.value
            if pwd == generate_password(mid):
                # حفظ حالة التفعيل بنجاح في الذاكرة لتخطي الشاشة مستقبلاً
                page.client_storage.set("is_activated", True)
                load_main_app() 
            else:
                error_msg.value = "Invalid Activation Key."
                error_msg.visible = True
                page.update()

        activation_input = ft.TextField(
            label="Enter Activation Key:", 
            password=True, 
            can_reveal_password=True
        )
        error_msg = ft.Text(value="", visible=False)

        page.add(
            ft.Text("Security Activation - Ask the programmer for your password", size=20, weight="bold"),
            ft.Text("Send your Machine ID to programmer email : mulham81ahmed@gmail.com"),
            ft.Text(f"Machine ID: {mid}", size=16),
            activation_input,
            ft.ElevatedButton("Activate", on_click=on_activate),
            error_msg
        )
        page.update()

ft.app(target=main)
