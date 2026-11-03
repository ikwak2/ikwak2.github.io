#!/usr/bin/env python3
"""CAU ET subpage refresh. Run at the repository root: python apply_refresh.py"""
from pathlib import Path
import shutil, sys
from bs4 import BeautifulSoup

ROOT=Path.cwd()
SECTIONS=['students','publications','teaching','software','tutorials','photos']
NAV=[('Professor','aboutme.html'),('Students','students/index.html'),('Projects & Publications','publications/index.html'),('Teaching','teaching/index.html'),('Software','software/index.html'),('Tutorials','tutorials/index.html'),('Photos','photos/index.html')]

def header(prefix):
    pieces=['<header class="site-header"><div class="header-inner">',f'<a class="brand" href="{prefix}index.html" aria-label="CAU ET home">CAU <span>ET</span></a>','<nav class="navigation" aria-label="Main navigation">']
    for i,(name,href) in enumerate(NAV):
        if i: pieces.append('<span class="separator">|</span>')
        pieces.append(f'<a href="{prefix}{href}">{name}</a>')
        if i==0: pieces.append(f'<a class="nav-minor" href="{prefix}ilyoup_cv.pdf" target="_blank" rel="noopener">[CV]</a>')
        if name=='Software':pieces.append('<a class="nav-minor" href="https://github.com/ikwak2" target="_blank" rel="noopener">[github]</a>')
    pieces.append('</nav></div></header>')
    return ''.join(pieces)

def students_cards(soup, main):
    tables=main.find_all('table')
    if not tables: return
    table=tables[0]
    cards=soup.new_tag('div',attrs={'class':'student-grid'})
    count=0
    for tr in table.find_all('tr',recursive=False):
        img=tr.find('img')
        if not img: continue
        tds=tr.find_all('td',recursive=False)
        if not tds: continue
        card=soup.new_tag('article',attrs={'class':'student-card'})
        photo=soup.new_tag('div',attrs={'class':'student-photo'})
        img.extract();img.attrs.pop('height',None);img.attrs.pop('width',None);img['loading']='lazy'
        photo.append(img);card.append(photo)
        details=soup.new_tag('div',attrs={'class':'student-details'})
        # Preserve the original name, degree, interests, dates and hyperlinks.
        for td in tds:
            for child in list(td.contents):
                if getattr(child,'name',None)=='img': continue
                details.append(child.extract() if hasattr(child,'extract') else child)
        for font in details.find_all('font'):
            font.name='span';font['class']='student-name';font.attrs.pop('color',None)
        for h2 in details.find_all('h2'):h2['class']='student-heading'
        for p in details.find_all('p'):
            if not p.get_text(strip=True) and not p.find('img'):p.decompose()
        card.append(details);cards.append(card);count+=1
    if count: table.replace_with(cards)

def convert(section):
    path=ROOT/section/'index.html'
    if not path.exists(): print('SKIP (missing):',path);return False
    backup=path.with_name('index_before_refresh.html')
    if backup.exists():
        # Always transform original backup so rerunning is idempotent.
        html=backup.read_text(encoding='utf-8-sig')
    else:
        html=path.read_text(encoding='utf-8-sig')
        shutil.copy2(path,backup)
    soup=BeautifulSoup(html,'html.parser')
    if not soup.html:
        outer=BeautifulSoup('<!doctype html><html lang="en"><head></head><body></body></html>','html.parser')
        for element in list(soup.contents):outer.body.append(element.extract())
        soup=outer
    if not soup.head: soup.html.insert(0,soup.new_tag('head'))
    if not soup.body: body=soup.new_tag('body');soup.html.append(body)
    for sheet in soup.head.find_all('link',rel=lambda v:v and 'stylesheet' in v): sheet.decompose()
    for node in soup.head.find_all('meta',attrs={'name':'viewport'}):node.decompose()
    viewport=soup.new_tag('meta',attrs={'name':'viewport','content':'width=device-width, initial-scale=1'})
    soup.head.append(viewport)
    style=soup.new_tag('link',attrs={'rel':'stylesheet','href':'../style.css?v=4'})
    soup.head.append(style)
    body=soup.body
    main=soup.new_tag('main',attrs={'class':f'section-page section-{section}'})
    for element in list(body.contents): main.append(element.extract())
    # Some legacy pages have title content erroneously adjacent to body.
    soup_head_content=[]
    for element in list(soup.html.contents):
        if element is soup.head or element is soup.body:continue
        soup_head_content.append(element.extract())
    for element in soup_head_content:main.insert(0,element)
    if section=='students':students_cards(soup,main)
    for hr in main.find_all('hr'):hr['class']='section-rule'
    for h1 in main.find_all('h1'):
        h1['class']='section-title'
    for image in main.find_all('img'):
        image.attrs.pop('height',None)
        image.attrs.pop('width',None)
        if section!='students':image['loading']='lazy'
    body.append(BeautifulSoup(header('../'),'html.parser'))
    body.append(main)
    footer=soup.new_tag('footer',attrs={'class':'site-footer'})
    footer.string='CAU ET · Artificial Intelligence and Data Science Lab · Chung-Ang University'
    body.append(footer)
    path.write_text('<!doctype html>\n'+str(soup).replace('<!DOCTYPE html>','').replace('<!doctype html>',''),encoding='utf-8')
    print(f'UPDATED {section}/index.html (backup: {section}/index_before_refresh.html)')
    return True

def main():
    if not (ROOT/'index.html').exists():
        print('ERROR: Run this script from the GitHub repository root (where index.html lives).');sys.exit(1)
    css_source=Path(__file__).resolve().parent/'style.css'
    if not css_source.exists():print('ERROR: style.css missing from package');sys.exit(1)
    css_dest=ROOT/'style.css'
    if css_dest.exists() and not (ROOT/'style_before_subpages.css').exists():shutil.copy2(css_dest,ROOT/'style_before_subpages.css')
    shutil.copy2(css_source,css_dest)
    changed=sum(convert(section) for section in SECTIONS)
    print(f'\nDone: {changed} subpages updated. Root index.html and aboutme.html unchanged.')

if __name__=='__main__':main()
