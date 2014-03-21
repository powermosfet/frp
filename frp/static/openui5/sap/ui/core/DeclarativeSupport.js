/*!
 * SAP UI development toolkit for HTML5 (SAPUI5/OpenUI5)
 * (c) Copyright 2009-2014 SAP AG or an SAP affiliate company. 
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
jQuery.sap.declare("sap.ui.core.DeclarativeSupport");sap.ui.core.DeclarativeSupport={};sap.ui.core.DeclarativeSupport.attributes={"data-sap-ui-type":true,"data-sap-ui-aggregation":true,"data-sap-ui-default-aggregation":true,"data-sap-ui-binding":function(v,s){var b=sap.ui.base.ManagedObject.bindingParser(v);s.objectBindings=s.objectBindings||{};s.objectBindings[b.model||undefined]=b},"data-tooltip":function(v,s){s["tooltip"]=v},"tooltip":function(v,s,c){s["tooltip"]=v;jQuery.sap.log.warning('[Deprecated] Control "'+s.id+'": The attribute "tooltip" is not prefixed with "data-*". Future version of declarative support will only suppport attributes with "data-*" prefix.')},"class":true,"style":true,"id":true};
sap.ui.core.DeclarativeSupport.compile=function(e,v,i){var s=this;jQuery(e).find("[data-sap-ui-type]").filter(function(){return jQuery(this).parents("[data-sap-ui-type]").length===0}).each(function(){s._compile(this,v,i)})};
sap.ui.core.DeclarativeSupport._compile=function(e,v,i){var $=jQuery(e);var t=$.attr("data-sap-ui-type");var c=[];var I=t==="sap.ui.core.UIArea";if(I){var s=this;$.children().each(function(){var C=s._createControl(this,v);if(C){c.push(C)}})}else{var C=this._createControl(e,v);if(C){c.push(C)}}$.empty();var a=[];jQuery.each(e.attributes,function(b,A){var n=A.name;if(!I||I&&/^data-/g.test(n.toLowerCase())){a.push(n)}});if(a.length>0){$.removeAttr(a.join(" "))}jQuery.each(c,function(k,C){if(C instanceof sap.ui.core.Control){if(v&&!i){v.addContent(C)}else{C.placeAt(e);if(v){v.connectControl(C)}}}})};
sap.ui.core.DeclarativeSupport._createControl=function(e,v){var $=jQuery(e);var c=null;var t=$.attr("data-sap-ui-type");if(t){jQuery.sap.require(t);var C=jQuery.sap.getObject(t);var s={};var i=s.id=this._getId($,v);this._addSettingsForAttributes(s,C,e,v);this._addSettingsForAggregations(s,C,e,v);var c;if(sap.ui.core.mvc.View.prototype.isPrototypeOf(C.prototype)&&typeof C._sType==="string"){c=sap.ui.view(s,undefined,C._sType)}else{c=new C(s)}if(e.className){c.addStyleClass(e.className)}$.removeAttr("data-sap-ui-type")}else{c=this._createHtmlControl(e,v)}return c};
sap.ui.core.DeclarativeSupport._createHtmlControl=function(e,v){var h=new sap.ui.core.HTML();h.setDOMContent(e);this.compile(e,v,true);return h};
sap.ui.core.DeclarativeSupport._addSettingsForAttributes=function(s,c,e,v){var a=this;var S=sap.ui.core.DeclarativeSupport.attributes;var b=sap.ui.base.ManagedObject.bindingParser;var C=[];var r=/^data-custom-data:(.+)/i;jQuery.each(e.attributes,function(i,A){var n=A.name;var V=A.value;if(!r.test(n)){if(typeof S[n]==="undefined"){n=a.convertAttributeToSettingName(n,s.id);var p=a._getProperty(c,n);if(p){var B=b(V,v&&v.getController(),true);if(B&&typeof B==="object"){s[n]=B}else{s[n]=a.convertValueToType(a.getPropertyDataType(p),B||V)}}else if(a._getAssociation(c,n)){var o=a._getAssociation(c,n);if(o.multiple){V=V.replace(/\s*,\s*|\s+/g,",");var I=V.split(",");jQuery.each(I,function(i,g){I[i]=v?v.createId(g):g});s[n]=I}else{s[n]=v?v.createId(V):V}}else if(a._getAggregation(c,n)){var d=a._getAggregation(c,n);if(d.multiple){var B=b(V,v&&v.getController());if(B){s[n]=B}else{throw new Error("Aggregation "+n+" with cardinality 0..n only allows binding paths as attribute value")}}else if(d.altTypes){var B=b(V,v&&v.getController(),true);if(B&&typeof B==="object"){s[n]=B}else{s[n]=a.convertValueToType(d.altTypes[0],B||V)}}else{throw new Error("Aggregation "+n+" not supported")}}else if(a._getEvent(c,n)){var h=jQuery.sap.getObject(V);if(v&&typeof h==="undefined"){var f=(v._oContainingView||v).getController();h=f[V];if(typeof h==="function"){h=jQuery.proxy(h,f);h._sapui_handlerName=V}}if(typeof h==="function"){s[n]=h}else{throw new Error('Control "'+s.id+'": The function "'+V+'" for the event "'+n+'" is not defined')}}}else if(typeof S[n]==="function"){S[n](V,s,c)}}else{n=jQuery.sap.camelCase(r.exec(n)[1]);var B=b(V,v&&v.getController());C.push(new sap.ui.core.CustomData({key:n,value:B||V}))}});if(C.length>0){s.customData=C}return s};
sap.ui.core.DeclarativeSupport._addSettingsForAggregations=function(s,c,e,v){var $=jQuery(e);var d=this._getDefaultAggregation(c,e);var a=this;var A=c.getMetadata().getAllAggregations();$.children().each(function(){var b=jQuery(this);var f=b.attr("data-sap-ui-aggregation");var t=b.attr("data-sap-ui-type");var u=false;if(!f){u=true;f=d}if(f&&A[f]){var m=A[f].multiple;var g=function(C){var o=a._createControl(C,v);if(o){if(m){if(!s[f]){s[f]=[]}if(typeof s[f].path==="string"){s[f].template=o}else{s[f].push(o)}}else{s[f]=o}}};if(u||(t&&!u)){g(this)}else{b.children().each(function(){g(this)})}}b.removeAttr("data-sap-ui-aggregation");b.removeAttr("data-sap-ui-type")});return s};
sap.ui.core.DeclarativeSupport._getId=function(e,v){var $=jQuery(e);var i=$.attr("id");if(i){if(v){i=v.createId(i);$.attr("data-sap-ui-id",i)}$.attr("id","")}return i};
sap.ui.core.DeclarativeSupport._getProperty=function(c,n){return c.getMetadata().getAllProperties()[n]};
sap.ui.core.DeclarativeSupport.convertValueToType=function(t,v){if(t instanceof sap.ui.base.DataType){v=t.parseValue(v)}return typeof v==="string"?sap.ui.base.ManagedObject.bindingParser.escape(v):v};
sap.ui.core.DeclarativeSupport.getPropertyDataType=function(p){var t=sap.ui.base.DataType.getType(p.type);if(!t){throw new Error("Property "+p.name+" has no known type")}return t};
sap.ui.core.DeclarativeSupport.convertAttributeToSettingName=function(a,i,d){if(a.indexOf("data-")===0){a=a.substr(5)}else if(d){jQuery.sap.log.warning('[Deprecated] Control "'+i+'": The attribute "'+a+'" is not prefixed with "data-*". Future version of declarative support will only suppport attributes with "data-*" prefix.')}else{throw new Error('Control "'+i+'": The attribute "'+a+'" is not prefixed with "data-*".')}return jQuery.sap.camelCase(a)};
sap.ui.core.DeclarativeSupport._getAssociation=function(c,n){return c.getMetadata().getAllAssociations()[n]};
sap.ui.core.DeclarativeSupport._getAggregation=function(c,n){return c.getMetadata().getAllAggregations()[n]};
sap.ui.core.DeclarativeSupport._getEvent=function(c,n){return c.getMetadata().getAllEvents()[n]};
sap.ui.core.DeclarativeSupport._getDefaultAggregation=function(c,e){var $=jQuery(e);var d=$.attr("data-sap-ui-default-aggregation")||c.getMetadata().getDefaultAggregationName();$.removeAttr("data-sap-ui-default-aggregation");return d};
