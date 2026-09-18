__version__ = "1.1.0"

import json
import os
import socket
import threading
from datetime import datetime
from urllib.parse import quote

import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


# ============================================================
# 1. GOOGLE FORM CONFIG  — REAL VALUES
# ============================================================
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc57UtLVNUmqY1ug1c8aN1HkdT0gZg5NHLSqoAWPwK9gaP9SA/formResponse"

ENTRY_IDS = {
    "date_year":     "entry.1344115585_year",
    "date_month":    "entry.1344115585_month",
    "date_day":      "entry.1344115585_day",
    "reference":     "entry.1460740528",
    "product":       "entry.1706794748",
    "batch_no":      "entry.2053221472",
    "qty":           "entry.1487877158",
    "received_from": "entry.283229920",
    "remarks":       "entry.686689049",
}

MANAGER_WHATSAPP = "2348065211837"
QUEUE_FILE = "receipt_queue.json"


# ============================================================
# 2. PRODUCTS (full 137)
# ============================================================
PRODUCTS = [
    "AFRABVITE 15ML DROPS",
    "AFRABVITE 100ML SYRUP",
    "ALLERGIN 60ML SYRUP",
    "AMIBAGYL 60ML SUSPENSION",
    "HOSPIMOX (AMOXYCILLIN) 125MG 100ML SUSPENSION",
    "CILLINOX SUSP. (AMPI/CLOX) 100MLS",
    "AMIBAGYL TABLETS 200MG",
    "BANEDIF OINTMENT",
    "BANEDIF POWDER",
    "CHEMOTRIM 100ML SUSPENSION",
    "CILLINOX 12ML DROPS",
    "CITRAMIN 15ML DROPS",
    "CHLORAF 100ML SUSPENSION",
    "CHEMOTRIM TAB 480MG (10X10)",
    "CHEMOTRIM 60ML SUSPENSION",
    "DETONIC 200ML SYRUP",
    "DIASTOP 100ML SUSPENSION",
    "DETONIC SYRUP (1 LTR)",
    "ENAPHRIN NASAL DROPS (10ML)",
    "FUNGUSOL 20GM CREAM",
    "FUNGUSOL 20GM POWDER",
    "FUNGUSOL 50ML LOTION",
    "GLIBENOL CAPLETS 5MG (10X10)",
    "AFRAB CHLOROQUINE DROPS 11ML",
    "AFRAB IBUPROFEN SUSPENSION",
    "LA-TESEN TABLETS",
    "NOSPAMIN 15ML DROPS",
    "NOCOF DROPS",
    "OTO MED 8ML DROPS",
    "PANDA 15ML DROPS",
    "PANDA 60ML SYRUP",
    "PANDA TABLET 96'S",
    "PANDA TABLET 1000'S",
    "PANDA COLD DROPS",
    "REUMEX LOTION",
    "STOPACID 200ML SUSPENSION",
    "TUSSYLIN 100ML SYRUP [Adult]",
    "TUSSYLIN 100ML SYRUP [Infant]",
    "CITRAMIN SYRUP 100ML",
    "CYSTAZOLE SUSPENSION",
    "HALOPERIDOL TABLETS (10MG)",
    "HALOPERIDOL TABLETS (5MG)",
    "PANDA COLD SYRUP",
    "PANDA NIGHT CAPLETS (500MG) 10X10",
    "CYSTAZOLE CAPLETS (200MG)",
    "NOCOF SYRUP",
    "FUNGUSOL PLUS CREAM",
    "FUNGUSOL PLUS LOTION",
    "AFRAB LORATADINE SYRUP (60ML)",
    "AFRAB LORATADINE TABS (10X10)",
    "AFRAB LORATADINE TABS 10MG (10 X 2)",
    "DETONIC PLUS SYRUP",
    "AFRAB METFORMIN TABLETS (3 X 10)",
    "PANDA NIGHT CAPLETS (12 X 8)",
    "AMIBAGYL TABLETS 200MG (1000'S)",
    "AFRABVITE PLUS DROPS",
    "AFRAMIN SYRUP (200ML)",
    "PANDA NIGHT SYRUP (60ML)",
    "AFRAB IVY SYRUP (100ML)",
    "THIVY SYRUP (100ML)",
    "AFRAB GRIPE WATER (100ML)",
    "STOPACID 200ML SUSPENSION (strawberry)",
    "STOPACID 200ML SUSPENSION (banana)",
    "PANDA SUSPENSION (60ML)",
    "AFRAB CIPROFLOXACIN CAPLET 500MG (10'S)",
    "PANDA NIGHT CAPLETS (2x10)",
    "PANDA CAPLETS 500mg (10X10)",
    "PANDA CAPLETS 500mg (10 X 2)",
    "PANDA NIGHT DROPS (15ML)",
    "AFRAGRA TABLETS (100MG (1 X 4)",
    "HOSPIMOX CAPSULES",
    "NOSPAMIN SYRUP",
    "AFRAB LEVOFLOXACIN CAPLET 500MG (10'S)",
    "CITRAMIN PLUS TAB (Effervescent)",
    "AFRAB ALENDOMAX 70mg",
    "B-Cor 2.5MG (10X3)",
    "B-Cor 5MG (15 X 2)",
    "B-Cor TABLETS 10MG (10 X 3)",
    "AFRAB RESPAL 1mg (2 X 10)",
    "AFRAB RISPERIDON 2mg (2 X 10)",
    "AFRAB RISPERIDON 4mg (2 X 10)",
    "PANDA EXTRA CAPLETS 500MG (10X10)",
    "AFRAB SALBUTAMOL SYRUP 100ML",
    "LATESEN DS CAPLETS (1 X 6)",
    "AFRAB SALBUTAMOL TABLET 4MG (10X10)",
    "ALFALEX CAPSULES 200MG (1 X 10)",
    "ALFALEX CAPSULES 400MG",
    "HISTOLAT SYRUP (60ML)",
    "HISTOLAT TABLETS (5MG)",
    "ALFADOX TABLETS (3x1)",
    "AFRAB IBUPROFEN DS DROPS 30ML",
    "ALFADOX SUSPENSION (15ML)",
    "AFRABRON SYRUP(200ML)",
    "ULTRA LINC TABLETS 5MG(2x15)",
    "ULTRA LINC TABLETS 20MG(1x4)",
    "AFRADIN DROPS(30ML)",
    "DEKOLIK SYRUP(60ML)",
    "AFRAB IBUPROFEN EFFERVESCENT",
    "AFRAB IBUPROFEN DS SUSPENSION 100ML",
    "PANDA EFFERVESCENT",
    "AFRAB TERAD DROPS(25ML)",
    "AFRAB SIMETHICONE DROPS",
    "TERAD CAPLETS (1X30)",
    "CITRAMIN DROPS 30ML",
    "AFRABVITE DROPS 30ML",
    "AFRABVITE PLUS DROPS 30ML",
    "PANDA DROPS 30ML",
    "NOCOF DROPS 30ML",
    "SOLOMAX SYRUP 100ML",
    "AFRABLEX SYRUP (100ML)",
    "AFRAB ZINC 11MG TABLETS(10 X 3)",
    "AFRAB LORATADINE SYRUP 100ML",
    "AFRAB ORS POWDER(3x1)",
    "AFRAB ZINC SULPHATE 20MG TABLETS(1 X 10)",
    "AFRAB HAND SANITIZER (100ML)",
    "METFORMIN TABLETS(10 X 10)",
    "AFRAB CHLOROQUINE TABLETS(1 x 10)",
    "LA-TESEN TABLETS 20/120MG (2 X 24)",
    "CETRAZEE TABLETS 60's",
    "AFRAB HYOSCINE BUTYLBROMIDE SYRUP",
    "LATESEN DISPERSIBLE TABS (6'S)",
    "DETONIC SYRUP (100ML)",
    "RESPERIDONE SYRUP",
    "IBUPROFEN TABLETS",
    "AFRABRON TABLETS(3 X 10)",
    "AFRAB LISINOPRIL TABLET 5MG(2 X 14)",
    "AFRAB LISINOPRIL TABLET 10MG(2 X 14)",
    "AFRAB AMLODIPINE TABLETS 5MG(2 X 14)",
    "AFRAB AMLODIPINE TABLETS 10MG(2 X 14)",
    "VITA JOY MOOD CARE TABLETS",
    "VITA JOY NEURO CARE TABLETS",
    "VITA JOY POSTNATAL CARE TABLETS",
    "VITA JOY PRENATAL CARE TABLETS",
    "VITA JOY SLEEP CARE TABLETS",
    "VITA JOY STRESS RELAX CARE TABLETS",
    "VITA JOY FEMALE TEEN CARE TABLETS",
    "VITA JOY MALE TEEN CARE TABLETS",
]


# ============================================================
# 3. HELPERS
# ============================================================
def get_app_dir():
    app = App.get_running_app()
    base = app.user_data_dir if app else os.path.expanduser("~")
    try:
        os.makedirs(base, exist_ok=True)
    except OSError:
        pass
    return base


def get_queue_path():
    return os.path.join(get_app_dir(), QUEUE_FILE)


def has_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3).close()
        return True
    except OSError:
        return False


def split_date(iso_date):
    if not iso_date:
        return "0", "0", "0"
    try:
        y, m, d = iso_date.split("-")
        return str(int(y)), str(int(m)), str(int(d))
    except ValueError:
        return "0", "0", "0"


def make_reference():
    return "REC-" + datetime.now().strftime("%Y%m%d-%H%M")


def build_payload(ref, date, received_from, remarks, item):
    y, m, d = split_date(date)
    return {
        ENTRY_IDS["date_year"]:     y,
        ENTRY_IDS["date_month"]:    m,
        ENTRY_IDS["date_day"]:      d,
        ENTRY_IDS["reference"]:     ref,
        ENTRY_IDS["product"]:       item.get("product", ""),
        ENTRY_IDS["batch_no"]:      item.get("batch_no", ""),
        ENTRY_IDS["qty"]:           item.get("qty", ""),
        ENTRY_IDS["received_from"]: received_from,
        ENTRY_IDS["remarks"]:       remarks,
    }


def try_submit_one(ref, date, received_from, remarks, item):
    try:
        r = requests.post(
            FORM_URL,
            data=build_payload(ref, date, received_from, remarks, item),
            timeout=15,
        )
        if r.status_code not in (200, 201, 202):
            return False
        if "accounts.google.com" in r.url:
            return False
        return True
    except requests.RequestException:
        return False


def load_queue():
    path = get_queue_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_queue(queue):
    try:
        with open(get_queue_path(), "w", encoding="utf-8") as f:
            json.dump(queue, f)
    except OSError:
        pass


def queue_batch(batch):
    q = load_queue()
    q.append(batch)
    save_queue(q)


def flush_queue():
    q = load_queue()
    if not q:
        return 0

    remaining = []
    sent_items = 0
    for batch in q:
        all_ok = True
        for item in batch.get("items", []):
            if try_submit_one(
                batch.get("ref", ""),
                batch.get("date", ""),
                batch.get("received_from", ""),
                batch.get("remarks", ""),
                item,
            ):
                sent_items += 1
            else:
                all_ok = False
                break
        if not all_ok:
            remaining.append(batch)

    save_queue(remaining)
    return sent_items


# ============================================================
# 4. SEARCHABLE PRODUCT PICKER
# ============================================================
class ListPicker(Popup):
    def __init__(self, title, items, on_pick, **kwargs):
        super().__init__(title=title, size_hint=(0.95, 0.9), **kwargs)
        self.all_items = list(items)
        self.on_pick = on_pick

        root = BoxLayout(orientation="vertical", padding=8, spacing=8)
        self.search = TextInput(hint_text="Type to search...", multiline=False,
                                size_hint_y=None, height=48, font_size=dp(15))
        self.search.bind(text=self.refresh)
        root.add_widget(self.search)

        self.scroll = ScrollView()
        self.list_layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing=2)
        self.list_layout.bind(minimum_height=self.list_layout.setter("height"))
        self.scroll.add_widget(self.list_layout)
        root.add_widget(self.scroll)

        self.add_widget(root)
        self.refresh(None, "")

    def refresh(self, instance, value):
        self.list_layout.clear_widgets()
        q = (value or "").strip().lower()
        items = [p for p in self.all_items if q in p.lower()] if q else self.all_items
        for item in items:
            btn = Button(text=item, size_hint_y=None, height=48,
                         halign="left", valign="middle", font_size=dp(14))
            btn.bind(on_release=lambda b, t=item: self.pick(t))
            self.list_layout.add_widget(btn)

    def pick(self, text):
        self.on_pick(text)
        self.dismiss()


# ============================================================
# 5. SESSION INFO POPUP
# ============================================================
class SessionInfoPopup(Popup):
    def __init__(self, form, **kwargs):
        super().__init__(title="Session Info", size_hint=(0.95, 0.75), **kwargs)
        self.form = form

        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))

        def row(label_text, initial_text, hint=""):
            box = BoxLayout(size_hint_y=None, height=dp(56), spacing=dp(6))
            lbl = Label(text=label_text, size_hint_x=0.35, font_size=dp(14),
                        halign="left", valign="middle")
            lbl.bind(size=lbl.setter("text_size"))
            box.add_widget(lbl)
            ti = TextInput(text=initial_text, hint_text=hint, multiline=False,
                           size_hint_x=0.65, font_size=dp(14))
            box.add_widget(ti)
            root.add_widget(box)
            return ti

        self.date_in = row("Date:", form.date_field.text, "YYYY-MM-DD")
        self.ref_in = row("Reference:", form.ref_field.text, "")
        self.from_in = row("Received From:", form.from_field.text, "e.g. Production")
        self.rem_in = row("Remarks:", form.remarks_field.text, "optional")

        root.add_widget(Label(text="", size_hint_y=None, height=dp(8)))

        btns = BoxLayout(size_hint_y=None, height=dp(56), spacing=dp(10))
        save_btn = Button(text="Save", font_size=dp(16), bold=True,
                          background_color=(0.2, 0.7, 0.3, 1))
        save_btn.bind(on_release=self.save)
        btns.add_widget(save_btn)
        cancel_btn = Button(text="Cancel", font_size=dp(16),
                            background_color=(0.5, 0.5, 0.5, 1))
        cancel_btn.bind(on_release=lambda *a: self.dismiss())
        btns.add_widget(cancel_btn)
        root.add_widget(btns)

        self.add_widget(root)

    def save(self, *args):
        self.form.date_field.text = self.date_in.text.strip()
        self.form.ref_field.text = self.ref_in.text.strip()
        self.form.from_field.text = self.from_in.text.strip()
        self.form.remarks_field.text = self.rem_in.text.strip()
        self.form.update_session_header()
        self.dismiss()


# ============================================================
# 6. MAIN UI
# ============================================================
class ReceiptForm(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        Window.softinput_mode = "below_target"

        self.items = []
        self.selected_product = ""

        # Hidden data holders (edited via Session Info popup)
        self.date_field = TextInput(text=datetime.now().strftime("%Y-%m-%d"))
        self.ref_field = TextInput(text=make_reference())
        self.from_field = TextInput(text="")
        self.remarks_field = TextInput(text="")

        # ---------- Header ----------
        self.add_widget(Label(
            text="Product Receipt Entry",
            font_size=dp(20), bold=True, size_hint_y=None,
            height=dp(44), color=(0.15, 0.45, 0.85, 1),
        ))

        # ---------- Session info button ----------
        self.session_btn = Button(
            text="",
            size_hint_y=None, height=dp(48), font_size=dp(14),
            halign="left", valign="middle",
            background_color=(0.22, 0.30, 0.45, 1),
        )
        self.session_btn.bind(on_release=self.open_session_popup)
        self.add_widget(self.session_btn)

        # ---------- Add-item section ----------
        add_box = BoxLayout(orientation="vertical", size_hint_y=None,
                            spacing=dp(6), padding=dp(8))
        add_box.bind(minimum_height=add_box.setter("height"))

        # Product row
        prod_row = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(6))
        prod_lbl = Label(text="Product:", size_hint_x=0.28,
                         font_size=dp(14), halign="left", valign="middle")
        prod_lbl.bind(size=prod_lbl.setter("text_size"))
        prod_row.add_widget(prod_lbl)
        self.prod_btn = Button(text="Tap to choose",
                               size_hint_x=0.72, font_size=dp(14),
                               background_color=(0.2, 0.6, 0.85, 1))
        self.prod_btn.bind(on_release=self.open_product_picker)
        prod_row.add_widget(self.prod_btn)
        add_box.add_widget(prod_row)

        # Batch row
        batch_row = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(6))
        batch_lbl = Label(text="Batch No:", size_hint_x=0.28,
                          font_size=dp(14), halign="left", valign="middle")
        batch_lbl.bind(size=batch_lbl.setter("text_size"))
        batch_row.add_widget(batch_lbl)
        self.batch_input = TextInput(hint_text="e.g. B-101", multiline=False,
                                     size_hint_x=0.72, font_size=dp(14))
        batch_row.add_widget(self.batch_input)
        add_box.add_widget(batch_row)

        # Quantity row
        qty_row = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(6))
        qty_lbl = Label(text="Quantity:", size_hint_x=0.28,
                        font_size=dp(14), halign="left", valign="middle")
        qty_lbl.bind(size=qty_lbl.setter("text_size"))
        qty_row.add_widget(qty_lbl)
        self.qty_input = TextInput(hint_text="e.g. 500", multiline=False,
                                   input_type="number",
                                   size_hint_x=0.72, font_size=dp(14))
        qty_row.add_widget(self.qty_input)
        add_box.add_widget(qty_row)

        self.add_widget(add_box)

        # Add button
        add_btn = Button(text="+  Add to List",
                         size_hint_y=None, height=dp(52),
                         font_size=dp(16), bold=True,
                         background_color=(0.15, 0.55, 0.85, 1))
        add_btn.bind(on_release=self.add_item)
        self.add_widget(add_btn)

        # Items header
        self.items_header = Label(
            text="Items (0) · Total 0",
            size_hint_y=None, height=dp(30),
            font_size=dp(13), bold=True,
            color=(0.55, 0.65, 0.85, 1),
        )
        self.add_widget(self.items_header)

        # Items list
        self.items_scroll = ScrollView(size_hint=(1, 1))
        self.items_layout = BoxLayout(orientation="vertical",
                                      size_hint_y=None, spacing=dp(4))
        self.items_layout.bind(minimum_height=self.items_layout.setter("height"))
        self.items_scroll.add_widget(self.items_layout)
        self.add_widget(self.items_scroll)

        # Status
        self.status = Label(
            text="Ready — add a product then tap Add to List.",
            size_hint_y=None, height=dp(28),
            font_size=dp(12),
            color=(0.3, 0.5, 0.3, 1),
        )
        self.add_widget(self.status)

        # Bottom buttons
        btn_row = BoxLayout(size_hint_y=None, height=dp(64),
                            spacing=dp(6), padding=dp(6))

        submit_btn = Button(text="Submit All", font_size=dp(14), bold=True,
                            background_color=(0.2, 0.7, 0.3, 1))
        submit_btn.bind(on_release=self.submit_all)
        btn_row.add_widget(submit_btn)

        sync_btn = Button(text="Sync", font_size=dp(14), bold=True,
                          background_color=(0.9, 0.6, 0.2, 1))
        sync_btn.bind(on_release=self.sync_queue)
        btn_row.add_widget(sync_btn)

        chat_btn = Button(text="Chat", font_size=dp(14), bold=True,
                          background_color=(0.15, 0.65, 0.4, 1))
        chat_btn.bind(on_release=self.open_whatsapp)
        btn_row.add_widget(chat_btn)

        clear_btn = Button(text="Clear", font_size=dp(14), bold=True,
                           background_color=(0.8, 0.3, 0.3, 1))
        clear_btn.bind(on_release=self.clear_form)
        btn_row.add_widget(clear_btn)

        self.add_widget(btn_row)

        # Initial state
        self.update_session_header()
        self.refresh_items_list()

        # Timers
        Clock.schedule_once(lambda dt: self._background_sync(0), 3)
        Clock.schedule_interval(self._background_sync, 30)

    # ---------- Session header ----------
    def update_session_header(self):
        date = self.date_field.text.strip() or "?"
        ref = self.ref_field.text.strip() or "?"
        recv = self.from_field.text.strip() or "(tap to set)"
        self.session_btn.text = f"📋 {recv}   ·   {date}   ·   {ref}"

    def open_session_popup(self, instance):
        SessionInfoPopup(self).open()

    # ---------- Product picker ----------
    def open_product_picker(self, instance):
        ListPicker(title="Select Product", items=PRODUCTS,
                   on_pick=self.set_product).open()

    def set_product(self, name):
        self.selected_product = name
        self.prod_btn.text = name

    # ---------- Add / remove items ----------
    def add_item(self, instance):
        if not self.selected_product or self.selected_product not in PRODUCTS:
            self.status.text = "Choose a product first."
            self.status.color = (0.9, 0.1, 0.1, 1)
            return

        batch = self.batch_input.text.strip()
        qty = self.qty_input.text.strip()
        if not batch or not qty:
            self.status.text = "Enter Batch No and Quantity."
            self.status.color = (0.9, 0.1, 0.1, 1)
            return

        # Duplicate check
        for it in self.items:
            if it["product"] == self.selected_product and it["batch_no"] == batch:
                self.status.text = "⚠ Duplicate: same product + batch already added."
                self.status.color = (0.9, 0.55, 0.1, 1)
                return

        self.items.append({
            "product":  self.selected_product,
            "batch_no": batch,
            "qty":      qty,
        })
        self.status.text = f"Added. {len(self.items)} item(s) in list."
        self.status.color = (0.3, 0.5, 0.3, 1)

        # Reset entry row
        self.selected_product = ""
        self.prod_btn.text = "Tap to choose"
        self.batch_input.text = ""
        self.qty_input.text = ""

        self.refresh_items_list()

    def remove_item(self, index):
        if 0 <= index < len(self.items):
            self.items.pop(index)
            self.refresh_items_list()
            self.status.text = f"Removed. {len(self.items)} item(s) left."
            self.status.color = (0.3, 0.5, 0.3, 1)

    def refresh_items_list(self):
        self.items_layout.clear_widgets()

        total_qty = 0
        for it in self.items:
            try:
                total_qty += int(it["qty"])
            except ValueError:
                pass
        self.items_header.text = f"Items ({len(self.items)}) · Total {total_qty}"

        if not self.items:
            self.items_layout.add_widget(Label(
                text="(no items yet)",
                size_hint_y=None, height=dp(36),
                color=(0.5, 0.5, 0.5, 1), font_size=dp(13),
            ))
            return

        for i, item in enumerate(self.items):
            row = BoxLayout(size_hint_y=None, height=dp(54),
                            spacing=dp(6), padding=(dp(6), 0))
            text = (f"[b]{i+1}. {item['product']}[/b]\n"
                    f"     Batch {item['batch_no']}   |   Qty {item['qty']}")
            lbl = Label(text=text, markup=True,
                        halign="left", valign="middle",
                        font_size=dp(12), size_hint_x=0.82)
            lbl.bind(size=lbl.setter("text_size"))
            row.add_widget(lbl)
            rm = Button(text="X", size_hint_x=0.18, font_size=dp(16),
                        background_color=(0.75, 0.25, 0.25, 1))
            rm.bind(on_release=lambda b, idx=i: self.remove_item(idx))
            row.add_widget(rm)
            self.items_layout.add_widget(row)

    # ---------- WhatsApp ----------
    def open_whatsapp(self, instance):
        date = self.date_field.text.strip()
        ref = self.ref_field.text.strip()
        recv = self.from_field.text.strip() or "-"
        rem = self.remarks_field.text.strip() or "-"

        if not self.items:
            self.status.text = "Add at least one product first."
            self.status.color = (0.9, 0.1, 0.1, 1)
            return

        lines = [
            "Product Receipt",
            f"Ref: {ref}",
            f"Date: {date}",
            f"Received From: {recv}",
            f"Remarks: {rem}",
            "",
            "Items:",
        ]
        total_qty = 0
        for i, item in enumerate(self.items, 1):
            lines.append(
                f"{i}. {item['product']} | Batch {item['batch_no']} | Qty {item['qty']}"
            )
            try:
                total_qty += int(item["qty"])
            except ValueError:
                pass
        lines.append("")
        lines.append(f"Total: {len(self.items)} item(s), {total_qty} units")

        msg = "\n".join(lines)
        url = f"https://wa.me/{MANAGER_WHATSAPP}?text={quote(msg)}"

        try:
            from kivy.utils import platform
            if platform == "android":
                from jnius import autoclass, cast
                Intent = autoclass("android.content.Intent")
                Uri = autoclass("android.net.Uri")
                PythonActivity = autoclass("org.kivy.android.PythonActivity")
                intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                current = cast("android.app.Activity", PythonActivity.mActivity)
                current.startActivity(intent)
            else:
                import webbrowser
                webbrowser.open(url)
        except Exception as e:
            self.status.text = f"Chat error: {e}"

    # ---------- Submit all ----------
    def submit_all(self, instance):
        if not self.items:
            self.status.text = "Nothing to submit. Add items first."
            self.status.color = (0.9, 0.1, 0.1, 1)
            return

        date = self.date_field.text.strip()
        ref = self.ref_field.text.strip() or make_reference()
        recv = self.from_field.text.strip()
        rem = self.remarks_field.text.strip()

        if not date or not recv:
            self.status.text = "Open Session Info and fill Date + Received From."
            self.status.color = (0.9, 0.1, 0.1, 1)
            return

        all_ok = True
        for item in self.items:
            if not try_submit_one(ref, date, recv, rem, item):
                all_ok = False
                break

        if all_ok:
            self.status.text = f"Submitted {len(self.items)} item(s) successfully."
            self.status.color = (0.3, 0.5, 0.3, 1)
            self.clear_form()
        else:
            queue_batch({
                "ref": ref,
                "date": date,
                "received_from": recv,
                "remarks": rem,
                "items": list(self.items),
            })
            if has_internet():
                self.status.text = "Partially failed — saved for retry."
            else:
                self.status.text = f"Saved offline ({len(self.items)} item(s)). Auto-sync."
            self.status.color = (0.9, 0.55, 0.1, 1)
            Clock.schedule_once(lambda dt: self._background_sync(0), 5)
            self.clear_form()

    # ---------- Auto-sync ----------
    def _background_sync(self, dt):
        if not load_queue():
            return
        if not has_internet():
            return
        threading.Thread(target=self._do_sync_in_thread, daemon=True).start()

    def _do_sync_in_thread(self):
        sent = flush_queue()
        if sent > 0:
            Clock.schedule_once(lambda dt: self._on_sync_done(sent), 0)

    def _on_sync_done(self, count):
        self.status.text = f"Auto-synced {count} item(s)."
        self.status.color = (0.3, 0.5, 0.3, 1)

    def sync_queue(self, instance):
        sent = flush_queue()
        if sent > 0:
            self.status.text = f"Synced {sent} item(s)."
        else:
            self.status.text = "Nothing to sync."
        self.status.color = (0.3, 0.5, 0.3, 1)

    # ---------- Clear ----------
    def clear_form(self, instance=None):
        self.items = []
        self.selected_product = ""
        self.prod_btn.text = "Tap to choose"
        self.batch_input.text = ""
        self.qty_input.text = ""
        self.from_field.text = ""
        self.remarks_field.text = ""
        self.date_field.text = datetime.now().strftime("%Y-%m-%d")
        self.ref_field.text = make_reference()
        self.update_session_header()
        self.refresh_items_list()


# ============================================================
# 7. APP
# ============================================================
class ReceiptApp(App):
    def build(self):
        self.title = "Product Receipt"
        return ReceiptForm()


if __name__ == "__main__":
    ReceiptApp().run()
