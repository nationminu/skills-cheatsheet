#!/usr/bin/env python3
"""논리 구성도 생성기 — shared/diagram/ARCH-DIAGRAM.md 디자인 표준 + 내용 YAML → SVG

디자인(위치·크기·색·선·글자)은 이 스크립트가 표준대로 계산하고,
내용(계층 이름·노드·칩·연결선)은 YAML로 받는다. 양식: shared/diagram/arch-diagram-template.yaml

사용:
  python3 scripts/arch-diagram.py 내용.yaml --svg 구성도.svg                # 단독 SVG (아이콘은 data-icon 참조)
  python3 scripts/arch-diagram.py 내용.yaml --svg 미리보기.svg --icons-dir {ppt-master}/templates/icons
                                                                             # 아이콘을 넣은 미리보기
  python3 scripts/arch-diagram.py 내용.yaml --fragment                        # 장표용 조각(defs·본문) → stdout
  python3 scripts/arch-diagram.py 내용.yaml --check                           # 점검 결과만

장표 반영: --fragment 출력의 defs를 장표 <defs>에, 본문을 표준 6.5 내용 영역(⑤) 자리에 넣음 (장표 파일은 작성자가 편집)
점검: 칸 중복·노드 관통·글자 넘침(추정)·영역 밖 — 오류가 있으면 종료 코드 1
"""
import argparse
import os
import re
import sys

import yaml

# ── 디자인 토큰 (ARCH-DIAGRAM.md 2~6장) ─────────────────────────────
NAVY, CAPTION, BORDER, TEXT = "#0B1F3A", "#5B6577", "#D5DBE3", "#222222"
CAT = {  # 분류: (색, 기본 아이콘, 기본 분류 라벨)
    "external": ("#5B6577", "users", ""),
    "network": ("#0E7C86", "load-balancer", "네트워크"),
    "infra": ("#546E7A", "world-www", "필수 인프라"),
    "security": ("#6B46C1", "shield-lock", "보안"),
    "compute": ("#0B1F3A", "server", "컴퓨팅"),
    "control": ("#0B1F3A", "server-cog", "컨트롤 플레인"),
    "application": ("#1F6FEB", "apps", "애플리케이션"),
    "data": ("#B7791F", "database", "데이터"),
    "storage": ("#8C5A2B", "folders", "스토리지"),
    "ops": ("#2F855A", "activity", "운영"),
    "cicd": ("#3B4BB5", "rocket", "CI/CD"),
}
CHIP_TINT = {"application": ("#E8F0FE", "#1F6FEB", True), "ops": ("#E6F4EA", "#2F855A", False)}
EDGE = {  # 색, 굵기, 점선, 범례
    "service": ("#1F6FEB", 2, None, "서비스 흐름"),
    "control": ("#8A94A6", 1.5, None, "관리 접속·제어"),
    "data": ("#5B6577", 2, None, "데이터"),
    "deploy": ("#3B4BB5", 2, None, "배포"),
    "monitor": ("#2F855A", 1.5, "4,3", "수집·모니터링"),
}
NET = {"service": ("#E3F2F3", "#0E7C86"), "internal": ("#E8EEF7", "#3D5A80"), "mgmt": ("#F3EEF8", "#6B46C1"), "dmz": ("#FDF3E3", "#B7791F")}
FS_NAME, FS_SMALL = 13.33, 11
RATE = {FS_NAME: (7.5, 14.5), FS_SMALL: (9.09, 17.5)}  # 글자 폭 추정 (chars / 100px: 한글, 그 밖)


def tw(text, size, bold=False):
    cjk = sum(1 for ch in str(text) if ord(ch) > 0x2E80)
    c, l = RATE[size]
    return (cjk / c + (len(str(text)) - cjk) / l) * 100 * (1.04 if bold else 1.0)


def f(v):
    return f"{round(v, 1):g}"


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Diagram:
    def __init__(self, spec):
        self.s = spec
        b = spec.get("box", {})
        self.X, self.Y = b.get("x", 57.6), b.get("y", 180)
        self.W, self.H = b.get("w", 1164.8), b.get("h", 463)
        self.err, self.warn = [], []
        self.catalog = spec.get("services", {})
        self.nodes = {}
        self.out = []

    # ── 배치 ────────────────────────────────────────────────
    def layout(self):
        s, X, Y = self.s, self.X, self.Y
        right = s.get("right")
        R = X + self.W
        self.left_x = X
        self.actor_x, self.actor_w = X + 12, 80
        self.lnode_x, self.lnode_w = X + 128, 144
        self.left_r = X + 284
        self.box_x = X + 296
        self.right_x = R - 144 if right else None
        self.box_r = (R - 156) if right else R
        self.box_y, self.box_b = Y + 31, Y + 432
        self.row_top, self.row_bot = Y + 60, Y + 410
        cols = s["main"]["columns"]
        nrow = s["main"].get("rows", 3)
        inner_x, inner_r = self.box_x + 14, self.box_r - 14
        wsum = sum(c.get("width", 1) for c in cols)
        avail = inner_r - inner_x - 16 * (len(cols) - 1)
        self.cols, cx = {}, inner_x
        for c in cols:
            w = avail * c.get("width", 1) / wsum
            self.cols[c["id"]] = (cx, w)
            cx += w + 16
        self.rh = (self.row_bot - self.row_top - 16 * (nrow - 1)) / nrow
        self.rowy = [self.row_top + i * (self.rh + 16) for i in range(nrow)]
        self.rowc = [y + self.rh / 2 for y in self.rowy]
        cells = {}
        for n in s["main"].get("nodes", []):
            x, w = self.cols[n["col"]]
            r0, r1 = (n["rows"] if "rows" in n else (n["row"], n["row"]))
            y = self.rowy[r0]
            h = self.rowy[r1] + self.rh - y
            self.add(n, x, y, w, h, "main")
            for r in range(r0, r1 + 1):
                k = (n["col"], r)
                if k in cells:
                    self.err.append(f"칸 중복: {cells[k]} / {n['id']}")
                cells[k] = n["id"]
        for n in s.get("left", {}).get("actors", []):
            c = self.center(n)
            self.add(n, self.actor_x, c - 40, self.actor_w, 80, "actor")
        for n in s.get("left", {}).get("nodes", []):
            h = self.side_h(n)
            self.add(n, self.lnode_x, self.center(n) - h / 2, self.lnode_w, h, "side")
        if right:
            for n in right.get("nodes", []):
                h = self.side_h(n)
                self.add(n, self.right_x + 12, self.center(n) - h / 2, 120, h, "side")

    def center(self, n):
        r = n.get("rows", [n.get("row", 0)] * 2)
        if isinstance(r, (int, float)):
            r = [r, r]
        lo, hi = r
        def c(v):
            i = int(v)
            fr = v - i
            if i >= len(self.rowc) - 1:
                return self.rowc[-1]
            return self.rowc[i] + (self.rowc[i + 1] - self.rowc[i]) * fr
        return (c(lo) + c(hi)) / 2

    def side_h(self, n, base=80):
        h = base if not n.get("spec") or not n.get("sub") else base + 16
        if n.get("chips"):
            h += 23 * ((len(n["chips"]) + 1) // 2) + 6
        return h

    def add(self, n, x, y, w, h, kind):
        n = dict(n)
        n.update(x=x, y=y, w=w, h=h, kind=kind, cx=x + w / 2, cy=y + h / 2, r=x + w, b=y + h)
        if n["id"] in self.nodes:
            self.err.append(f"id 중복: {n['id']}")
        self.nodes[n["id"]] = n
        if y < self.row_top - 30 or y + h > self.Y + self.H - 30:
            self.err.append(f"{n['id']}: 세로 범위 밖 (행 수·높이 조정)")

    # ── 연결선 ──────────────────────────────────────────────
    def xlanes(self):
        lanes = [(self.actor_x, self.actor_x + self.actor_w), (self.lnode_x, self.lnode_x + self.lnode_w)]
        lanes += sorted((x, x + w) for x, w in self.cols.values())
        if self.right_x:
            lanes.append((self.right_x + 12, self.right_x + 132))
        return lanes

    def channel_after(self, xr):
        lanes = self.xlanes()
        for i, (a, b) in enumerate(lanes[:-1]):
            if abs(b - xr) < 1:
                return (b + lanes[i + 1][0]) / 2
        return xr + 8

    def channel_before(self, xl):
        lanes = self.xlanes()
        for i, (a, b) in enumerate(lanes[1:], 1):
            if abs(a - xl) < 1:
                return (lanes[i - 1][1] + a) / 2
        return xl - 8

    def hits(self, x1, x2, y, skip):
        lo, hi = sorted((x1, x2))
        for n in self.nodes.values():
            if n["id"] in skip:
                continue
            if n["y"] - 2 < y < n["b"] + 2 and lo < n["r"] - 1 and hi > n["x"] + 1:
                return n["id"]
        return None

    def gap_y(self, near):
        gaps = [self.rowy[i] + self.rh + 8 for i in range(len(self.rowy) - 1)]
        return min(gaps, key=lambda g: abs(g - near)) if gaps else near

    def port(self, n, side, other_y, straight):
        if straight:
            return n["cy"]
        k = 0.82 if other_y > n["cy"] else 0.18
        return n["y"] + n["h"] * k

    def route_to(self, x0, y0, t, skip):
        """(x0,y0)에서 t의 왼쪽(또는 아래/위)으로 들어가는 직각 경로"""
        if not self.hits(x0, t["x"], t["cy"], skip) and abs(y0 - t["cy"]) < 0.5:
            return [(x0, y0), (t["x"] - 1, t["cy"])]
        cx = self.channel_before(t["x"]) if t["x"] > x0 else self.channel_after(t["r"])
        tx = t["x"] - 1 if t["x"] > x0 else t["r"] + 1
        if not self.hits(cx, tx, t["cy"], skip) and not self.hits(x0, cx, y0, skip):
            return [(x0, y0), (cx, y0), (cx, t["cy"]), (tx, t["cy"])]
        gy = self.gap_y(t["cy"])
        ty = t["b"] + 1 if gy > t["cy"] else t["y"] - 1
        return [(x0, y0), (x0, gy), (t["cx"], gy), (t["cx"], ty)] if abs(x0 - t["cx"]) > 1 else [(x0, y0), (x0, ty)]

    def route(self):
        self.paths = []
        for e in self.s.get("edges", []):
            typ = e.get("type", "service")
            srcs = e["from"] if isinstance(e["from"], list) else [e["from"]]
            dsts = e["to"] if isinstance(e["to"], list) else [e["to"]]
            for sid in srcs + dsts:
                if sid not in self.nodes:
                    self.err.append(f"연결선 대상 없음: {sid}")
                    return
            S = [self.nodes[i] for i in srcs]
            T = [self.nodes[i] for i in dsts]
            skip = set(srcs + dsts)
            leftward = T[0]["x"] < S[0]["x"]
            if len(S) == 1 and len(T) == 1:
                a, t = S[0], T[0]
                if leftward:
                    y = t["cy"] if a["y"] <= t["cy"] <= a["b"] else a["cy"]
                    if t["y"] <= y <= t["b"] and not self.hits(t["r"], a["x"], y, skip):
                        pts = [(a["x"], y), (t["r"] + 1, y)]
                    else:
                        cx = self.channel_before(a["x"])
                        pts = [(a["x"], y), (cx, y), (cx, t["cy"]), (t["r"] + 1, t["cy"])]
                elif a["y"] <= t["cy"] <= a["b"] and not self.hits(a["r"], t["x"], t["cy"], skip):
                    pts = [(a["r"], t["cy"]), (t["x"] - 1, t["cy"])]
                elif t["y"] <= a["cy"] <= t["b"] and not self.hits(a["r"], t["x"], a["cy"], skip):
                    pts = [(a["r"], a["cy"]), (t["x"] - 1, a["cy"])]
                else:
                    y0 = self.port(a, "r", t["cy"], False) if a["kind"] == "main" else a["cy"]
                    pts = self.route_to(a["r"], y0, t, skip)
                self.paths.append((typ, [pts], e.get("label")))
            elif len(S) == 1:  # 분기
                a = S[0]
                cx = self.channel_after(a["r"])
                segs = [[(a["r"], a["cy"]), (cx, a["cy"])]]
                for t in T:
                    segs.append([(cx, a["cy"]), (cx, t["cy"]), (t["x"] - 1, t["cy"])])
                self.paths.append((typ, segs, e.get("label")))
            else:  # 합류
                t = T[0]
                cx = self.channel_after(S[0]["r"])
                my = self.gap_y(sum(a["cy"] for a in S) / len(S)) if any(a["kind"] == "main" for a in S) else t["cy"]
                ys = [self.port(a, "r", my, False) for a in S]
                segs = [[(a["r"], y), (cx, y), (cx, my)] for a, y in zip(S, ys)]
                segs.append(self.route_to(cx, my, t, skip))
                self.paths.append((typ, segs, e.get("label"), "merge"))
        # 관통 점검
        for p in self.paths:
            for seg in p[1]:
                for (x1, y1), (x2, y2) in zip(seg, seg[1:]):
                    if abs(y1 - y2) < 0.5:
                        h = self.hits(x1, x2, y1, set())
                        if h and not any(abs(x - self.nodes[h]["x"]) < 2 or abs(x - self.nodes[h]["r"]) < 2 for x in (x1, x2)):
                            self.err.append(f"선이 노드 관통: {h}")

    # ── 그리기 ──────────────────────────────────────────────
    def emit(self, line):
        self.out.append(line)

    def draw(self):
        s, X, Y = self.s, self.X, self.Y
        P = s.get("prefix", "arch")
        e = self.emit
        # 영역
        e(f'<rect id="{P}-main" data-pptx-role="decoration" x="{f(self.box_x)}" y="{f(self.box_y)}" width="{f(self.box_r - self.box_x)}" height="{f(self.box_b - self.box_y)}" rx="8" fill="#FAFBFD" stroke="#7F97B8" stroke-width="1.33" stroke-dasharray="6,4"/>')
        nets = s["main"].get("networks", [])
        zones = []
        for z in nets:
            c0, w0 = self.cols[z["cols"][0]]
            c1, w1 = self.cols[z["cols"][-1]]
            zones.append([z, c0 - 8, c1 + w1 + 8])
        zones.sort(key=lambda t: t[1])
        for i in range(len(zones) - 1):
            if zones[i][2] > zones[i + 1][1] - 4:
                mid = (zones[i][2] + zones[i + 1][1]) / 2
                zones[i][2], zones[i + 1][1] = mid - 2, mid + 2
        for z, zx, zr in zones:
            zx = max(zx, self.box_x + 6)
            zr = min(zr, self.box_r - 6)
            fill, col = NET.get(z.get("kind", "internal"), NET["internal"])
            e(f'<rect id="{P}-net-{z["id"]}" data-pptx-role="decoration" x="{f(zx)}" y="{f(self.box_y + 5)}" width="{f(zr - zx)}" height="{f(self.box_b - self.box_y - 11)}" rx="6" fill="{fill}"/>')
        rules = [(self.left_x, self.left_r), (self.box_x, self.box_r)] + ([(self.right_x, X + self.W)] if self.right_x else [])
        e(f'<g id="{P}-tier-rules" data-pptx-role="decoration" data-pptx-bounds="{f(X)} {f(Y + 25)} {f(self.W)} 2" fill="#C5CCD6">')
        for a, b in rules:
            e(f'  <rect x="{f(a)}" y="{f(Y + 25)}" width="{f(b - a)}" height="1"/>')
        e("</g>")
        e(f'<g id="{P}-tier-labels" data-pptx-role="header" data-pptx-bounds="{f(X)} {f(Y + 2)} {f(self.W)} 22" font-size="{FS_SMALL}" font-weight="bold" fill="{CAPTION}">')
        e(f'  <text x="{f(self.left_x)}" y="{f(Y + 18)}">{esc(s.get("left", {}).get("label", "사용자"))}</text>')
        e(f'  <text x="{f(self.box_x)}" y="{f(Y + 18)}">{esc(s["main"]["label"])}</text>')
        if s["main"].get("caption"):
            e(f'  <text x="{f(self.box_r)}" y="{f(Y + 18)}" font-weight="normal" text-anchor="end">{esc(s["main"]["caption"])}</text>')
        if self.right_x:
            e(f'  <text x="{f(self.right_x)}" y="{f(Y + 18)}">{esc(s["right"]["label"])}</text>')
        e("</g>")
        if zones:
            e(f'<g id="{P}-net-labels" data-pptx-bounds="{f(self.box_x + 14)} {f(self.box_y + 7)} {f(self.box_r - self.box_x - 28)} 16" font-size="{FS_SMALL}" font-weight="bold">')
            for z, zx, zr in zones:
                fill, col = NET.get(z.get("kind", "internal"), NET["internal"])
                lx = max(zx, self.box_x + 6) + 8
                e(f'  <rect x="{f(lx)}" y="{f(self.box_y + 10)}" width="8" height="8" rx="2" fill="{col}"/>')
                e(f'  <text x="{f(lx + 14)}" y="{f(self.box_y + 18)}" fill="{col}">{esc(z["label"])}</text>')
                if tw(z["label"], FS_SMALL, True) + 22 > zr - zx:
                    self.warn.append(f"네트워크 라벨 폭 초과: {z['label']}")
            e("</g>")
        # 연결선
        markers = set()
        e(f'<g id="{P}-connectors" data-pptx-role="decoration" data-pptx-bounds="{f(X)} {f(Y + 31)} {f(self.W)} {f(self.H - 62)}" fill="none">')
        labels = []
        for p in self.paths:
            typ, segs, label = p[0], p[1], p[2]
            col, wd, dash, _ = EDGE[typ]
            ds = f' stroke-dasharray="{dash}"' if dash else ""
            merge = len(p) > 3
            for i, seg in enumerate(segs):
                d = "M" + " ".join(("H" + f(b[0])) if abs(a[1] - b[1]) < 0.5 else ("V" + f(b[1])) for a, b in zip(seg, seg[1:]))
                d = f"M{f(seg[0][0])} {f(seg[0][1])} " + d[1:]
                last = (not merge and (len(segs) == 1 or i > 0)) or (merge and i == len(segs) - 1)
                mk = f' marker-end="url(#{P}-a-{typ})"' if last else ""
                if last:
                    markers.add(typ)
                e(f'  <path d="{d}" stroke="{col}" stroke-width="{wd}"{ds}{mk}/>')
            if label:
                seg = max((s2 for s2 in segs), key=lambda s2: max(abs(a[0] - b[0]) for a, b in zip(s2, s2[1:])))
                a, b = max(zip(seg, seg[1:]), key=lambda ab: abs(ab[0][0] - ab[1][0]))
                sx = min(a[0], b[0])
                if sx < self.box_x < max(a[0], b[0]):
                    sx = self.box_x + 10
                labels.append((sx + 8, a[1] - 8, label, col))
        e("</g>")
        for i, (lx, ly, lab, col) in enumerate(labels):
            e(f'<g id="{P}-edge-label-{i + 1}" data-pptx-bounds="{f(lx - 2)} {f(ly - 12)} {f(tw(lab, FS_SMALL, True) + 4)} 16">')
            e(f'  <text x="{f(lx)}" y="{f(ly)}" font-size="{FS_SMALL}" font-weight="bold" fill="{col}">{esc(lab)}</text>')
            e("</g>")
        self.markers = markers
        # 노드
        for n in self.nodes.values():
            self.tile(n, P)
        # 범례
        used = [t for t in EDGE if any(p[0] == t for p in self.paths)]
        kinds = []
        if any(n.get("common") for n in self.nodes.values()):
            kinds.append(("업무", "#E8F0FE", None))
        if any(n.get("services") for n in self.nodes.values()):
            kinds.append(("플랫폼 서비스", "#FFFFFF", BORDER))
        items = [(EDGE[t][3], 26 + 6 + tw(EDGE[t][3], FS_SMALL) + 18) for t in used] + [(k[0], 12 + 6 + tw(k[0], FS_SMALL) + 18) for k in kinds]
        total = sum(w for _, w in items)
        lx, ly = X + self.W - total, Y + 455
        e(f'<g id="{P}-legend" data-pptx-bounds="{f(lx)} {f(ly - 13)} {f(total)} 18" font-size="{FS_SMALL}" fill="{CAPTION}">')
        for t in used:
            col, wd, dash, lab = EDGE[t]
            ds = f' stroke-dasharray="{dash}"' if dash else ""
            e(f'  <line x1="{f(lx)}" y1="{f(ly - 4)}" x2="{f(lx + 26)}" y2="{f(ly - 4)}" stroke="{col}" stroke-width="{wd}"{ds}/>')
            e(f'  <text x="{f(lx + 32)}" y="{f(ly)}">{lab}</text>')
            lx += 26 + 6 + tw(lab, FS_SMALL) + 18
        for lab, fill, stroke in kinds:
            st = f' stroke="{stroke}"' if stroke else ""
            e(f'  <rect x="{f(lx)}" y="{f(ly - 10)}" width="12" height="12" rx="2" fill="{fill}"{st}/>')
            e(f'  <text x="{f(lx + 18)}" y="{f(ly)}">{lab}</text>')
            lx += 12 + 6 + tw(lab, FS_SMALL) + 18
        e("</g>")

    def chip(self, x, y, w, name, P):
        info = self.catalog.get(name, {})
        cat = info.get("category", "ops")
        icon = info.get("icon", CAT.get(cat, CAT["ops"])[1])
        col = CAT.get(cat, CAT["ops"])[0]
        tint = CHIP_TINT.get(info.get("tint", ""))
        if tint:
            fill, tcol, bold = tint
            r = f'    <rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="21" rx="4" fill="{fill}"/>'
            txt = f'    <text x="{f(x + 24)}" y="{f(y + 15)}" font-size="{FS_SMALL}"{" font-weight=" + chr(34) + "bold" + chr(34) if bold else ""} fill="{tcol}">{esc(name)}</text>'
            col = tcol
        else:
            r = f'    <rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="21" rx="4" fill="#FFFFFF" stroke="{BORDER}" stroke-width="1"/>'
            txt = f'    <text x="{f(x + 24)}" y="{f(y + 15)}" font-size="{FS_SMALL}" fill="{TEXT}">{esc(name)}</text>'
        if tw(name, FS_SMALL, bool(tint and tint[2])) + 26 > w:
            self.warn.append(f"칩 글자 넘침 가능: {name} ({w:.0f}px)")
        return [r, f'    <use data-icon="tabler-outline/{icon}" x="{f(x + 6)}" y="{f(y + 4)}" width="13" height="13" fill="{col}" stroke-width="2"/>', txt]

    def tile(self, n, P):
        e = self.emit
        cat = n.get("category", "external" if n["kind"] == "actor" else "compute")
        col, icon, caption = CAT[cat]
        icon = n.get("icon", icon)
        caption = n.get("caption", caption)
        x, y, w, h = n["x"], n["y"], n["w"], n["h"]
        dashed = n.get("customer") or n.get("dashed")
        strong = n.get("strong") or n.get("common") or n.get("chips")
        stroke = CAPTION if n.get("customer") else (NAVY if strong else BORDER)
        ds = ' stroke-dasharray="4,3"' if n.get("customer") else (' stroke-dasharray="6,4"' if n.get("dashed") else "")
        top = y - 9 if n.get("required") else y
        e(f'<g id="{P}-n-{n["id"]}" data-pptx-bounds="{f(x)} {f(top)} {f(w)} {f(y + h - top)}">')
        e(f'  <rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="6" fill="#FFFFFF" stroke="{stroke}" stroke-width="1.33"{ds}/>')
        sq = "#8A94A6" if n.get("dashed") else col
        e(f'  <rect x="{f(x + 10)}" y="{f(y + 10 if n["kind"] == "actor" else y + 12)}" width="28" height="28" rx="6" fill="{sq}"/>')
        e(f'  <use data-icon="tabler-outline/{icon}" x="{f(x + 14)}" y="{f(y + 14 if n["kind"] == "actor" else y + 16)}" width="20" height="20" fill="#FFFFFF" stroke-width="2"/>')
        if n["kind"] == "actor":
            e(f'  <text x="{f(x + 10)}" y="{f(y + 66)}" font-size="{FS_NAME}" font-weight="bold" fill="{NAVY}">{esc(n["label"])}</text>')
            e("</g>")
            return
        if caption:
            ccol = CAPTION if n.get("dashed") else CAT.get(n.get("caption_category", cat), CAT[cat])[0]
            e(f'  <text x="{f(x + 46)}" y="{f(y + 31)}" font-size="{FS_SMALL}" font-weight="bold" fill="{ccol}">{esc(caption)}</text>')
            if tw(caption, FS_SMALL, True) + 46 > (w if not n.get("common") else 120) - 2:
                self.warn.append(f"{n['id']}: 분류 라벨 넘침 가능")
        ny = y + (64 if (n["kind"] == "main" and h >= 100) else 54)
        e(f'  <text x="{f(x + 10)}" y="{f(ny)}" font-size="{FS_NAME}" font-weight="bold" fill="{NAVY}">{esc(n["label"])}</text>')
        lines = [t for t in (n.get("spec"), n.get("sub")) if t]
        infow = 120 if n.get("common") else w - 14
        if tw(n["label"], FS_NAME, True) > infow:
            self.warn.append(f"{n['id']}: 이름 넘침 가능")
        for i, t in enumerate(lines):
            e(f'  <text x="{f(x + 10)}" y="{f(ny + 18 + 16 * i)}" font-size="{FS_SMALL}" fill="{CAPTION}">{esc(t)}</text>')
            if tw(t, FS_SMALL) > infow:
                self.warn.append(f"{n['id']}: 설명 넘침 가능 ({t})")
        if n.get("chips"):  # 보조 목록 (회색 칩 격자)
            cy0 = ny + 18 + 16 * len(lines) - 4
            cw = (w - 24) / 2
            for i, c in enumerate(n["chips"]):
                cx = x + 10 + (i % 2) * (cw + 4)
                yy = cy0 + (i // 2) * 23
                e(f'  <rect x="{f(cx)}" y="{f(yy)}" width="{f(cw)}" height="20" rx="4" fill="#EEF1F5"/>')
                e(f'  <text x="{f(cx + 6)}" y="{f(yy + 14)}" font-size="{FS_SMALL}" fill="{TEXT}">{esc(c)}</text>')
        if n.get("common") or n.get("services") or n.get("note"):
            dx = x + 120
            e(f'  <rect x="{f(dx)}" y="{f(y + 12)}" width="1" height="{f(h - 24)}" fill="#E2E6EC"/>')
            cx0, cw = dx + 10, (x + w - 8 - dx - 10 - 6) / 2
            rows = []
            common = n.get("common", [])
            for i, c in enumerate(common):
                rows += self.chip(cx0 + (i % 2) * (cw + 6), y + 10 + (i // 2) * 26, cw, c, P)
            yy = y + 10 + ((len(common) + 1) // 2) * 26
            if n.get("services"):
                e(f'  <text x="{f(cx0)}" y="{f(yy + 12)}" font-size="{FS_SMALL}" font-weight="bold" fill="{CAPTION}">{esc(n.get("services_label", "플랫폼 서비스"))}</text>')
                for i, c in enumerate(n["services"]):
                    rows += self.chip(cx0 + (i % 2) * (cw + 6), yy + 20 + (i // 2) * 26, cw, c, P)
                if yy + 20 + ((len(n["services"]) + 1) // 2 - 1) * 26 + 21 > y + h - 2:
                    self.err.append(f"{n['id']}: 칩이 노드 높이를 넘음 — 행 수를 줄이거나 서비스를 나눔")
            elif n.get("note"):
                for i, t in enumerate(str(n["note"]).split("\n")):
                    e(f'  <text x="{f(cx0)}" y="{f(yy + 22 + 16 * i)}" font-size="{FS_SMALL}" fill="{CAPTION}">{esc(t)}</text>')
            for r in rows:
                e(r)
        if n.get("required"):
            bx = x + w - 40
            e(f'  <rect x="{f(bx)}" y="{f(y - 9)}" width="32" height="18" rx="9" fill="{NAVY}"/>')
            e(f'  <text x="{f(bx + 16)}" y="{f(y + 4)}" font-size="{FS_SMALL}" font-weight="bold" fill="#FFFFFF" text-anchor="middle">필수</text>')
        e("</g>")

    def defs(self):
        P = self.s.get("prefix", "arch")
        return "\n".join(
            f'<marker id="{P}-a-{t}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="3" markerHeight="3" orient="auto"><polygon points="0,0 10,5 0,10" fill="{EDGE[t][0]}"/></marker>'
            for t in sorted(self.markers))


def embed_icons(svg, icons_dir):
    def rep(m):
        attrs = dict(re.findall(r'([\w:-]+)="([^"]*)"', m.group(0)))
        lib, name = attrs["data-icon"].split("/", 1)
        p = os.path.join(icons_dir, lib, name + ".svg")
        if not os.path.exists(p):
            return m.group(0)
        src = open(p, encoding="utf-8").read()
        inner = re.sub(r"(?s)^.*?<svg[^>]*>|</svg>\s*$", "", re.sub(r"<!--.*?-->", "", src, flags=re.S))
        x, y, w = float(attrs["x"]), float(attrs["y"]), float(attrs["width"])
        col = attrs.get("fill", "#000000")
        return (f'<g transform="translate({x} {y}) scale({w / 24})" fill="none" stroke="{col}" '
                f'stroke-width="{attrs.get("stroke-width", "2")}" stroke-linecap="round" stroke-linejoin="round">{inner}</g>')
    return re.sub(r"<use [^>]*data-icon=\"[^\"]+\"[^>]*/>", rep, svg)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--svg", help="단독 SVG 저장 경로")
    ap.add_argument("--icons-dir", help="아이콘 라이브러리 경로 (미리보기용 아이콘 삽입)")
    ap.add_argument("--fragment", action="store_true", help="장표용 defs·본문 조각을 stdout으로")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    spec = yaml.safe_load(open(a.spec, encoding="utf-8"))
    d = Diagram(spec)
    d.layout()
    if not d.err:
        d.route()
    if not d.err:
        d.draw()
    print(f"[점검] 오류 {len(d.err)} · 경고 {len(d.warn)}", file=sys.stderr)
    for m in d.err:
        print("  ERROR", m, file=sys.stderr)
    for m in d.warn:
        print("  WARN ", m, file=sys.stderr)
    if d.err or a.check:
        sys.exit(1 if d.err else 0)
    body = "\n".join(d.out)
    if a.fragment:
        print("<!-- defs -->\n" + d.defs() + "\n<!-- body -->\n" + body)
    if a.svg:
        X, Y, W, H = d.X, d.Y, d.W, d.H
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f(X - 12.6)} {f(Y - 12)} {f(W + 25.2)} {f(H + 22)}" '
               f'width="{f(W + 25.2)}" height="{f(H + 22)}" lang="ko" font-family="Pretendard, \'Malgun Gothic\'">\n'
               f'<defs>\n{d.defs()}\n</defs>\n<rect id="bg" data-pptx-role="background" x="{f(X - 12.6)}" y="{f(Y - 12)}" width="{f(W + 25.2)}" height="{f(H + 22)}" fill="#FFFFFF"/>\n'
               f'{body}\n</svg>\n')
        if a.icons_dir:
            svg = embed_icons(svg, a.icons_dir)
        open(a.svg, "w", encoding="utf-8").write(svg)
        print(f"[저장] {a.svg}", file=sys.stderr)


if __name__ == "__main__":
    main()
