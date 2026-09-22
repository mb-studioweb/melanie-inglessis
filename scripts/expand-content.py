#!/usr/bin/env python3
"""Expand verified Work / People / News for Mélanie Inglessis portfolio."""
from __future__ import annotations

import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "template" / "data"
IMG = ROOT / "template" / "images"
SOURCES = IMG / "SOURCES.json"

UA = {
    "User-Agent": "Mozilla/5.0 (compatible; MBStudioPortfolioBot/1.0; +concept)",
    "Accept": "text/html,application/xhtml+xml,image/*,*/*",
}


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def save(name, data):
    (DATA / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def norm_cats(cats):
    out = []
    for c in cats or []:
        c = c.upper().replace("COVER", "COVERS").replace("CAMPAIGN", "CAMPAIGNS")
        if c in ("PRESS", "TUTORIAL"):
            c = "MOTION" if c == "TUTORIAL" else "RED CARPET"
        if c == "COVERS" and "COVERS" not in out:
            out.append("COVERS")
        elif c in ("EDITORIAL", "COVERS", "RED CARPET", "CAMPAIGNS", "MOTION") and c not in out:
            out.append(c)
    return out or ["RED CARPET"]


NEW_PROJECTS = [
    {
        "slug": "emmys-jenna-ortega-2025",
        "title": "75th Primetime Emmy Awards",
        "talent": "Jenna Ortega",
        "year": "2025",
        "month": "September",
        "categories": ["RED CARPET"],
        "publication": "Variety",
        "peopleSlugs": ["jenna-ortega"],
        "credits": {"Makeup": "Mélanie Inglessis using Dior Beauty", "Talent": "Jenna Ortega"},
        "sourceUrl": "https://variety.com/2025/shopping/news/jenna-ortega-emmys-makeup-products-buy-online-1236519318/",
        "summary": "Gothic Emmys glam with whisper-thin brows, smoky kohl eye, baby-blue shadow and a deep plum lip — product approach quoted by Inglessis.",
        "alt": "Jenna Ortega at the 2025 Emmy Awards, makeup by Mélanie Inglessis",
        "featured": True,
    },
    {
        "slug": "ballerina-premiere-ana-de-armas-2025",
        "title": "Ballerina London Premiere",
        "talent": "Ana de Armas",
        "year": "2025",
        "month": "May",
        "categories": ["RED CARPET"],
        "publication": "Harper's Bazaar UK",
        "peopleSlugs": ["ana-de-armas"],
        "credits": {"Makeup": "Mélanie Inglessis using Estée Lauder", "Talent": "Ana de Armas"},
        "sourceUrl": "https://www.harpersbazaar.com/uk/beauty/make-up-nails/a64822567/getting-ready-with-ana-de-armas-ballerina-premiere/",
        "summary": "Getting-ready beauty for the London Ballerina premiere — luminous skin and a classic Estée Lauder red lip for Louis Vuitton.",
        "alt": "Ana de Armas at the Ballerina London premiere, makeup by Mélanie Inglessis",
        "featured": True,
    },
    {
        "slug": "oscars-ana-de-armas-2025",
        "title": "97th Academy Awards",
        "talent": "Ana de Armas",
        "year": "2025",
        "month": "March",
        "categories": ["RED CARPET"],
        "publication": "Harper's Bazaar",
        "peopleSlugs": ["ana-de-armas"],
        "credits": {"Makeup": "Mélanie Inglessis for Estée Lauder", "Talent": "Ana de Armas"},
        "sourceUrl": "https://www.harpersbazaar.com/beauty/makeup/g64001522/best-hair-makeup-beauty-oscars-2025/",
        "summary": "Statuesque Oscars beauty for Ana de Armas with Estée Lauder — listed among Harper’s Bazaar’s best looks of the night.",
        "alt": "Ana de Armas at the 2025 Oscars, makeup by Mélanie Inglessis",
        "featured": True,
    },
    {
        "slug": "critics-choice-maisy-stella-2025",
        "title": "Critics Choice Awards",
        "talent": "Maisy Stella",
        "year": "2025",
        "month": "February",
        "categories": ["RED CARPET"],
        "publication": "Who What Wear",
        "peopleSlugs": ["maisy-stella"],
        "credits": {
            "Makeup": "Mélanie Inglessis",
            "Hair": "Sylvia Wheeler",
            "Stylist": "Tara Swennen",
            "Talent": "Maisy Stella",
        },
        "sourceUrl": "https://www.whowhatwear.com/fashion/celebrity/maisy-stella-critics-choice-awards",
        "summary": "Fresh, timeless Critics Choice glam for Maisy Stella — product breakdown published by Who What Wear.",
        "alt": "Maisy Stella at the Critics Choice Awards, makeup by Mélanie Inglessis",
        "featured": True,
    },
    {
        "slug": "sleek-leslie-bibb-2025",
        "title": "In Full Bloom",
        "talent": "Leslie Bibb",
        "year": "2025",
        "month": "March",
        "categories": ["EDITORIAL"],
        "publication": "Sleek Magazine",
        "peopleSlugs": ["leslie-bibb"],
        "credits": {
            "Photography": "Emma Louise Swanson",
            "Styling": "SK Tang",
            "Hair": "John D",
            "Makeup": "Mélanie Inglessis",
            "Talent": "Leslie Bibb",
        },
        "sourceUrl": "https://www.sleek-mag.com/article/leslie-bibb-starring-in-white-lotus-in-full-bloom/",
        "summary": "Sleek Magazine editorial timed to White Lotus — makeup credited to Mélanie Inglessis.",
        "alt": "Leslie Bibb for Sleek Magazine, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "academy-museum-gala-olivia-wilde-2024",
        "title": "Academy Museum Gala",
        "talent": "Olivia Wilde",
        "year": "2024",
        "month": "October",
        "categories": ["RED CARPET"],
        "publication": "NewBeauty",
        "peopleSlugs": ["olivia-wilde"],
        "credits": {"Makeup": "Mélanie Inglessis", "Talent": "Olivia Wilde"},
        "sourceUrl": "https://www.newbeauty.com/view/olivia-wilde-tirtir-foundation-academy-museum-gala",
        "summary": "Flawless skin, subtle rock-and-roll eye and a nude lip — Inglessis quotes TIRTIR as a red-carpet hero product.",
        "alt": "Olivia Wilde at the Academy Museum Gala, makeup by Mélanie Inglessis",
        "featured": True,
    },
    {
        "slug": "beetlejuice-press-tour-2024",
        "title": "Beetlejuice Beetlejuice Press Tour",
        "talent": "Jenna Ortega",
        "year": "2024",
        "month": "August",
        "categories": ["RED CARPET"],
        "publication": "NewBeauty",
        "peopleSlugs": ["jenna-ortega"],
        "credits": {
            "Makeup": "Mélanie Inglessis",
            "Styling": "Enrique Melendez",
            "Hair": "Bobby Eliot",
            "Talent": "Jenna Ortega",
        },
        "sourceUrl": "https://www.newbeauty.com/view/jenna-ortega-beetlejuice-press-tour-makeup-looks",
        "summary": "Soft-goth press-tour beauty across London, Venice and NYC — documented by NewBeauty.",
        "alt": "Jenna Ortega Beetlejuice Beetlejuice press tour beauty, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "emmys-jenna-ortega-2024",
        "title": "75th Primetime Emmy Awards (delayed)",
        "talent": "Jenna Ortega",
        "year": "2024",
        "month": "January",
        "categories": ["RED CARPET"],
        "publication": "Glamour",
        "peopleSlugs": ["jenna-ortega"],
        "credits": {"Makeup": "Mélanie Inglessis using Dior Beauty", "Talent": "Jenna Ortega"},
        "sourceUrl": "https://www.glamour.com/story/jenna-ortega-emmys-look-2024",
        "summary": "Romantic Dior Beauty Emmys look — rosy cheeks, diffused purple smoky lids and Rouge Dior Daisy Plum.",
        "alt": "Jenna Ortega at the delayed 2023 Emmy Awards, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "vf-oscars-afterparty-olivia-wilde-2018",
        "title": "Vanity Fair Oscars After Party",
        "talent": "Olivia Wilde",
        "year": "2018",
        "month": "March",
        "categories": ["RED CARPET"],
        "publication": "Vogue",
        "peopleSlugs": ["olivia-wilde"],
        "credits": {"Makeup": "Mélanie Inglessis", "Hair": "Lona Vigi", "Talent": "Olivia Wilde"},
        "sourceUrl": "https://www.vogue.com/article/olivia-wilde-oscars-vanity-fair-after-party-los-angeles-roberto-cavalli-gold-dress-2018",
        "summary": "Brown smoky eye with a feline flick for Roberto Cavalli Couture — getting-ready diary in Vogue.",
        "alt": "Olivia Wilde getting ready for the Vanity Fair Oscars after party, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "oscars-olivia-wilde-2016",
        "title": "Academy Awards 2016",
        "talent": "Olivia Wilde",
        "year": "2016",
        "month": "February",
        "categories": ["RED CARPET"],
        "publication": "The Hollywood Reporter",
        "peopleSlugs": ["olivia-wilde"],
        "credits": {"Makeup": "Mélanie Inglessis", "Talent": "Olivia Wilde"},
        "sourceUrl": "https://www.hollywoodreporter.com/movies/movie-news/olivia-wildes-makeup-2016-oscars-871430/",
        "summary": "Ethereal bronzy peach-and-gold eye for Valentino Couture — step-by-step with Inglessis in THR.",
        "alt": "Olivia Wilde at the 2016 Oscars, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "met-gala-olivia-wilde-2016",
        "title": "Met Gala 2016",
        "talent": "Olivia Wilde",
        "year": "2016",
        "month": "May",
        "categories": ["RED CARPET"],
        "publication": "The Hollywood Reporter",
        "peopleSlugs": ["olivia-wilde"],
        "credits": {"Makeup": "Mélanie Inglessis", "Talent": "Olivia Wilde"},
        "sourceUrl": "https://www.hollywoodreporter.com/lifestyle/style/how-olivia-wildes-metallic-smoky-890165/",
        "summary": "Metallic “smoky eyes on steroids” for Michael Kors — chromatic eye breakdown in THR.",
        "alt": "Olivia Wilde at the 2016 Met Gala, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "met-gala-olivia-wilde-2013",
        "title": "Met Gala 2013",
        "talent": "Olivia Wilde",
        "year": "2013",
        "month": "May",
        "categories": ["RED CARPET"],
        "publication": "Allure",
        "peopleSlugs": ["olivia-wilde"],
        "credits": {"Makeup": "Mélanie Inglessis", "Talent": "Olivia Wilde"},
        "sourceUrl": "https://www.allure.com/story/behind-the-scenes-olivia-wilde-makeup-met-ball-2013",
        "summary": "Stacked black-and-white eyeliner for custom Calvin Klein — BTS beauty with Inglessis quotes.",
        "alt": "Olivia Wilde at the 2013 Met Gala, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "golden-globes-olivia-wilde-2014",
        "title": "Golden Globe Awards 2014",
        "talent": "Olivia Wilde",
        "year": "2014",
        "month": "January",
        "categories": ["RED CARPET"],
        "publication": "The Hollywood Reporter",
        "peopleSlugs": ["olivia-wilde"],
        "credits": {"Makeup": "Mélanie Inglessis", "Hair": "Lona Vigi", "Talent": "Olivia Wilde"},
        "sourceUrl": "https://www.hollywoodreporter.com/news/general-news/golden-globes-2014-beauty-olivia-670610/",
        "summary": "Dewy skin and a purple smoky eye for emerald Gucci — Revlon steps published by THR.",
        "alt": "Olivia Wilde at the 2014 Golden Globes, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "golden-globes-kate-hudson-2016",
        "title": "Golden Globe Awards 2016",
        "talent": "Kate Hudson",
        "year": "2016",
        "month": "January",
        "categories": ["RED CARPET"],
        "publication": "E!",
        "peopleSlugs": ["kate-hudson"],
        "credits": {"Makeup": "Mélanie Inglessis", "Talent": "Kate Hudson"},
        "sourceUrl": "https://www.eonline.com/news/730048/kate-hudson-s-signature-glow-how-to-get-her-golden-globes-2016-makeup-look",
        "summary": "Signature Studio 54 dewy glow for sequin Michael Kors — Chantecaille bronzer/highlighter steps from Inglessis.",
        "alt": "Kate Hudson at the 2016 Golden Globes, makeup by Mélanie Inglessis",
        "featured": True,
    },
    {
        "slug": "fabletics-ss2015-kate-hudson",
        "title": "Fabletics Spring/Summer 2015",
        "talent": "Kate Hudson",
        "year": "2015",
        "month": "January",
        "categories": ["CAMPAIGNS"],
        "publication": "Fabletics",
        "peopleSlugs": ["kate-hudson"],
        "credits": {
            "Photography": "Benny Horne",
            "Hair": "Chris McMillan",
            "Makeup": "Mélanie Inglessis",
            "Talent": "Kate Hudson",
        },
        "sourceUrl": "https://www.designscene.net/2015/01/kate-hudsons-fabletics-spring-summer-2015.html",
        "summary": "Fabletics S/S 2015 advertising campaign with Kate Hudson — makeup credited to Mélanie Inglessis.",
        "alt": "Kate Hudson for Fabletics Spring/Summer 2015, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "klossy-met-gala-makeup-test-2019",
        "title": "Klossy Met Gala Makeup Test",
        "talent": "Karlie Kloss",
        "year": "2019",
        "categories": ["MOTION"],
        "publication": "Klossy",
        "peopleSlugs": ["karlie-kloss"],
        "credits": {"Makeup": "Mélanie Inglessis", "Talent": "Karlie Kloss"},
        "sourceUrl": "https://www.forwardartists.com/makeup/melanie-inglessis-press",
        "summary": "On-camera Met Gala makeup test & tutorial for Klossy — listed on Forward Artists’ press / on-camera page.",
        "alt": "Karlie Kloss Met Gala makeup test with Mélanie Inglessis for Klossy",
        "featured": False,
    },
    {
        "slug": "oscars-ruth-negga-2017",
        "title": "Academy Awards 2017",
        "talent": "Ruth Negga",
        "year": "2017",
        "month": "February",
        "categories": ["RED CARPET"],
        "publication": "Healthista",
        "peopleSlugs": ["ruth-negga"],
        "credits": {"Makeup": "Mélanie Inglessis", "Styling": "Karla Welch", "Talent": "Ruth Negga"},
        "sourceUrl": "https://www.healthista.com/ruth-neggas-makeup-artist-reveals-get-red-carpet-look-exclusive/",
        "summary": "Earthy matte smoky eye and matte ruby lip for Valentino — Chanel product exclusive with Inglessis.",
        "alt": "Ruth Negga at the 2017 Oscars, makeup by Mélanie Inglessis",
        "featured": True,
    },
    {
        "slug": "golden-globes-ruth-negga-2017",
        "title": "Golden Globe Awards 2017",
        "talent": "Ruth Negga",
        "year": "2017",
        "month": "January",
        "categories": ["RED CARPET"],
        "publication": "The Hollywood Reporter",
        "peopleSlugs": ["ruth-negga"],
        "credits": {"Makeup": "Mélanie Inglessis", "Talent": "Ruth Negga"},
        "sourceUrl": "https://www.hollywoodreporter.com/lifestyle/style/golden-globes-2017-ruth-negga-beauty-look-962989/",
        "summary": "Skin-focused glow with a soft plum/purple smoky eye for metallic Louis Vuitton Couture.",
        "alt": "Ruth Negga at the 2017 Golden Globes, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "met-gala-ruth-negga-2017",
        "title": "Met Gala 2017",
        "talent": "Ruth Negga",
        "year": "2017",
        "month": "May",
        "categories": ["RED CARPET"],
        "publication": "The Hollywood Reporter",
        "peopleSlugs": ["ruth-negga"],
        "credits": {"Makeup": "Mélanie Inglessis", "Talent": "Ruth Negga"},
        "sourceUrl": "https://www.hollywoodreporter.com/lifestyle/style/ruth-neggas-met-gala-2017-makeup-999556/",
        "summary": "Minimal dewy monochrome for Valentino Couture — Japanese aesthetic interpretation by Inglessis.",
        "alt": "Ruth Negga at the 2017 Met Gala, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "oscars-rosamund-pike-2015",
        "title": "Academy Awards 2015",
        "talent": "Rosamund Pike",
        "year": "2015",
        "month": "February",
        "categories": ["RED CARPET"],
        "publication": "Allure",
        "peopleSlugs": ["rosamund-pike"],
        "credits": {"Makeup": "Mélanie Inglessis", "Talent": "Rosamund Pike"},
        "sourceUrl": "https://www.allure.com/story/rosamund-pike-oscars-beauty-look-2015",
        "summary": "Grace Kelly–inspired soft earth tones for custom Givenchy — exclusive Allure beauty prep with Inglessis.",
        "alt": "Rosamund Pike at the 2015 Oscars, makeup by Mélanie Inglessis",
        "featured": True,
    },
    {
        "slug": "golden-globes-rosamund-pike-2019",
        "title": "Golden Globe Awards 2019",
        "talent": "Rosamund Pike",
        "year": "2019",
        "month": "January",
        "categories": ["RED CARPET"],
        "publication": "Us Weekly",
        "peopleSlugs": ["rosamund-pike"],
        "credits": {"Makeup": "Mélanie Inglessis", "Talent": "Rosamund Pike"},
        "sourceUrl": "https://www.usmagazine.com/stylish/news/get-tressed-with-us-podcast-melanie-inglessis-golden-globes-makeup/",
        "summary": "Her-only-better Globes glam with Chantecaille lip and cheek — Inglessis interviewed on Get Tressed.",
        "alt": "Rosamund Pike at the 2019 Golden Globes, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "thr-cannes-natalie-portman-2015",
        "title": "The Hollywood Reporter Cannes Cover",
        "talent": "Natalie Portman",
        "year": "2015",
        "month": "May",
        "categories": ["COVERS", "EDITORIAL"],
        "publication": "The Hollywood Reporter",
        "peopleSlugs": ["natalie-portman"],
        "credits": {"Photography": "Miller Mobley", "Makeup": "Mélanie Inglessis", "Talent": "Natalie Portman"},
        "sourceUrl": "https://www.hollywoodreporter.com/news/general-news/how-get-natalie-portmans-gorgeous-793887/",
        "summary": "Natural healthy-skin cover look for THR’s Cannes issue — Dior and Make Up For Ever product notes.",
        "alt": "Natalie Portman for The Hollywood Reporter Cannes cover, makeup by Mélanie Inglessis",
        "featured": True,
    },
    {
        "slug": "golden-globes-natalie-portman-2018",
        "title": "Golden Globe Awards 2018",
        "talent": "Natalie Portman",
        "year": "2018",
        "month": "January",
        "categories": ["RED CARPET"],
        "publication": "Haute Living",
        "peopleSlugs": ["natalie-portman"],
        "credits": {"Makeup": "Mélanie Inglessis", "Talent": "Natalie Portman"},
        "sourceUrl": "https://hauteliving.com/hautebeauty/627611/4-golden-globes-beauty-looks-love/",
        "summary": "Smoky Dior eyes and nude Rouge Dior Liquid lip — Dior Beauty Globes look attributed to Inglessis.",
        "alt": "Natalie Portman at the 2018 Golden Globes, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "la-dance-project-gala-natalie-portman-2018",
        "title": "L.A. Dance Project Gala",
        "talent": "Natalie Portman",
        "year": "2018",
        "month": "October",
        "categories": ["RED CARPET"],
        "publication": "Us Weekly",
        "peopleSlugs": ["natalie-portman"],
        "credits": {"Makeup": "Mélanie Inglessis", "Talent": "Natalie Portman"},
        "sourceUrl": "https://www.usmagazine.com/stylish/news/natalie-portmans-dior-red-lipstick-for-holiday-2018-how-to/",
        "summary": "Lady-in-red Dior Ultra Rouge #777 Ultra Star with glow skin and mascara-only eyes.",
        "alt": "Natalie Portman at the L.A. Dance Project Gala, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "golden-globes-lea-michele-2013",
        "title": "Golden Globe Awards 2013",
        "talent": "Lea Michele",
        "year": "2013",
        "month": "January",
        "categories": ["RED CARPET"],
        "publication": "Teen Vogue",
        "peopleSlugs": ["lea-michele"],
        "credits": {"Makeup": "Mélanie Inglessis", "Talent": "Lea Michele"},
        "sourceUrl": "https://www.teenvogue.com/gallery/lea-michele-golden-globes-makeup",
        "summary": "Goddess-like dewy glow for a white sequined gown — Armani Luminous Silk steps in Teen Vogue.",
        "alt": "Lea Michele at the 2013 Golden Globes, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "emmys-lea-michele-2011",
        "title": "Primetime Emmy Awards 2011",
        "talent": "Lea Michele",
        "year": "2011",
        "month": "September",
        "categories": ["RED CARPET"],
        "publication": "Teen Vogue",
        "peopleSlugs": ["lea-michele"],
        "credits": {"Makeup": "Mélanie Inglessis", "Talent": "Lea Michele"},
        "sourceUrl": "https://www.teenvogue.com/gallery/celebrity-emmy-beauty-looks",
        "summary": "Classic red-carpet makeup for Marchesa — Lancôme-heavy breakdown quoted from Inglessis.",
        "alt": "Lea Michele at the 2011 Emmy Awards, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "motion-rebel-wilson-afterpay",
        "title": "Afterpay",
        "talent": "Rebel Wilson",
        "year": None,
        "categories": ["MOTION", "CAMPAIGNS"],
        "publication": "Afterpay",
        "peopleSlugs": ["rebel-wilson"],
        "credits": {"Makeup": "Mélanie Inglessis", "Director": "Martin Granger", "Talent": "Rebel Wilson"},
        "sourceUrl": "https://www.forwardartists.com/makeup/melanie-inglessis-motion",
        "summary": "Commercial credit listed on Forward Artists’ motion page — Dir. Martin Granger.",
        "alt": "Rebel Wilson for Afterpay, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "motion-rebel-wilson-match",
        "title": "Match.com",
        "talent": "Rebel Wilson",
        "year": None,
        "categories": ["MOTION", "CAMPAIGNS"],
        "publication": "Match.com",
        "peopleSlugs": ["rebel-wilson"],
        "credits": {"Makeup": "Mélanie Inglessis", "Director": "Neal Brennan", "Talent": "Rebel Wilson"},
        "sourceUrl": "https://www.forwardartists.com/makeup/melanie-inglessis-motion",
        "summary": "Commercial credit listed on Forward Artists’ motion page — Dir. Neal Brennan.",
        "alt": "Rebel Wilson for Match.com, makeup by Mélanie Inglessis",
        "featured": False,
    },
    {
        "slug": "motion-rebel-wilson-olly",
        "title": "OLLY",
        "talent": "Rebel Wilson",
        "year": None,
        "categories": ["MOTION", "CAMPAIGNS"],
        "publication": "OLLY",
        "peopleSlugs": ["rebel-wilson"],
        "credits": {"Makeup": "Mélanie Inglessis", "Director": "Emma Westenberg", "Talent": "Rebel Wilson"},
        "sourceUrl": "https://www.forwardartists.com/makeup/melanie-inglessis-motion",
        "summary": "Commercial credit listed on Forward Artists’ motion page — Dir. Emma Westenberg.",
        "alt": "Rebel Wilson for OLLY, makeup by Mélanie Inglessis",
        "featured": False,
    },
]

NEW_PEOPLE = [
    {
        "slug": "maisy-stella",
        "name": "Maisy Stella",
        "profession": "Actor",
        "relationshipStatus": "current",
        "summary": "Recent red-carpet collaboration including the 2025 Critics Choice Awards — covered by Who What Wear and Forward Artists press.",
        "sourceUrls": [
            "https://www.whowhatwear.com/fashion/celebrity/maisy-stella-critics-choice-awards",
            "https://www.forwardartists.com/makeup/melanie-inglessis-press",
        ],
        "heroImageSource": "https://www.whowhatwear.com/fashion/celebrity/maisy-stella-critics-choice-awards",
    },
    {
        "slug": "leslie-bibb",
        "name": "Leslie Bibb",
        "profession": "Actor",
        "relationshipStatus": "current",
        "summary": "2025 Sleek Magazine editorial makeup credit timed to White Lotus.",
        "sourceUrls": [
            "https://www.sleek-mag.com/article/leslie-bibb-starring-in-white-lotus-in-full-bloom/",
        ],
        "heroImageSource": "https://www.sleek-mag.com/article/leslie-bibb-starring-in-white-lotus-in-full-bloom/",
    },
    {
        "slug": "adria-arjona",
        "name": "Adria Arjona",
        "profession": "Actor",
        "relationshipStatus": "current",
        "summary": "Giorgio Armani Beauty Luminous Silk campaign with Madisin Ryan — Forward Artists motion credit.",
        "sourceUrls": ["https://www.forwardartists.com/makeup/melanie-inglessis-motion"],
        "heroImageSource": "https://www.forwardartists.com/makeup/melanie-inglessis-motion",
    },
    {
        "slug": "eva-longoria",
        "name": "Eva Longoria",
        "profession": "Actor",
        "relationshipStatus": "archive",
        "summary": "L’Oréal Paris campaign with Aja Naomi King — Forward Artists motion credit.",
        "sourceUrls": ["https://www.forwardartists.com/makeup/melanie-inglessis-motion"],
        "heroImageSource": "https://www.forwardartists.com/makeup/melanie-inglessis-motion",
    },
    {
        "slug": "rebel-wilson",
        "name": "Rebel Wilson",
        "profession": "Actor / Comedian",
        "relationshipStatus": "archive",
        "summary": "Three Forward Artists motion commercials: Afterpay, Match.com and OLLY.",
        "sourceUrls": ["https://www.forwardartists.com/makeup/melanie-inglessis-motion"],
        "heroImageSource": "https://www.forwardartists.com/makeup/melanie-inglessis-motion",
    },
]

NEW_NEWS = [
    {
        "date": "2025-10",
        "slug": "the-cut-subcultures-2025",
        "title": "The Cut: Inspired by Subcultures",
        "summary": "Mélanie Inglessis on psychobilly roots, ethereal-goth language and Jenna Ortega as muse — The Cut muses interview.",
        "sourceUrl": "https://www.thecut.com/article/jenna-ortega-makeup-artist-melanie-inglessis-inspired-by-subcultures.html",
        "category": "Press",
        "projectSlug": None,
    },
    {
        "date": "2025-09",
        "slug": "emmys-2025-variety",
        "title": "Gothic dream at the 2025 Emmys",
        "summary": "Variety shops Jenna Ortega’s Emmys products with quotes from @melaniemakeup and Dior Beauty notes.",
        "sourceUrl": "https://variety.com/2025/shopping/news/jenna-ortega-emmys-makeup-products-buy-online-1236519318/",
        "category": "Red carpet",
        "projectSlug": "emmys-jenna-ortega-2025",
    },
    {
        "date": "2025-07",
        "slug": "glamour-wednesday-premiere",
        "title": "Dark feminine energy at Wednesday premiere",
        "summary": "Glamour details Inglessis’ sculpted gothic look — radiant skin, smoky lids and bleached brows.",
        "sourceUrl": "https://www.glamour.com/story/jenna-ortega-wednesday-premiere-makeup",
        "category": "Red carpet",
        "projectSlug": "wednesday-s2-premiere-2025",
    },
    {
        "date": "2025-05",
        "slug": "ballerina-premiere-hb",
        "title": "Getting ready: Ana de Armas × Ballerina",
        "summary": "Harper’s Bazaar UK exclusive GRWM for the London premiere — Estée Lauder red lip technique.",
        "sourceUrl": "https://www.harpersbazaar.com/uk/beauty/make-up-nails/a64822567/getting-ready-with-ana-de-armas-ballerina-premiere/",
        "category": "Red carpet",
        "projectSlug": "ballerina-premiere-ana-de-armas-2025",
    },
    {
        "date": "2025-03",
        "slug": "oscars-2025-hb",
        "title": "Best beauty looks at the 2025 Oscars",
        "summary": "Harper’s Bazaar includes Ana de Armas / Inglessis for Estée Lauder among the night’s best looks.",
        "sourceUrl": "https://www.harpersbazaar.com/beauty/makeup/g64001522/best-hair-makeup-beauty-oscars-2025/",
        "category": "Red carpet",
        "projectSlug": "oscars-ana-de-armas-2025",
    },
    {
        "date": "2025-03",
        "slug": "sleek-leslie-bibb",
        "title": "Leslie Bibb — In Full Bloom",
        "summary": "Sleek Magazine editorial with Mélanie Inglessis makeup credit.",
        "sourceUrl": "https://www.sleek-mag.com/article/leslie-bibb-starring-in-white-lotus-in-full-bloom/",
        "category": "Editorial",
        "projectSlug": "sleek-leslie-bibb-2025",
    },
    {
        "date": "2025-02",
        "slug": "maisy-stella-critics-choice",
        "title": "Maisy Stella at Critics Choice",
        "summary": "Who What Wear covers timeless Critics Choice glam credited to Mélanie Inglessis.",
        "sourceUrl": "https://www.whowhatwear.com/fashion/celebrity/maisy-stella-critics-choice-awards",
        "category": "Red carpet",
        "projectSlug": "critics-choice-maisy-stella-2025",
    },
    {
        "date": "2024-10",
        "slug": "olivia-wilde-academy-museum",
        "title": "Olivia Wilde × Academy Museum Gala",
        "summary": "NewBeauty: TIRTIR cushion as red-carpet hero product with quotes from Inglessis.",
        "sourceUrl": "https://www.newbeauty.com/view/olivia-wilde-tirtir-foundation-academy-museum-gala",
        "category": "Red carpet",
        "projectSlug": "academy-museum-gala-olivia-wilde-2024",
    },
    {
        "date": "2024-08",
        "slug": "beetlejuice-soft-goth",
        "title": "Soft goth on Beetlejuice press tour",
        "summary": "NewBeauty roundup of Jenna Ortega’s soft-goth press looks with Inglessis.",
        "sourceUrl": "https://www.newbeauty.com/view/jenna-ortega-beetlejuice-press-tour-makeup-looks",
        "category": "Press",
        "projectSlug": "beetlejuice-press-tour-2024",
    },
    {
        "date": "2024-01",
        "slug": "emmys-2024-glamour",
        "title": "Elegant Emmys beauty (delayed 2023)",
        "summary": "Glamour beauty breakdown for Jenna Ortega’s delayed Emmys — Daisy Plum lip, Soft Cashmere eyes.",
        "sourceUrl": "https://www.glamour.com/story/jenna-ortega-emmys-look-2024",
        "category": "Red carpet",
        "projectSlug": "emmys-jenna-ortega-2024",
    },
    {
        "date": "2020-02",
        "slug": "makeup-artistry-dinner-2020",
        "title": "Honored at Makeup Artistry Dinner",
        "summary": "Variety: Olivia Wilde helps honor Mélanie Inglessis — “She’s a healer.” Listed on Forward Artists press.",
        "sourceUrl": "https://variety.com/2020/scene/news/maya-rudolph-rachel-mcadams-and-olivia-wilde-help-honor-their-makeup-artists-1203493748/",
        "category": "Press",
        "projectSlug": None,
    },
]

# Wikimedia / public portrait fallbacks for new people heroes (concept mockup)
PEOPLE_WIKI = {
    "maisy-stella": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Maisy_Stella_2019.jpg/800px-Maisy_Stella_2019.jpg",
    "leslie-bibb": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Leslie_Bibb_by_Gage_Skidmore.jpg/800px-Leslie_Bibb_by_Gage_Skidmore.jpg",
    "adria-arjona": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Adria_Arjona_by_Gage_Skidmore.jpg/800px-Adria_Arjona_by_Gage_Skidmore.jpg",
    "eva-longoria": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Eva_Longoria_Cannes_2015.jpg/800px-Eva_Longoria_Cannes_2015.jpg",
    "rebel-wilson": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Rebel_Wilson_2019_by_Gage_Skidmore.jpg/800px-Rebel_Wilson_2019_by_Gage_Skidmore.jpg",
}


def fetch_bytes(url: str, retries=3):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.read(), r.headers.get_content_type()
        except Exception as e:
            last = e
            time.sleep(1.2 * (i + 1))
    raise last  # type: ignore


def og_image(url: str) -> str | None:
    try:
        html, _ = fetch_bytes(url)
        text = html.decode("utf-8", errors="ignore")
        for pat in [
            r'property=["\']og:image["\']\s+content=["\']([^"\']+)',
            r'content=["\']([^"\']+)["\']\s+property=["\']og:image["\']',
            r'name=["\']twitter:image["\']\s+content=["\']([^"\']+)',
        ]:
            m = re.search(pat, text, re.I)
            if m:
                return m.group(1).replace("&amp;", "&")
    except Exception:
        return None
    return None


def write_image(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def ensure_placeholder(path: Path, label: str):
    """Minimal JPEG via Pillow if available, else skip."""
    if path.exists() and path.stat().st_size > 1000:
        return
    try:
        from PIL import Image, ImageDraw, ImageFont

        img = Image.new("RGB", (1200, 1500), (18, 18, 18))
        d = ImageDraw.Draw(img)
        d.text((40, 40), label[:40], fill=(220, 220, 220))
        path.parent.mkdir(parents=True, exist_ok=True)
        img.save(path, "JPEG", quality=85)
    except Exception:
        path.parent.mkdir(parents=True, exist_ok=True)
        # tiny valid jpeg
        path.write_bytes(
            bytes.fromhex(
                "ffd8ffe000104a46494600010100000100010000ffdb004300080606070605080707"
                "070909080a0c140d0c0b0b0c1912130f141d1a1f1e1d1a1c1c20242e2720222c231c"
                "1c2837292c30313434341f27393d38323c2e333432ffdb0043010909090c0b0c180d"
                "0d1832211c2132323232323232323232323232323232323232323232323232323232"
                "323232323232323232323232323232323232323232ffc00011080001000103011100"
                "0211031101ffc40014000100000000000000000000000000000000ffc40014100100"
                "000000000000000000000000000000ffda000c0301000210031000003f00bf80ffd9"
            )
        )


def main():
    projects = load("projects.json")
    people = load("people.json")
    news = load("news.json")
    sources = json.loads(SOURCES.read_text(encoding="utf-8")) if SOURCES.exists() else []
    if not isinstance(sources, list):
        sources = []

    existing_slugs = {p["slug"] for p in projects}
    next_id = max(int(re.sub(r"\D", "", p.get("id") or "0") or 0) for p in projects) + 1
    order = max((p.get("order") or 0) for p in projects) + 1

    added_projects = []
    for raw in NEW_PROJECTS:
        if raw["slug"] in existing_slugs:
            continue
        hero = f"images/projects/{raw['slug']}/hero.jpg"
        item = {
            "id": f"p{next_id:02d}",
            "slug": raw["slug"],
            "title": raw["title"],
            "talent": raw["talent"],
            "year": raw.get("year"),
            "month": raw.get("month"),
            "categories": norm_cats(raw.get("categories")),
            "publication": raw.get("publication"),
            "featured": bool(raw.get("featured")),
            "order": order,
            "peopleSlugs": raw.get("peopleSlugs") or [],
            "heroImage": hero,
            "galleryImages": [],
            "credits": raw.get("credits") or {"Makeup": "Mélanie Inglessis"},
            "sourceUrl": raw["sourceUrl"],
            "imageSourceUrl": raw["sourceUrl"],
            "alt": raw.get("alt") or f"{raw['talent']} — {raw['title']}, makeup by Mélanie Inglessis",
            "summary": raw["summary"],
        }
        projects.append(item)
        added_projects.append(item)
        next_id += 1
        order += 1
        existing_slugs.add(raw["slug"])

    # Update people projectSlugs from all projects
    people_by_slug = {p["slug"]: p for p in people}
    next_person = max(int(re.sub(r"\D", "", p.get("id") or "0") or 0) for p in people) + 1
    person_order = max((p.get("order") or 0) for p in people) + 1

    for raw in NEW_PEOPLE:
        if raw["slug"] in people_by_slug:
            continue
        hero = f"images/people/{raw['slug']}/hero.jpg"
        person = {
            "id": f"person-{next_person:02d}",
            "slug": raw["slug"],
            "name": raw["name"],
            "profession": raw["profession"],
            "relationshipStatus": raw["relationshipStatus"],
            "order": person_order,
            "heroImage": hero,
            "heroImageSource": raw.get("heroImageSource") or (raw.get("sourceUrls") or [""])[0],
            "summary": raw["summary"],
            "projectSlugs": [],
            "sourceUrls": raw.get("sourceUrls") or [],
        }
        people.append(person)
        people_by_slug[raw["slug"]] = person
        next_person += 1
        person_order += 1

    # Rebuild projectSlugs for every person from projects.peopleSlugs
    for person in people:
        slugs = []
        for p in projects:
            if person["slug"] in (p.get("peopleSlugs") or []):
                slugs.append(p["slug"])
        # keep stable: featured/recent first by sorting projects order
        person["projectSlugs"] = slugs
        # enrich sourceUrls with project sources
        urls = list(person.get("sourceUrls") or [])
        for p in projects:
            if p["slug"] in slugs and p.get("sourceUrl") and p["sourceUrl"] not in urls:
                urls.append(p["sourceUrl"])
        person["sourceUrls"] = urls[:12]

    # Link motion-armani to adria, motion-loreal to eva
    if "adria-arjona" in people_by_slug:
        for p in projects:
            if p["slug"] == "motion-armani-luminous-silk":
                ps = p.setdefault("peopleSlugs", [])
                if "adria-arjona" not in ps:
                    ps.append("adria-arjona")
    if "eva-longoria" in people_by_slug:
        for p in projects:
            if p["slug"] == "motion-loreal-longoria-king":
                ps = p.setdefault("peopleSlugs", [])
                if "eva-longoria" not in ps:
                    ps.append("eva-longoria")
    # refresh after links
    for person in people:
        slugs = [p["slug"] for p in projects if person["slug"] in (p.get("peopleSlugs") or [])]
        person["projectSlugs"] = slugs

    # News
    existing_news = {n["slug"] for n in news}
    nid = max(int(re.sub(r"\D", "", n.get("id") or "0") or 0) for n in news) + 1
    for raw in NEW_NEWS:
        if raw["slug"] in existing_news:
            continue
        news.append(
            {
                "id": f"n{nid}",
                "slug": raw["slug"],
                "date": raw["date"],
                "title": raw["title"],
                "summary": raw["summary"],
                "projectSlug": raw.get("projectSlug"),
                "sourceUrl": raw["sourceUrl"],
                "category": raw["category"],
            }
        )
        nid += 1
        existing_news.add(raw["slug"])
    news.sort(key=lambda n: n.get("date") or "", reverse=True)

    # Fetch images for new projects
    print(f"Fetching images for {len(added_projects)} new projects…")
    for item in added_projects:
        path = ROOT / "template" / item["heroImage"]
        if path.exists() and path.stat().st_size > 5000:
            print("  skip", item["slug"])
            continue
        img_url = og_image(item["sourceUrl"])
        ok = False
        if img_url:
            try:
                data, ctype = fetch_bytes(img_url)
                if data and len(data) > 4000 and "html" not in (ctype or ""):
                    write_image(path, data)
                    sources.append(
                        {
                            "path": item["heroImage"],
                            "source_page": item["sourceUrl"],
                            "image_url": img_url,
                            "note": "Downloaded for private concept mockup only. Replace with licensed asset before public launch.",
                        }
                    )
                    ok = True
                    print("  ok", item["slug"], len(data))
            except Exception as e:
                print("  fail", item["slug"], e)
        if not ok:
            ensure_placeholder(path, item["title"])
            print("  placeholder", item["slug"])
        time.sleep(0.35)

    # People heroes for new people
    for slug, url in PEOPLE_WIKI.items():
        person = people_by_slug.get(slug)
        if not person:
            continue
        path = ROOT / "template" / person["heroImage"]
        if path.exists() and path.stat().st_size > 5000:
            continue
        try:
            data, ctype = fetch_bytes(url)
            if data and len(data) > 4000:
                write_image(path, data)
                sources.append(
                    {
                        "path": person["heroImage"],
                        "source_page": person.get("heroImageSource"),
                        "image_url": url,
                        "note": "Wikimedia identity reference for concept only — not a Melania beauty credit photo.",
                    }
                )
                print("  person ok", slug)
            else:
                ensure_placeholder(path, person["name"])
        except Exception as e:
            print("  person fail", slug, e)
            ensure_placeholder(path, person["name"])
        time.sleep(0.4)

    save("projects.json", projects)
    save("people.json", people)
    save("news.json", news)
    SOURCES.write_text(json.dumps(sources, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(
        f"Done: {len(projects)} projects, {len(people)} people, {len(news)} news "
        f"(+{len(added_projects)} projects)"
    )
    for person in people:
        print(f"  {person['slug']}: {len(person.get('projectSlugs') or [])} projects")


if __name__ == "__main__":
    main()
