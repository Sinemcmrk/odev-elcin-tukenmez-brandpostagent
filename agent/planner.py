"""AGENT 1 — Content & Design Planner.

Görevi: kullanıcının niyetini anlamak, gerçekten eksik olan bilgiyi sormak, Brand Kit ve Post Kütüphanesi
kurallarıyla seriyi seçmek, başlık / içerik / CTA / caption / hashtag'i yazmak, Brand Kit'e göre denetlemek
ve kısa bir tasarım planı hazırlamak.

Agent 1 PNG ÜRETMEZ. Metnin şablona sığıp sığmadığını ölçmek için şablonu yalnızca ölçüm kipinde açar
(render_pages(..., measure_only=True)); dosya yazılmaz. Görsel üretimi onaydan sonra Agent 2'nin işidir.

Çıktı: plan sözlüğü (JSON). Yapısı README.md › "Plan JSON yapısı" bölümünde.
"""
import copy, datetime, json, pathlib, re, shutil, time, uuid
from . import series as SR, prompts as PR, validate as V, platforms as PF, themes as TH, design as DS
from .render import render_pages
from .llm import LLMError

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA = "brandpostagent/plan@1"

# Kod düzeyinde zorunlu bilgi kuralları: model soru önermese bile bu durumlarda sorulur;
# genel bilgilendirici postlarda (info) modelin önerdiği sorular da sorulmaz.
DATE_RE = re.compile(r"\b\d{1,2}\s*[./-]\s*\d{1,2}\b|\b\d{1,2}\s+" + V.MONTHS + r"|\b" + V.MONTHS + r"\s+\d{1,2}\b", re.I)
REQUIRED_Q = {
    "event": "Etkinliğin tarihi, saati ve yeri (ya da çevrim içi bilgisi) nedir?",
    "deadline": "Son tarih nedir ve hangi program / sınav / başvuru için geçerli?",
    "achievement": "Paylaşılacak doğrulanmış sonuç nedir? (ör. kaç öğrenci, hangi okullar; paylaşım izni var mı?)",
}
LOGO_RULE = {
    "aba_psikoloji": "Sağ üstte turuncu yuvarlak karo içinde beyaz çiçek logo",
    "aba_egitim": "Sağ üstte turuncu karo içinde beyaz logo",
    "e4i": "Sağ üstte beyaz kart içinde vakıf logosu",
    "design_house": "Sol üstte şarap rengi monogram karosu (krem serilerde wordmark)",
}
PAGE_ROLE = {"kapak": "Kapak", "cover": "Kapak", "kapanis": "Kapanış", "son": "Kapanış", "close": "Kapanış"}


def load_kb(brand):
    return json.loads((ROOT / "knowledge" / f"{brand}.json").read_text(encoding="utf-8"))


def merge_facts(facts, answers):
    parts = [facts.strip()] if (facts or "").strip() else []
    for q, a in (answers or {}).items():
        if str(a).strip():
            parts.append(f"{q} → {str(a).strip()}")
    return "\n".join(parts)


def first_text(d):
    for v in d.values():
        if isinstance(v, str) and V.visible(v).strip():
            return V.visible(v)[:70]
        if isinstance(v, list) and v and isinstance(v[0], str):
            return " ".join(V.visible(x) for x in v)[:70]
    return ""


def normalize_draft(d):
    """Model çıktısını beklenen biçime getirir (caption liste, hashtag tek metin gibi küçük sapmalar)."""
    d = d if isinstance(d, dict) else {}
    cap = d.get("caption", "")
    if isinstance(cap, list): cap = "\n\n".join(map(str, cap))
    tags = d.get("hashtags", [])
    if isinstance(tags, str): tags = tags.replace(",", " ").split()
    fields = d.get("fields", {})
    return dict(d, fields=fields if isinstance(fields, dict) else {}, caption=str(cap or ""), hashtags=list(tags or []))


class ContentPlanner:
    """Agent 1. start() → soru ya da plan; revise() → geri bildirimle yeni sürüm; edit() → elle düzenleme."""

    def __init__(self, llm, max_rounds=2, deep_review=True, work_root=None):
        self.llm, self.max_rounds, self.deep_review = llm, max_rounds, deep_review
        self.work_root = pathlib.Path(work_root or ROOT / "outputs")

    # ------------------------------------------------------------------ 1. analiz
    def start(self, brand, topic, platform=PF.DEFAULT, facts="", series_id=None, answers=None,
              skip_questions=False, photo=None, photo_opacity=0.3, on_step=None, theme=None):
        say = on_step or (lambda step, msg, data=None: None)
        t0, calls0 = time.time(), self.llm.calls
        if brand not in SR.BRANDS:
            raise ValueError(f"Bilinmeyen marka: {brand}")
        pf = PF.get(platform)
        topic = (topic or "").strip()
        if len(topic) < 3:
            raise ValueError("Lütfen bir post konusu yazın.")
        kb = load_kb(brand)
        all_facts = merge_facts(facts, answers)
        options = SR.options(brand, platform)
        usable = [s for s in options if not (s.needs_facts and not all_facts)]
        log = []

        hist = DS.recent(brand)
        sp, up = PR.analyze_prompt(kb, options, topic, all_facts, pf.name, TH.options(brand), hist, bool(photo))
        an = self.llm.generate_json(sp, up, temperature=0.3)
        ptype = an.get("post_type") if an.get("post_type") in PR.POST_TYPES else "info"
        analysis = {"intent": str(an.get("intent", "")).strip(), "post_type": ptype,
                    "audience": an.get("audience", ""), "angle": an.get("angle", "")}

        # Seri seçimi: kullanıcı seçtiyse o, yoksa modelin önerisi (kullanılabilir değilse ilk uygun seri)
        if series_id:
            ser = SR.get(brand, series_id, platform)
            reason = "Seri kullanıcı tarafından seçildi."
        else:
            ids = [s.id for s in usable] or [options[0].id]
            want = str(an.get("series") or "").strip().strip("'\"").lower()
            by_name = {s.name.lower(): s.id for s in usable}
            want = want if want in ids else by_name.get(want) or next((i for n, i in by_name.items() if want and (n.startswith(want) or want in n)), want)
            an["series"] = want
            ranked = DS.rank(brand, usable or options, topic, ptype, kb, bool(photo), hist)
            pick = want if want in ids else ranked[0].id
            ser = SR.get(brand, pick, platform)
            reason = str(an.get("reason", "")).strip()
            if an.get("series") not in ids:
                reason = (f"(Model geçerli bir seri önermedi; konu ve kompozisyon metadata'sına göre '{ser.name}' seçildi.) " + reason).strip()
        theme = TH.pick(brand, ser, topic, theme or an.get("theme"))
        ranked = DS.rank(brand, usable or options, topic, ptype, kb, bool(photo), hist)
        alts = [DS.describe(a) for a in DS.alternatives(ser, ranked, [str(x) for x in (an.get("alternatives") or [])])]
        analysis.update(series=ser.id, reason=reason, theme=theme, design_reason=str(an.get("design_reason", "")).strip(),
                        recent=[h.get("series") for h in hist])

        # Eksik bilgi: yalnızca gerçekten gerekli olduğunda soru
        questions = []
        if ser.needs_facts and not all_facts:
            questions.append(f"'{ser.name}' serisi doğrulanmış bilgi ister: {ser.needs_facts}. Bu bilgiyi paylaşır mısınız?")
        if ptype in ("event", "deadline") and not DATE_RE.search(topic + " " + all_facts):
            questions.append(REQUIRED_Q[ptype])
        if ptype == "achievement" and not all_facts:
            questions.append(REQUIRED_Q["achievement"])
        # Modelin önerdiği ek sorular yalnızca zaten zorunlu bir eksik varsa ve ilk turda eklenir;
        # böylece bilgisi tam olan ya da genel bilgilendirici postlarda kullanıcı gereksiz soruyla durdurulmaz.
        if questions and ptype != "info" and not answers:
            for q in an.get("questions") or []:
                q = str(q).strip()
                if q and len(questions) < 3 and q not in questions:
                    questions.append(q)
        questions = questions[:3]
        say("analyze", f"Niyet: {analysis['intent']} · Tür: {ptype} · Seri: {ser.name}", analysis)
        log.append({"step": "analyze", "data": analysis, "questions": questions})

        if questions and not skip_questions:
            hard = bool(ser.needs_facts and not all_facts)
            say("questions", f"{len(questions)} soru soruluyor.", questions)
            return {"status": "needs_info", "questions": questions, "analysis": analysis, "blocking": hard,
                    "brand": brand, "platform": platform, "topic": topic, "llm_calls": self.llm.calls - calls0}
        if questions and skip_questions and ser.needs_facts and not all_facts:
            if series_id:
                raise ValueError(f"'{ser.name}' serisi doğrulanmış bilgi olmadan hazırlanamaz ({ser.needs_facts}). "
                                 "Bilgiyi yazın ya da başka bir seri seçin.")
            # Kullanıcı bilgi vermeden devam etti: bilgi gerektirmeyen en uygun kompozisyona geçilir (bilgi uydurulmaz)
            fallback = [x for x in DS.rank(brand, usable or options, topic, ptype, kb, bool(photo), hist) if not x.needs_facts]
            if fallback:
                ser = fallback[0]
                analysis["reason"] = (f"Doğrulanmış bilgi verilmediği için bilgi gerektirmeyen '{ser.name}' kompozisyonu seçildi. "
                                      + analysis.get("reason", ""))
                analysis["series"] = ser.id
                theme = TH.pick(brand, ser, topic, theme)
                analysis["theme"] = theme
                alts = [DS.describe(a) for a in DS.alternatives(ser, ranked, [])]

        # 2. yazım + 3. denetim/düzeltme
        sp, up = PR.write_prompt(kb, ser, topic, all_facts, analysis, pf.name)
        draft = normalize_draft(self.llm.generate_json(sp, up, temperature=0.85))
        say("write", "Başlık, içerik, CTA, caption ve hashtag'ler yazıldı.", draft)
        log.append({"step": "write", "data": draft})
        self._theme = theme
        clean, cap, tags, rounds, remaining = self._check_loop(kb, ser, draft, topic, all_facts, pf, photo, photo_opacity, say, log)

        plan = {
            "schema": SCHEMA, "plan_id": uuid.uuid4().hex[:12], "version": 1, "status": "ready",
            "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "brand": brand, "brand_name": SR.BRANDS[brand], "language": kb["language"],
            "platform": platform, "platform_name": pf.name, "size": [pf.width, pf.height],
            "topic": topic, "facts": all_facts, "answers": answers or {}, "skipped_questions": questions if skip_questions else [],
            "analysis": analysis, "series": ser.id, "series_name": ser.name, "kind": ser.kind, "theme": theme,
            "composition": DS.describe(ser), "alternatives": alts,
            "content": {"fields": clean, "caption": cap, "hashtags": tags},
            "photo": photo, "photo_opacity": photo_opacity,
            "checks": {"rounds": rounds, "remaining_warnings": remaining, "self_check": draft.get("self_check", [])},
            "feedback_history": [], "model": self.llm.model,
            "llm_calls": self.llm.calls - calls0, "seconds": round(time.time() - t0, 1),
            "approval": {"status": "pending"}, "log": log,
        }
        plan["design"] = self.design_plan(plan, kb, ser)
        say("design", "Tasarım planı hazır. Kullanıcı onayı bekleniyor.", plan["design"])
        return {"status": "ready", "plan": plan}

    # ------------------------------------------------------------------ geri bildirim
    def revise(self, plan, feedback, on_step=None):
        """Kullanıcının geri bildirimiyle yeni bir plan sürümü üretir. Onay sıfırlanır."""
        say = on_step or (lambda step, msg, data=None: None)
        feedback = (feedback or "").strip()
        if not feedback:
            raise ValueError("Geri bildirim boş olamaz.")
        calls0 = self.llm.calls
        kb, ser, pf = load_kb(plan["brand"]), SR.get(plan["brand"], plan["series"], plan["platform"]), PF.get(plan["platform"])
        c = plan["content"]
        opts = [o for o in SR.options(plan["brand"], plan["platform"]) if not (o.needs_facts and not plan["facts"])]
        sp, up = PR.feedback_prompt(kb, ser, {"fields": c["fields"], "caption": c["caption"], "hashtags": c["hashtags"]},
                                    feedback, plan["topic"], plan["facts"], pf.name, opts)
        self._theme = plan.get("theme")
        raw = self.llm.generate_json(sp, up, temperature=0.6)
        sw = str(raw.get("switch_series") or "").strip()
        if sw and sw != ser.id and sw in [o.id for o in opts]:
            say("feedback", f"Geri bildirim farklı bir tasarım istiyor: {SR.get(plan['brand'], sw, plan['platform']).name}.")
            return self.switch_design(plan, sw, feedback, on_step, _calls0=calls0)
        draft = normalize_draft(raw)
        say("feedback", "Geri bildirim uygulandı.", draft)
        log = [{"step": "feedback", "feedback": feedback, "data": draft}]
        clean, cap, tags, rounds, remaining = self._check_loop(kb, ser, draft, plan["topic"], plan["facts"], pf,
                                                               plan.get("photo"), plan.get("photo_opacity", 0.3), say, log, review=False)
        return self._new_version(plan, kb, ser, clean, cap, tags, rounds, remaining,
                                 {"type": "feedback", "text": feedback, "model_note": str(draft.get("not", "") or ""),
                                  "llm_calls": self.llm.calls - calls0}, log)

    def switch_design(self, plan, series_id, feedback="", on_step=None, _calls0=None):
        """Aynı konu için FARKLI bir kompozisyon ailesi: içerik yeni şablonun alanlarına göre yeniden yazılır (1 Gemini çağrısı
        + gerekirse düzeltme). Tema yeni seride geçerliyse korunur. Yeni plan sürümü; onay sıfırlanır."""
        say = on_step or (lambda step, msg, data=None: None)
        calls0 = self.llm.calls if _calls0 is None else _calls0
        brand, pfid = plan["brand"], plan["platform"]
        kb, pf = load_kb(brand), PF.get(pfid)
        ser = SR.get(brand, series_id, pfid)
        if ser.needs_facts and not plan["facts"]:
            raise ValueError(f"'{ser.name}' doğrulanmış bilgi ister ({ser.needs_facts}); önce bilgiyi ekleyin.")
        analysis = dict(plan["analysis"], series=ser.id)
        if feedback:
            analysis["angle"] = f"{analysis.get('angle', '')} · Kullanıcının tasarım isteği: {feedback}"
        sp, up = PR.write_prompt(kb, ser, plan["topic"], plan["facts"], analysis, pf.name)
        draft = normalize_draft(self.llm.generate_json(sp, up, temperature=0.85))
        say("write", f"İçerik '{ser.name}' tasarımına göre yeniden yazıldı.", draft)
        old_theme = plan.get("theme")
        self._theme = old_theme if (old_theme in TH.options(brand) and TH.themable(brand, ser)) else TH.pick(brand, ser, plan["topic"])
        log = [{"step": "switch_design", "series": ser.id, "feedback": feedback, "data": draft}]
        clean, cap, tags, rounds, remaining = self._check_loop(kb, ser, draft, plan["topic"], plan["facts"], pf,
                                                               plan.get("photo"), plan.get("photo_opacity", 0.3), say, log, review=False)
        base = dict(plan, series=ser.id, series_name=ser.name, kind=ser.kind, theme=self._theme, analysis=analysis,
                    composition=DS.describe(ser))
        ranked = DS.rank(brand, [o for o in SR.options(brand, pfid) if not (o.needs_facts and not plan["facts"])],
                         plan["topic"], analysis.get("post_type", "info"), kb, bool(plan.get("photo")))
        base["alternatives"] = [DS.describe(a) for a in DS.alternatives(ser, ranked, [plan["series"]])]
        return self._new_version(base, kb, ser, clean, cap, tags, rounds, remaining,
                                 {"type": "design", "text": feedback or f"Tasarım değiştirildi: {ser.name}", "series": ser.id,
                                  "llm_calls": self.llm.calls - calls0}, log)

    def edit(self, plan, fields=None, caption=None, hashtags=None, theme="__keep__"):
        """Kullanıcının elle düzenlemesi ya da görünüm (tema) değişikliği. Gemini çağrısı yok; denetim ve sığma ölçümü yapılır."""
        kb, ser, pf = load_kb(plan["brand"]), SR.get(plan["brand"], plan["series"], plan["platform"]), PF.get(plan["platform"])
        if theme != "__keep__":
            plan = dict(plan, theme=theme if theme in TH.options(plan["brand"]) and TH.themable(plan["brand"], ser) else None)
        self._theme = plan.get("theme")
        c = plan["content"]
        draft = {"fields": fields if fields is not None else c["fields"], "caption": caption if caption is not None else c["caption"],
                 "hashtags": hashtags if hashtags is not None else c["hashtags"]}
        draft = normalize_draft(draft)
        log = [{"step": "edit", "data": draft}]
        clean, cap, tags, rounds, remaining = self._check_loop(kb, ser, draft, plan["topic"], plan["facts"], pf,
                                                               plan.get("photo"), plan.get("photo_opacity", 0.3), None, log,
                                                               review=False, max_rounds=0)
        return self._new_version(plan, kb, ser, clean, cap, tags, rounds, remaining,
                                 {"type": "edit" if theme == "__keep__" else "theme"}, log)

    # ------------------------------------------------------------------ yardımcılar
    def _new_version(self, plan, kb, ser, clean, cap, tags, rounds, remaining, fb, log):
        p = copy.deepcopy(plan)
        p["version"] = plan["version"] + 1
        p["content"] = {"fields": clean, "caption": cap, "hashtags": tags}
        p["checks"] = {"rounds": rounds, "remaining_warnings": remaining, "self_check": plan["checks"].get("self_check", [])}
        p["feedback_history"] = plan.get("feedback_history", []) + [dict(fb, version=p["version"],
                                                                         at=datetime.datetime.now().isoformat(timespec="seconds"))]
        p["approval"] = {"status": "pending"}
        p["log"] = plan.get("log", []) + log
        p["design"] = self.design_plan(p, kb, ser)
        return p

    def _check_loop(self, kb, ser, draft, topic, facts, pf, photo, photo_opacity, say, log, review=True, max_rounds=None):
        say = say or (lambda step, msg, data=None: None)
        rounds, reviewed = [], not (review and self.deep_review)
        max_rounds = self.max_rounds if max_rounds is None else max_rounds
        for rnd in range(max_rounds + 1):
            clean, cap, tags, issues, fixes = V.check_post(ser.brand, kb["language"], ser,
                                                            draft.get("fields", {}), draft.get("caption", ""), draft.get("hashtags", []),
                                                            topic, facts, kb["verified_facts"])
            rev = None
            if not reviewed:
                reviewed = True
                rs, ru = PR.review_prompt(kb, ser, {"fields": clean, "caption": cap, "hashtags": tags})
                rev = self.llm.generate_json(rs, ru, temperature=0.2)
                issues += [f"Marka denetimi: {x}" for x in (rev.get("issues") or [])][:5]
            issues += self._fit(ser, clean, photo, photo_opacity)
            rounds.append({"round": rnd, "issues": issues, "auto_fixes": fixes, "review": rev})
            say("check", f"Denetim {rnd + 1}: {len(issues)} sorun" + (f", {len(fixes)} otomatik düzeltme" if fixes else ""),
                {"issues": issues, "auto_fixes": fixes, "review": rev})
            if not issues or rnd == max_rounds:
                break
            sp, up = PR.revise_prompt(kb, ser, {k: draft.get(k) for k in ("fields", "caption", "hashtags")}, issues, topic, facts)
            draft = normalize_draft(self.llm.generate_json(sp, up, temperature=0.6))
            say("revise", f"{len(issues)} sorun düzeltildi (tur {rnd + 1}).", draft)
            log.append({"step": "revise", "data": draft})
        remaining = rounds[-1]["issues"]
        if remaining:
            trimmed = V.hard_trim(ser.schema, clean)
            if trimmed != clean:
                clean = trimmed
                left = self._fit(ser, clean, photo, photo_opacity)
                remaining = [i for i in remaining if not i.startswith("Sayfa ")] + left
        return clean, cap, tags, rounds, remaining

    def _fit(self, ser, clean, photo, photo_opacity):
        """Metni gerçek şablonda ölçer (PNG yazmadan)."""
        try:
            pages = [(f"{k + 1:02d}", t, d) for k, (t, d) in enumerate(ser.build(clean))]
        except Exception:
            return ["Alan yapısı şablona uymuyor (eksik liste öğesi ya da alan); şemaya tam uy."]
        tmp = self.work_root / "_olcum" / uuid.uuid4().hex[:10]
        try:
            _, overflow = render_pages(ser.brand, pages, tmp, photo, photo_opacity, measure_only=True,
                                       theme=getattr(self, "_theme", None))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        return [f"Sayfa {pg}: “{tx}…” metni alana sığmadı; bu alanı yaklaşık %30 kısalt." for pg, texts in overflow.items() for tx in texts]

    @staticmethod
    def design_plan(plan, kb, ser):
        built = ser.build(plan["content"]["fields"])
        n = len(built)
        pages = []
        for k, (tpl, data) in enumerate(built):
            role = next((v for key, v in PAGE_ROLE.items() if key in tpl), None)
            if not role:
                role = "Story ekranı" if ser.kind == "story" else ("Tek post" if n == 1 else f"İçerik sayfası {k}")
            pages.append({"no": k + 1, "template": tpl, "role": role, "main_text": first_text(data)})
        fmt = {"carousel": f"Carousel · {n} sayfa", "story": "Story · tek ekran"}.get(ser.kind, "Tek post")
        pal = [{"name": c["name"], "hex": c["hex"], "use": c["use"]} for c in kb["palette"][:4]]
        warn = plan["checks"]["remaining_warnings"]
        return {
            "platform": plan["platform_name"], "size": f'{plan["size"][0]}×{plan["size"][1]}', "format": fmt,
            "series": ser.name, "composition": DS.describe(ser)["desc"], "layout": DS.describe(ser)["layout"],
            "pages": pages, "colors": pal,
            "theme": TH.options(plan["brand"]).get(plan.get("theme"), "Serinin kendi görünümü"), "fonts": kb["fonts"][:2], "logo": LOGO_RULE[plan["brand"]],
            "photo": (f"Kullanıcı fotoğrafı arka planda, görünürlük %{int(plan['photo_opacity'] * 100)}" if plan.get("photo")
                      else "Fotoğraf yok; markanın grafik düzeni (dekor, renk alanları) kullanılır."),
            "fixed_identity": "Logo, renk paleti, fontlar ve iletişim bandı şablonda sabittir; içerik metni bunları değiştiremez.",
            "layout_check": "Tüm metinler şablona sığıyor." if not any(w.startswith("Sayfa ") for w in warn)
                            else "Bazı metinler sığmıyor; geri bildirimle kısaltılabilir.",
        }
