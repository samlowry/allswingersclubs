function CSS3MultiColumn(){var cssCache=new Object();var splitableTags=new Array('P','DIV','SPAN','BLOCKQUOTE','ADDRESS','PRE','A','EM','I','STRONG','B','CITE','OL','UL','LI');var pseudoCSSRules=new Object();var ut=new CSS3Utility();var debug=ut.debug;if(document.location.search.match('mode=debug'))var isDebug=true;else var isDebug=false;var bestSplitPoint=null;var secondSplitPoint=null;var secondSplitBottom=0;var documentReady=false;ut.XBrowserAddEventHandler(window,'load',function(){documentReady=true;processElements();});loadStylesheets();function loadStylesheets(){if(document.styleSheets){for(var i=0;i<document.styleSheets.length;i++){cssCache[document.styleSheets[i].href]=false;}
for(var i=0;i<document.styleSheets.length;i++){loadCssCache(document.styleSheets[i],'parseStylesheets');}}else if(document.getElementsByTagName){var Lt=document.getElementsByTagName('link');for(var i=0;i<Lt.length;i++){cssCache[Lt[i].href]=false;}
for(var i=0;i<Lt.length;i++){loadCssCache(Lt[i],'parseStylesheets');}}}
function loadCssCache(s,callback){if(s.href&&s.cssText){cssCache[s.href]=s.cssText;eval(callback)();}
if(s.href&&typeof XMLHttpRequest!='undefined'){var xmlhttp=new XMLHttpRequest();xmlhttp.onreadystatechange=function(){if(xmlhttp.readyState==4){if(typeof xmlhttp.status=='undefined'||xmlhttp.status==200||xmlhttp.status==304){cssCache[s.href]=xmlhttp.responseText;eval(callback)();}}}
xmlhttp.open("GET",s.href,true);xmlhttp.send(null);}}
function parseStylesheets(){var allDone=true;for(var i in cssCache){if(cssCache[i]!=false)parseStylesheet(cssCache[i]);else allDone=false;}
if(allDone){processElements();}}
function parseStylesheet(cssText){var cc=new ut.getPseudoCssRules('column-count',cssText);for(var i=0;cc&&i<cc.cssRules.length;i++){if(!pseudoCSSRules[cc.cssRules[i].selectorText])
pseudoCSSRules[cc.cssRules[i].selectorText]=new Object();pseudoCSSRules[cc.cssRules[i].selectorText]['column-count']=cc.cssRules[i].value;}
cc=new ut.getPseudoCssRules('column-width',cssText);for(var i=0;cc&&i<cc.cssRules.length;i++){if(!pseudoCSSRules[cc.cssRules[i].selectorText])
pseudoCSSRules[cc.cssRules[i].selectorText]=new Object();pseudoCSSRules[cc.cssRules[i].selectorText]['column-width']=cc.cssRules[i].value;}
cc=new ut.getPseudoCssRules('column-gap',cssText);for(var i=0;cc&&i<cc.cssRules.length;i++){if(!pseudoCSSRules[cc.cssRules[i].selectorText])
pseudoCSSRules[cc.cssRules[i].selectorText]=new Object();pseudoCSSRules[cc.cssRules[i].selectorText]['column-gap']=cc.cssRules[i].value;}
cc=new ut.getPseudoCssRules('column-rule',cssText);for(var i=0;cc&&i<cc.cssRules.length;i++){if(!pseudoCSSRules[cc.cssRules[i].selectorText])
pseudoCSSRules[cc.cssRules[i].selectorText]=new Object();pseudoCSSRules[cc.cssRules[i].selectorText]['column-rule']=cc.cssRules[i].value;}}
function processElements(){if(!documentReady)return;for(var i in pseudoCSSRules){debug(i+' cc:'+pseudoCSSRules[i]['column-count']+' cw:'+pseudoCSSRules[i]['column-width']+' cr:'+pseudoCSSRules[i]['column-rule']+' cg:'+pseudoCSSRules[i]['column-gap']);var affectedElements=ut.cssQuery(i);for(var j=0;j<affectedElements.length;j++){processElement(affectedElements[j],pseudoCSSRules[i]['column-count'],pseudoCSSRules[i]['column-width'],pseudoCSSRules[i]['column-gap'],pseudoCSSRules[i]['column-rule']);}}}
function processElement(affectedElement,column_count,column_width,column_gap,column_rule){var widthUnit;var width;var column_rule_width=0;if(affectedElement.clientWidth&&affectedElement.clientWidth!=0){var padding;if(affectedElement.currentStyle){padding=parseInt(affectedElement.currentStyle.paddingLeft.replace(/[\D]*/gi,""))+parseInt(affectedElement.currentStyle.paddingRight.replace(/[\D]*/gi,""))}else if(document.defaultView&&document.defaultView.getComputedStyle){padding=parseInt(document.defaultView.getComputedStyle(affectedElement,"").getPropertyValue("padding-left").replace(/[\D]*/gi,""))+parseInt(document.defaultView.getComputedStyle(affectedElement,"").getPropertyValue("padding-left").replace(/[\D]*/gi,""))}
if(isNaN(padding))padding=0;width=(affectedElement.clientWidth-padding).toString()+"px";}
else if(affectedElement.scrollWidth){var borderWidth;var padding;if(affectedElement.currentStyle){padding=parseInt(affectedElement.currentStyle.paddingLeft.replace(/[\D]*/gi,""))+parseInt(affectedElement.currentStyle.paddingRight.replace(/[\D]*/gi,""))}else if(document.defaultView&&document.defaultView.getComputedStyle){padding=parseInt(document.defaultView.getComputedStyle(affectedElement,"").getPropertyValue("padding-left").replace(/[\D]*/gi,""))+parseInt(document.defaultView.getComputedStyle(affectedElement,"").getPropertyValue("padding-left").replace(/[\D]*/gi,""))}
if(isNaN(padding))padding=0;if(affectedElement.currentStyle){borderWidth=parseInt(affectedElement.currentStyle.borderLeftWidth.replace(/[\D]*/gi,""))+parseInt(affectedElement.currentStyle.borderRightWidth.replace(/[\D]*/gi,""))}else if(document.defaultView&&document.defaultView.getComputedStyle){borderWidth=parseInt(document.defaultView.getComputedStyle(affectedElement,"").getPropertyValue("border-left-width").replace(/[\D]*/gi,""))+parseInt(document.defaultView.getComputedStyle(affectedElement,"").getPropertyValue("border-right-width").replace(/[\D]*/gi,""))}
if(isNaN(borderWidth))borderWidth=0;width=(affectedElement.scrollWidth-padding-borderWidth).toString()+"px";}
else width="99%";var availableWidth=parseInt(width.replace(/[\D]*/gi,""));if(!column_width||column_width=='auto')
widthUnit=width.replace(/[\d]*/gi,"");else
widthUnit=column_width.replace(/[\d]*/gi,"");if(!widthUnit)
widthUnit="px";if(!column_gap){if(widthUnit=="%")
column_gap=1;else
column_gap=15;}else{column_gap=parseInt(column_gap.replace(/[\D]*/gi,""));}
if(column_rule&&column_rule!='none'){column_gap=Math.floor(column_gap/2);column_rule_width=column_gap+parseInt(column_rule.substring(column_rule.search(/\d/),column_rule.search(/\D/)));}
if(!column_width||column_width=='auto'){column_width=(availableWidth-((column_gap+column_rule_width)*(column_count-1)))/column_count;}else{column_width=parseInt(column_width.replace(/[\D]*/gi,""))
if(!column_count||column_count=='auto'){column_count=Math.floor(availableWidth/(column_width+column_gap));}}
column_width-=1;var wrapper=document.createElement('div');var pn=affectedElement.parentNode;wrapper=pn.insertBefore(wrapper,affectedElement);var elem=pn.removeChild(affectedElement);elem=wrapper.appendChild(elem);wrapper.className=elem.className;elem.className="";elem.id=ut.randomId();elem.style.width=column_width.toString()+widthUnit;if(typeof elem.style.styleFloat!='undefined')
elem.style.styleFloat="left";if(typeof elem.style.cssFloat!='undefined')
elem.style.cssFloat="left";var newHeight=Math.floor(elem.offsetHeight/column_count)+14;if(!wrapper.id)wrapper.id=ut.randomId();var j=1;for(var i=1;i<column_count&&elem&&j<(column_count+5);i++){bestSplitPoint=null;secondSplitPoint=null;secondSplitBottom=0;findSplitPoint(elem,newHeight*i,wrapper);if(isDebug)bestSplitPoint.style.border="1px solid #00FF00";if(bestSplitPoint&&!isElementSplitable(bestSplitPoint)){newHeight=getElementRelativeTop(bestSplitPoint,wrapper)+bestSplitPoint.offsetHeight+10;i=1;debug('reset new Height = '+newHeight+' relativetop='+getElementRelativeTop(bestSplitPoint,wrapper)+' offsetHeight= '+bestSplitPoint.offsetHeight);}
else if(!bestSplitPoint){debug("No split point found with "+newHeight);}
j++;}
debug('<table><tr><td>Avail. Width</td><td>'+availableWidth+'</td><td>Units</td><td>'+widthUnit+'</td></tr><tr><td>column_width</td><td>'+column_width+'</td><td>column_count</td><td>'+column_count+'</td></tr><tr><td>column_gap</td><td>'+column_gap+'</td><td>column_rule</td><td>'+column_rule+'</td></tr><tr><td>New Height</td><td>'+newHeight+'</td><td></td><td></td></tr></table>');for(var i=1;i<column_count&&elem;i++){bestSplitPoint=null;secondSplitPoint=null;secondSplitBottom=0;findSplitPoint(elem,newHeight,wrapper);if(bestSplitPoint&&isElementSplitable(bestSplitPoint)&&elem.id!=bestSplitPoint.id){var splitE=bestSplitPoint;if(isDebug)secondSplitPoint.style.border="1px dotted #00F";}
else{var splitE=secondSplitPoint;}
if(!splitE){debug("<hr />No split point found for "+elem.tagName+' '+newHeight);return;}
if(isDebug)splitE.style.border="1px solid #F00";var newCol=elem.cloneNode(false);newCol.id=ut.randomId();elem.parentNode.insertBefore(newCol,elem.nextSibling);newCol.style.paddingLeft=column_gap+widthUnit;if(column_rule&&column_rule!='none'){newCol.style.borderLeft=column_rule;elem.style.paddingRight=column_gap+widthUnit;}
if(document.all&&!window.opera)
elem.style.height=newHeight+'px';elem.style.minHeight=newHeight+'px';var insertPoint=createNodeAncestors(splitE,elem,newCol,'append');var refElement=splitE;while(refElement&&refElement.id!=elem.id){var littleSib=refElement.nextSibling;while(littleSib){moveNode(littleSib,elem,newCol);littleSib=refElement.nextSibling;}
refElement=refElement.parentNode;}
var strippedLine=splitElement(splitE,newHeight-getElementRelativeTop(splitE,wrapper),elem,newCol);var pn=splitE.parentNode;while(pn&&pn.id!=elem.id){var n=pn.firstChild;while(n){if((n.nodeType==1&&n.childNodes.length==0)||(n.nodeType==3&&n.nodeValue.replace(/[\u0020\u0009\u000A]*/,'')=="")){pn.removeChild(n);n=pn.firstChild;}else{n=n.nextSibling;}}
pn=pn.parentNode;}
if(strippedLine){splitE=elem.lastChild;if(splitE&&(document.defaultView&&document.defaultView.getComputedStyle(splitE,'').getPropertyValue('text-align')=='justify')||(splitE.currentStyle&&splitE.currentStyle.textAlign=='justify')){var txtFiller=document.createTextNode(' '+strippedLine.replace(/./g,"\u00a0"));var filler=document.createElement('span');splitE.appendChild(filler);filler.style.lineHeight="1px";filler.appendChild(txtFiller);}}
elem=newCol;}
if(elem){if(document.all&&!window.opera)
elem.style.height=newHeight+'px';elem.style.minHeight=newHeight+'px';}
var clearFloatDiv=document.createElement('div');clearFloatDiv.style.clear="left";clearFloatDiv.appendChild(document.createTextNode(' '));wrapper.appendChild(clearFloatDiv);if(navigator.userAgent.toLowerCase().indexOf('safari')+1)
wrapper.innerHTML+=' ';}
function findSplitPoint(n,newHeight,wrapper){if(n.nodeType==1){var top=getElementRelativeTop(n,wrapper);var bot=top+n.offsetHeight;if(top<newHeight&&bot>newHeight){bestSplitPoint=n;if(isElementSplitable(n)){for(var i=0;i<n.childNodes.length;i++){findSplitPoint(n.childNodes[i],newHeight,wrapper);}}
return;}
if(bot<=newHeight&&bot>=secondSplitBottom){secondSplitBottom=bot;secondSplitPoint=n;}}
return;}
function isElementSplitable(n){if(n.tagName){var tagName=n.tagName.toUpperCase();for(var i=0;i<splitableTags.length;i++)
if(tagName==splitableTags[i])return true;}
return false;}
function splitElement(n,targetHeight,col1,col2){var cn=n.lastChild;while(cn){if(cn.nodeType==3){var strippedText="dummmy";var allStrippedText="";while(n.offsetHeight>targetHeight+2&&strippedText!=""){strippedText=stripOneLine(cn);allStrippedText=strippedText+allStrippedText;}
if(allStrippedText!=""){var insertPoint=createNodeAncestors(cn,col1,col2,'insertBefore');insertPoint.insertBefore(document.createTextNode(allStrippedText),insertPoint.firstChild);}
if(cn.nodeValue==""){cn.parentNode.removeChild(cn);}
else
break;}
else{var insertPoint=createNodeAncestors(cn,col1,col2,'insertBefore');insertPoint.insertBefore(cn.parentNode.removeChild(cn),insertPoint.firstChild);}
cn=n.lastChild;}
return strippedText;}
function stripOneLine(n){while(n&&n.nodeType!=3)
n=n.firstChild;if(!n)return;var e=n.parentNode;var h=e.offsetHeight;if(!h){return"";}
var str=n.nodeValue;var wIdx=n.nodeValue.lastIndexOf(' ');while(wIdx!=-1&&e.offsetHeight==h){n.nodeValue=n.nodeValue.substr(0,wIdx);wIdx=n.nodeValue.lastIndexOf(' ');if(wIdx==-1)wIdx=n.nodeValue.lastIndexOf('\n');}
if(e.offsetHeight==h)
n.nodeValue="";return str.substr(n.nodeValue.length);}
function createNodeAncestors(n,col1,col2,method){var ancestors=new Array;var insertNode=col2;var pn=n.parentNode;while(pn&&pn.id!=col1.id){ancestors[ancestors.length]=pn;if(!pn.id)pn.id=ut.randomId();pn=pn.parentNode;}
for(var i=ancestors.length-1;i>=0;i--){for(var j=0;j<insertNode.childNodes.length&&(insertNode.childNodes[j].nodeType==3||!insertNode.childNodes[j].className.match(ancestors[i].id+'-css3mc'));j++);if(j==insertNode.childNodes.length){if(method=='append')
insertNode=insertNode.appendChild(document.createElement(ancestors[i].tagName));else
insertNode=insertNode.insertBefore(document.createElement(ancestors[i].tagName),insertNode.firstChild);insertNode.className=ancestors[i].className+' '+ancestors[i].id+'-css3mc';insertNode.style.marginTop="0";insertNode.style.paddingTop="0";if(insertNode.tagName.toUpperCase()=='OL'&&n.nodeType==1&&n.tagName.toUpperCase()=='LI'){var prevsib=n.previousSibling;var count=0;while(prevsib){if(prevsib.nodeType==1&&prevsib.tagName.toUpperCase()=='LI')
count++;prevsib=prevsib.previousSibling;}
insertNode.setAttribute('start',count);}}else{insertNode=insertNode.childNodes[j];if(insertNode.tagName.toUpperCase()=='OL'&&(insertNode.start==-1||insertNode.start==1)&&n.nodeType==1&&n.tagName.toUpperCase()=='LI'){var prevsib=n.previousSibling;var count=0;while(prevsib){if(prevsib.nodeType==1&&prevsib.tagName.toUpperCase()=='LI')
count++;prevsib=prevsib.previousSibling;}
insertNode.setAttribute('start',count);}}}
return insertNode;}
function moveNode(n,col1,col2){var insertNode=createNodeAncestors(n,col1,col2,'append');var movedNode=insertNode.appendChild(n.parentNode.removeChild(n));if(insertNode.id==col2.id&&movedNode.nodeType==1){movedNode.style.paddingTop="0px";movedNode.style.marginTop="0px";}
return movedNode;}
function getElementRelativeTop(obj,refObj){var cur=0;if(obj.offsetParent){while(obj.offsetParent){cur+=obj.offsetTop;obj=obj.offsetParent;}}
var cur2=0;if(refObj.offsetParent){while(refObj.offsetParent){cur2+=refObj.offsetTop;refObj=refObj.offsetParent;}}
return cur-cur2;}}
function CSS3Utility(){this.handlerList=new Array();}
CSS3Utility.prototype.cssQuery=function(){var version="1.0.1";var STANDARD_SELECT=/^[^>\+~\s]/;var STREAM=/[\s>\+~:@#\.]|[^\s>\+~:@#\.]+/g;var NAMESPACE=/\|/;var IMPLIED_SELECTOR=/([\s>\+~\,]|^)([\.:#@])/g;var ASTERISK="$1*$2";var WHITESPACE=/^\s+|\s*([\+\,>\s;:])\s*|\s+$/g;var TRIM="$1";var NODE_ELEMENT=1;var NODE_TEXT=3;var NODE_DOCUMENT=9;var isMSIE=/MSIE/.test(navigator.appVersion),isXML;var cssCache={};function cssQuery(selector,from){if(!selector)return[];var useCache=arguments.callee.caching&&!from;from=(from)?(from.constructor==Array)?from:[from]:[document];isXML=false;var selectors=parseSelector(selector).split(",");var match=[];for(var i in selectors){selector=toStream(selectors[i]);var j=0,token,filter,cacheSelector="",filtered=from;while(j<selector.length){token=selector[j++];filter=selector[j++];cacheSelector+=token+filter;filtered=(useCache&&cssCache[cacheSelector])?cssCache[cacheSelector]:select(filtered,token,filter);if(useCache)cssCache[cacheSelector]=filtered;}
match=match.concat(filtered);}
return match;};cssQuery.caching=false;cssQuery.reset=function(){cssCache={};};cssQuery.toString=function(){return"function cssQuery() {\n  [version "+version+"]\n}";};var checkXML=(isMSIE)?function(node){if(node.nodeType!=NODE_DOCUMENT)node=node.document;return node.mimeType=="XML Document";}:function(node){if(node.nodeType==NODE_DOCUMENT)node=node.documentElement;return node.localName!="HTML";};function parseSelector(selector){return selector.replace(WHITESPACE,TRIM).replace(attributeSelector.ALL,attributeSelector.ID).replace(IMPLIED_SELECTOR,ASTERISK);};function toStream(selector){if(STANDARD_SELECT.test(selector))selector=" "+selector;return selector.match(STREAM)||[];};var pseudoClasses={"link":function(element){for(var i=0;i<document.links;i++){if(document.links[i]==element)return true;}},"visited":function(element){},"first-child":function(element){return!previousElement(element);},"last-child":function(element){return!nextElement(element);},"root":function(element){var document=element.ownerDocument||element.document;return Boolean(element==document.documentElement);},"empty":function(element){for(var i=0;i<element.childNodes.length;i++){if(isElement(element.childNodes[i])||element.childNodes[i].nodeType==NODE_TEXT)return false;}
return true;}};var QUOTED=/([\'\"])[^\1]*\1/;function quote(value){return(QUOTED.test(value))?value:"'"+value+"'"};function unquote(value){return(QUOTED.test(value))?value.slice(1,-1):value};var attributeSelectors=[];function attributeSelector(attribute,compare,value){this.id=attributeSelectors.length;var test="element.";switch(attribute.toLowerCase()){case"id":test+="id";break;case"class":test+="className";break;default:test+="getAttribute('"+attribute+"')";}
switch(compare){case"=":test+="=="+quote(value);break;case"~=":test="/(^|\\s)"+unquote(value)+"(\\s|$)/.test("+test+")";break;case"|=":test="/(^|-)"+unquote(value)+"(-|$)/.test("+test+")";break;}
push(attributeSelectors,new Function("element","return "+test));};attributeSelector.prototype.toString=function(){return attributeSelector.PREFIX+this.id;};attributeSelector.PREFIX="@";attributeSelector.ALL=/\[([^~|=\]]+)([~|]?=?)([^\]]+)?\]/g;attributeSelector.ID=function(match,attribute,compare,value){return new attributeSelector(attribute,compare,value);};function select(from,token,filter){var namespace="";if(NAMESPACE.test(filter)){filter=filter.split("|");namespace=filter[0];filter=filter[1];}
var filtered=[],i;switch(token){case" ":for(i in from){if(typeof from[i]=='function')continue;var subset=getElementsByTagNameNS(from[i],filter,namespace);for(var j=0;j<subset.length;j++){if(isElement(subset[j])&&(!namespace||compareNamespace(subset[j],namespace)))
push(filtered,subset[j]);}}
break;case">":for(i in from){var subset=from[i].childNodes;for(var j=0;j<subset.length;j++)
if(compareTagName(subset[j],filter,namespace))push(filtered,subset[j]);}
break;case"+":for(i in from){var adjacent=nextElement(from[i]);if(adjacent&&compareTagName(adjacent,filter,namespace))push(filtered,adjacent);}
break;case"~":for(i in from){var adjacent=from[i];while(adjacent=nextElement(adjacent)){if(adjacent&&compareTagName(adjacent,filter,namespace))push(filtered,adjacent);}}
break;case".":filter=new RegExp("(^|\\s)"+filter+"(\\s|$)");for(i in from)if(filter.test(from[i].className))push(filtered,from[i]);break;case"#":for(i in from)if(from[i].id==filter)push(filtered,from[i]);break;case"@":filter=attributeSelectors[filter];for(i in from)if(filter(from[i]))push(filtered,from[i]);break;case":":filter=pseudoClasses[filter];for(i in from)if(filter(from[i]))push(filtered,from[i]);break;}
return filtered;};var getElementsByTagNameNS=(isMSIE)?function(from,tagName){return(tagName=="*"&&from.all)?from.all:from.getElementsByTagName(tagName);}:function(from,tagName,namespace){return(namespace)?from.getElementsByTagNameNS("*",tagName):from.getElementsByTagName(tagName);};function compareTagName(element,tagName,namespace){if(namespace&&!compareNamespace(element,namespace))return false;return(tagName=="*")?isElement(element):(isXML)?(element.tagName==tagName):(element.tagName==tagName.toUpperCase());};var PREFIX=(isMSIE)?"scopeName":"prefix";function compareNamespace(element,namespace){return element[PREFIX]==namespace;};function previousElement(element){while((element=element.previousSibling)&&!isElement(element))continue;return element;};function nextElement(element){while((element=element.nextSibling)&&!isElement(element))continue;return element;};function isElement(node){return Boolean(node.nodeType==NODE_ELEMENT&&node.tagName!="!");};function push(array,item){array[array.length]=item;};if("i".replace(/i/,function(){return""})){var string_replace=String.prototype.replace;var function_replace=function(regexp,replacement){var match,newString="",string=this;while((match=regexp.exec(string))){newString+=string.slice(0,match.index)+replacement(match[0],match[1],match[2],match[3],match[4]);string=string.slice(match.lastIndex);}
return newString+string;};String.prototype.replace=function(regexp,replacement){this.replace=(typeof replacement=="function")?function_replace:string_replace;return this.replace(regexp,replacement);};}
return cssQuery;}();CSS3Utility.prototype.XBrowserAddEventHandler=function(target,eventName,handlerName){if(!target)return;if(target.addEventListener){target.addEventListener(eventName,function(e){eval(handlerName)(e);},false);}else if(target.attachEvent){target.attachEvent("on"+eventName,function(e){eval(handlerName)(e);});}else{var originalHandler=target["on"+eventName];if(originalHandler){target["on"+eventName]=function(e){originalHandler(e);eval(handlerName)(e);};}else{target["on"+eventName]=eval(handlerName);}}
var l=this.handlerList.length;this.handlerList[l]=new Array(2);this.handlerList[l][0]=target.id;this.handlerList[l][1]=eventName;}
CSS3Utility.prototype.getPseudoCssRules=function(propertyName,serializedStylesheet){this.cssRules=new Array();var valuePattern=propertyName.replace("-","\-")+"[\\s]*:[\\s]*([^;}]*)[;}]";var selectorPattern="$";var regx=new RegExp(valuePattern,"g");var regxMatch=regx.exec(serializedStylesheet);var j=0;while(regxMatch){var str=serializedStylesheet.substr(0,serializedStylesheet.substr(0,serializedStylesheet.indexOf(regxMatch[0])).lastIndexOf('{'));var selectorText=str.substr(str.lastIndexOf('}')+1).replace(/^\s*|\s*$/g,"");this.cssRules[j]=new Object();this.cssRules[j].selectorText=selectorText;this.cssRules[j].property=propertyName;this.cssRules[j].value=regxMatch[1].replace(/(\r?\n)*/g,"");j++;regxMatch=regx.exec(serializedStylesheet);}}
CSS3Utility.prototype.randomId=function(){var rId="";for(var i=0;i<6;i++)
rId+=String.fromCharCode(97+Math.floor((Math.random()*24)))
return rId;}
CSS3Utility.prototype.debug=function(text){var debugOutput=document.getElementById('debugOutput');if(typeof debugOutput!="undefined"&&debugOutput){debugOutput.innerHTML+=text;}}
var css3MC=new CSS3MultiColumn();if(typeof jQuery!='undefined'){(function($){$.scrollFollow=function(box,options)
{box=$(box);var position=box.css('position');function ani()
{box.queue([]);var viewportHeight=parseInt($(window).height());var pageScroll=parseInt($(document).scrollTop());var parentTop=parseInt(box.cont.offset().top);var parentHeight=parseInt(box.cont.attr('offsetHeight'));var boxHeight=parseInt(box.attr('offsetHeight')+(parseInt(box.css('marginTop'))||0)+(parseInt(box.css('marginBottom'))||0));var aniTop;if(isActive)
{if(options.relativeTo=='top')
{if(box.initialOffsetTop>=(pageScroll+options.offset))
{aniTop=box.initialTop;}
else
{aniTop=Math.min((Math.max((-parentTop),(pageScroll-box.initialOffsetTop+box.initialTop))+options.offset),(parentHeight-boxHeight-box.paddingAdjustment));}}
else if(options.relativeTo=='bottom')
{if((box.initialOffsetTop+boxHeight)>=(pageScroll+options.offset+viewportHeight))
{aniTop=box.initialTop;}
else
{aniTop=Math.min((pageScroll+viewportHeight-boxHeight-options.offset),(parentHeight-boxHeight));}}
if((new Date().getTime()-box.lastScroll)>=(options.delay-20))
{box.animate({top:aniTop},options.speed,options.easing);}}};var isActive=true;if($.cookie!=undefined)
{if($.cookie('scrollFollowSetting'+box.attr('id'))=='false')
{var isActive=false;$('#'+options.killSwitch).text(options.offText).toggle(function()
{isActive=true;$(this).text(options.onText);$.cookie('scrollFollowSetting'+box.attr('id'),true,{expires:365,path:'/'});ani();},function()
{isActive=false;$(this).text(options.offText);box.animate({top:box.initialTop},options.speed,options.easing);$.cookie('scrollFollowSetting'+box.attr('id'),false,{expires:365,path:'/'});});}
else
{$('#'+options.killSwitch).text(options.onText).toggle(function()
{isActive=false;$(this).text(options.offText);box.animate({top:box.initialTop},0);$.cookie('scrollFollowSetting'+box.attr('id'),false,{expires:365,path:'/'});},function()
{isActive=true;$(this).text(options.onText);$.cookie('scrollFollowSetting'+box.attr('id'),true,{expires:365,path:'/'});ani();});}}
if(options.container=='')
{box.cont=box.parent();}
else
{box.cont=$('#'+options.container);}
box.initialOffsetTop=parseInt(box.offset().top);box.initialTop=parseInt(box.css('top'))||0;if(box.css('position')=='relative')
{box.paddingAdjustment=parseInt(box.cont.css('paddingTop'))+parseInt(box.cont.css('paddingBottom'));}
else
{box.paddingAdjustment=0;}
$(window).scroll(function()
{$.fn.scrollFollow.interval=setTimeout(function(){ani();},options.delay);box.lastScroll=new Date().getTime();});$(window).resize(function()
{$.fn.scrollFollow.interval=setTimeout(function(){ani();},options.delay);box.lastScroll=new Date().getTime();});box.lastScroll=0;ani();};$.fn.scrollFollow=function(options)
{options=options||{};options.relativeTo=options.relativeTo||'top';options.speed=options.speed||500;options.offset=options.offset||0;options.easing=options.easing||'swing';options.container=options.container||this.parent().attr('id');options.killSwitch=options.killSwitch||'killSwitch';options.onText=options.onText||'Turn Slide Off';options.offText=options.offText||'Turn Slide On';options.delay=options.delay||0;this.each(function()
{new $.scrollFollow(this,options);});return this;};})(jQuery);}
var items=new Array;var markers=new Array;var param_iconType="green";var param_iconOverType="red";function getIcons(rank){var iconImageUrl;var iconImageOverUrl;var iconImageOutUrl;if(rank>0&&rank<100){iconImageOutUrl="http://gmaps-samples.googlecode.com/svn/trunk/"+"markers/"+param_iconType+"/marker"+rank+".png";iconImageOverUrl="http://gmaps-samples.googlecode.com/svn/trunk/"+"markers/"+param_iconOverType+"/marker"+rank+".png";}else{iconImageOutUrl="http://gmaps-samples.googlecode.com/svn/trunk/"+"markers/"+param_iconType+"/blank.png";iconImageOverUrl="http://gmaps-samples.googlecode.com/svn/trunk/"+"markers/"+param_iconOverType+"/blank.png";}
return[iconImageOutUrl,iconImageOverUrl];}
function cm_createMarker(map,latlng,id,title,url){var iconSize=new google.maps.Size(20,34);var iconShadowSize=new google.maps.Size(37,34);var iconHotSpotOffset=new google.maps.Point(9,0);var iconPosition=new google.maps.Point(0,0);var infoWindowAnchor=new google.maps.Point(9,2);var infoShadowAnchor=new google.maps.Point(18,25);var iconShadowUrl="http://www.google.com/mapfiles/shadow50.png";var iconImageUrl;var iconImageOverUrl;var iconImageOutUrl;var rank=id+1;var icons=getIcons(rank);iconImageOutUrl=icons[0];iconImageOverUrl=icons[1];iconImageUrl=iconImageOutUrl;if(rank>0&&rank<100){iconImageOutUrl="http://gmaps-samples.googlecode.com/svn/trunk/"+"markers/"+param_iconType+"/marker"+rank+".png";iconImageOverUrl="http://gmaps-samples.googlecode.com/svn/trunk/"+"markers/"+param_iconOverType+"/marker"+rank+".png";iconImageUrl=iconImageOutUrl;}else{iconImageOutUrl="http://gmaps-samples.googlecode.com/svn/trunk/"+"markers/"+param_iconType+"/blank.png";iconImageOverUrl="http://gmaps-samples.googlecode.com/svn/trunk/"+"markers/"+param_iconOverType+"/blank.png";iconImageUrl=iconImageOutUrl;}
var markerShadow=new google.maps.MarkerImage(iconShadowUrl,iconShadowSize,iconPosition,iconHotSpotOffset);var markerImage=new google.maps.MarkerImage(iconImageUrl,iconSize,iconPosition,iconHotSpotOffset);var markerImageOver=new google.maps.MarkerImage(iconImageOverUrl,iconSize,iconPosition,iconHotSpotOffset);var markerImageOut=new google.maps.MarkerImage(iconImageOutUrl,iconSize,iconPosition,iconHotSpotOffset);var markerOptions={title:title,icon:markerImage,shadow:markerShadow,position:latlng,map:map}
var marker=new google.maps.Marker(markerOptions);google.maps.event.addListener(marker,"mouseover",function(){marker.setIcon(markerImageOver);document.getElementById('icon'+items[id]['itemId']).src=iconImageOverUrl;});google.maps.event.addListener(marker,"mouseout",function(){marker.setIcon(markerImageOut);document.getElementById('icon'+items[id]['itemId']).src=iconImageOutUrl;});google.maps.event.addListener(marker,"click",function(){document.location=url;});return marker;}
function initialize(){if(items.length==0)return;var myOptions={zoom:14,scrollwheel:false,center:items[0]['position'],mapTypeId:google.maps.MapTypeId.ROADMAP}
var map=new google.maps.Map(document.getElementById("map_canvas"),myOptions);var bounds=new google.maps.LatLngBounds(items[0]['position'],items[0]['position']);for(var i=0;i<items.length;i++)
{bounds.extend(items[i]['position']);markers[i]=cm_createMarker(map,items[i]['position'],i,items[i]['title'],items[i]['url']);}
map.fitBounds(bounds);}
function addItem(lat,lng,id,title,url){var i=items.length;var rank=i+1;var icons=getIcons(rank);items[i]={itemId:id,position:new google.maps.LatLng(lat,lng),title:title,url:url};var item=document.getElementById(id);item.innerHTML='<img src="'+icons[0]+'" width="20" height="34" border="0" alt="" id="icon'+id+'">'+item.innerHTML;item.onmouseover=function(){google.maps.event.trigger(markers[i],'mouseover');};item.onmouseout=function(){google.maps.event.trigger(markers[i],'mouseout');};}
$(document).ready(function(){var id="#dialog";var maskHeight=$(document).height();var maskWidth=$(window).width();$('#mask').css({'width':maskWidth,'height':maskHeight});$('#mask').fadeIn(1000);$('#mask').fadeTo("slow",0.8);var winH=$(window).height();var winW=$(window).width();$(id).css('top',winH/2-$(id).height()/2);$(id).css('left',winW/2-$(id).width()/2);$(id).fadeIn(2000);$('.window .close').click(function(e){e.preventDefault();$('#mask').hide();$('.window').hide();});$('#mask').click(function(){$(this).hide();$('.window').hide();});});