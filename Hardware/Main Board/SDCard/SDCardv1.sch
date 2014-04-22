<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="6.0">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="2" name="Route2" color="1" fill="3" visible="no" active="no"/>
<layer number="3" name="Route3" color="4" fill="3" visible="no" active="no"/>
<layer number="4" name="Route4" color="1" fill="4" visible="no" active="no"/>
<layer number="5" name="Route5" color="4" fill="4" visible="no" active="no"/>
<layer number="6" name="Route6" color="1" fill="8" visible="no" active="no"/>
<layer number="7" name="Route7" color="4" fill="8" visible="no" active="no"/>
<layer number="8" name="Route8" color="1" fill="2" visible="no" active="no"/>
<layer number="9" name="Route9" color="4" fill="2" visible="no" active="no"/>
<layer number="10" name="Route10" color="1" fill="7" visible="no" active="no"/>
<layer number="11" name="Route11" color="4" fill="7" visible="no" active="no"/>
<layer number="12" name="Route12" color="1" fill="5" visible="no" active="no"/>
<layer number="13" name="Route13" color="4" fill="5" visible="no" active="no"/>
<layer number="14" name="Route14" color="1" fill="6" visible="no" active="no"/>
<layer number="15" name="Route15" color="4" fill="6" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="15" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="ekohub2013">
<packages>
<package name="MICROSD_SOCKET">
<smd name="RSV" x="-4.7" y="-7.475" dx="1.75" dy="0.7" layer="1" rot="R90"/>
<smd name="DO" x="-3.6" y="-7.475" dx="1.75" dy="0.7" layer="1" rot="R90"/>
<smd name="VSS" x="-2.5" y="-7.475" dx="1.75" dy="0.7" layer="1" rot="R90"/>
<smd name="CLK" x="-1.4" y="-7.475" dx="1.75" dy="0.7" layer="1" rot="R90"/>
<smd name="VDD" x="-0.3" y="-7.475" dx="1.75" dy="0.7" layer="1" rot="R90"/>
<smd name="DI" x="0.8" y="-7.475" dx="1.75" dy="0.7" layer="1" rot="R90"/>
<smd name="CS" x="1.9" y="-7.475" dx="1.75" dy="0.7" layer="1" rot="R90"/>
<smd name="NC" x="3" y="-7.475" dx="1.75" dy="0.7" layer="1" rot="R90"/>
<smd name="MOUNT2" x="5.45" y="-7.35" dx="1.5" dy="1.5" layer="1"/>
<smd name="CD" x="-5.875" y="1.75" dx="1" dy="1.45" layer="1" rot="R90"/>
<smd name="MOUNT3" x="-6.2" y="-0.05" dx="0.8" dy="1.5" layer="1"/>
<smd name="MOUNT4" x="5.85" y="0.825" dx="0.8" dy="1.4" layer="1"/>
<smd name="CD2" x="5.3" y="3.225" dx="1" dy="1.55" layer="1"/>
<wire x1="-6.6" y1="-6.6" x2="6.6" y2="-6.6" width="0.127" layer="21"/>
<wire x1="6.6" y1="-6.6" x2="6.6" y2="4.4" width="0.127" layer="21"/>
<wire x1="6.6" y1="4.4" x2="-6.6" y2="4.4" width="0.127" layer="21"/>
<wire x1="-6.6" y1="4.4" x2="-6.6" y2="-6.6" width="0.127" layer="21"/>
<text x="-3.175" y="0" size="0.8128" layer="21">MICRO SD</text>
</package>
</packages>
<symbols>
<symbol name="MICROSD_SOCKET">
<pin name="NC" x="20.32" y="7.62" length="middle" rot="R180"/>
<pin name="CS" x="20.32" y="5.08" length="middle" rot="R180"/>
<pin name="DI" x="20.32" y="2.54" length="middle" rot="R180"/>
<pin name="VDD" x="20.32" y="0" length="middle" rot="R180"/>
<pin name="CLK" x="20.32" y="-2.54" length="middle" rot="R180"/>
<pin name="VSS" x="20.32" y="-5.08" length="middle" rot="R180"/>
<pin name="DO" x="20.32" y="-7.62" length="middle" rot="R180"/>
<pin name="RSV" x="20.32" y="-10.16" length="middle" rot="R180"/>
<wire x1="15.24" y1="10.16" x2="15.24" y2="-12.7" width="0.254" layer="94"/>
<wire x1="15.24" y1="-12.7" x2="-10.16" y2="-12.7" width="0.254" layer="94"/>
<wire x1="-10.16" y1="-12.7" x2="-10.16" y2="10.16" width="0.254" layer="94"/>
<wire x1="-10.16" y1="10.16" x2="15.24" y2="10.16" width="0.254" layer="94"/>
<pin name="CD" x="-15.24" y="7.62" length="middle"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="MICROSD_SOCKET">
<gates>
<gate name="G$1" symbol="MICROSD_SOCKET" x="-2.54" y="0"/>
</gates>
<devices>
<device name="" package="MICROSD_SOCKET">
<connects>
<connect gate="G$1" pin="CD" pad="CD"/>
<connect gate="G$1" pin="CLK" pad="CLK"/>
<connect gate="G$1" pin="CS" pad="CS"/>
<connect gate="G$1" pin="DI" pad="DI"/>
<connect gate="G$1" pin="DO" pad="DO"/>
<connect gate="G$1" pin="NC" pad="NC"/>
<connect gate="G$1" pin="RSV" pad="RSV"/>
<connect gate="G$1" pin="VDD" pad="VDD"/>
<connect gate="G$1" pin="VSS" pad="VSS"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="jumper">
<description>&lt;b&gt;Jumpers&lt;/b&gt;&lt;p&gt;
&lt;author&gt;Created by librarian@cadsoft.de&lt;/author&gt;</description>
<packages>
<package name="JP2W">
<description>&lt;b&gt;JUMPER&lt;/b&gt;</description>
<wire x1="3.556" y1="2.794" x2="1.524" y2="2.794" width="0.1524" layer="21"/>
<wire x1="1.27" y1="2.54" x2="1.524" y2="2.794" width="0.1524" layer="21"/>
<wire x1="3.556" y1="0.254" x2="1.524" y2="0.254" width="0.1524" layer="21"/>
<wire x1="1.27" y1="0.508" x2="1.524" y2="0.254" width="0.1524" layer="21"/>
<wire x1="1.27" y1="0.508" x2="1.27" y2="2.54" width="0.1524" layer="21"/>
<wire x1="3.556" y1="0.254" x2="3.81" y2="0.508" width="0.1524" layer="21"/>
<wire x1="3.556" y1="2.794" x2="3.81" y2="2.54" width="0.1524" layer="21"/>
<wire x1="3.81" y1="2.54" x2="3.81" y2="0.508" width="0.1524" layer="21"/>
<wire x1="-1.27" y1="0.508" x2="-1.27" y2="2.54" width="0.1524" layer="21"/>
<wire x1="-1.27" y1="0.508" x2="-1.016" y2="0.254" width="0.1524" layer="21"/>
<wire x1="-1.524" y1="0.254" x2="-1.27" y2="0.508" width="0.1524" layer="21"/>
<wire x1="-3.81" y1="0.508" x2="-3.556" y2="0.254" width="0.1524" layer="21"/>
<wire x1="-3.81" y1="0.508" x2="-3.81" y2="2.54" width="0.1524" layer="21"/>
<wire x1="1.016" y1="0.254" x2="-1.016" y2="0.254" width="0.1524" layer="21"/>
<wire x1="1.016" y1="0.254" x2="1.27" y2="0.508" width="0.1524" layer="21"/>
<wire x1="-1.524" y1="0.254" x2="-3.556" y2="0.254" width="0.1524" layer="21"/>
<wire x1="1.016" y1="2.794" x2="-1.016" y2="2.794" width="0.1524" layer="21"/>
<wire x1="-1.524" y1="2.794" x2="-3.556" y2="2.794" width="0.1524" layer="21"/>
<wire x1="-1.27" y1="2.54" x2="-1.016" y2="2.794" width="0.1524" layer="21"/>
<wire x1="-3.81" y1="2.54" x2="-3.556" y2="2.794" width="0.1524" layer="21"/>
<wire x1="1.016" y1="2.794" x2="1.27" y2="2.54" width="0.1524" layer="21"/>
<wire x1="-1.524" y1="2.794" x2="-1.27" y2="2.54" width="0.1524" layer="21"/>
<wire x1="2.54" y1="3.302" x2="2.54" y2="8.255" width="0.6604" layer="21"/>
<wire x1="0" y1="3.302" x2="0" y2="8.255" width="0.6604" layer="21"/>
<wire x1="-2.54" y1="3.302" x2="-2.54" y2="8.255" width="0.6604" layer="21"/>
<pad name="1" x="-2.54" y="-1.27" drill="0.9144" shape="long" rot="R90"/>
<pad name="2" x="0" y="-1.27" drill="0.9144" shape="long" rot="R90"/>
<pad name="3" x="2.54" y="-1.27" drill="0.9144" shape="long" rot="R90"/>
<text x="-4.191" y="0.254" size="1.27" layer="25" ratio="10" rot="R90">&gt;NAME</text>
<text x="-2.794" y="1.27" size="0.9906" layer="21" ratio="12">1</text>
<text x="-0.381" y="1.27" size="0.9906" layer="21" ratio="12">2</text>
<text x="2.032" y="1.27" size="0.9906" layer="21" ratio="12">3</text>
<text x="5.461" y="0.127" size="1.27" layer="27" ratio="10" rot="R90">&gt;VALUE</text>
<rectangle x1="2.2352" y1="2.794" x2="2.8448" y2="3.302" layer="21"/>
<rectangle x1="2.2352" y1="-0.254" x2="2.8448" y2="0.254" layer="21"/>
<rectangle x1="-0.3048" y1="-0.254" x2="0.3048" y2="0.254" layer="21"/>
<rectangle x1="-2.8448" y1="-0.254" x2="-2.2352" y2="0.254" layer="21"/>
<rectangle x1="2.2352" y1="-1.524" x2="2.8448" y2="-0.254" layer="51"/>
<rectangle x1="-0.3048" y1="-1.524" x2="0.3048" y2="-0.254" layer="51"/>
<rectangle x1="-2.8448" y1="-1.524" x2="-2.2352" y2="-0.254" layer="51"/>
<rectangle x1="-0.3048" y1="2.794" x2="0.3048" y2="3.302" layer="21"/>
<rectangle x1="-2.8448" y1="2.794" x2="-2.2352" y2="3.302" layer="21"/>
</package>
</packages>
<symbols>
<symbol name="JP3E">
<wire x1="2.54" y1="0" x2="2.54" y2="1.27" width="0.1524" layer="94"/>
<wire x1="0" y1="0" x2="0" y2="1.27" width="0.1524" layer="94"/>
<wire x1="-2.54" y1="0" x2="-2.54" y2="1.27" width="0.1524" layer="94"/>
<wire x1="2.54" y1="2.54" x2="2.54" y2="1.27" width="0.4064" layer="94"/>
<wire x1="0" y1="2.54" x2="0" y2="1.27" width="0.4064" layer="94"/>
<wire x1="-2.54" y1="2.54" x2="-2.54" y2="1.27" width="0.4064" layer="94"/>
<wire x1="-3.175" y1="0" x2="3.175" y2="0" width="0.4064" layer="94"/>
<wire x1="3.175" y1="0" x2="3.175" y2="0.635" width="0.4064" layer="94"/>
<wire x1="3.175" y1="0.635" x2="-3.175" y2="0.635" width="0.4064" layer="94"/>
<wire x1="-3.175" y1="0.635" x2="-3.175" y2="0" width="0.4064" layer="94"/>
<text x="-3.81" y="0" size="1.778" layer="95" rot="R90">&gt;NAME</text>
<text x="5.715" y="0" size="1.778" layer="96" rot="R90">&gt;VALUE</text>
<pin name="1" x="-2.54" y="-2.54" visible="pad" length="short" direction="pas" rot="R90"/>
<pin name="2" x="0" y="-2.54" visible="pad" length="short" direction="pas" rot="R90"/>
<pin name="3" x="2.54" y="-2.54" visible="pad" length="short" direction="pas" rot="R90"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="JP2W" prefix="JP" uservalue="yes">
<description>&lt;b&gt;JUMPER&lt;/b&gt;</description>
<gates>
<gate name="1" symbol="JP3E" x="0" y="0"/>
</gates>
<devices>
<device name="" package="JP2W">
<connects>
<connect gate="1" pin="1" pad="1"/>
<connect gate="1" pin="2" pad="2"/>
<connect gate="1" pin="3" pad="3"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="U$1" library="ekohub2013" deviceset="MICROSD_SOCKET" device=""/>
<part name="JP1" library="jumper" deviceset="JP2W" device=""/>
<part name="JP2" library="jumper" deviceset="JP2W" device=""/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="U$1" gate="G$1" x="12.7" y="30.48" rot="R270"/>
<instance part="JP1" gate="1" x="15.24" y="-2.54" rot="R180"/>
<instance part="JP2" gate="1" x="7.62" y="-2.54" rot="R180"/>
</instances>
<busses>
</busses>
<nets>
<net name="N$1" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="CS"/>
<pinref part="JP1" gate="1" pin="1"/>
<wire x1="17.78" y1="10.16" x2="17.78" y2="0" width="0.1524" layer="91"/>
</segment>
</net>
<net name="N$2" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="DI"/>
<pinref part="JP1" gate="1" pin="2"/>
<wire x1="15.24" y1="10.16" x2="15.24" y2="0" width="0.1524" layer="91"/>
</segment>
</net>
<net name="N$3" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="VDD"/>
<pinref part="JP1" gate="1" pin="3"/>
<wire x1="12.7" y1="10.16" x2="12.7" y2="0" width="0.1524" layer="91"/>
</segment>
</net>
<net name="N$4" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="CLK"/>
<pinref part="JP2" gate="1" pin="1"/>
<wire x1="10.16" y1="10.16" x2="10.16" y2="0" width="0.1524" layer="91"/>
</segment>
</net>
<net name="N$5" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="VSS"/>
<pinref part="JP2" gate="1" pin="2"/>
<wire x1="7.62" y1="10.16" x2="7.62" y2="0" width="0.1524" layer="91"/>
</segment>
</net>
<net name="N$6" class="0">
<segment>
<pinref part="U$1" gate="G$1" pin="DO"/>
<pinref part="JP2" gate="1" pin="3"/>
<wire x1="5.08" y1="10.16" x2="5.08" y2="0" width="0.1524" layer="91"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
</eagle>
