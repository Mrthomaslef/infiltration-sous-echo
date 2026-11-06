#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Curation des iconographies par geste : uniquement position de sonde / coupe
écho cible, recadrées sur l'image (plus de pages entières) + légende.

Sources (hors dépôt, utilisées seulement pour régénérer les recadrages) :
  - figures Gel Contact extraites des PDF SIMS : /tmp/infil_review/figs{,2}/
  - diapositives des ateliers SIMS : pages/sNN_xxx.jpg ou /tmp/sims_slides/NN/xxx.jpg
Les recadrages finaux sont versionnés dans assets/figs/.
"""
import json, os, re, sys
from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "figs")
F1 = "/tmp/infil_review/figs"; F2 = "/tmp/infil_review/figs2"
LEG = {}
if os.path.exists("/tmp/infil_review/figs.json"):
    for v in json.load(open("/tmp/infil_review/figs.json")).values():
        for f in v["figs"]:
            if f.get("legend", "").lower().startswith("fig"): LEG[f["file"]] = f["legend"]
if os.path.exists("/tmp/infil_review/figs2.json"):
    LEG.update({k: v["legend"] for k, v in json.load(open("/tmp/infil_review/figs2.json")).items() if v.get("legend")})

def S(deck, n, legend):   # diapositive SIMS
    return {"src": f"s{deck}_{n}", "legend": legend}
def G(name, legend=None, v1=False):  # figure Gel Contact
    return {"src": name, "legend": legend, "v1": v1}

# ───────── sélection validée visuellement, geste par geste ─────────
CUR = {
 "epaule-bsad": [
  G("gc20_p40_f0", "Infiltration de la BSAD : position de la sonde, trajet de l'aiguille et schéma de la bourse (B) entre deltoïde et tendon (T)."),
  S(110,"022","Coupe cible : BSAD (liseré orange) entre le deltoïde et le supra-épineux."),
  G("gc21_p38_f1"), G("gc14_p26_f0"),
  G("gc16_p10_f1", "Fig 2 : Injection dans la BSAD — ampliation de la bourse séparant ses deux feuillets (flèches).", v1=True)],
 "epaule-gleno-humerale": [
  S(110,"028","Voie combinée BSAD + gléno-humérale (voie de D. Jacob) : trajet de l'aiguille sur la coupe axiale."),
  G("gc16_p10_f2", "Fig 3 : Gléno-humérale par voie postérieure — épanchement du récessus postérieur (*), cible de la ponction.", v1=True),
  G("gc21_p40_f1"),
  S(110,"027","Coupe écho cible : BSAD (jaune) et récessus gléno-huméral (cerclé).")],
 "epaule-capsulite-arthrodistension": [
  S(109,"009","Intervalle des rotateurs normal : cible de l'infiltration (LB et ligament coraco-huméral)."),
  S(109,"017","Récessus axillaire : épaississement capsulaire de la capsulite."),
  G("gc21_p41_f0"),
  S(109,"024","Abord de l'intervalle des rotateurs : trajet de l'aiguille (ligne échogène oblique).")],
 "epaule-calcification": [
  S(110,"055","Mise en pression de la calcification : cavitation à la pointe de l'aiguille (« cœur qui bat »)."),
  G("gc21_p39_f1"), G("gc21_p39_f0"),
  S(110,"056","Lavage : position de la sonde et de l'aiguille, aller-retour de la seringue."),
  S(110,"060","Quelles calcifications ? Hyperéchogène avec cône d'ombre partiel — confronter à la radio du jour."),
  G("gc32_p11_f0")],
 "epaule-acromio-claviculaire": [
  S(110,"034","Acromio-claviculaire : position de la sonde (coupe coronale) et image écho de l'interligne."),
  S(110,"036","Interligne AC en écho : cible de l'aiguille."),
  G("gc16_p11_f0", "Fig 4 : Infiltration acromio-claviculaire — pointe de l'aiguille avec son ombre acoustique (flèche).", v1=True),
  S(110,"040","Variante : abord combiné acromio-claviculaire + BSAD.")],
 "epaule-long-biceps": [
  G("gc23_p53_f0", "Abord antérieur de la gouttière bicipitale : sonde axiale, aiguille dans le plan."),
  G("gc23_p53_f1", "Aiguille au contact du tendon du long biceps, dans sa gaine."),
  G("gc16_p11_f1", "Fig 5 : Ponction sélective de la gaine du long biceps dans la gouttière bicipitale (coupe axiale, Doppler).", v1=True),
  S(110,"070","Ténotomie du long biceps à l'aiguille.")],
 "epaule-kyste-spinoglenoidien": [
  S(110,"066","Échancrure spino-glénoïdienne : position de la sonde (abord postérieur) et coupe écho cible."),
  G("gc21_p40_f0"),
  S(110,"065","Rapports avec le nerf supra-scapulaire (anatomie, écho, IRM)."),
  G("gc16_p11_f2", "Fig 6 : Kyste para-glénoïdien anéchogène, cible de la ponction échoguidée.", v1=True)],
 "coude-articulaire": [
  G("gc16_p12_f0", "Fig 7 : Coude — épanchement du récessus olécrânien postérieur, accumulé en extension (flèche) : cible de la ponction.", v1=True)],
 "coude-epicondylite-prp": [
  S(69,"010","Court extenseur radial du carpe (CERC) : position du coude et de la sonde, coupe cible."),
  S(69,"009","Coupe écho de référence : CERC (vert), ECD, EUC."),
  S(69,"018","Dérivé cortisoné : injection péri-tendineuse sous contrôle écho."),
  S(69,"023","PRP : criblage de la zone de tendinose puis injection.")],
 "coude-biceps-distal": [
  G("gc19_p24_f0"), G("gc20_p30_f1")],
 "poignet-de-quervain": [
  G("gc22_p60_f0"), G("gc22_p60_f1"),
  S(38,"018","Coupe de référence : premier compartiment, position de la sonde."),
  S(38,"023","Injection : ½ mL d'hydrocortancyl, toujours autour du rétinaculum."),
  G("gc19_p28_f3"),
  S(38,"031","De Quervain type 2 : septum séparant le premier compartiment.")],
 "main-doigt-ressaut": [
  S(38,"039","Doigt à ressaut : position de la sonde et de l'aiguille, injection autour du rétinaculum (poulie A1)."),
  S(38,"041","Puis injection dans la gaine en cas de tendinopathie / ténosynovite."),
  G("gc16_p12_f2", "Fig 8 : Doigt à ressaut en coupe axiale, abord latéral — injection dans la gaine puis au contact superficiel de la poulie (flèches).", v1=True),
  S(38,"051","Dry-needling / libération à l'aiguille 21G sous anesthésie locale.")],
 "poignet-canal-carpien": [
  G("gc22_p61_f0"),
  S(38,"056","Coupe axiale du canal carpien : trajet de l'aiguille 21G (schéma et écho)."),
  G("gc22_p57_f0"),
  S(38,"055","Voie d'abord 21G : position de la main et de l'aiguille."),
  G("gc30_p69_f0")],
 "main-rhizarthrose-pisotriquetrale": [
  G("gc22_p59_f0"),
  S(38,"066","Rhizarthrose : coupe sagittale à la base de l'éminence thénar, dans l'axe du 2e rayon."),
  S(38,"062","Voie d'abord palmaire : repérage « axe commissure ou M2 »."),
  S(38,"068","Critère de réussite : distension synoviale, mouvements browniens.")],
 "main-articulations-mcp-ipp-ipd": [
  S(38,"077","MCP : coupe sagittale dorsale cible."),
  S(38,"078","MCP : diffusion du produit dans le récessus (contour vert)."),
  S(38,"080","IPP : coupe sagittale cible."),
  S(38,"082","IPP / IPD : coupe sagittale cible.")],
 "poignet-kystes-dupuytren": [
  G("gc22_p62_f0"), G("gc22_p62_f1"), G("gc31_p106_f0"), G("gc31_p75_f0")],
 "hanche-coxofemorale": [
  G("gc16_p13_f0"), G("gc21_p53_f1")],
 "hanche-psoas-pth": [
  G("gc16_p13_f1"),
  G("gc26_p22_f0", "Figure 10 : Coupe axiale — trajectoire de l'aiguille lors de l'infiltration de la bourse ilio-psoas, au contact d'un débord antérieur de cupule (flèches).", v1=True),
  G("gc21_p56_f0")],
 "hanche-moyen-gluteal": [
  G("gc16_p14_f0", "Fig 3 : Ponction-infiltration péri-trochantérienne par voie latérale, selon la localisation superficielle (A) ou profonde (B) de la bursite ; C : aiguille dans la bursite.", v1=True),
  G("gc21_p57_f0")],
 "bassin-piriforme-alcock-pubalgie": [],
 "rachis-hydrodissection-lombaire-esp": [
  G("gc33_p27_f0", "Hydrodissection ESP au niveau du processus transverse : sonde convexe longitudinale à 3–5 cm de la ligne médiane, aiguille dans le plan.", v1=True),
  G("gc33_p25_f0", "Hydrodissection des plans interfasciaux paraspinaux (multifidus, longissimus) en balayage transversal.", v1=True),
  G("gc33_p24_f0", "Balayage axial lombaire (sonde convexe transversale sur la ligne médiane) : muscles paraspinaux et fascia thoraco-lombaire.", v1=True)],
 "genou-articulaire-ha-prp": [
  S(102,"004","Position : genou fléchi ~30°, sonde transversale sur le récessus sous-quadricipital."),
  S(102,"005","Coupe cible : récessus sous-quadricipital."),
  S(102,"006","Aiguille dans le récessus sous-quadricipital.")],
 "genou-kyste-poplite-meniscal": [
  S(102,"026","Kyste poplité (Baker) : cible de l'aspiration / fenestration (cathlon 18G)."),
  S(102,"041","Kyste méniscal : trajet de l'aiguille (pointillés)."),
  S(102,"044","Ponction du kyste : aiguille (flèches)."),
  S(102,"042","Kyste para-articulaire avant ponction.")],
 "genou-periarticulaire-bandelette-patte-oie": [
  S(102,"030","Bursite de la patte d'oie : coupe cible (flèche) en regard du plateau tibial interne."),
  S(102,"024","Injections échoguidées péri-patellaires : trajet de l'aiguille."),
  G("gc30_p121_f1", "Figure 6 : Injection échoguidée de PRP dans la partie postérieure du tendon patellaire proximal, aiguille dans le plan (A-B) ; position (C).", v1=True)],
 "cheville-articulaire-tibiotalienne": [
  G("gc24_p13_f1"), G("gc30_p129_f4")],
 "cheville-gaines-tibial-posterieur-fibulaires": [
  G("gc16_p15_f0"), G("gc16_p15_f1"), G("gc20_p41_f1"),
  S(38,"011","Critère de réussite : diffusion du produit dans la gaine synoviale du tibial postérieur.")],
 "cheville-achille-bursite-haut-volume": [
  G("gc20_p42_f1"),
  G("gc16_p16_f1", "Fig 7 : Ponction d'une bursite pré-achilléenne. A) Voie d'abord latérale avec contrôle de l'aiguille en coupe axiale rétro-achilléenne. B) Aiguille dans la bursite.", v1=True),
  G("gc30_p123_f0", "Figure 8 : Injection échoguidée de PRP dans le tendon d'Achille, approche latérale vers médiale en coupe transversale ; position de la sonde.", v1=True)],
 "pied-aponevrosite-plantaire": [
  G("gc16_p16_f0"), G("gc20_p42_f0"),
  G("gc33_p83_f0", "Figure 11 : Infiltration de l'aponévrose plantaire (pied gauche) : positionnement de la sonde et de l'aiguille.", v1=True),
  G("gc33_p83_f1", "Figure 12 : Coupe sagittale correspondante, sans (a) et avec (b) annotations : aiguille au contact de l'aponévrose, calcanéus.", v1=True)],
 "pied-nevrome-morton": [
  G("gc30_p99_f1"), G("gc21_p77_f1"), G("gc30_p100_f0")],
 "cheville-tunnel-tarsien-petits-nerfs": [
  S(117,"031","Tunnel tarsien, approche postéro-médiale : position de la sonde et de l'aiguille."),
  S(117,"032","Image cible : aiguille dans le tunnel tarsien (technique au gel pad)."),
  S(117,"135","Nerf plantaire médial propre de l'hallux (névrome de Joplin) : infiltration."),
  S(117,"101","Nerf fibulaire superficiel : test anesthésique + infiltration.")],
 "cheville-bloc-nerf-tibial-supra-malleolaire": [
  G("gc33_p80_f0"), G("gc33_p80_f1"), G("gc33_p81_f1"), G("gc33_p82_f0"), G("gc33_p82_f1")],
 "muscles-hematome-tennis-leg": [
  S(110,"045","Ponction-évacuation d'un hématome musculaire : collection ponctionnable, puis ponction."),
  G("gc14_p07_f0"), G("gc29_p28_f1"),
  G("gc26_p55_f1", "Collection inter-aponévrotique liquidienne, compressible sous la sonde : toujours ponctionner un hématome aigu.", v1=True)],
 "parties-molles-corps-etranger-harpon": [
  G("gc30_p110_f0", "Fig. 1a : Exérèse de corps étranger sous échographie — la pince est introduite à travers la peau, guidée par la sonde jusqu'au corps étranger."),
  G("gc30_p111_f0", "Fig. 3a : Épine de palmier dans les parties molles de la jambe — corps étranger linéaire échogène, cible de l'extraction à la pince."),
  G("gc16_p17_f0")],
 "parties-molles-biopsie-tumeur": [
  G("gc30_p101_f1")],
}

def trim(im):
    """Retire les bordures uniformes (fond noir/gris des diapositives)."""
    rgb = im.convert("RGB")
    bg = Image.new("RGB", rgb.size, rgb.getpixel((2, 2)))
    diff = ImageChops.difference(rgb, bg).convert("L").point(lambda v: 255 if v > 28 else 0)
    box = diff.getbbox()
    if box and (box[2]-box[0]) * (box[3]-box[1]) > 0.25 * rgb.size[0] * rgb.size[1]:
        rgb = rgb.crop(box)
    return rgb

def tidy(t):
    t = re.sub(r"\s+", " ", t or "").replace("­", "").strip()
    t = re.sub(r"^(F[Ii]g(?:ure)?\.?\s*)(\d+)\s*[:\.]?\s*", r"Fig. \2 : ", t)
    t = re.sub(r"(\s+[a-dA-D]){1,4}$", "", t)          # lettres de panneaux orphelines
    if len(t) >= 340 and not re.search(r"[.)»!]$", t):                 # légende coupée : on s'arrête à la dernière phrase complète
        cut = t.rfind(". ")
        t = t[:cut + 1] if cut > 40 else t.rstrip(" ,;:") + "…"
    return t

def materialize(item):
    src = item["src"]
    if src.startswith("s"):
        deck, n = src[1:].split("_")
        path = os.path.join(ROOT, "pages", f"{src}.jpg")
        if not os.path.exists(path): path = f"/tmp/sims_slides/{deck}/{n}.jpg"
        im = trim(Image.open(path)); legend = item["legend"]
        out = f"assets/figs/{src}.jpg"
    else:
        base = F1 if item.get("v1") and os.path.exists(f"{F1}/{src}.jpg") else F2
        if not os.path.exists(f"{base}/{src}.jpg"): base = F1
        im = Image.open(f"{base}/{src}.jpg").convert("RGB")
        legend = item["legend"] or LEG.get(src + ".jpg", "")
        out = f"assets/figs/{src}.jpg"
    im.thumbnail((1400, 1400))
    im.save(os.path.join(ROOT, out), quality=84, optimize=True, progressive=True)
    return out, tidy(legend)

def main():
    jp = os.path.join(ROOT, "data", "guide-data.json")
    data = json.load(open(jp, encoding="utf-8"))
    for p in data["procedures"]:
        if p["id"] not in CUR: continue
        figs = [materialize(i) for i in CUR[p["id"]]]
        p["allSlides"] = [f[0] for f in figs]
        p["legends"] = [f[1] for f in figs]
        p["heroSlides"] = p["allSlides"][:2]
        assert all(p["legends"]), (p["id"], p["legends"])
    missing = [p["id"] for p in data["procedures"] if p["category"] != "gel-contact" and p["id"] not in CUR]
    if missing: sys.exit(f"Non curés : {missing}")
    json.dump(data, open(jp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    with open(os.path.join(ROOT, "data", "embedded_data.js"), "w", encoding="utf-8") as f:
        f.write("window.GUIDE_DATA = "); json.dump(data, f, ensure_ascii=False)
        f.write(";\nwindow.ECHO_GUIDE_DATA = window.GUIDE_DATA.procedures;\n")
    print(sum(len(v) for v in CUR.values()), "figures curées")

if __name__ == "__main__":
    main()
