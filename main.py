import flet as ft
from datetime import date

def main(page: ft.Page):
    # إعدادات الواجهة
    page.title = "HENRadar"
    page.padding = 20
    
    # رسالة تعريفية
    status_text = ft.Text("Enter your Birth Date to start Analysis", size=16)
    results_col = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    # معادلة الرادار (بدون أي تعديل)
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

    # منطق العرض
    def show_results(e):
        if date_picker.value:
            res = run_engine(date_picker.value)
            results_col.controls.clear()
            for r in res:
                results_col.controls.append(
                    ft.Text(f"Date: {r['date']} - {r['status']}", 
                            color=ft.colors.RED if r['status'] == "CRITICAL" else ft.colors.GREEN)
                )
            page.update()

    date_picker = ft.DatePicker(on_change=lambda e: show_results(e))
    page.overlay.append(date_picker)
    
    page.add(
        ft.ElevatedButton("Select Birth Date", on_click=lambda _: date_picker.pick_date()),
        status_text,
        results_col
    )

ft.app(target=main)
