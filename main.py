import flet as ft
from datetime import date

def main(page: ft.Page):
    page.title = "HENRadar"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # رسالة للتحقق
    status_text = ft.Text("Press the button to pick a date:", size=16)
    results_col = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    # دالة الحساب (تبقى كما هي)
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
            data.append({"date": f"{y}-{m:02d}-{d:02d}", "status": status})
        return data

    # دالة تظهر عند اختيار التاريخ
    def date_picked(e):
        if date_picker.value:
            status_text.value = f"Selected: {date_picker.value.strftime('%Y-%m-%d')}"
            res = run_engine(date_picker.value)
            results_col.controls.clear()
            for r in res:
                color = ft.colors.RED_500 if r['status'] == "CRITICAL" else ft.colors.GREEN_700
                results_col.controls.append(ft.Text(f"{r['date']} -> {r['status']}", color=color))
            page.update()

    # إنشاء الـ DatePicker وإضافته للـ Overlay بشكل صحيح
    date_picker = ft.DatePicker(on_change=date_picked, first_date=date(1900, 1, 1), last_date=date(2099, 12, 31))
    page.overlay.append(date_picker)
    
    # الزر الذي يفتح النافذة
    page.add(
        ft.ElevatedButton("Select Birth Date", icon=ft.icons.CALENDAR_MONTH, on_click=lambda _: date_picker.pick_date()),
        status_text,
        results_col
    )
    page.update()

ft.app(target=main)
