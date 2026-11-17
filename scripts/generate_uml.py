"""Generate both UML views of the CTI Feasibility Metamodel.

Run from the repository root:
    python scripts/generate_uml.py --src src --reference docs/diagrams/metamodel_v2.drawio --output-dir docs/diagrams

The Python package is imported from --src. Only standard-library modules are
required by this generator. The reference supplies class positions only;
all semantic information comes from the Python registry.
"""
from __future__ import annotations

import argparse
import inspect
import sys
import types
import typing
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

PALETTE = {
    'organization': ('Organization', '#285E96', '#DCEBFA', '#F4F8FD'),
    'infrastructure': ('Infrastructure', '#397B54', '#DDEFE3', '#F4FAF6'),
    'cyberThreat': ('CyberThreat', '#A45B20', '#FCE7D2', '#FFF9F2'),
}
INK = '#172B40'
FONT = 'Arial'
CARD_W, HEAD_H, LINE_H, GAP = 266, 34, 21, 14

@dataclass
class Entity:
    name: str
    domain: str
    attributes: list[tuple[str, str]]
    bases: tuple[str, ...]

    @property
    def height(self):
        return HEAD_H + (14 + LINE_H * len(self.attributes) if self.attributes else 0)


def display_type(annotation):
    origin = typing.get_origin(annotation)
    if origin in (typing.Union, types.UnionType):
        args = [a for a in typing.get_args(annotation) if a is not type(None)]
        return ' | '.join(display_type(a) for a in args)
    if origin is not None:
        return f'{display_type(origin)}[{", ".join(display_type(a) for a in typing.get_args(annotation))}]'
    return getattr(annotation, '__name__', str(annotation).removeprefix('typing.'))


def extract(src):
    sys.path.insert(0, str(src.resolve()))
    from metamodel.core.Registry import Registry
    from metamodel.registry_data import ENTITY_IMPORTS, RELATIONSHIP_IMPORTS
    registry = Registry.load_default()
    names = {name for name, _, _ in ENTITY_IMPORTS}
    entities = []
    for name, _, _ in ENTITY_IMPORTS:
        cls = registry.get_entity_class(name)
        domain = cls.__module__.split('.')[1]
        inherited = {a for b in cls.__bases__ for a in getattr(b, '_domain_attributes', ())}
        attrs = []
        for attr in cls._domain_attributes:
            if attr in inherited:
                continue
            prop = inspect.getattr_static(cls, attr)
            if not isinstance(prop, property) or prop.fget is None:
                raise TypeError(f'{name}.{attr}: expected a readable property')
            annotation = typing.get_type_hints(prop.fget)['return']
            attrs.append((attr, display_type(annotation)))
        entities.append(Entity(name, domain, attrs,
                               tuple(b.__name__ for b in cls.__bases__ if b.__name__ in names)))
    return entities, len(RELATIONSHIP_IMPORTS)


def layout(entities):
    by_domain = {d: [e for e in entities if e.domain == d] for d in PALETTE}
    positions, panels = {}, []
    def grid(items, x, y, cols):
        for k in range(0, len(items), cols):
            row = items[k:k+cols]
            for i, e in enumerate(row):
                positions[e.name] = (x+i*(CARD_W+GAP), y, CARD_W, e.height)
            y += max(e.height for e in row)+GAP
        return y-GAP
    top = 166
    left, right = 32, 1192
    def panel(domain, x, y, cols):
        w = cols*CARD_W+(cols-1)*GAP+36
        bottom = grid(by_domain[domain], x+18, y+58, cols)
        panels.append((domain, x, y, w, bottom+18-y))
        return bottom+18
    org_bottom = panel('organization', left, top, 4)
    infra_bottom = panel('infrastructure', left, org_bottom+20, 4)
    domain = 'cyberThreat'
    special = {e.name for e in by_domain[domain] if e.bases}
    parents = {b for e in by_domain[domain] for b in e.bases}
    normal = [e for e in by_domain[domain] if e.name not in special|parents]
    x = right+18
    bottom = grid(normal, x, top+58, 3)
    # Current model has one domain superclass and three children. Fail rather
    # than silently omit a new hierarchy if the domain changes.
    if parents != {'Vulnerability'} or len(special) != 3:
        raise ValueError('Update the hierarchy layout for the changed model')
    parent = next(e for e in entities if e.name == 'Vulnerability')
    children = [e for e in entities if 'Vulnerability' in e.bases]
    py = bottom+46
    positions[parent.name] = (x+CARD_W+GAP, py, CARD_W, parent.height)
    child_y = py+parent.height+65
    child_bottom = grid(children, x, child_y, 3)
    panels.append((domain, right, top, 3*CARD_W+2*GAP+36, child_bottom+18-top))
    width = right+3*CARD_W+2*GAP+36+32
    height = max(infra_bottom, child_bottom+18)+70
    return positions, panels, width, height


def generate(entities, out):
    positions, panels, width, height = layout(entities)
    svg = ET.Element('svg', {'xmlns':'http://www.w3.org/2000/svg', 'width':str(width), 'height':str(height), 'viewBox':f'0 0 {width} {height}'})
    mx = ET.Element('mxfile', {'host':'app.diagrams.net'})
    page = ET.SubElement(mx, 'diagram', {'id':'entity-structure', 'name':'Metamodel Entity Structure'})
    graph = ET.SubElement(page, 'mxGraphModel', {'grid':'1','gridSize':'10','guides':'1','tooltips':'1','connect':'1','arrows':'1','fold':'1','page':'1','pageScale':'1','pageWidth':str(width),'pageHeight':str(height),'background':'#FFFFFF'})
    root = ET.SubElement(graph, 'root')
    ET.SubElement(root,'mxCell',{'id':'0'})
    ET.SubElement(root,'mxCell',{'id':'1','parent':'0'})
    def rect(x,y,w,h,fill,stroke='none',sw=1,rx=0):
        ET.SubElement(svg,'rect', {k:str(v) for k,v in dict(x=x,y=y,width=w,height=h,fill=fill,stroke=stroke,rx=rx).items()}|{'stroke-width':str(sw)})
    def text(x,y,value,size=15,bold=False,color=INK,anchor='start'):
        ET.SubElement(svg,'text',{'x':str(x),'y':str(y),'font-family':FONT,'font-size':str(size),'font-weight':'700' if bold else '400','fill':color,'text-anchor':anchor}).text=value
    def cell(id,value,x,y,w,h,style,parent='1'):
        c=ET.SubElement(root,'mxCell',{'id':id,'value':value,'style':style,'vertex':'1','parent':parent})
        ET.SubElement(c,'mxGeometry',{'x':str(x),'y':str(y),'width':str(w),'height':str(h),'as':'geometry'})
        return c
    def label(id,value,x,y,w,h,size=15,bold=False,color=INK,align='left',parent='1'):
        cell(id,value,x,y,w,h, f'text;html=0;strokeColor=none;fillColor=none;align={align};verticalAlign=middle;whiteSpace=wrap;spacing=0;fontFamily={FONT};fontSize={size};fontStyle={1 if bold else 0};fontColor={color};',parent)
    rect(0,0,width,height,'#FFFFFF')
    title='CTI Feasibility Metamodel | Entity Structure'
    text(32,48,title,30,True); label('title',title,32,16,width-64,44,30,True)
    total=sum(len(e.attributes) for e in entities)
    subtitle=f'{len(entities)} domain entities  /  {total} domain attribute declarations  /  3 submodels'
    text(32,77,subtitle,17,False,'#536477'); label('subtitle',subtitle,32,58,width-64,26,17,color='#536477')
    notes=["All domain entities inherit directly or indirectly from BaseEntity (id, type, name, description, source). Common attributes are omitted.",
           "Types follow Python property annotations; optionality, methods and visibility are omitted. Only domain inheritance is shown in this view."]
    for i,n in enumerate(notes):
        text(32,108+i*23,n,15,False,'#536477'); label(f'note{i}',n,32,90+i*23,width-64,26,15,color='#536477')
    for domain,x,y,w,h in panels:
        name,stroke,header,body=PALETTE[domain]
        rect(x,y,w,h,'#FFFFFF',stroke,1.3,8)
        cell('panel-'+domain,'',x,y,w,h,f'rounded=1;arcSize=1;whiteSpace=wrap;html=0;fillColor=#FFFFFF;strokeColor={stroke};strokeWidth=1.3;connectable=0;')
        count=sum(e.domain==domain for e in entities)
        attrs=sum(len(e.attributes) for e in entities if e.domain==domain)
        text(x+18,y+31,name,23,True,stroke)
        label('panel-title-'+domain,name,x+18,y+7,w-36,37,23,True,stroke)
        detail=f'{count} entities   /   {attrs} attributes'
        text(x+w-18,y+31,detail,15,False,stroke,anchor='end')
        label('panel-count-'+domain,detail,x+w-270,y+10,252,32,15,color=stroke,align='right')
    for e in entities:
        x,y,w,h=positions[e.name]; _,stroke,header,body=PALETTE[e.domain]
        rect(x,y,w,h,body,stroke,1.1)
        rect(x,y,w,HEAD_H,header,stroke,1.1)
        text(x+w/2,y+22,e.name,15,True,anchor='middle')
        cell(e.name,'',x,y,w,h,f'rounded=0;html=0;fillColor={body};strokeColor={stroke};strokeWidth=1.1;')
        cell(e.name+'-header',e.name,0,0,w,HEAD_H,f'rounded=0;html=0;fillColor={header};strokeColor={stroke};fontColor={INK};fontFamily={FONT};fontSize=15;fontStyle=1;align=center;verticalAlign=middle;connectable=0;',e.name)
        for i,(a,t) in enumerate(e.attributes):
            val=f'{a} : {t}'
            text(x+12,y+HEAD_H+20+i*LINE_H,val,14)
            label(f'{e.name}-attr-{i}',val,12,HEAD_H+5+i*LINE_H,w-24,LINE_H,14,parent=e.name)
    # Three generalizations; a shared trunk in the SVG and matching explicit
    # bend points in Draw.io. Triangles point to the superclass.
    for e in entities:
        for b in e.bases:
            x,y,w,h=positions[e.name]; bx,by,bw,bh=positions[b]
            sx,tx,ty=x+w/2,bx+bw/2,by+bh
            mid=ty+37
            ET.SubElement(svg,'path',{'d':f'M {sx} {y} V {mid} H {tx} V {ty+14}','stroke':INK,'stroke-width':'1.45','fill':'none'})
            ET.SubElement(svg,'path',{'d':f'M {tx-8} {ty+14} L {tx} {ty} L {tx+8} {ty+14} Z','stroke':INK,'stroke-width':'1.45','fill':'#FFFFFF'})
            edge=ET.SubElement(root,'mxCell',{'id':f'inherits-{e.name}', 'edge':'1','parent':'1','source':e.name,'target':b,'style':f'edgeStyle=orthogonalEdgeStyle;rounded=0;html=0;endArrow=block;endFill=0;endSize=12;strokeColor={INK};strokeWidth=1.45;exitX=0.5;exitY=0;entryX=0.5;entryY=1;'} )
            geom=ET.SubElement(edge,'mxGeometry',{'relative':'1','as':'geometry'})
            points=ET.SubElement(geom,'Array',{'as':'points'})
            for px,yy in [(sx,mid),(tx,mid)]:ET.SubElement(points,'mxPoint',{'x':str(px),'y':str(yy)})
    footer='Domain attribute declarations are counted once, at their defining class. Associations and multiplicities are reserved for the complete view.'
    text(32,height-25,footer,14,False,'#536477'); label('footer',footer,32,height-45,width-64,30,14,color='#536477')
    out.mkdir(parents=True,exist_ok=True)
    for tree,name in [(mx,'metamodel_entities.drawio'),(svg,'metamodel_entities.svg')]:
        ET.indent(tree,space='  ')
        ET.ElementTree(tree).write(out/name,encoding='utf-8',xml_declaration=True)
    print(f'{len(entities)} entities, {total} domain attributes, {sum(len(e.bases) for e in entities)} generalizations')


# Complete view: orthogonal paths, independent from the reference edge cells.
# Grid coordinates are used internally; all output coordinates are in pixels.
import heapq
import math
import re
import html
from collections import defaultdict

STEP = 20
SCALE_X, SCALE_Y = 3.2, 4.3
BOX_W = 280
DIRECTIONS = [(1,0),(0,1),(-1,0),(0,-1)]

@dataclass
class Association:
    name: str
    source: str
    target: str
    source_cardinality: str | None
    target_cardinality: str | None
    generalization: bool = False


def associations(entities):
    from metamodel.core.Registry import Registry
    from metamodel.registry_data import RELATIONSHIP_IMPORTS
    reg=Registry.load_default()
    result=[]
    for name,_,_ in RELATIONSHIP_IMPORTS:
        cls=reg.get_relationship_class(name)
        result.append(Association(name,cls.source_type.__name__,cls.target_type.__name__,cls.source_cardinality,cls.target_cardinality))
    return result+[Association('inherits-'+e.name,e.name,b,None,None,True) for e in entities for b in e.bases]


def reference_positions(reference, entities):
    page=next(d for d in ET.parse(reference).getroot().findall('diagram') if d.get('name')=="Leonardo's touch")
    cells=page.find('mxGraphModel/root')
    names={e.name:e for e in entities}; coords={}
    for c in cells:
        if c.get('vertex')!='1':continue
        name=re.sub(r'\s+','',html.unescape(re.sub(r'<[^>]*>','',c.get('value',''))))
        if name not in names:continue
        g=c.find('mxGeometry')
        if name in coords:raise ValueError(f'Duplicate class {name} in reference')
        coords[name]=(float(g.get('x','0'))+float(g.get('width','0'))/2,float(g.get('y','0'))+float(g.get('height','0'))/2)
    if set(coords)!=set(names):raise ValueError(f'Missing positions: {set(names)-set(coords)}')
    xmin=min(x for x,y in coords.values()); ymin=min(y for x,y in coords.values())
    pos={}
    for e in entities:
        cx,cy=coords[e.name]; w=BOX_W//STEP; h=math.ceil(e.height/STEP)
        pos[e.name]=(round((cx-xmin)*SCALE_X/STEP)+14-w//2,round((cy-ymin)*SCALE_Y/STEP)+18-h//2,w,h)
    for a,(x,y,w,h) in pos.items():
        for b,(xx,yy,ww,hh) in pos.items():
            if a!=b and x<xx+ww+2 and x+w+2>xx and y<yy+hh+2 and y+h+2>yy:raise ValueError(f'Classes too close: {a}, {b}')
    return pos


def allocate_ports(pos, edges):
    # Assign each endpoint to a side, then order ports by the remote class
    # position. Side capacity prevents multiple edges sharing a terminal.
    allocated=defaultdict(list); chosen={}
    for i,e in enumerate(edges):
        for end,name,other in [(0,e.source,e.target),(1,e.target,e.source)]:
            x,y,w,h=pos[name]; xx,yy,ww,hh=pos[other]
            dx=xx+ww/2-x-w/2;dy=yy+hh/2-y-h/2
            norm=max(1,math.hypot(dx,dy)); dx/=norm;dy/=norm
            if name==other: dx,dy=(.8,-.9) if end==0 else (-.9,-.8)
            options=[]
            for side,(vx,vy) in enumerate(DIRECTIONS):
                cap=(h if vx else w)-1
                used=len(allocated[name,side])
                if used>=cap:continue
                preferred={('producesIndicator',0):2,('producesIndicator',1):2,('associatedToTool',0):0,('associatedToTool',1):0}.get((e.name,end))
                score=(dx*vx+dy*vy)*4 - 1.9*used/max(cap,1)
                if preferred==side:score+=10
                if e.generalization and name!=other:score+=0.4 if side in (0,2) else 0
                options.append((score,side))
            if not options:raise ValueError(f'No ports for {name}')
            side=max(options)[1]; vx,vy=DIRECTIONS[side]
            sortval=yy+hh/2 if vx else xx+ww/2
            allocated[name,side].append((sortval,i,end));chosen[i,end]=(name,side)
    ports={}
    for (name,side),items in allocated.items():
        x,y,w,h=pos[name]; vx,vy=DIRECTIONS[side]; length=h if vx else w
        for j,(_,i,end) in enumerate(sorted(items)):
            k=round((j+1)*length/(len(items)+1));k=max(1,min(length-1,k))
            point=(x+(w if vx>0 else 0),y+k) if vx else (x+k,y+(h if vy>0 else 0))
            ports[i,end]=(point,(point[0]+2*vx,point[1]+2*vy),side)
    return ports


def route_all(pos, edges):
    ports=allocate_ports(pos,edges)
    W=max(x+w for x,y,w,h in pos.values())+11; H=max(y+h for x,y,w,h in pos.values())+11
    blocked=set(); occupied=set(); used_nodes=defaultdict(int)
    for x,y,w,h in pos.values():
        blocked.update((a,b) for a in range(x-1,x+w+2) for b in range(y-1,y+h+2))
    # Reserve other terminal stubs to keep card entry and exit clear.
    reserved={}
    for key,(p,q,side) in ports.items():
        vx,vy=DIRECTIONS[side]
        for k in (1,2):reserved[p[0]+k*vx,p[1]+k*vy]=key
    paths={}
    def search(start,goal,key_start,key_goal):
        # A* with orthogonal moves; reuse of an edge is heavily penalized.
        # Small crossing cost is preferable to long detours.
        heap=[(0.,0.,start,4)]; best={start:0.}; parent={}; prev_dir={start:4}
        while heap:
            _,cost,p,d=heapq.heappop(heap)
            if cost!=best.get(p):continue
            if p==goal:
                path=[p]
                while p!=start:p=parent[p];path.append(p)
                return path[::-1]
            for nd,(dx,dy) in enumerate(DIRECTIONS):
                q=(p[0]+dx,p[1]+dy)
                if not (3<=q[0]<W and 10<=q[1]<H):continue
                if q!=goal and (q in blocked or (q in reserved and reserved[q] not in (key_start,key_goal))):continue
                edge=tuple(sorted((p,q)))
                nc=cost+1+(2.8 if d!=4 and nd!=d else 0)+(40 if edge in occupied else 0)+1.7*used_nodes.get(q,0)
                if nc>=best.get(q,float('inf')):continue
                best[q]=nc;parent[q]=p;prev_dir[q]=nd
                h=abs(q[0]-goal[0])+abs(q[1]-goal[1])
                heapq.heappush(heap,(nc+1.12*h,nc,q,nd))
        raise ValueError(f'No route from {start} to {goal}')
    # Route short associations first, then longer inter-domain links.
    order=sorted(range(len(edges)),key=lambda i:(abs(ports[i,0][1][0]-ports[i,1][1][0])+abs(ports[i,0][1][1]-ports[i,1][1][1])))
    for i in order:
        sp,s,ss=ports[i,0];tp,t,ts=ports[i,1]
        middle=search(s,t,(i,0),(i,1));path=[sp]+middle+[tp]
        for a,b in zip(middle,middle[1:]):occupied.add(tuple(sorted((a,b))))
        for p in middle:used_nodes[p]+=1
        compact=[path[0]]
        for j in range(1,len(path)-1):
            a,b,c=path[j-1:j+2]
            if not ((a[0]==b[0]==c[0]) or (a[1]==b[1]==c[1])):compact.append(b)
        compact.append(path[-1]);paths[i]=[(x*STEP,y*STEP) for x,y in compact]
    return paths,ports,W*STEP+40,H*STEP+40


def label_positions(pos,paths,edges):
    boxes=[(x*STEP-3,y*STEP-3,(x+w)*STEP+3,(y+h)*STEP+3) for x,y,w,h in pos.values()]
    lines=[(i,a,b) for i,p in paths.items() for a,b in zip(p,p[1:])]
    labels=[]; placed=[]
    def overlaps(a,b):return a[0]<b[2] and a[2]>b[0] and a[1]<b[3] and a[3]>b[1]
    def line_hits(rect,a,b):
        return (min(a[0],b[0])<rect[2] and max(a[0],b[0])>rect[0] and rect[1]<a[1]<rect[3]) if a[1]==b[1] else (min(a[1],b[1])<rect[3] and max(a[1],b[1])>rect[1] and rect[0]<a[0]<rect[2])
    def place(i,value,kind):
        p=paths[i]; seg=list(zip(p,p[1:])); total=sum(math.dist(a,b) for a,b in seg)
        font=16 if kind=='name' else 15
        width=max(28,math.ceil(len(value)*font*.58)+10); height=22
        candidates=[]; cum=0
        for j,(a,b) in enumerate(seg):
            length=math.dist(a,b)
            if length==0:continue
            horiz=a[1]==b[1]
            for t in ([j/20 for j in range(1,20)] if kind=='name' else [min(1,k/length) for k in (15,25,35,45,60,80,100,125)] + [max(0,1-k/length) for k in (15,25,35,45,60,80,100,125)] + [.5]):
                along=cum+t*length
                if kind=='source' and along>145:continue
                if kind=='target' and total-along>145:continue
                x=a[0]+(b[0]-a[0])*t;y=a[1]+(b[1]-a[1])*t
                for sign in (-1,1):
                    for offset in (3,6,9,13,17,23,30,40,50):
                        cx=x if horiz else x+sign*(width/2+offset)
                        cy=y+sign*(height/2+offset) if horiz else y
                        rect=(cx-width/2,cy-height/2,cx+width/2,cy+height/2)
                        if any(overlaps(rect,r) for r in boxes+placed):continue
                        hit=sum(line_hits(rect,u,v) for k,u,v in lines if k!=i)
                        if kind=='name':score=abs(along-total/2)/total*15+(0 if horiz else 5)+max(0,width+10-length)*.14
                        else:score=abs((along if kind=='source' else total-along)-27)*.23
                        candidates.append((score+hit*100+offset*.18,rect,cx,cy,along,hit))
                # Standard UML edge labels may sit on their own connector.
                # This is preferable to obscuring a different association.
                if kind=='name':
                    rect=(x-width/2,y-height/2,x+width/2,y+height/2)
                    if not any(overlaps(rect,r) for r in boxes+placed):
                        hit=sum(line_hits(rect,u,v) for k,u,v in lines if k!=i)
                        score=11+abs(along-total/2)/total*15+(0 if horiz else 8)+max(0,width+10-length)*.14
                        candidates.append((score+hit*100,rect,x,y,along,hit))
            cum+=length
        if not candidates:raise ValueError(f'Cannot place label {edges[i].name} {value}')
        score,r,cx,cy,along,hit=min(candidates,key=lambda v:v[0]);placed.append(r)
        if hit: print('Label crosses other connector:',edges[i].name,kind,value,hit)
        labels.append((i,kind,value,cx,cy,width,height,along,total,hit))
    # Multiplicities first, so association names cannot occupy their space.
    for i,e in enumerate(edges):
        for k,v in [('source',e.source_cardinality),('target',e.target_cardinality)]:
            if v is not None:place(i,str(v),k)
    for i,e in enumerate(edges):
        if not e.generalization:place(i,e.name,'name')
    return labels


def generate_complete(entities,reference,out):
    pos=reference_positions(reference,entities); edges=associations(entities)
    paths,ports,width,height=route_all(pos,edges); labels=label_positions(pos,paths,edges)
    svg=ET.Element('svg',{'xmlns':'http://www.w3.org/2000/svg','width':str(width),'height':str(height),'viewBox':f'0 0 {width} {height}'})
    mx=ET.Element('mxfile',{'host':'app.diagrams.net'});page=ET.SubElement(mx,'diagram',{'id':'complete-metamodel','name':'Complete Metamodel Class Diagram'})
    graph=ET.SubElement(page,'mxGraphModel',{'grid':'1','gridSize':'10','guides':'1','tooltips':'1','connect':'1','arrows':'1','fold':'1','page':'1','pageScale':'1','pageWidth':str(width),'pageHeight':str(height),'background':'#FFFFFF'})
    root=ET.SubElement(graph,'root');ET.SubElement(root,'mxCell',{'id':'0'});ET.SubElement(root,'mxCell',{'id':'1','parent':'0'})
    def cell(id,value,x,y,w,h,style,parent='1'):
        c=ET.SubElement(root,'mxCell',{'id':id,'value':value,'style':style,'vertex':'1','parent':parent});ET.SubElement(c,'mxGeometry',{'x':str(x),'y':str(y),'width':str(w),'height':str(h),'as':'geometry'});return c
    def rect(x,y,w,h,fill,stroke='none',sw=1):ET.SubElement(svg,'rect',{'x':str(x),'y':str(y),'width':str(w),'height':str(h),'fill':fill,'stroke':stroke,'stroke-width':str(sw)})
    def text(x,y,value,size=15,bold=False,color=INK,anchor='start'):
        ET.SubElement(svg,'text',{'x':str(x),'y':str(y),'font-family':FONT,'font-size':str(size),'font-weight':'700' if bold else '400','fill':color,'text-anchor':anchor}).text=value
    def txt(id,value,x,y,w,h,size=15,bold=False,color=INK,align='left',parent='1'):
        return cell(id,value,x,y,w,h,f'text;html=0;strokeColor=none;fillColor=none;align={align};verticalAlign=middle;whiteSpace=wrap;spacing=0;fontFamily={FONT};fontSize={size};fontStyle={1 if bold else 0};fontColor={color};connectable=0;',parent)
    rect(0,0,width,height,'#FFFFFF')
    for i,(s,size,bold) in enumerate([('CTI Feasibility Metamodel | Complete Class Diagram',36,True),(f'{len(entities)} domain entities  /  {sum(len(e.attributes) for e in entities)} domain attribute declarations  /  {sum(not e.generalization for e in edges)} associations  /  {sum(e.generalization for e in edges)} generalizations',22,False),('All domain entities inherit directly or indirectly from BaseEntity. Common attributes (id, type, name, description, source), optionality, methods and visibility are omitted.',19,False),('Open arrows: directed associations. Hollow triangles: generalization. Blank multiplicities: unspecified. Line breaks at crossings distinguish independent connectors.',19,False)]):
        y=[48,85,116,145][i];text(40,y,s,size,bold);txt(f'title{i}',s,40,y-size,width-80,size+8,size,bold)
    for j,(d,(n,stroke,header,body)) in enumerate(PALETTE.items()):
        x=40+j*290;rect(x,170,25,23,header,stroke);cell('legend-'+d,'',x,170,25,23,f'fillColor={header};strokeColor={stroke};connectable=0;');text(x+36,188,n,20,True,stroke);txt('legend-label-'+d,n,x+36,167,244,28,20,True,stroke)
    # At strict intersections, interrupt horizontal lines briefly; this avoids
    # suggesting a junction between independent associations in the SVG.
    verticals=[(i,a,b) for i,p in paths.items() for a,b in zip(p,p[1:]) if a[0]==b[0]]
    crossings=0
    # Draw all edges first, then classes, then annotations.
    for i,e in enumerate(edges):
        p=paths[i]; color=INK if e.generalization else '#536173'; sw=2.1 if e.generalization else 1.6
        a,b=p[-2:];dist=math.dist(a,b);ux,uy=(b[0]-a[0])/dist,(b[1]-a[1])/dist
        size=15 if e.generalization else 12; bw=8 if e.generalization else 6
        base=(b[0]-ux*size,b[1]-uy*size);l=(base[0]-uy*bw,base[1]+ux*bw);r=(base[0]+uy*bw,base[1]-ux*bw)
        drawpath=p[:-1]+([base] if e.generalization else [b])
        for u,v in zip(drawpath,drawpath[1:]):
            if u[1]==v[1]:
                lo,hi=sorted((u[0],v[0])); y=u[1]
                hits=sorted({a[0] for k,a,b in verticals if k!=i and lo+9<a[0]<hi-9 and min(a[1],b[1])<y<max(a[1],b[1])})
                cuts=[lo]+[c for x in hits for c in (x-5,x+5)]+[hi];crossings+=len(hits)
                fragments=[((a,y),(b,y)) for a,b in zip(cuts[::2],cuts[1::2])]
            else:fragments=[(u,v)]
            for l1,l2 in fragments:
                ET.SubElement(svg,'path',{'d':f'M {l1[0]} {l1[1]} L {l2[0]} {l2[1]}','fill':'none','stroke':color,'stroke-width':str(sw),'stroke-linecap':'round'})
        ET.SubElement(svg,'path',{'d':f'M {l[0]} {l[1]} L {b[0]} {b[1]} L {r[0]} {r[1]}'+(' Z' if e.generalization else ''),'fill':'#FFFFFF' if e.generalization else 'none','stroke':color,'stroke-width':str(sw)})
        sx,sy,swid,sh=pos[e.source];tx,ty,tw,th=pos[e.target]
        ex,ey=p[0];ix,iy=p[-1]
        style=f'edgeStyle=none;noEdgeStyle=1;rounded=0;html=0;jumpStyle=gap;jumpSize=8;endArrow={"block" if e.generalization else "open"};endFill=0;endSize={12 if e.generalization else 8};strokeColor={color};strokeWidth={sw};exitX={(ex/STEP-sx)/swid};exitY={(ey/STEP-sy)/sh};entryX={(ix/STEP-tx)/tw};entryY={(iy/STEP-ty)/th};exitPerimeter=0;entryPerimeter=0;'
        edge=ET.SubElement(root,'mxCell',{'id':'edge-'+e.name,'value':'','edge':'1','parent':'1','source':e.source,'target':e.target,'style':style})
        geom=ET.SubElement(edge,'mxGeometry',{'relative':'1','as':'geometry'});arr=ET.SubElement(geom,'Array',{'as':'points'})
        for x,y in p[1:-1]:ET.SubElement(arr,'mxPoint',{'x':str(x),'y':str(y)})
    for e in entities:
        x,y,w,h=(v*STEP for v in pos[e.name]);_,stroke,header,body=PALETTE[e.domain]
        rect(x,y,w,h,body,stroke,1.5);rect(x,y,w,HEAD_H,header,stroke,1.5);text(x+w/2,y+23,e.name,16,True,anchor='middle')
        cell(e.name,'',x,y,w,h,f'rounded=0;html=0;fillColor={body};strokeColor={stroke};strokeWidth=1.5;')
        cell(e.name+'-header',e.name,0,0,w,HEAD_H,f'rounded=0;html=0;fillColor={header};strokeColor={stroke};fontColor={INK};fontFamily={FONT};fontSize=16;fontStyle=1;align=center;verticalAlign=middle;connectable=0;',e.name)
        for j,(a,t) in enumerate(e.attributes):
            value=f'{a} : {t}';text(x+12,y+HEAD_H+20+j*LINE_H,value,14);txt(f'{e.name}-attr-{j}',value,12,HEAD_H+5+j*LINE_H,w-24,LINE_H,14,parent=e.name)
    for i,kind,value,cx,cy,w,h,along,total,hit in labels:
        font=16 if kind=='name' else 15; bold=kind=='name';color=INK if bold else '#415367'
        rect(cx-w/2,cy-h/2,w,h,'#FFFFFF');text(cx,cy+font*.34,value,font,bold,color,'middle')
        # Attach each label to its edge at the corresponding path fraction,
        # then offset it to the same position used in the SVG.
        p=paths[i];remaining=along;px,py=p[0]
        for a,b in zip(p,p[1:]):
            length=math.dist(a,b)
            if remaining<=length:
                frac=remaining/length;px=a[0]+(b[0]-a[0])*frac;py=a[1]+(b[1]-a[1])*frac;break
            remaining-=length
        c=ET.SubElement(root,'mxCell',{'id':f'edge-{edges[i].name}-{kind}','value':value,'vertex':'1','connectable':'0','parent':'edge-'+edges[i].name,'style':f'edgeLabel;html=0;align=center;verticalAlign=middle;resizable=0;points=[];labelBackgroundColor=#FFFFFF;fontFamily={FONT};fontSize={font};fontStyle={1 if bold else 0};fontColor={color};'})
        g=ET.SubElement(c,'mxGeometry',{'x':str(2*along/total-1),'y':'0','relative':'1','as':'geometry'});ET.SubElement(g,'mxPoint',{'x':str(cx-px),'y':str(cy-py),'as':'offset'})
    out.mkdir(parents=True,exist_ok=True)
    for tree,n in [(mx,'metamodel_complete.drawio'),(svg,'metamodel_complete.svg')]:
        ET.indent(tree,space='  ');ET.ElementTree(tree).write(out/n,encoding='utf-8',xml_declaration=True)
    print(f'{len(edges)} edges; {len(labels)} labels; {sum(l[-1]>0 for l in labels)} labels intersect another connector; {crossings} crossing gaps; {width} x {height}')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--src',type=Path,default=Path('src'))
    p.add_argument('--reference',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,default=Path('metamodel_uml'))
    args=p.parse_args();entities,_=extract(args.src)
    generate(entities,args.output_dir);generate_complete(entities,args.reference,args.output_dir)

if __name__=='__main__':main()
