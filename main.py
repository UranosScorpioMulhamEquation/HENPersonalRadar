import flet as ft
from datetime import date

def main(page: ft.Page):
    page.title = "HENRadar"
    page.padding = 20
    page.window_width = 600
    page.window_height = 600

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

    birth_input = ft.TextField(label="Paste Birth Date YYYY-MM-DD", value="1981-04-17", width=400)
    results_col = ft.Column(spacing=5)
    
    # هذا هو الحل: Container فيه ارتفاع + ScrollMode.AUTO 
    scroll_box = ft.Container(
        content=ft.Column([results_col], scroll=ft.ScrollMode.AUTO),
        height=400,
        width=400,
        expand=True,
    )

    page.add(
        ft.Text("HENRadar - Analysis Engine v2.0", size=30, weight="bold"),
        birth_input,
        ft.ElevatedButton("Generate", on_click=on_generate),
        scroll_box
    )

ft.app(target=main)
