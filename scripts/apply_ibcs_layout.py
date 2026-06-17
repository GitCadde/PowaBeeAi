#!/usr/bin/env python3
"""Apply IBCS standard layout to C-HPU Power BI report visuals."""

import json
import copy
from pathlib import Path

REPORT_ROOT = Path(__file__).resolve().parent.parent / "CHPUFinal.Report"
PAGES_ROOT = REPORT_ROOT / "definition" / "pages"

# --- Layout tokens (1920x1080) ---
MARGIN = 24
COL_W = 134
GUTTER = 24
CONTENT_TOP = 184
CONTENT_BOTTOM = 1012
CONTENT_H = CONTENT_BOTTOM - CONTENT_TOP
CANVAS_W = 1920
CANVAS_H = 1080

FONT = "'''DIN'', wf_standard-font, helvetica, arial, sans-serif'"
ACCENT = "#5B7D96"
WHITE = "#FFFFFF"
TEXT = "#404040"
FOOTER_GRAY = "#808080"

NAV_BUTTONS = [
    ("📊 Management Summary", "fa54048b8ec7b8263d24"),
    ("📋 Cockpit C-HPU", "8024b360c47454031473"),
    ("📈 Entwicklung VK", "08f710e515284d51e335"),
    ("🔍 Abw.-Analyse VK", "7173cb80c73dedce7e13"),
    ("🔍 Abw.-Analyse DE", "9e4ca7bb00393c391b73"),
    ("🎯 C-HPU Ziele VK", "6a9599d59439bb976e47"),
]
NAV_X = [656, 864, 1072, 1280, 1488, 1696]
NAV_W, NAV_H, NAV_Y = 200, 48, 24

PAGE_SUBTITLES = {
    "fa54048b8ec7b8263d24": "Management Summary",
    "8024b360c47454031473": "C-HPU Cockpit",
    "08f710e515284d51e335": "C-HPU Entwicklung VK",
    "7173cb80c73dedce7e13": "Abweichungsanalyse VK",
    "9e4ca7bb00393c391b73": "Abweichungsanalyse Deutsche Werke – Direkter Bereich",
    "6a9599d59439bb976e47": "C-HPU Ziele",
    "de6f5cf168792de4bb44": "Kostenstelle Detail",
    "c1e2b52e764d2a707ce0": "Werk Detail",
    "61bf829ca2e4db8b2d75": "Ziele Werk",
    "dfcec17766a780add1a9": "Data Dump",
    "50f61a29bab002e9a127": 'Duplikat von "C-HPU Ziele"',
}

MAIN_PAGES = {
    "fa54048b8ec7b8263d24",
    "8024b360c47454031473",
    "08f710e515284d51e335",
    "7173cb80c73dedce7e13",
    "9e4ca7bb00393c391b73",
    "6a9599d59439bb976e47",
}


def col_x(col: int) -> int:
    return MARGIN + col * (COL_W + GUTTER)


def col_width(span: int) -> int:
    return span * COL_W + (span - 1) * GUTTER


def set_pos(visual: dict, x: float, y: float, w: float, h: float, z: int | None = None) -> None:
    p = visual.setdefault("position", {})
    p["x"] = x
    p["y"] = y
    p["width"] = w
    p["height"] = h
    if z is not None:
        p["z"] = z


def get_button_text(v: dict) -> str | None:
    try:
        texts = v["visual"]["objects"]["text"]
        for t in texts:
            props = t.get("properties", {})
            if "text" in props:
                val = props["text"]["expr"]["Literal"]["Value"]
                return val.strip("'")
    except (KeyError, TypeError):
        pass
    return None


def get_textbox_content(v: dict) -> str:
    try:
        paras = v["visual"]["objects"]["general"][0]["properties"]["paragraphs"]
        return " ".join(
            run.get("value", "")
            for p in paras
            for run in p.get("textRuns", [])
        )
    except (KeyError, TypeError, IndexError):
        return ""


def is_logo(v: dict) -> bool:
    return v.get("visual", {}).get("visualType") == "image"


def is_title_textbox(v: dict) -> bool:
    if v.get("visual", {}).get("visualType") != "textbox":
        return False
    return "Insight Factory" in get_textbox_content(v)


def is_confidential_footer(v: dict) -> bool:
    if v.get("visual", {}).get("visualType") != "textbox":
        return False
    return "VERTRAULICH" in get_textbox_content(v)


def is_version_footer(v: dict) -> bool:
    if v.get("visual", {}).get("visualType") != "textbox":
        return False
    return "Version" in get_textbox_content(v)


def is_section_label(v: dict) -> bool:
    if v.get("visual", {}).get("visualType") != "textbox":
        return False
    txt = get_textbox_content(v)
    return txt in ("Wesentliche Entscheidungsbedarfe", "Kontext / Hintergrund")


def is_datenschutz(v: dict) -> bool:
    txt = get_button_text(v)
    return txt == "Datenschutzerklärung" if txt else False


def is_nav_button(v: dict) -> bool:
    txt = get_button_text(v)
    if not txt:
        return False
    return any(txt == label for label, _ in NAV_BUTTONS)


def is_back_button(v: dict) -> bool:
    if v.get("visual", {}).get("visualType") != "actionButton":
        return False
    txt = get_button_text(v)
    if txt:
        return False
    try:
        link = v["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]
        return link.get("type", {}).get("expr", {}).get("Literal", {}).get("Value") == "'Back'"
    except (KeyError, TypeError, IndexError):
        return v["position"].get("y", 999) < 50 and v["position"].get("width", 0) <= 120


def style_nav_button(v: dict, active: bool) -> None:
    vco = v.setdefault("visual", {}).setdefault("visualContainerObjects", {})
    bg = vco.setdefault("background", [{}])[0].setdefault("properties", {})
    border = vco.setdefault("border", [{}])[0].setdefault("properties", {})
    text_objs = v.setdefault("visual", {}).setdefault("objects", {}).setdefault("text", [])
    if len(text_objs) < 2:
        text_objs.append({"properties": {}})
    text_props = text_objs[1].setdefault("properties", {})
    text_props.setdefault("fontFamily", {"expr": {"Literal": {"Value": FONT}}})
    text_props["fontSize"] = {"expr": {"Literal": {"Value": "11D"}}}
    text_props["bold"] = {"expr": {"Literal": {"Value": "true"}}}
    if active:
        bg["show"] = {"expr": {"Literal": {"Value": "true"}}}
        bg["color"] = {"solid": {"color": {"expr": {"Literal": {"Value": f"'{ACCENT}'"}}}}}
        bg["transparency"] = {"expr": {"Literal": {"Value": "0D"}}}
        border["show"] = {"expr": {"Literal": {"Value": "false"}}}
        text_props["fontColor"] = {"solid": {"color": {"expr": {"Literal": {"Value": f"'{WHITE}'"}}}}}
    else:
        bg["show"] = {"expr": {"Literal": {"Value": "false"}}}
        border["show"] = {"expr": {"Literal": {"Value": "true"}}}
        border["color"] = {"solid": {"color": {"expr": {"Literal": {"Value": f"'{ACCENT}'"}}}}}
        border["width"] = {"expr": {"Literal": {"Value": "1D"}}}
        text_props["fontColor"] = {"solid": {"color": {"expr": {"Literal": {"Value": f"'{TEXT}'"}}}}}


def update_title_textbox(v: dict, subtitle: str) -> None:
    v["visual"]["objects"]["general"][0]["properties"]["paragraphs"] = [
        {
            "textRuns": [
                {
                    "value": "Insight Factory – C-HPU-Bericht",
                    "textStyle": {"fontWeight": "bold", "fontSize": "20pt", "fontFamily": "DIN"},
                }
            ]
        },
        {
            "textRuns": [
                {
                    "value": subtitle,
                    "textStyle": {"fontSize": "13pt", "fontFamily": "DIN", "color": ACCENT},
                }
            ]
        },
    ]
    set_pos(v, 104, 8, 520, 80, 1000)


def style_card_visual(v: dict) -> None:
    objs = v.setdefault("visual", {}).setdefault("objects", {})
    value = objs.setdefault("value", [{}])
    for item in value:
        props = item.setdefault("properties", {})
        props["fontSize"] = {"expr": {"Literal": {"Value": "30D"}}}
        props["horizontalAlignment"] = {"expr": {"Literal": {"Value": "'center'"}}}
        props["textWrap"] = {"expr": {"Literal": {"Value": "true"}}}
    label = objs.setdefault("label", [{}])
    for item in label:
        props = item.setdefault("properties", {})
        props["show"] = {"expr": {"Literal": {"Value": "true"}}}
        props["fontSize"] = {"expr": {"Literal": {"Value": "11D"}}}
    fill = objs.setdefault("fillCustom", [{}])
    if len(fill) == 1:
        fill.append({"properties": {}, "selector": {"id": "default"}})
    fill[1].setdefault("properties", {})["fillColor"] = {
        "solid": {"color": {"expr": {"Literal": {"Value": f"'{WHITE}'"}}}}
    }
    shadow = objs.setdefault("shadowCustom", [{}])
    shadow[0].setdefault("properties", {})["show"] = {"expr": {"Literal": {"Value": "true"}}}
    vco = v.setdefault("visual", {}).setdefault("visualContainerObjects", {})
    vco.setdefault("border", [{}])[0].setdefault("properties", {}).update(
        {
            "show": {"expr": {"Literal": {"Value": "true"}}},
            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E0E0E0'"}}}}},
            "radius": {"expr": {"Literal": {"Value": "4D"}}},
        }
    )


def style_chart(v: dict, title: str | None = None) -> None:
    vco = v.setdefault("visual", {}).setdefault("visualContainerObjects", {})
    title_obj = vco.setdefault("title", [{}])[0].setdefault("properties", {})
    if title:
        title_obj["show"] = {"expr": {"Literal": {"Value": "true"}}}
        title_obj["text"] = {"expr": {"Literal": {"Value": f"'{title}'"}}}
        title_obj["fontSize"] = {"expr": {"Literal": {"Value": "12D"}}}
        title_obj["fontColor"] = {"solid": {"color": {"expr": {"Literal": {"Value": f"'{TEXT}'"}}}}}
        title_obj["bold"] = {"expr": {"Literal": {"Value": "true"}}}
    objs = v.setdefault("visual", {}).setdefault("objects", {})
    for axis_key in ("categoryAxis", "valueAxis"):
        if axis_key in objs:
            for item in objs[axis_key]:
                props = item.setdefault("properties", {})
                props["fontSize"] = {"expr": {"Literal": {"Value": "10D"}}}
    if "labels" in objs:
        for item in objs["labels"]:
            item.setdefault("properties", {})["fontSize"] = {"expr": {"Literal": {"Value": "9D"}}}
    vco.setdefault("background", [{}])[0].setdefault("properties", {})["show"] = {
        "expr": {"Literal": {"Value": "true"}}
    }
    vco.setdefault("border", [{}])[0].setdefault("properties", {}).update(
        {
            "show": {"expr": {"Literal": {"Value": "true"}}},
            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E0E0E0'"}}}}},
        }
    )


def style_table(v: dict, title: str | None = None) -> None:
    vco = v.setdefault("visual", {}).setdefault("visualContainerObjects", {})
    if title:
        title_obj = vco.setdefault("title", [{}])[0].setdefault("properties", {})
        title_obj["show"] = {"expr": {"Literal": {"Value": "true"}}}
        title_obj["text"] = {"expr": {"Literal": {"Value": f"'{title}'"}}}
        title_obj["fontSize"] = {"expr": {"Literal": {"Value": "12D"}}}
        title_obj["bold"] = {"expr": {"Literal": {"Value": "true"}}}
    vco.setdefault("border", [{}])[0].setdefault("properties", {}).update(
        {
            "show": {"expr": {"Literal": {"Value": "true"}}},
            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E0E0E0'"}}}}},
        }
    )


def style_slicer(v: dict) -> None:
    vco = v.setdefault("visual", {}).setdefault("visualContainerObjects", {})
    vco.setdefault("background", [{}])[0].setdefault("properties", {}).update(
        {
            "show": {"expr": {"Literal": {"Value": "true"}}},
            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#F5F8FA'"}}}}},
            "transparency": {"expr": {"Literal": {"Value": "0D"}}},
        }
    )
    vco.setdefault("border", [{}])[0].setdefault("properties", {}).update(
        {
            "show": {"expr": {"Literal": {"Value": "true"}}},
            "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#E0E0E0'"}}}}},
            "radius": {"expr": {"Literal": {"Value": "4D"}}},
        }
    )


def apply_chrome(page_id: str, visuals: list[dict]) -> None:
    subtitle = PAGE_SUBTITLES.get(page_id, "")
    has_nav = page_id in MAIN_PAGES
    nav_index = {label: i for i, (label, pid) in enumerate(NAV_BUTTONS)}

    for v in visuals:
        if is_logo(v):
            set_pos(v, 24, 16, 64, 64, 9000)
        elif is_title_textbox(v):
            update_title_textbox(v, subtitle)
        elif is_confidential_footer(v):
            set_pos(v, 24, 1032, 360, 36, 500)
            v["visual"]["objects"]["general"][0]["properties"]["paragraphs"] = [
                {
                    "textRuns": [
                        {
                            "value": "KSU 0.2 – VERTRAULICH",
                            "textStyle": {"fontSize": "9pt", "color": FOOTER_GRAY, "fontFamily": "DIN"},
                        }
                    ]
                }
            ]
        elif is_version_footer(v):
            set_pos(v, 1496, 1032, 400, 36, 500)
            v["visual"]["objects"]["general"][0]["properties"]["paragraphs"] = [
                {
                    "textRuns": [
                        {
                            "value": "Version 0.9 | Stand 08.06.2026",
                            "textStyle": {
                                "fontSize": "9pt",
                                "color": FOOTER_GRAY,
                                "fontFamily": "DIN",
                                "textAlign": "right",
                            },
                        }
                    ]
                }
            ]
        elif is_datenschutz(v):
            set_pos(v, 400, 1024, 288, 44, 500)
        elif is_nav_button(v) and has_nav:
            txt = get_button_text(v)
            idx = nav_index.get(txt, 0)
            set_pos(v, NAV_X[idx], NAV_Y, NAV_W, NAV_H, 8000 + idx)
            style_nav_button(v, NAV_BUTTONS[idx][1] == page_id)
        elif is_back_button(v):
            set_pos(v, 24, 24, 100, 48, 8500)


def place_slicers_right(visuals: list[dict], count: int | None = None) -> None:
    slicers = [v for v in visuals if v.get("visual", {}).get("visualType") == "slicer"]
    if count is not None:
        slicers = slicers[:count]
    sw, sh, sy = 220, 56, 112
    for i, v in enumerate(reversed(slicers)):
        x = CANVAS_W - MARGIN - sw - i * (sw + 8)
        set_pos(v, x, sy, sw, sh, 7000 + i)
        style_slicer(v)


def ibcs_color_for_measure(name: str) -> str:
    upper = name.upper()
    if "SOLL" in upper or "PLAN" in upper or "VSI" in upper and "IST" not in upper:
        return "#BCD5E3"
    if "IST D" in upper or "IST DI" in upper:
        return "#5B7D96"
    if "IST I" in upper or " IST" in upper:
        return "#404040"
    if "DELTA" in upper or "ABW" in upper:
        return "#ED7373"
    if "TREND" in upper:
        return "#8FB8D0"
    return "#5B7D96"


def apply_ibcs_chart_colors(v: dict) -> None:
    vt = v.get("visual", {}).get("visualType", "")
    if vt not in (
        "lineStackedColumnComboChart",
        "lineClusteredColumnComboChart",
        "columnChart",
        "lineChart",
        "barChart",
    ):
        return
    query = v.get("visual", {}).get("query", {}).get("queryState", {})
    projections = []
    for bucket in ("Y", "Y2", "Category", "Series"):
        if bucket in query:
            projections.extend(query[bucket].get("projections", []))
    objs = v.setdefault("visual", {}).setdefault("objects", {})
    data_points = []
    line_styles = list(objs.get("lineStyles", []))
    for proj in projections:
        ref = proj.get("queryRef") or proj.get("nativeQueryRef")
        if not ref:
            continue
        measure_name = ref.split(".")[-1] if "." in ref else ref
        color = ibcs_color_for_measure(measure_name)
        data_points.append(
            {
                "properties": {
                    "fill": {
                        "solid": {
                            "color": {"expr": {"Literal": {"Value": f"'{color}'"}}}
                        }
                    }
                },
                "selector": {"metadata": ref},
            }
        )
        if "Soll" in measure_name or "PL" in measure_name:
            line_styles.append(
                {
                    "properties": {
                        "lineStyle": {"expr": {"Literal": {"Value": "'dashed'"}}},
                        "lineChartLineStyle": {"expr": {"Literal": {"Value": "'dashed'"}}},
                    },
                    "selector": {"metadata": ref},
                }
            )
    if data_points:
        objs["dataPoint"] = data_points
    if line_styles:
        objs["lineStyles"] = line_styles
    objs["legend"] = [
        {
            "properties": {
                "show": {"expr": {"Literal": {"Value": "true"}}},
                "position": {"expr": {"Literal": {"Value": "'Top'"}}},
                "fontSize": {"expr": {"Literal": {"Value": "10D"}}},
            }
        }
    ]


def style_section_labels(v: dict) -> None:
    txt = get_textbox_content(v)
    mapping = {
        "Wesentliche Entscheidungsbedarfe": "⚠️ Wesentliche Entscheidungsbedarfe",
        "Kontext / Hintergrund": "ℹ️ Kontext / Hintergrund",
    }
    if txt not in mapping:
        return
    v["visual"]["objects"]["general"][0]["properties"]["paragraphs"] = [
        {
            "textRuns": [
                {
                    "value": mapping[txt],
                    "textStyle": {"fontWeight": "bold", "fontSize": "12pt", "fontFamily": "DIN", "color": ACCENT},
                }
            ]
        }
    ]


def apply_styling_pass(v: dict) -> None:
    vt = v.get("visual", {}).get("visualType")
    if vt == "cardVisual":
        style_card_visual(v)
    elif vt in ("pivotTable", "tableEx"):
        pass  # title set in layout
    elif vt in (
        "lineStackedColumnComboChart",
        "lineClusteredColumnComboChart",
        "columnChart",
        "lineChart",
        "barChart",
    ):
        apply_ibcs_chart_colors(v)
    elif vt == "slicer":
        style_slicer(v)
    elif is_section_label(v):
        style_section_labels(v)


def apply_page_layout(page_id: str, visuals: dict[str, dict]) -> None:
    vlist = list(visuals.values())
    apply_chrome(page_id, vlist)

    full_w = col_width(12)
    full_x = col_x(0)

    if page_id == "fa54048b8ec7b8263d24":
        place_slicers_right(vlist, 2)
        for v in vlist:
            name = v["name"]
            if name == "5be46d2bb492384390b0":
                set_pos(v, full_x, CONTENT_TOP, full_w, 200, 3000)
                style_card_visual(v)
            elif name == "66108d4a3bba4a09a30a":
                set_pos(v, full_x, CONTENT_TOP + 216, full_w, 360, 2000)
            elif name == "3cac658ca0060ad02c51":
                set_pos(v, full_x, CONTENT_TOP + 216, full_w, 360, 2000)
            elif name == "f3ff9d05bab97a2002d4":
                set_pos(v, full_x, CONTENT_TOP + 592, full_w, 200, 3000)
                style_card_visual(v)
            elif name == "9d636db421ca849d980c":
                set_pos(v, full_x + 8, CONTENT_TOP + 224, 400, 32, 4000)
            elif name == "c1631e0371c2e6696dbd":
                set_pos(v, full_x + 8, CONTENT_TOP + 600, 400, 32, 4000)

    elif page_id == "8024b360c47454031473":
        place_slicers_right(vlist, 3)
        for v in vlist:
            if v.get("visual", {}).get("visualType") == "pivotTable":
                set_pos(v, full_x, CONTENT_TOP, full_w, CONTENT_H, 2000)
                style_table(v, "📋 C-HPU Cockpit Übersicht")

    elif page_id == "08f710e515284d51e335":
        chart_top = [v for v in vlist if v["name"] == "613feb6a38b031cc8805"]
        chart_bot = [v for v in vlist if v["name"] == "2cefd67f06eb70ea1302"]
        cards = [v for v in vlist if v.get("visual", {}).get("visualType") == "cardVisual"]
        shapes = [v for v in vlist if v.get("visual", {}).get("visualType") == "shape"]
        werk_slicer = [v for v in vlist if v["name"] == "71397121870cee03b340"]
        other_slicers = [
            v for v in vlist if v.get("visual", {}).get("visualType") == "slicer" and v["name"] != "71397121870cee03b340"
        ]

        if chart_top:
            set_pos(chart_top[0], col_x(0), CONTENT_TOP, col_width(8), 480, 2000)
            style_chart(chart_top[0], "📈 C-HPU Entwicklung VK – Wochenverlauf")
        if chart_bot:
            set_pos(chart_bot[0], col_x(0), CONTENT_TOP + 504, col_width(8), CONTENT_H - 504, 2000)
            style_chart(chart_bot[0], "📊 Detailverlauf nach Kategorie")
        for i, v in enumerate(cards[:8]):
            row, col = divmod(i, 2)
            cx = col_x(8) + col * (col_width(2) + GUTTER)
            cy = CONTENT_TOP + row * (120 + GUTTER)
            set_pos(v, cx, cy, col_width(2), 120, 3000 + i)
            style_card_visual(v)
        for s in shapes:
            set_pos(s, col_x(8), CONTENT_TOP, col_width(4), CONTENT_H, 1000)
        if werk_slicer:
            set_pos(werk_slicer[0], col_x(8), 112, col_width(4), 56, 7000)
            style_slicer(werk_slicer[0])
        for i, v in enumerate(reversed(other_slicers[:2])):
            x = CANVAS_W - MARGIN - 220 - i * 228
            set_pos(v, x, 112, 220, 56, 7100 + i)
            style_slicer(v)

    elif page_id in ("7173cb80c73dedce7e13", "9e4ca7bb00393c391b73"):
        place_slicers_right(vlist, 2)
        title = "🔍 Abweichungsanalyse VK" if page_id == "7173cb80c73dedce7e13" else "🔍 Abweichungsanalyse Deutsche Werke"
        for v in vlist:
            if v.get("visual", {}).get("visualType") == "pivotTable":
                set_pos(v, full_x, CONTENT_TOP, full_w, CONTENT_H, 2000)
                style_table(v, title)

    elif page_id == "6a9599d59439bb976e47":
        place_slicers_right(vlist, 2)
        for v in vlist:
            if v.get("visual", {}).get("visualType") == "pivotTable":
                set_pos(v, col_x(1), CONTENT_TOP, col_width(10), CONTENT_H, 2000)
                style_table(v, "🎯 C-HPU Ziele VK")

    elif page_id == "de6f5cf168792de4bb44":
        place_slicers_right(vlist, 2)
        cards = [v for v in vlist if v.get("visual", {}).get("visualType") == "cardVisual"]
        card_w = col_width(3)
        for i, v in enumerate(cards[:4]):
            set_pos(v, col_x(i * 3), CONTENT_TOP, card_w, 144, 3000 + i)
            style_card_visual(v)
        for v in vlist:
            vt = v.get("visual", {}).get("visualType")
            if vt == "lineStackedColumnComboChart":
                set_pos(v, col_x(0), CONTENT_TOP + 168, col_width(6), 400, 2000)
                style_chart(v, "📈 Kostenstellenverlauf")
            elif vt == "tableEx":
                set_pos(v, col_x(6), CONTENT_TOP + 168, col_width(6), 400, 2000)
                style_table(v, "📋 Kostendetails")

    elif page_id == "c1e2b52e764d2a707ce0":
        place_slicers_right(vlist, 2)
        cards = [v for v in vlist if v.get("visual", {}).get("visualType") == "cardVisual"]
        card_w = col_width(2)
        for i, v in enumerate(cards[:5]):
            if i < 4:
                set_pos(v, col_x(i * 3), CONTENT_TOP, col_width(3), 144, 3000 + i)
            else:
                set_pos(v, col_x(0), CONTENT_TOP + 168, col_width(12), 128, 3000 + i)
            style_card_visual(v)
        for v in vlist:
            if v.get("visual", {}).get("visualType") == "pivotTable":
                set_pos(v, col_x(0), CONTENT_TOP + 312, col_width(12), CONTENT_H - 312, 2000)
                style_table(v, "🏭 Werk Detail – Übersicht")

    elif page_id == "61bf829ca2e4db8b2d75":
        place_slicers_right(vlist, 2)
        for v in vlist:
            vt = v.get("visual", {}).get("visualType")
            if vt == "cardVisual":
                set_pos(v, col_x(0), CONTENT_TOP, col_width(12), 160, 3000)
                style_card_visual(v)
            elif vt == "pivotTable":
                set_pos(v, col_x(0), CONTENT_TOP + 184, col_width(12), CONTENT_H - 184, 2000)
                style_table(v, "🎯 Ziele Werk")

    elif page_id == "dfcec17766a780add1a9":
        slicers = [v for v in vlist if v.get("visual", {}).get("visualType") == "slicer"]
        for i, v in enumerate(slicers[:2]):
            set_pos(v, col_x(0), CONTENT_TOP + i * 160, col_width(3), 144, 7000 + i)
            style_slicer(v)
        for v in vlist:
            if v.get("visual", {}).get("visualType") == "tableEx":
                set_pos(v, col_x(3), CONTENT_TOP, col_width(9), CONTENT_H, 2000)
                style_table(v, "📋 Data Dump")

    elif page_id == "50f61a29bab002e9a127":
        for v in vlist:
            if v.get("visual", {}).get("visualType") == "pivotTable":
                set_pos(v, col_x(0), CONTENT_TOP, col_width(12), CONTENT_H, 2000)
                style_table(v, "🎯 C-HPU Ziele (Duplikat)")


def update_page_json(page_dir: Path) -> None:
    page_file = page_dir / "page.json"
    data = json.loads(page_file.read_text(encoding="utf-8"))
    data["displayOption"] = "FitToPage"
    data["height"] = 1080
    data["width"] = 1920
    page_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def process_page(page_dir: Path) -> int:
    page_id = page_dir.name
    visuals_dir = page_dir / "visuals"
    if not visuals_dir.exists():
        return 0
    count = 0
    visuals: dict[str, dict] = {}
    for vf in visuals_dir.glob("*/visual.json"):
        data = json.loads(vf.read_text(encoding="utf-8"))
        visuals[data["name"]] = data
        count += 1
    apply_page_layout(page_id, visuals)
    for v in visuals.values():
        apply_styling_pass(v)
    for vf in visuals_dir.glob("*/visual.json"):
        name = vf.parent.name
        vf.write_text(json.dumps(visuals[name], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    update_page_json(page_dir)
    return count


def validate_geometry(page_dir: Path) -> list[str]:
    issues = []
    for vf in (page_dir / "visuals").glob("*/visual.json"):
        v = json.loads(vf.read_text(encoding="utf-8"))
        p = v.get("position", {})
        x, y, w, h = p.get("x", 0), p.get("y", 0), p.get("width", 0), p.get("height", 0)
        if x + w > CANVAS_W + 1 or y + h > CANVAS_H + 1 or x < -10 or y < -10:
            issues.append(f"{page_dir.name}/{v['name']}: out of bounds ({x},{y},{w},{h})")
    return issues


def main() -> None:
    total = 0
    all_issues = []
    for page_dir in sorted(PAGES_ROOT.iterdir()):
        if not page_dir.is_dir() or page_dir.name == "pages.json":
            continue
        n = process_page(page_dir)
        total += n
        all_issues.extend(validate_geometry(page_dir))
        print(f"Processed {page_dir.name}: {n} visuals")
    print(f"\nTotal: {total} visuals updated")
    if all_issues:
        print("Geometry warnings:")
        for i in all_issues:
            print(f"  - {i}")
    else:
        print("All visuals within canvas bounds.")


if __name__ == "__main__":
    main()
