/*!
 * SAP UI development toolkit for HTML5 (SAPUI5/OpenUI5)
 * (c) Copyright 2009-2014 SAP AG or an SAP affiliate company. 
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
jQuery.sap.declare("sap.m.ListBase");jQuery.sap.require("sap.m.library");jQuery.sap.require("sap.ui.core.Control");sap.ui.core.Control.extend("sap.m.ListBase",{metadata:{publicMethods:["getSelectedItem","setSelectedItem","getSelectedItems","setSelectedItemById","removeSelections","selectAll","getSwipedItem","swipeOut","getGrowingInfo","getSelectedContexts"],library:"sap.m",properties:{"inset":{type:"boolean",group:"Appearance",defaultValue:false},"visible":{type:"boolean",group:"Appearance",defaultValue:true},"headerText":{type:"string",group:"Misc",defaultValue:null},"headerDesign":{type:"sap.m.ListHeaderDesign",group:"Appearance",defaultValue:sap.m.ListHeaderDesign.Standard,deprecated:true},"footerText":{type:"string",group:"Misc",defaultValue:null},"mode":{type:"sap.m.ListMode",group:"Behavior",defaultValue:sap.m.ListMode.None},"width":{type:"sap.ui.core.CSSSize",group:"Dimension",defaultValue:'100%'},"includeItemInSelection":{type:"boolean",group:"Behavior",defaultValue:false},"showUnread":{type:"boolean",group:"Misc",defaultValue:false},"noDataText":{type:"string",group:"Misc",defaultValue:null},"showNoData":{type:"boolean",group:"Misc",defaultValue:true},"modeAnimationOn":{type:"boolean",group:"Misc",defaultValue:true},"showSeparators":{type:"sap.m.ListSeparators",group:"Appearance",defaultValue:sap.m.ListSeparators.All},"swipeDirection":{type:"sap.m.SwipeDirection",group:"Misc",defaultValue:sap.m.SwipeDirection.Both},"growing":{type:"boolean",group:"Behavior",defaultValue:false},"growingThreshold":{type:"int",group:"Misc",defaultValue:20},"growingTriggerText":{type:"string",group:"Appearance",defaultValue:null},"growingScrollToLoad":{type:"boolean",group:"Behavior",defaultValue:false},"rememberSelections":{type:"boolean",group:"Behavior",defaultValue:true}},defaultAggregation:"items",aggregations:{"items":{type:"sap.m.ListItemBase",multiple:true,singularName:"item",bindable:"bindable"},"swipeContent":{type:"sap.ui.core.Control",multiple:false},"headerToolbar":{type:"sap.m.Toolbar",multiple:false},"infoToolbar":{type:"sap.m.Toolbar",multiple:false}},events:{"select":{deprecated:true},"selectionChange":{},"delete":{},"swipe":{allowPreventDefault:true},"growingStarted":{deprecated:true},"growingFinished":{deprecated:true},"updateStarted":{},"updateFinished":{}}}});sap.m.ListBase.M_EVENTS={'select':'select','selectionChange':'selectionChange','delete':'delete','swipe':'swipe','growingStarted':'growingStarted','growingFinished':'growingFinished','updateStarted':'updateStarted','updateFinished':'updateFinished'};jQuery.sap.require("sap.ui.core.theming.Parameters");jQuery.sap.require("sap.ui.core.delegate.ItemNavigation");
sap.m.ListBase.prototype.init=function(){this._oGrowingDelegate=null;this._bSelectionMode=false;this._bReceivingData=false;this._oSelectedItem=null;this._aSelectedPaths=[];this._aNavSections=[];this._bUpdating=false};
sap.m.ListBase.prototype.onBeforeRendering=function(){this._aNavSections.length=0;if(this.hasOwnProperty("_$touchBlocker")){this._removeSwipeContent();delete this._$touchBlocker}};
sap.m.ListBase.prototype.onAfterRendering=function(){this._startItemNavigation();if(!this._oGrowingDelegate){this._updateFinished()}};
sap.m.ListBase.prototype.exit=function(){this._detachDataEvents();this._oSelectedItem=null;this._bReceivingData=false;this._aNavSections.length=0;this._aSelectedPaths.length=0;this._destroyGrowingDelegate();this._destroyItemNavigation()};
sap.m.ListBase.prototype.updateItems=function(r){if(this._oGrowingDelegate){this._oGrowingDelegate.updateItems(r)}else{this._updateStarted(r);this.updateAggregation("items")}};
sap.m.ListBase.prototype.bindAggregation=function(n){if(n=="items"&&this.isBound("items")){this._bUpdating=false;this._detachDataEvents();this.removeSelections(true);this._oGrowingDelegate&&this._oGrowingDelegate.reset()}return sap.ui.base.ManagedObject.prototype.bindAggregation.apply(this,arguments)};
sap.m.ListBase.prototype.addAggregation=function(a,o){a=="items"&&this._applySettingsToItem(o);sap.ui.base.ManagedObject.prototype.addAggregation.apply(this,arguments);a=="items"&&this._applySelectionToItem(o);return this};
sap.m.ListBase.prototype.insertAggregation=function(a,o){a=="items"&&this._applySettingsToItem(o);sap.ui.base.ManagedObject.prototype.insertAggregation.apply(this,arguments);a=="items"&&this._applySelectionToItem(o);return this};
sap.m.ListBase.prototype.destroyAggregation=function(a){a=="items"&&(this._oSelectedItem=null);return sap.ui.base.ManagedObject.prototype.destroyAggregation.apply(this,arguments)};
sap.m.ListBase.prototype.removeAggregation=function(a){var o=sap.ui.base.ManagedObject.prototype.removeAggregation.apply(this,arguments);if(a=="items"&&o&&o===this._oSelectedItem){this._oSelectedItem=null}return o};
sap.m.ListBase.prototype.removeAllAggregation=function(a){a=="items"&&(this._oSelectedItem=null);return sap.ui.base.ManagedObject.prototype.removeAllAggregation.apply(this,arguments)};
sap.m.ListBase.prototype.getId=function(s){var i=this.sId;return s?i+"-"+s:i};
sap.m.ListBase.prototype.setGrowing=function(g){g=!!g;if(this.getGrowing()!=g){this.setProperty("growing",g,!g);if(g){jQuery.sap.require("sap.m.GrowingEnablement");this._oGrowingDelegate=new sap.m.GrowingEnablement(this,this.getItems().length)}else if(this._oGrowingDelegate){this._oGrowingDelegate.destroy();this._oGrowingDelegate=null}}return this};
sap.m.ListBase.prototype.setGrowingThreshold=function(t){this.setProperty("growingThreshold",t,true);this._oItemNavigation&&this._oItemNavigation.setPageSize(this.getGrowingThreshold());return this};
sap.m.ListBase.prototype.setGrowingTriggerText=function(t){this.setProperty("growingTriggerText",t,true);if(this._oGrowingDelegate){this._oGrowingDelegate.setTriggerText(this.getGrowingTriggerText())}return this};
sap.m.ListBase.prototype.setBackgroundDesign=function(b){var B=this.getBackgroundDesign();this.setProperty("backgroundDesign",b,true);this.$().removeClass("sapMListBG"+B).addClass("sapMListBG"+this.getBackgroundDesign());return this};
sap.m.ListBase.prototype.setShowSeparators=function(s){var S=this.getShowSeparators();this.setProperty("showSeparators",s,true);this.$("listUl").removeClass("sapMListShowSeparators"+S).addClass("sapMListShowSeparators"+this.getShowSeparators());return this};
sap.m.ListBase.prototype.setIncludeItemInSelection=function(i){i=this.validateProperty("includeItemInSelection",i);if(i!=this.getIncludeItemInSelection()){this.setProperty("includeItemInSelection",i,true);this.getItems().forEach(function(I){I._includeItemInSelection=i;I.$().toggleClass("sapMLIBCursor",i)})}return this};
sap.m.ListBase.prototype.setInset=function(i){i=this.validateProperty("inset",i);if(i!=this.getInset()){this.setProperty("inset",i,true);if(this.getDomRef()){this.$().toggleClass("sapMListInsetBG",i);this.$("listUl").toggleClass("sapMListInset",i);this._setSwipePosition()}}return this};
sap.m.ListBase.prototype.setWidth=function(w){this.setProperty("width",w,true);var d=this.getDomRef();if(d){d.style.width=this.getWidth()}return this};
sap.m.ListBase.prototype.setNoDataText=function(n){this.setProperty("noDataText",n,true);this.$("nodata-text").text(this.getNoDataText());return this};
sap.m.ListBase.prototype.getNoDataText=function(){var n=this.getProperty("noDataText");if(!n){var r=sap.ui.getCore().getLibraryResourceBundle("sap.m");n=r.getText("LIST_NO_DATA")}return n};
sap.m.ListBase.prototype.getSelectedItem=function(){var I=this.getItems();for(var i=0;i<I.length;i++){if(I[i].getSelected()){return I[i]}}return null};
sap.m.ListBase.prototype.setSelectedItem=function(l,s,f){if(!l instanceof sap.m.ListItemBase){jQuery.sap.log.warning("setSelectedItem is called without ListItem parameter on "+this);return}if(this._bSelectionMode){l.setSelected((typeof s=="undefined")?true:!!s);f&&this._fireSelectionChangeEvent([l])}};
sap.m.ListBase.prototype.getSelectedItems=function(){return this.getItems().filter(function(i){return i.getSelected()})};
sap.m.ListBase.prototype.setSelectedItemById=function(i,s){var l=sap.ui.getCore().byId(i);return this.setSelectedItem(l,s)};
sap.m.ListBase.prototype.getSelectedContexts=function(a){var b=this.getBindingInfo("items"),m=(b||{}).model,M=this.getModel(m);if(!b||!M){return[]}if(a&&this.getRememberSelections()){return this._aSelectedPaths.map(function(p){return M.getContext(p)})}return this.getSelectedItems().map(function(i){return i.getBindingContext(m)})};
sap.m.ListBase.prototype.removeSelections=function(a,f){var c=[];this._oSelectedItem=null;a&&(this._aSelectedPaths.length=0);this.getItems().forEach(function(i){if(i.getSelected()){i.setSelected(false,true);c.push(i);!a&&this._updateSelectedPaths(i)}},this);if(f&&c.length){this._fireSelectionChangeEvent(c)}return this};
sap.m.ListBase.prototype.selectAll=function(f){if(this.getMode()!="MultiSelect"){return this}var c=[];this.getItems().forEach(function(i){if(!i.getSelected()){i.setSelected(true,true);c.push(i);this._updateSelectedPaths(i)}},this);if(f&&c.length){this._fireSelectionChangeEvent(c)}return this};
sap.m.ListBase.prototype.setMode=function(m){var o=this.getMode();if(o!=m){this.setProperty("mode",m);var s=this.getSelectedItems().length;this._bSelectionMode=this.getMode().indexOf("Select")>-1;if(s>1||!this._bSelectionMode){this.removeSelections(true)}}return this};
sap.m.ListBase.prototype.getGrowingInfo=function(){if(this._oGrowingDelegate){return this._oGrowingDelegate.getInfo()}return null};
sap.m.ListBase.prototype.setRememberSelections=function(r){this.setProperty("rememberSelections",r,true);!this.getRememberSelections()&&(this._aSelectedPaths.length=0);return this};
sap.m.ListBase.prototype.onItemSetSelected=function(i,s){if(this.getMode()=="MultiSelect"){this._updateSelectedPaths(i,s);return}if(s){this._aSelectedPaths.length=0;this._oSelectedItem&&this._oSelectedItem.setSelected(false,true);this._oSelectedItem=i}else if(this._oSelectedItem===i){this._oSelectedItem=null}this._updateSelectedPaths(i,s)};
sap.m.ListBase.prototype.getItemsContainerDomRef=function(){return this.getDomRef("listUl")};
sap.m.ListBase.prototype.onBeforePageLoaded=function(g,c){this._updateStarted(c,g);this.fireGrowingStarted(g)};
sap.m.ListBase.prototype.onAfterPageLoaded=function(g,c){this._startItemNavigation();this.getShowNoData()&&this.getMaxItemsCount()&&this.$("nodata").remove();this._updateFinished(c,g);this.fireGrowingFinished(g)};
sap.m.ListBase.prototype.addNavSection=function(i){this._aNavSections.push(i);return i};
sap.m.ListBase.prototype.getMaxItemsCount=function(){var b=this.getBinding("items");if(b){return b.getLength()||0}return this.getItems().length};
sap.m.ListBase.prototype._attachDataEvents=function(){var b=this.getBinding("items");if(b){b.attachDataReceived(this._onDataReceived,this);b.attachDataRequested(this._onDataRequested,this)}};
sap.m.ListBase.prototype._detachDataEvents=function(){var b=this.getBinding("items");if(b){this._bReceivingData=false;b.detachDataReceived(this._onDataReceived,this);b.detachDataRequested(this._onDataRequested,this)}};
sap.m.ListBase.prototype._onDataRequested=function(){this._bReceivingData=true};
sap.m.ListBase.prototype._onDataReceived=function(){this._bReceivingData=false};
sap.m.ListBase.prototype._updateStarted=function(r,i){if(this._bUpdating||this._bReceivingData||!this.isBound("items")){return}this._bUpdating=true;!this.getGrowing()&&this._attachDataEvents();this._sUpdateReason=jQuery.sap.charToUpperCase(r||"Binding");this.fireUpdateStarted({reason:this._sUpdateReason,actual:i?i.actual:this.getItems().length,total:i?i.total:this.getMaxItemsCount()})};
sap.m.ListBase.prototype._updateFinished=function(r,i){if(!this._bUpdating||this._bReceivingData||!this.isBound("items")){return}!this.getGrowing()&&this._detachDataEvents();jQuery.sap.delayedCall(0,this,function(){this._bUpdating=false;this.fireUpdateFinished({reason:this._sUpdateReason||r,actual:i?i.actual:this.getItems().length,total:i?i.total:this.getMaxItemsCount()})})};
sap.m.ListBase.prototype._applySettingsToItem=function(i,o){if(!i||!i.isSelectable()){return i}i._mode=this.getMode();i._listId=this.getId();i._showUnread=this.getShowUnread();i._modeAnimationOn=this.getModeAnimationOn();i._includeItemInSelection=this.getIncludeItemInSelection();if(o){return i}i._select=this._select;i._delete=this._delete;if(!i.getParent()&&i.getSelected()){this.onItemSetSelected(i,true)}return i};
sap.m.ListBase.prototype._applySelectionToItem=function(i){if(!this.getRememberSelections()||!i||!this._bSelectionMode||!this._aSelectedPaths.length||i.getSelected()){return}var p=i.getBindingContextPath();if(p&&this._aSelectedPaths.indexOf(p)>-1){i.setSelected(true)}};
sap.m.ListBase.prototype._select=function(e){var l=sap.ui.getCore().byId(this.oParent.getId()),L=sap.ui.getCore().byId(l._listId),s=e.getParameter("selected"),m=L.getMode();l.setSelected(s);if(m=="MultiSelect"){L._fireSelectionChangeEvent([l])}else if(L._bSelectionMode&&s){L._fireSelectionChangeEvent([l])}};
sap.m.ListBase.prototype._selectTapped=function(l){this._fireSelectionChangeEvent([l])};
sap.m.ListBase.prototype._fireSelectionChangeEvent=function(l){var L=l&&l[0];if(!L){return}this.fireSelectionChange({listItem:L,listItems:l,selected:L.getSelected()});this.fireSelect({listItem:L})};
sap.m.ListBase.prototype._delete=function(e){var l=sap.ui.getCore().byId(this.oParent.getId());var L=sap.ui.getCore().byId(l._listId);L.fireDelete({listItem:l})};
sap.m.ListBase.prototype._updateSelectedPaths=function(i,s){if(!this.getRememberSelections()){return}var p=i.getBindingContextPath();if(!p){return}s=(typeof s=="undefined")?i.getSelected():s;var I=this._aSelectedPaths.indexOf(p);if(s){I<0&&this._aSelectedPaths.push(p)}else{I>-1&&this._aSelectedPaths.splice(I,1)}};
sap.m.ListBase.prototype._destroyGrowingDelegate=function(){if(this._oGrowingDelegate){this._oGrowingDelegate.destroy();this._oGrowingDelegate=null}};
sap.m.ListBase.prototype._destroyItemNavigation=function(){if(this._oItemNavigation){this.removeEventDelegate(this._oItemNavigation);this._oItemNavigation.destroy();this._oItemNavigation=null}};
sap.m.ListBase.prototype._getTouchBlocker=function(){return this._$touchBlocker||(this._$touchBlocker=this.$().children())};
sap.m.ListBase.prototype._getSwipeContainer=function(){return this._$swipeContainer||(jQuery.sap.require("sap.m.InstanceManager"),this._$swipeContainer=jQuery("<div>",{"id":this.getId("swp"),"class":"sapMListSwp"+(sap.ui.core.theming.Parameters.get("sapMPlatformDependent")=="true"&&jQuery.os.ios?" sapMBar-CTX":"")}))};
sap.m.ListBase.prototype._setSwipePosition=function(){if(this._isSwipeActive){return this._getSwipeContainer().css("top",this._swipedItem.$().position().top)}};
sap.m.ListBase.prototype._renderSwipeContent=function(){var $=this._swipedItem.$(),a=this._getSwipeContainer();this.$().prepend(a.css({top:$.position().top,height:$.outerHeight(true)}));if(this._bRerenderSwipeContent){this._bRerenderSwipeContent=false;var r=sap.ui.getCore().createRenderManager();r.render(this.getSwipeContent(),a.empty()[0]);r.destroy()}return this};
sap.m.ListBase.prototype._swipeIn=function(){var t=this,$=t._getTouchBlocker(),a=t._getSwipeContainer();t._isSwipeActive=true;t._renderSwipeContent();sap.m.InstanceManager.addDialogInstance(t);window.document.activeElement.blur();jQuery(window).on("resize.swp",function(){t._setSwipePosition()});$.css("pointer-events","none").on("touchstart.swp",function(e){if(!a[0].firstChild.contains(e.target)){e.preventDefault();e.stopPropagation()}});a.bind("webkitAnimationEnd animationend",function(){jQuery(this).unbind("webkitAnimationEnd animationend");a.css("opacity",1).focus();$.parent().on("touchend.swp",function(e){if(!a[0].firstChild.contains(e.target)){t.swipeOut()}})}).removeClass("sapMListSwpOutAnim").addClass("sapMListSwpInAnim")};
sap.m.ListBase.prototype._onSwipeOut=function(c){this._getSwipeContainer().css("opacity",0).remove();jQuery(window).off("resize.swp");this._getTouchBlocker().css("pointer-events","auto").off("touchstart.swp");if(typeof c=="function"){c.call(this,this._swipedItem,this.getSwipeContent())}this._isSwipeActive=false;sap.m.InstanceManager.removeDialogInstance(this)};
sap.m.ListBase.prototype.swipeOut=function(c){if(!this._isSwipeActive){return this}var t=this,$=this._getSwipeContainer();this._getTouchBlocker().parent().off("touchend.swp");$.bind("webkitAnimationEnd animationend",function(){jQuery(this).unbind("webkitAnimationEnd animationend");t._onSwipeOut(c)}).removeClass("sapMListSwpInAnim").addClass("sapMListSwpOutAnim");return this};
sap.m.ListBase.prototype._removeSwipeContent=function(){if(this._isSwipeActive){this.swipeOut()._onSwipeOut()}};
sap.m.ListBase.prototype.close=sap.m.ListBase.prototype._removeSwipeContent;
sap.m.ListBase.prototype._onSwipe=function(e){var c=this.getSwipeContent(),s=e.srcControl;if(c&&s&&jQuery.support.touch&&!this._isSwipeActive&&this!==s&&!this._eventHandledByControl){for(var l=s;l&&!(l instanceof sap.m.ListItemBase);l=l.oParent);if(l instanceof sap.m.ListItemBase){this._swipedItem=l;this.fireSwipe({listItem:this._swipedItem,swipeContent:c,srcControl:s},true)&&this._swipeIn()}}};
sap.m.ListBase.prototype.ontouchstart=function(e){this._eventHandledByControl=e.originalEvent._sapui_handledByControl};
sap.m.ListBase.prototype.onswipeleft=function(e){var a=sap.ui.getCore().getConfiguration().getRTL()?"RightToLeft":"LeftToRight";if(this.getSwipeDirection()!=a){this._onSwipe(e)}};
sap.m.ListBase.prototype.onswiperight=function(e){var a=sap.ui.getCore().getConfiguration().getRTL()?"LeftToRight":"RightToLeft";if(this.getSwipeDirection()!=a){this._onSwipe(e)}};
sap.m.ListBase.prototype.setSwipeDirection=function(d){return this.setProperty("swipeDirection",d,true)};
sap.m.ListBase.prototype.getSwipedItem=function(){return(this._isSwipeActive?this._swipedItem:null)};
sap.m.ListBase.prototype.setSwipeContent=function(c){this._bRerenderSwipeContent=true;return this.setAggregation("swipeContent",c,true)};
sap.m.ListBase.prototype.invalidate=function(o){if(o&&o===this.getSwipeContent()){this._bRerenderSwipeContent=true}sap.ui.core.Control.prototype.invalidate.apply(this,arguments);return this};
sap.m.ListBase.prototype.addItemGroup=function(g,h,s){h=h||new sap.m.GroupHeaderListItem({title:g.text||g.key});this.addAggregation("items",h,s);return h};
sap.m.ListBase.prototype._startItemNavigation=function(){if(!this.getItems().length){this._destroyItemNavigation();return}if(!this._oItemNavigation){this._oItemNavigation=new sap.ui.core.delegate.ItemNavigation();this._oItemNavigation.setCycling(false);this.addEventDelegate(this._oItemNavigation);this._oItemNavigation.setPageSize(this.getGrowingThreshold());this._oItemNavigation.setTableMode(true,true).setColumns(1);this._oItemNavigation.setDisabledModifiers({sapnext:["alt"],sapprevious:["alt"]})}var i=this.getItemsContainerDomRef();if(i){this._oItemNavigation.setRootDomRef(i);this._oItemNavigation.setItemDomRefs(i.childNodes)}};
sap.m.ListBase.prototype.getItemNavigation=function(){return this._oItemNavigation};
sap.m.ListBase.prototype._navToSection=function(f){var i=0;var s=f?1:-1;var l=this._aNavSections.length;this._aNavSections.some(function(S,a){var o=jQuery.sap.domById(S);if(o&&o.contains(document.activeElement)){i=a;return true}});this._aNavSections.some(function(){i=(i+s+l)%l;var S=jQuery.sap.byId(this._aNavSections[i]);if(S.is(":focusable")){S.focus();return true}},this)};
sap.m.ListBase.prototype._navToTabChain=function(a){var s=a?1:-1;var e=a?"after":"before";var E=this.$(e).attr("tabindex","0");for(var p=this;(p=p.getParent())&&p.$;){var t=p.$().find(":tabbable");var l=a?t.length-1:0;var i=t.index(E);if(t.length>1&&i!=l){break}}t=t||this.$().parent().find(":tabbable");t.eq(t.index(E)+s).focus();E.attr("tabindex","-1")};
sap.m.ListBase.prototype.onsapskipforward=function(e){if(e.isMarked()){return}this._navToTabChain(true);e.preventDefault();e.setMarked()};
sap.m.ListBase.prototype.onsapskipback=function(e){if(e.isMarked()){return}this._navToTabChain(false);e.preventDefault();e.setMarked()};
sap.m.ListBase.prototype.onsapshow=function(e){if(e.isMarked()||e.keyCode==jQuery.sap.KeyCodes.F4){return}this._navToSection(true);e.preventDefault();e.setMarked()};
sap.m.ListBase.prototype.onsaphide=function(e){if(e.isMarked()){return}this._navToSection(false);e.preventDefault();e.setMarked()};
