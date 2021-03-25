# -*- coding: utf-8 -*-
"""recipe_notes2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f2Er_keVC9D_AEuL1lgtbcm5x40KLPTq
"""

from IPython.display import display,HTML
import random
f1,f2,f3,f4,f5,f6,f7,f8,f9=\
'Smokum','Akronim','Wallpoet','Orbitron','Ewert',\
'Lobster','Roboto','Miss Fajardose','Monoton'
fs1,fs2,fs3,fs4,fs5,fs6,fs7,fs8,fs9,fs10,fs11=\
10,12,14,16,18,20,22,24,26,28,30
def chtml(string,font_family=f2,font_size=fs9,font_color='#ff36ff'):
    css_str="""<style>@import """+\
    """'https://fonts.googleapis.com/css?family="""+font_family+"""'; 
    .ch1 {color:"""+font_color+"""; font-family:"""+font_family+"""; 
    font-size:"""+str(font_size)+"""px;}</style>"""
    h1_str="""<h1 class='ch1'>"""+string+"""</h1>"""
    display(HTML(css_str+h1_str))
def idhtml(string,font_family=f5,
           font_size=fs5,font_color='darkslategray'):
    randi=random.randint(1,999999999)
    css_str="""<style>@import """+\
    """'https://fonts.googleapis.com/css?family="""+font_family+"""'; 
    #ch1_"""+str(randi)+""" {font-family:"""+font_family+"""; 
    color:"""+font_color+"""; font-size:"""+str(font_size)+"""px;}</style>"""
    h1_str="""<h1 id='ch1_"""+str(randi)+"""'>"""+string+"""</h1>"""
    scr_str="""<script>
    var idc=setInterval(function() {
        var iddoc=document.getElementById('ch1_"""+str(randi)+"""'), 
            sec=Math.floor(new Date().getTime()%60000/1000); 
        var col='rgb('+(5+Math.abs(245-8*sec))+',0,'+
                (250-Math.abs(245-8*sec))+')';  
        iddoc.style.color=col;}, 1000);</script>"""
    display(HTML(css_str+h1_str+scr_str))
def whtml(string,background_color='black',padding=2,
          font_family='Akronim',font_size_px=int(28),
          deg=int(120),percent=[0,33,67,100],
          colors=['magenta','orange','cyan','purple']):
    randi=str(random.randint(1,999999999))
    css_str="""<style>@import 'https://fonts.googleapis.com/"""+\
    """css?family="""+font_family+"""';</style>"""
    html_str="""<div id='col_div"""+str(randi)+"""' 
    style='background:"""+background_color+"""; width:75%; 
    padding:"""+str(padding)+"""vw;'>
    <div style='background:linear-gradient("""+str(deg)+"""deg, 
    """+colors[0]+""" """+str(percent[0])+"""%,
    """+colors[1]+""" """+str(percent[1])+"""%,
    """+colors[2]+""" """+str(percent[2])+"""%,
    """+colors[3]+""" """+str(percent[3])+"""%); 
    font-family:"""+font_family+"""; font-size:"""+str(font_size_px)+"""px; 
    -webkit-background-clip:text; color:transparent;'>"""+string+"""
    </div></div>"""
    display(HTML(css_str+html_str))

#this one looks fine in the working space
chtml('Style Applying to Classes of Elements')
#and this one looks fine in the working space and after notebooks' execution
idhtml('Style Applying to Id of Elements')
whtml('Linear Gradient Applying to Id of Elements')

from IPython.display import display,HTML
import random
def d3barchart_list(num_list1,num_list2,background_color='silver',
                    width=600,height=400):
    num_list1,num_list2=str(num_list1),str(num_list2) 
    randi=random.randint(1,999999999)
    css_str="""<style>#run_update 
    {fill:slategray;stroke:#fff; fill-opacity:.7}</style>"""
    html_str="""<script src='https://d3js.org/d3.v6.min.js'>
    <"""+"""/script><svg id='svg"""+str(randi)+"""' 
    style='background-color:"""+background_color+""";'></svg><br/><br/>"""
    scr_str="""<script>
        var data="""+num_list1+""",m=20; 
        var n=data.length,ymax=1.2*d3.max(data),
            margin={top:m,right:m,bottom:m,left:m},
            width="""+str(width)+"""-margin.left-margin.right,
            height="""+str(height)+"""-margin.top-margin.bottom;
        var trans='translate('+margin.left+','+margin.top+')'; 
        var xScale=d3.scaleBand().domain(d3.range(n))
                     .rangeRound([0,width]).paddingInner(.1),
            yScale=d3.scaleLinear().domain([0,ymax]).range([0,height]);
        var svg=d3.select('#svg"""+str(randi)+"""')
                  .attr('width',width).attr('height',height)
                  .attr('transform',trans); 
        svg.selectAll('rect').data(data).enter().append('rect')
           .attr('x',function(d,i) {return xScale(i);})
           .attr('y',function(d) {return height-yScale(d);})
           .attr('width',xScale.bandwidth())
           .attr('height',function(d) {return yScale(d);})
           .attr('fill',function(d) { 
               return 'rgb('+Math.round(d*50/ymax)+',0,'+
                       Math.round(d*255/ymax)+')';}); 
        function newData() {
            var n=data.length; 
            while (data.length>0) {data.pop();}; 
            for (var i=0; i<n; i++) {data.push("""+num_list2+"""[i]);}; 
            return data}; 
        function updateBar() {
            svg.selectAll('rect').data(data).transition().duration(3000)
               .attr('y',function(d) {return height-yScale(d);})
               .attr('height',function(d) {return yScale(d);})
               .attr('fill',function(d) {
                   return 'rgb('+Math.round(d*50/ymax)+',0,'+
                          Math.round(d*255/ymax)+')';}); }; 
        svg.append('circle').attr('id','run_update')
           .attr('cx',m).attr('cy',1.25*m).attr('r',15)
           .on('click',function() {newData(); updateBar();}); 
        svg.append('text').text(' <<< UPDATE')
           .attr('x',2*m).attr('y',1.25*m).attr('fill','#fff');
    </script>"""
    display(HTML(css_str+html_str+scr_str))

import numpy as np
num_list1=list(np.random.randint(1,100,50))
num_list2=list(np.random.randint(1,100,50))
d3barchart_list(num_list1,num_list2)

from IPython.display import display,HTML
import random
def d3scatter2d_csv(csv_url,x='x',y='y',marker_size=3,
                    background_color='silver',grid_color='black',
                    width=500,height=500):
    randi=random.randint(1,999999999)
    css_str="""<style>.grid1 line,.grid1 path,.xaxis1,.yaxis1 
    {stroke:"""+grid_color+"""; stroke-opacity:.5;}</style>"""
    html_str="""<script src='https://d3js.org/d3.v4.min.js'>
    </"""+"""script><svg id='svg"""+str(randi)+"""' 
    style='background-color:"""+background_color+"""'></svg><br/>"""
    scr_str="""<script>
    var url='"""+csv_url+"""'; 
    d3.csv(url,function(data) {
        var xmin=d3.min(data,function(d) {return parseFloat(d."""+x+""");}),
            xmax=d3.max(data,function(d) {return parseFloat(d."""+x+""");});
        var ymin=d3.min(data,function(d) {return parseFloat(d."""+y+""");}),
            ymax=d3.max(data,function(d) {return parseFloat(d."""+y+""");});
        var n=data.length,m=20,margin={top:m,right:m,bottom:m,left:m},
            width="""+str(width)+"""-margin.left-margin.right,
            height="""+str(height)+"""-margin.top-margin.bottom;
        var xScale=d3.scaleLinear()
                     .domain([1.1*xmin,1.1*xmax]).range([0,width]),
            yScale=d3.scaleLinear()
                     .domain([1.1*ymin,1.1*ymax]).range([height,0]); 
        function make_x_gridlines() {
            return d3.axisBottom(xScale).ticks(11)}; 
        function make_y_gridlines() { 
            return d3.axisLeft(yScale).ticks(11)};  
        var pointColor=d3.scaleSequential().domain([0,n]) 
                         .interpolator(d3.interpolateRainbow);  
        var tr1='translate('+margin.left+','+margin.top+')',
            tr2='translate(0,'+height+')';  
        var svg=d3.select('#svg"""+str(randi)+"""') 
                  .attr('width',width+margin.left+margin.right) 
                  .attr('height',height+margin.top+margin.bottom) 
                  .append('g').attr('transform',tr1);  
        svg.append('g').attr('class','xaxis1') 
           .call(d3.axisBottom(xScale).tickSize(.5)).attr('transform',tr2);  
        svg.append('g').attr('class','yaxis1') 
           .call(d3.axisLeft(yScale).tickSize(.5)); 
        svg.append('g').attr('class','grid1').attr('transform',tr2)
           .call(make_x_gridlines().tickSize(-height).tickFormat(''));
        svg.append('g').attr('class','grid1').call(make_y_gridlines()
           .tickSize(-width).tickFormat(''));
        svg.selectAll('.point').data(data).enter()
           .append('circle').attr('class','point')
           .attr('fill',function(d,i){return pointColor(i)})
           .attr('r',"""+str(marker_size)+""")
           .attr('stroke','#fff')
           .attr('stroke-width',"""+str(.1*marker_size)+""")
           .attr('cx',function(d) {return xScale(d."""+x+""")})
           .attr('cy',function(d) {return yScale(d."""+y+""")}); 
    });</script>"""
    display(HTML(css_str+html_str+scr_str))

csv_url='https://olgabelitskaya.github.io/castle.csv'
d3scatter2d_csv(csv_url,'x','z',2,'ghostwhite','steelblue',600,300)

csv_url='https://olgabelitskaya.github.io/beethoven.csv'
d3scatter2d_csv(csv_url,'x','z',.7,'black','slategray',600,700)

from IPython.display import display,HTML
import random
def js_color_print(string,font_size):
    randi=str(random.randint(0,99999))
    html_str="""<p id='color_timer"""+randi+"""' 
    style='font-size:"""+str(font_size)+"""px;'>
    """+string+"""</p>
    <script>
    var tc=setInterval(function() {
        var doc=document.getElementById('color_timer"""+randi+"""');
        var sec=Math.floor(new Date().getTime()%60000/1000);
        var col='rgb(0,'+(5+Math.abs(245-8*sec))+','+
                (250-Math.abs(245-8*sec))+')';
        doc.style.color=col},1);
    </"""+"""script>"""
    display(HTML(html_str))
js_color_print('string printing',24)

# Commented out IPython magic to ensure Python compatibility.
# %%javascript
# var out=document.querySelector('#output-area'),
#     p1=document.createElement('p'),
#     p2=document.createElement('p'),
#     p3=document.createElement('p'),
#     str1='🕒 <<<<< this html element has id="color_timer" >>>>> 🕒',
#     str2='😍 <<<<< this html element has id="color_timer" >>>>> 😍',
#     str3='😋 <<<<< this html element has id="new_year_countdown" >>>>> 😋';
# out.style.border='double'; out.style.width='50%';  
# p1.appendChild(document.createTextNode(str1));
# p2.appendChild(document.createTextNode(str2));
# p3.appendChild(document.createTextNode(str3));
# out.appendChild(p1); out.appendChild(p2); out.appendChild(p3);
# p1.id='simple_timer'; p1.style.padding='20px';
# p2.id='color_timer'; p2.style.padding='20px';
# p3.id='new_year_countdown'; p3.style.padding='20px';
# var t=setInterval(function() {
#   var doc=document.getElementById('simple_timer');
#   var now=new Date().getTime();
#   var sec=Math.floor(now%60000/1000);
#   doc.innerHTML='🕒 '+sec;
#   doc.style.color='rgb('+4*(sec+1)+',0,'+4*(sec+1)+')'},1000);
# var tc=setInterval(function() {
#   var doc=document.getElementById('color_timer');
#   var now=new Date().getTime();
#   var sec=Math.floor(now%60000/1000);
#   var col='rgb(0,'+(5+Math.abs(245-8*sec))+','+
#           (250-Math.abs(245-8*sec))+')';
#   doc.style.color=col},1);
# var countDownDate=new Date('Jan 1, 2022 00:00:00').getTime();
# var cdd=setInterval(function() {
#   var doc=document.getElementById('new_year_countdown');
#   var now=new Date().getTime();
#   var distance=countDownDate-now;
#   var days=Math.floor(distance/(1000*60*60*24)),
#       hours=Math.floor(distance%(1000*60*60*24)/(1000*60*60)),
#       minutes=Math.floor(distance%(1000*60*60)/(1000*60)),
#       seconds=Math.floor(distance%(1000*60)/1000);
#   doc.innerHTML=days+' days '+hours+' hours '+minutes+
#                 ' minutes '+seconds+' seconds';
#   if (distance<0) {
#     clearInterval(x); doc.innerHTML='Happy New Year!';}},3000);