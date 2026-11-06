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
  S(110,"021","Infiltration de la BSAD : position du patient et de la sonde, trajet de l'aiguille (abord latéral)."),
  G("gc20_p40_f0", "Infiltration de la BSAD : position de la sonde, trajet de l'aiguille et schéma de la bourse (B) entre deltoïde et tendon (T)."),
  S(110,"022","Coupe cible : BSAD (liseré orange) entre le deltoïde et le supra-épineux."),
  G("gc21_p38_f0", "Aiguille (flèches) entre les feuillets de la BSAD non distendue (flèche courbe)."),
  G("gc21_p38_f1"), G("gc14_p26_f0")],
 "epaule-gleno-humerale": [
  S(110,"017","Position du patient (PLS) et du médecin pour l'abord postérieur de l'épaule."),
  G("gc16_p10_f2", "Fig. 3 : Gléno-humérale par voie postérieure — épanchement du récessus postérieur (*), cible de la ponction.", v1=True),
  S(110,"028","Voie combinée BSAD + gléno-humérale (voie de D. Jacob) : trajet de l'aiguille, BSAD (jaune) et récessus gléno-huméral (cerclé)."),
  G("gc21_p40_f1", "Fig. 8 : Infiltration gléno-humérale par voie antéro-latérale dans le récessus bicipital. A : aiguille (flèches bleues droites) dans le récessus en évitant le tendon du long biceps (flèche courbe) ; B : diffusion intra-articulaire.")],
 "epaule-capsulite-arthrodistension": [
  S(109,"024","Abord de l'intervalle des rotateurs : trajet de l'aiguille (ligne échogène oblique)."),
  S(109,"009","Intervalle des rotateurs normal : cible de l'infiltration (LB et ligament coraco-huméral)."),
  S(109,"017","Récessus axillaire : épaississement capsulaire de la capsulite.")],
 "epaule-calcification": [
  S(110,"056","Lavage de calcification : position de la sonde et de l'aiguille ; mise en pression avec cavitation à la pointe (« cœur qui bat »)."),
  G("gc21_p39_f1"), G("gc21_p39_f0"),
  G("gc32_p11_f0", "Fig. 10 : Évolution radio-échographique après ponction-lavage d'une calcification du supra-épineux (aspect avant, puis résorption).")],
 "epaule-acromio-claviculaire": [
  S(110,"034","Acromio-claviculaire : position de la sonde (coupe coronale) et image écho de l'interligne."),
  S(110,"036","Aiguille dans l'interligne acromio-claviculaire (coupe coronale)."),
  G("gc21_p41_f0", "Fig. 9 : Abord sagittal de l'interligne acromio-claviculaire (flèche courbe), aiguille bien visible (flèches droites).", v1=True),
  S(110,"040","Variante : abord combiné acromio-claviculaire + BSAD."),
  G("gc16_p11_f0", "Fig. 4 : Infiltration acromio-claviculaire — pointe de l'aiguille avec son ombre acoustique (flèche).", v1=True)],
 "epaule-long-biceps": [
  G("gc23_p53_f0", "Abord antérieur de la gouttière bicipitale : sonde axiale, aiguille dans le plan."),
  G("gc23_p53_f1", "Aiguille au contact du tendon du long biceps, dans sa gaine."),
  G("gc16_p11_f1", "Fig. 5 : Ténosynovite du long biceps, coupe axiale Doppler : gaine distendue hyperhémique, cible de l'injection.", v1=True),
  S(110,"070","Ténotomie du long biceps à l'aiguille.")],
 "epaule-kyste-spinoglenoidien": [
  S(110,"066","Échancrure spino-glénoïdienne : position de la sonde (abord postérieur) et coupe écho cible."),
  G("gc21_p40_f0"),
  G("gc16_p11_f2", "Fig. 6 : Kyste para-glénoïdien anéchogène, cible de la ponction échoguidée.", v1=True),
  S(110,"065","Rapports avec le nerf supra-scapulaire (anatomie, écho, IRM).")],
 "coude-articulaire": [
  G("gc16_p12_f0", "Fig. 7 : Coude — épanchement du récessus olécrânien postérieur, accumulé en extension (flèche) : cible de la ponction.", v1=True)],
 "coude-epicondylite-prp": [
  S(69,"010","Court extenseur radial du carpe (CERC) : position du coude et de la sonde, coupe cible."),
  S(69,"014","Coupes écho du CERC (longitudinale, axiale, Doppler) : tendinose hypoéchogène et fissure, cible du criblage / de l'injection."),
  S(69,"018","Dérivé cortisoné : injection péri-tendineuse sous contrôle écho."),
  S(69,"023","PRP : criblage de la zone de tendinose puis injection.")],
 "coude-biceps-distal": [
  G("gc19_p24_f0", "Fig. 1 : Tendon distal du biceps en coupe transversale à son enthèse. A : position de la sonde, parallèle à l'axe de l'avant-bras ; B : repère de la sonde sur la tubérosité radiale (TDM 3D) ; C : coupe écho du tendon (flèches) recouvrant la tubérosité radiale."),
  G("gc20_p30_f1", "Bursite bicipito-radiale : repérage échographique de la cible avant ponction (tuméfaction liquidienne autour de l'insertion du tendon)."),
  G("gc20_p30_f0", "Coupe axiale antérieure du coude : tendon distal du biceps (T BIC), épanchement péritendineux (LIQ) et artère brachiale (ART) à éviter avant ponction.")],
 "poignet-de-quervain": [
  S(38,"017","De Quervain : poignet en flexion ulnaire, repérage axial, voie d'abord longitudinale (ou axiale)."),
  G("gc25_p51_f0", "Infiltration d'une ténosynovite de De Quervain, technique du gel pad (étoile) : aiguille (flèches creuses) dans le rétinaculum épaissi et la gaine du 1er compartiment, en préservant la branche superficielle du nerf radial (têtes de flèche) (coupes axiales ; a : Doppler).", v1=True),
  G("gc22_p60_f0", "Fig. 8 : Abord dans le grand axe des tendons. a – bord ulnaire de la main posé sur un tube de gel ; b – coupe axiale : pas de cloison entre court extenseur (CE) et long abducteur (LA), rétinaculum épaissi hyperhémique ; c – trajet de l'aiguille au contact des tendons et du rétinaculum ; d – diffusion du produit dans la gaine (**)."),
  G("gc22_p60_f1", "Fig. 9 : Abord axial transverse (recommandé dans le type II avec cloison). a – position (simulation) ; b-c – trajet idéal (pointillés) traversant la cloison sans traverser les tendons (LA, CE) ; le gel pad (GP) évite la branche sensitive du nerf radial (flèche)."),
  G("gc25_p52_f0", "Type II avec septum : a – gaine du court extenseur inflammatoire (Doppler) et long abducteur normal ; b – mise en place sélective de l'aiguille dans la gaine atteinte.", v1=True)],
 "main-doigt-ressaut": [
  S(38,"037","Doigt à ressaut : position de la sonde et de l'aiguille ; toujours infiltrer autour du rétinaculum (A1), puis dans la gaine."),
  S(38,"039","Injection autour du rétinaculum (poulie A1) : ½ cc d'hydrocortancyl."),
  S(38,"041","Puis injection dans la gaine en cas de tendinopathie / ténosynovite."),
  G("gc25_p56_f2", "Coupe sagittale en fin de procédure : aiguille dans la gaine des fléchisseurs et poulie A1 dilacérée (flèche).", v1=True),
  G("gc16_p12_f2", "Fig. 8 : Coupe axiale, abord latéral — injection dans la gaine puis au contact superficiel de la poulie (flèches).", v1=True),
  S(38,"052","Pouce à ressaut : installation et position de l'aiguille.")],
 "poignet-canal-carpien": [
  S(38,"055","Voie d'abord 21G : position de la main et de l'aiguille."),
  S(38,"056","Coupe axiale du canal carpien : trajet de l'aiguille (schéma et écho)."),
  G("gc25_p54_f1", "Abord latéral en avant du fléchisseur radial du carpe (FRC) : aiguille (flèche creuse) et diffusion hypoéchogène du produit (têtes de flèche) autour du nerf médian.", v1=True),
  G("gc22_p61_f0", "Fig. 10 : a – position (simulation) ; b – avec le gel pad (GP), trajet prévu (pointillés) en avant du FRC, se terminant en arrière du nerf médian (NM) ; c-d – progression de l'aiguille jusqu'à la face profonde du nerf médian."),
  G("gc30_p69_f0", "Fig. 3 : Échochirurgie du canal carpien (section du ligament carpien transverse au crochet) : a – hydrodissection de l'espace de sécurité entre nerf médian (flèche épaisse) et artère ulnaire (tête de flèche) ; b-d – introduction du crochet, rotation sous le ligament (flèche courbe) et section en coupe longitudinale.")],
 "main-rhizarthrose-pisotriquetrale": [
  S(38,"062","Rhizarthrose, voie d'abord palmaire : repérage « axe commissure ou M2 »."),
  G("gc22_p59_f0", "Fig. 7 : Rhizarthrose. a – voie d'abord sagittale oblique ascendante simulée sur la radiographie ; b-c – avec le gel pad (GP), l'aiguille entre dans l'articulation entre les ostéophytes du trapèze (Tz) et de M1 ; distension synoviale (**) à l'injection de xylocaïne."),
  G("gc25_p53_f2", "Rhizarthrose, abord palmaire en coupe sagittale : a – progression de l'aiguille (flèche creuse) ; b – aiguille dans l'interligne trapèze (T) – M1 ; c – injection intra-articulaire : contenu échogène, mouvements browniens (flèche).", v1=True),
  S(38,"066","Coupe sagittale à la base de l'éminence thénar, dans l'axe du 2e rayon."),
  S(38,"068","Critère de réussite : distension synoviale, mouvements browniens."),
  G("gc25_p55_f1", "Kyste piso-triquétral (coupes axiales) : a – kyste (flèche) au contact du nerf ulnaire (tête de flèche) ; b – affaissement du kyste au cathlon (flèche creuse) en évitant le nerf ulnaire.", v1=True)],
 "main-articulations-mcp-ipp-ipd": [
  S(38,"075","MCP : position de la sonde et de l'aiguille, coupe sagittale dorsale."),
  S(38,"077","MCP : aiguille dans le récessus dorsal (coupe sagittale)."),
  S(38,"078","MCP : diffusion du produit dans le récessus (contour vert)."),
  G("gc25_p52_f1", "Poignet : trajet de l'aiguille par abord dorsal de l'interligne radio-carpien (IRM sagittale T1 ; R : radius, L : lunatum, C : capitatum).", v1=True),
  S(38,"082","IPP / IPD : coupe sagittale cible.")],
 "poignet-kystes-dupuytren": [
  G("gc25_p55_f0", "Fig. 9 (panneaux a et c) : kyste scapho-lunaire dorsal (flèches), en superficie des extenseurs (têtes de flèche). a – approche du cathlon 18G (flèche creuse) par voie dorsale ; c – aspiration.", v1=True),
  G("gc25_p55_f3", "Fig. 9 (panneaux b et d) : b – aiguille retirée, cathéter (flèche creuse) laissé dans le kyste ; d – kyste affaissé en fin de geste.", v1=True),
  G("gc22_p62_f0", "Fig. 11 : Kyste occulte dorsal du carpe, né en arrière du faisceau dorsal du ligament scapho-lunaire (lu, sca). a-b – IRM ; c – repérage écho du kyste (flèches) ; d – aiguille dans le kyste."),
  G("gc22_p62_f1"), G("gc31_p75_f0")],
 "hanche-coxofemorale": [
  G("gc16_p13_f0")],
 "hanche-psoas-pth": [
  G("gc16_p13_f1"),
  G("gc26_p22_f0", "Fig. 10 : Coupe axiale — trajectoire de l'aiguille lors de l'infiltration de la bourse ilio-psoas, au contact d'un débord antérieur de cupule (flèches).", v1=True),
  G("gc21_p56_f0", "Fig. 12 : Double conflit PTH – ilio-psoas (cotyle saillant et vis intrapsoïque) : bilan radiographique et TDM (A-D), repérage échographique (E) et infiltration échoguidée au contact de la vis, sous les vaisseaux iliaques (F).")],
 "hanche-moyen-gluteal": [
  G("gc16_p14_f1", "Fig. 3B : Ponction-infiltration péri-trochantérienne par voie latérale : position de la sonde et trajet de l'aiguille vers une bursite superficielle."),
  G("gc16_p14_f2", "Fig. 3C : Coupe écho coronale : aiguille (têtes de flèche) dans la bursite (flèche), en superficie du moyen glutéal et du grand trochanter (TROCH)."),
  G("gc16_p14_f0", "Fig. 3A : Variante pour une bursite profonde (sous le tendon du moyen glutéal) : trajet de l'aiguille."),
  G("gc21_p57_f0", "Fig. 14 : Moyen glutéal : rupture de la lame latérale (A, B) ; bursopathie trochantérienne superficielle en coupe axiale avec trajet de ponction-infiltration (C, D).")],
 "bassin-piriforme-alcock-pubalgie": [],
 "rachis-hydrodissection-lombaire-esp": [
  G("gc33_p27_f0", "Hydrodissection ESP au niveau du processus transverse : sonde convexe longitudinale à 3–5 cm de la ligne médiane, aiguille dans le plan.", v1=True),
  G("gc33_p25_f0", "Hydrodissection des plans interfasciaux paraspinaux (multifidus, longissimus) en balayage transversal.", v1=True),
  G("gc33_p24_f0", "Balayage axial lombaire (sonde convexe transversale sur la ligne médiane) : muscles paraspinaux et fascia thoraco-lombaire.", v1=True)],
 "genou-articulaire-ha-prp": [
  S(102,"004","Position : genou fléchi ~30°, sonde transversale sur le récessus sous-quadricipital."),
  S(102,"005","Coupe cible : récessus sous-quadricipital.")],
 "genou-kyste-poplite-meniscal": [
  S(102,"026","Kyste poplité (Baker) : cible de l'aspiration / fenestration (cathlon 18G)."),
  S(102,"041","Kyste méniscal : trajet de l'aiguille (pointillés)."),
  S(102,"044","Ponction du kyste : aiguille (flèches).")],
 "genou-periarticulaire-bandelette-patte-oie": [
  G("gc30_p121_f1", "Fig. 6 : Injection échoguidée de PRP dans la partie postérieure du tendon patellaire proximal, aiguille dans le plan (A-B) ; position (C).", v1=True),
  S(102,"024","Abord péri-patellaire : aiguille dans le plan (en bas à gauche)."),
  S(102,"030","Bursite de la patte d'oie : coupe cible (flèche) en regard du plateau tibial interne.")],
 "cheville-articulaire-tibiotalienne": [
  G("gc24_p13_f1", "Fig. 14 : Infiltration antéro-latérale péri-ligamentaire et intra-articulaire (récessus sous le TFA). a – réaction cicatricielle hypervascularisée du ligament talo-fibulaire antérieur (ML : malléole latérale) ; b – aiguille 25G au contact du TFA avec gel pad (**) ; c – pointe sous le TFA dans le récessus articulaire ; d – recul au contact de la face superficielle du ligament."),
  G("gc30_p129_f4")],
 "cheville-gaines-tibial-posterieur-fibulaires": [
  G("gc16_p15_f0", "Fig. 4 : Infiltration de la gaine du tibial postérieur (tendinopathie avec ténosynovite) dans l'axe longitudinal du tendon. A – voie d'abord (simulation, sans asepsie) ; B – aiguille dans la gaine.", v1=True),
  G("gc16_p15_f1", "Fig. 5 : Infiltration de la gaine du tibial postérieur dans l'axe transversal du tendon. A – voie d'abord (simulation, sans asepsie) ; B – aiguille et ténosynovite.", v1=True),
  S(38,"011","Critère de réussite : diffusion du produit dans la gaine synoviale du tibial postérieur.")],
 "cheville-achille-bursite-haut-volume": [
  G("gc16_p16_f1", "Fig. 7A : Bursite pré-achilléenne : sonde en coupe axiale rétro-achilléenne, aiguille introduite par voie latérale."),
  G("gc16_p16_f2", "Fig. 7B : Coupe axiale cible : aiguille (tête de flèche) dans la bursite, en avant du tendon d'Achille."),
  G("gc20_p42_f1"),
  G("gc30_p123_f0", "Fig. 8 : Injection de PRP intratendineuse dans le tendon d'Achille (approche latérale vers médiale, coupe transversale) ; position de la sonde.", v1=True)],
 "pied-aponevrosite-plantaire": [
  G("gc16_p16_f0", v1=True),
  G("gc33_p83_f0", "Fig. 11 : Infiltration (ici PRP, après bloc tibial) de l'aponévrose plantaire, abord sagittal : positionnement de la sonde et de l'aiguille.", v1=True),
  G("gc33_p83_f1", "Fig. 12 : Coupe sagittale correspondante, sans (a) et avec (b) annotations : aiguille au contact de l'aponévrose, calcanéus.", v1=True)],
 "pied-nevrome-morton": [
  S(117,"121","Nerfs interdigitaux : position de la sonde sur l'espace inter-métatarsien et coupe correspondante."),
  S(117,"125","Infiltration du pseudo-névrome de Morton : aiguille (trait blanc) au contact du névrome (bleu), nerf interdigital (jaune)."),
  G("gc30_p100_f1", "Bursite inter-capito-métatarsienne, coupe longitudinale par voie dorsale : A – bourse épaissie (têtes de flèche) ; B – infiltration échoguidée, aiguille (flèches)."),
  G("gc21_p77_f1", "Fig. 6b : Névrome de Morton, coupe coronale du 3e espace inter-métatarsien (M3–M4) : nerf interdigital plantaire commun (flèches).")],
 "cheville-tunnel-tarsien-petits-nerfs": [
  S(117,"031","Tunnel tarsien, approche postéro-médiale : position de la sonde et de l'aiguille."),
  S(117,"032","Image cible : aiguille dans le tunnel tarsien (technique au gel pad)."),
  S(117,"101","Nerf fibulaire superficiel : test anesthésique + infiltration.")],
 "cheville-bloc-nerf-tibial-supra-malleolaire": [
  G("gc33_p80_f0"), G("gc33_p82_f0"), G("gc33_p81_f1"),
  G("gc33_p80_f1", "Fig. 6 : Coupe axiale de référence de l'abord supra-malléolaire médial (cheville gauche), sans (a) et avec (b) annotations : nerf tibial (jaune) en arrière de l'artère (rouge) et des veines (bleu) tibiales postérieures.")],
 "muscles-hematome-tennis-leg": [
  S(110,"043","Ponction-évacuation d'un hématome musculaire : trajet de l'aiguille dans la collection."),
  S(110,"045","Collection ponctionnable, puis ponction."),
  G("gc14_p07_f0", "Ponction d'un hématome : per-ponction (coupe transverse) et après ponction (coupe sagittale)."),
  G("gc29_p28_f1", "Hématome du vaste latéral avant et après évacuation."),
  G("gc26_p55_f1", "Collection inter-aponévrotique liquidienne, compressible sous la sonde : toujours ponctionner un hématome aigu.", v1=True)],
 "parties-molles-corps-etranger-harpon": [
  G("gc30_p110_f0", "Fig. 1a : Exérèse de corps étranger sous échographie — la pince est introduite à travers la peau, guidée par la sonde jusqu'au corps étranger."),
  G("gc30_p111_f2", "Fig. 3c : Extraction d'une épine de palmier : pince (flèches) guidée jusqu'au corps étranger échogène (tête de flèche)."),
  G("gc30_p111_f0", "Fig. 3a : Épine de palmier dans les parties molles de la jambe — corps étranger linéaire échogène, cible de l'extraction."),
  G("gc30_p110_f1", "Fig. 1b : Exérèse à la pince sous sonde type « club de golf »."),
  G("gc16_p17_f0")],
 "parties-molles-biopsie-tumeur": [],
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

# Recadrages d'anonymisation (bandeaux IRM, visage) — coordonnées dans l'image source
CROP = {
    "gc25_p52_f1": (60, 40, 760, 505),   # bandeaux IRM (nom/âge patient, machine)
    "gc23_p53_f0": (0, 0, 495, 449),     # visage du patient
}

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
        if src in CROP: im = im.crop(CROP[src])
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
