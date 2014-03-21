/*!
 * SAP UI development toolkit for HTML5 (SAPUI5/OpenUI5)
 * (c) Copyright 2009-2014 SAP AG or an SAP affiliate company. 
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
jQuery.sap.declare("sap.ui.core.support.plugins.TechInfo");jQuery.sap.require("sap.ui.core.support.Plugin");jQuery.sap.require("jquery.sap.encoder");jQuery.sap.require("jquery.sap.script");(function(){sap.ui.core.support.Plugin.extend("sap.ui.core.support.plugins.TechInfo",{constructor:function(S){sap.ui.core.support.Plugin.apply(this,["sapUiSupportTechInfo","Technical Information",S]);this._aEventIds=this.isToolPlugin()?[this.getId()+"Data",this.getId()+"FinishedE2ETrace"]:[this.getId()+"ToggleDebug",this.getId()+"Refresh",this.getId()+"StartE2ETrace",this.getId()+"ToggleStatistics"];if(this.isToolPlugin()){this.e2eLogLevel="medium"}}});sap.ui.core.support.plugins.TechInfo.prototype.onsapUiSupportTechInfoData=function(e){var t=this;var d=e.getParameter("data");d.modules.sort();var h=["<div class='sapUiSupportToolbar'>","<a href='javascript:void(0);' id='",t.getId(),"-Refresh' class='sapUiSupportLink'>Refresh</a>","<div><div class='sapUiSupportTechInfoCntnt'>","<table border='0' cellpadding='3'>"];l(h,true,true,"SAPUI5 Version",function(b){b.push(d.version," (built at ",d.build,", last change ",d.change,")")});l(h,true,true,"User Agent",function(b){b.push(d.useragent,(d.docmode?", Document Mode '"+d.docmode+"'":""))});l(h,true,true,"Debug Sources",function(b){b.push((d.debug?"ON":"OFF"),"<a href='javascript:void(0);' id='",t.getId(),"-tggleDbgSrc' class='sapUiSupportLink'>Toggle</a>")});l(h,true,true,"Application",d.appurl);m(h,true,true,"Configuration (bootstrap)",d.bootconfig);m(h,true,true,"Configuration (computed)",d.config);l(h,true,true,"Loaded Modules",function(b){jQuery.each(d.modules,function(i,v){if(v.indexOf("sap.ui.core.support")<0){b.push("<span>",v,"</span>");if(i<d.modules.length-1){b.push(", ")}}})});m(h,true,true,"URI Parameters",d.uriparams);l(h,true,true,"E2E Trace",function(b){b.push("<label class='sapUiSupportLabel'>Trace Level:</label>","<select id='",t.getId(),"-logLevelE2ETrace' class='sapUiSupportTxtFld' style='margin-left:10px'>","<option value='low'"+(t.e2eLogLevel==='low'?" selected":"")+">LOW</option>","<option value='medium'"+(t.e2eLogLevel==='medium'?" selected":"")+">MEDIUM</option>","<option value='high'"+(t.e2eLogLevel==='hight'?" selected":"")+">HIGH</option>","</select>");b.push("<button id='"+t.getId()+"-startE2ETrace' class='sapUiSupportBtn "+(d["e2e-trace"].isStarted?" active":"")+"' style='margin-left: 10px;'>Start</button>");b.push("<div style='margin-top:5px'>");b.push("<label class='sapUiSupportLabel'>XML Output:</label>");b.push("<textarea id='"+t.getId()+"-outputE2ETrace' style='width:100%;height:50px;margin-top:5px;resize:none;box-sizing:border-box'></textarea>");b.push("</div>")});l(h,true,true,"SAP-statistics for oData calls",function(b){b.push((d.statistics?"ON":"OFF"),"<a href='javascript:void(0);' id='",t.getId(),"-tggleStatistics' class='sapUiSupportLink'>Toggle</a>")});h.push("</table></div>");this.$().html(h.join(""));jQuery.sap.byId(this.getId()+"-tggleDbgSrc").bind("click",function(){sap.ui.core.support.Support.getStub().sendEvent(t.getId()+"ToggleDebug",{})});jQuery.sap.byId(this.getId()+"-Refresh").bind("click",function(){sap.ui.core.support.Support.getStub().sendEvent(t.getId()+"Refresh",{})});jQuery.sap.byId(this.getId()+"-outputE2ETrace").bind("click",function(){this.focus();this.select()});this.$("tggleStatistics").bind("click",function(){sap.ui.core.support.Support.getStub().sendEvent(t.getId()+"ToggleStatistics",{})});if(!d["e2e-trace"].isStarted){jQuery.sap.byId(this.getId()+"-startE2ETrace").bind("click",function(){t.e2eLogLevel=jQuery.sap.byId(t.getId()+"-logLevelE2ETrace").val();jQuery.sap.byId(t.getId()+"-startE2ETrace").addClass("active").text("Running...");jQuery.sap.byId(t.getId()+"-outputE2ETrace").text("");sap.ui.core.support.Support.getStub().sendEvent(t.getId()+"StartE2ETrace",{level:t.e2eLogLevel})})}document.title="SAPUI5 Diagnostics - "+d.title};sap.ui.core.support.plugins.TechInfo.prototype.onsapUiSupportTechInfoToggleDebug=function(e){jQuery.sap.debug(!!!jQuery.sap.debug());s(this)};sap.ui.core.support.plugins.TechInfo.prototype.onsapUiSupportTechInfoStartE2ETrace=function(e){if(!jQuery.sap.isDeclared("sap.ui.core.support.trace.E2eTraceLib")){jQuery.sap.require("sap.ui.core.support.trace.E2eTraceLib")}var t=this;sap.ui.core.support.trace.E2eTraceLib.start(e.getParameter("level"),function(a){sap.ui.core.support.Support.getStub().sendEvent(t.getId()+"FinishedE2ETrace",{trace:a})})};sap.ui.core.support.plugins.TechInfo.prototype.onsapUiSupportTechInfoFinishedE2ETrace=function(e){jQuery.sap.byId(this.getId()+"-startE2ETrace").removeClass("active").text("Start");jQuery.sap.byId(this.getId()+"-outputE2ETrace").text(e.getParameter("trace"))};sap.ui.core.support.plugins.TechInfo.prototype.onsapUiSupportTechInfoRefresh=function(e){s(this)};sap.ui.core.support.plugins.TechInfo.prototype.onsapUiSupportTechInfoToggleStatistics=function(e){jQuery.sap.statistics(!jQuery.sap.statistics());s(this)};sap.ui.core.support.plugins.TechInfo.prototype.init=function(S){sap.ui.core.support.Plugin.prototype.init.apply(this,arguments);if(!this.isToolPlugin()){s(this);return}this.$().html("No Information available")};function s(p){var c=sap.ui.getCore().getConfiguration();var C={"theme":c.getTheme(),"language":c.getLanguage(),"formatLocale":c.getFormatLocale(),"accessibility":""+c.getAccessibility(),"animation":""+c.getAnimation(),"rtl":""+c.getRTL(),"debug":""+c.getDebug(),"inspect":""+c.getInspect(),"originInfo":""+c.getOriginInfo(),"noDuplicateIds":""+c.getNoDuplicateIds()};var d={"version":sap.ui.version,"build":sap.ui.buildinfo.buildtime,"change":sap.ui.buildinfo.lastchange,"useragent":navigator.userAgent,"docmode":document.documentMode?document.documentMode:"","debug":jQuery.sap.debug(),"bootconfig":window["sap-ui-config"]?window["sap-ui-config"]:{},"config":C,"modules":jQuery.sap.getAllDeclaredModules(),"uriparams":jQuery.sap.getUriParameters().mParams,"appurl":window.location.href,"title":document.title,"statistics":jQuery.sap.statistics()};if(jQuery.sap.isDeclared("sap.ui.core.support.trace.E2eTraceLib")){d["e2e-trace"]={isStarted:sap.ui.core.support.trace.E2eTraceLib.isStarted()}}else{d["e2e-trace"]={isStarted:false}}sap.ui.core.support.Support.getStub().sendEvent(p.getId()+"Data",{data:d})};function l(b,r,a,c,d){b.push("<tr><td ",r?"align='right' ":"","valign='top'>","<label class='sapUiSupportLabel'>",jQuery.sap.escapeHTML(c),"</label></td><td",a?" class='sapUiSupportTechInfoBorder'":"",">");var e=d;if(jQuery.isFunction(d)){e=d(b)||""}b.push(jQuery.sap.escapeHTML(e));b.push("</td></tr>")};function m(b,r,a,c,d){l(b,r,a,c,function(b){b.push("<table border='0' cellspacing='0' cellpadding='3'>");jQuery.each(d,function(i,v){var e="";if(v){if(typeof(v)==="string"||typeof(v)==="string"||typeof(v)==="boolean"){e=v}else if((jQuery.isArray(v)||jQuery.isPlainObject(v))&&window.JSON){e=window.JSON.stringify(v)}}l(b,false,false,i,""+e)});b.push("</table>")})}}());
