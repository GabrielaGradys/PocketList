from datetime import datetime, timedelta

import flet as ft
from flet_core import MainAxisAlignment, FontWeight, alignment, View

from models.family import Family, FamilyMember
from models.visual_weather import FutureWeather
from scripts.visual_weather import get_weather

family = Family()


def get_family_row(page, family):
    def checkbox_changed(e):
        member = e.control.label.value
        is_going = e.control.selected
        if is_going:
            if e.control.label not in members:
                members.append(member)
        else:
            members.remove(member)
        print(f"{member} Going: {is_going}, All going: {members}")

    def get_family_list():
        members_names = [ft.Icon(ft.icons.FAMILY_RESTROOM),
                         ft.Text(value="Kto jedzie?")]
        for member in family.members:
            members_names.append(ft.Chip(
                label=ft.Text(member),
                selected=True,
                on_select=checkbox_changed)
            )
        return members_names

    members = page.client_storage.get("members") or list(family.members.keys())
    print(f"Initial members: {members}")

    return ft.Row(
        wrap=True,
        spacing=20,
        run_spacing=2,
        controls=get_family_list(),
        width=page.window_width,
    ), members


def get_dates_rows(page):
    def change_start_date(e):
        print(f"Start date set, value is {start_date_picker.value}")
        page.client_storage.set("start_date", str(start_date_picker.value))

        start_date_button.text = str(start_date_picker.value.date())
        page.update()
        end_date_picker.first_date = start_date_picker.value
        end_date_picker.value = start_date_picker.value + timedelta(days=3)

    def change_end_date(e):
        print(f"End date set, value is {end_date_picker.value}")
        page.client_storage.set("end_date", str(end_date_picker.value))
        end_date_button.text = str(end_date_picker.value.date())
        page.update()

    start_date_picker = ft.DatePicker(
        on_change=change_start_date,
        first_date=datetime.now(),
        last_date=datetime.now() + timedelta(days=300),
    )
    end_date_picker = ft.DatePicker(
        on_change=change_end_date,
        first_date=datetime.strptime(page.client_storage.get(
            'start_date'), "%Y-%m-%d %H:%M:%S"),
        last_date=datetime.now() + timedelta(days=300),
    )

    page.overlay.append(start_date_picker)
    page.overlay.append(end_date_picker)

    start_date_button = ft.ElevatedButton(
        "Od",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: start_date_picker.pick_date(),
    )

    end_date_button = ft.ElevatedButton(
        "Do",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: end_date_picker.pick_date(),
    )
    date_label = ft.Text(value="Na kiedy planujemy wycieczkę?")

    return ft.Row(
        wrap=True,
        spacing=20,
        run_spacing=10,
        controls=[
            ft.Icon(ft.icons.EDIT_CALENDAR),
            date_label,
            start_date_button,
            ft.Text(value="-"),
            end_date_button
        ],
        width=page.window_width,
    )


def get_button_row(page, location_name, members, summary_page):
    def btn_click(e):
        if not location_name.value:
            location_name.error_text = "Upss... podaj dokąd jedziemy."
            page.update()
        if len(members) == 0:
            page.add(ft.Text(f"Looks like you haven't choose anyone to go!!"))
            page.update()
        else:
            page.go(summary_page.route)
            page.views.append(summary_page)
            page.update()
            page.client_storage.set("location", location_name.value)
            page.add(ft.Text(f"Hello, {page.client_storage.get('location')}!"))
            page.update()

    btn = ft.ElevatedButton(content=ft.Container(ft.Row([
        ft.Text(value="Let's go!", size=20, weight=FontWeight.BOLD),
        ft.Icon(ft.icons.DIRECTIONS_CAR)
    ], alignment=MainAxisAlignment.CENTER), padding=10, width=120,
        alignment=alignment.center_right),
        on_click=btn_click)

    return ft.Row([ft.Container(
        btn, alignment=alignment.center_right, width=page.width * 0.9
    )])

def day_container(weather):
    icon_translation = {
        "rain": ft.Icon(ft.icons.CLOUDY_SNOWING, color="white"),
        "cloudy": ft.Icon(ft.icons.CLOUD),
        "partly-cloudy-day": ft.Icon(ft.icons.CLOUD),
        "sun": ft.Icon(ft.icons.SUNNY),
    }
    content = ft.Row([
        icon_translation[weather.icon]
    ])

    return ft.Container(
        content=content,
        alignment=ft.alignment.center,
        width=50,
        height=50,
        bgcolor=ft.colors.BLACK,
        border_radius=ft.border_radius.all(5),
    )


def main(page: ft.Page):
    page.title = "PocketList"

    def route_change(e):
        print("Route change:", e.route)
        page.views.clear()
        page.views.append(main_page)

        if page.route == "/summary":
            page.views.append(summary_page)

        page.update()

    # Summary Page
    location = page.client_storage.get("location")
    content = [ft.Text(value=f"Hello {location}!")]
    location, alerts, current_weather, future_weather = get_weather()
    for key in future_weather[0].__dataclass_fields__:
        label = FutureWeather.__dataclass_fields__[key].metadata['verbose_name']
        value = getattr(future_weather[0], key)
        print(f"{label}: {value}")

    future_weather_row = ft.Row(
        wrap=True,
        spacing=10,
        run_spacing=10,
        controls=[day_container(weather) for weather in future_weather],
        width=200,
    )

    summary_page = View("/summary", [future_weather_row])

    # Main Page
    dates_row = get_dates_rows(page)
    location_name = ft.TextField(label="Dokąd jedziemy?", icon="location_pin")
    family_row, members = get_family_row(page, family)
    button_row = get_button_row(page, location_name, members, summary_page)
    main_page = View("/", [dates_row, location_name, family_row, button_row])

    # Add styling
    for view in [main_page, summary_page]:
        view.vertical_alignment = ft.MainAxisAlignment.CENTER
        view.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=ft.colors.INDIGO,
                primary_container=ft.colors.INDIGO_400
            ),
        )
        view.padding = 30

    page.views.append(main_page)
    page.go(page.route)

ft.app(target=main)
