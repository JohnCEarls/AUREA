<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML>
	
	
<?php
  $DOCUMENT_ROOT = $_SERVER['DOCUMENT_ROOT'];
  /* $Id$ */
  $TITLE="Institute for Systems Biology";

  include("$DOCUMENT_ROOT/includes/style.inc.php");

  include("$DOCUMENT_ROOT/includes/header.inc.php");
  
  include("$DOCUMENT_ROOT/includes/mainnav.inc.php");

    include("$DOCUMENT_ROOT/includes/leftnavbar.inc.php");

?>

<!-- START Body content table -->


<br />
					<table align="center" bgcolor="white" border="0" cellpadding="0" cellspacing="0" width="740">
					<tbody>
					<tr>
					<td bgcolor="#c6c1b8"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
					<td colspan="3" bgcolor="#c6c1b8" width="535" height="2"><img src="/images/clear.gif" border="0" height="2" width="1"></td>
					<td bgcolor="#c6c1b8"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
					</tr>
					<tr height="20">
					<td bgcolor="#c6c1b8" height="20" width="1"><img src="/images/clear.gif" border="0" height="20" width="1"></td>
					<td colspan="3" class="Pagetitle" bgcolor="#c6c1b8" width="538" height="20"><img src="/images/clear.gif" border="0" height="1" width="6">
					<!--Header of Content page goes here.  Should match left nav that was clicked-->
					AUREA
					</td>
					<td bgcolor="#c6c1b8" height="20" width="1"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
					</tr>
					<tr>
					<td bgcolor="#c6c1b8" height="1" width="1"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
					<td colspan="3" bgcolor="#c6c1b8" height="2"><img src="/images/clear.gif" border="0" height="2" width="1"></td>
					<td bgcolor="#c6c1b8" height="1" width="1"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
					</tr>
					<tr>
					<td bgcolor="#c6c1b8" height="1" width="1"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
					<td width="4"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
					<td width="655"><img src="/images/clear.gif" border="0" height="20" width="1"></td>
					<td bgcolor="white" height="1" width="9"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
					<td width="1" bgcolor="#c6c1b8"><img src="/images/clear.gif" alt="" height="2" width="1" border="0"></td>
					</tr>
					<tr valign="top" height="598">
					<td bgcolor="#c6c1b8" height="598" width="1"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
					<td width="4"><img src="/images/clear.gif" border="0" height="1" width="8"></td>
					<td class="text">
					<!-- This space is reserved for the Content of your Site-->
					<!--Title Content page goes here. Title of Content-->
					<p>
					 
					<p class="text">
					<h2>AUREA - Frequently Asked Questions</h2>

<p>

            <ol>
            <li><a class="textlink" href="/AUREA/faq.php#gen">General Questions</a></li>
            <li><a class="textlink" href="/AUREA/faq.php#inst">Installation</a>
                <ol>
                    <li><a class="textlink" href="/AUREA/faq.php#path">Why do I have to add python to my system path?</a></li>

                </ol>
            </li>
            <li><a class="textlink" href="/AUREA/faq.html#gui">Graphical Interface</a>
                <ol>
                    
                    <li><a class="textlink" href="/AUREA/faq.html#soft">What are SOFT files?</a></li>
                    <li><a class="textlink" href="/AUREA/faq.html#comp">How can I find compatible data files at the Gene Expression Omnibus?</a></li>
                    <li><a class="textlink" href="/AUREA/faq.html#gnf">Where can I find different gene network files?</a></li>
                </ol>
            </li>
            <li><a class="textlink" href="/AUREA/faq.php#lib">Library</a></li>
            
        </ol>

            <h3><a name="gen">General Questions</a></h3>
            <h3<a name="inst">Installation</a></h3>
            <ol>
               <li><a name="path">Why do I have to add python to my system path?</a>
                    <ul>
                        <li>Your system path tells your system where to look for executable programs.  AUREA needs the python interpreter to run.  In order for the system to know where the python interpreter is, you have to add its location to the system path.</li>
                    </ul>
                </a></li></ol>
            <h3><a name="gui">Graphical Interface</a></h3>
            <ol>
                <li><a name="soft">What are SOFT files?</a>
                    <ul>
                        <li>SOFT(Simple Omnibus Format in Text) is a format used by NCBI for storing transcriptomic data in GEO.  The format is described at <a href="http://www.ncbi.nlm.nih.gov/geo/info/soft2.html">http://www.ncbi.nlm.nih.gov/geo/info/soft2.html</a>.
                            AUREA allows the importing of SOFT files from GEO of the GDS type.  GDS (GEO Dataset) files are curated microarray data files that contain expression values and meta-data from the experiments that generated the data.
                        </li>
                    </ul>

                </li>
                <li><a name="comp">How can I find compatible data files at the Gene Expression Omnibus?</a>
                    <ul>
                        <li>You can visit the NCBI GEO Dataset browse at <a href="http://www.ncbi.nlm.nih.gov/sites/GDSbrowser/"> http://www.ncbi.nlm.nih.gov/sites/GDSbrowser/</a> and search for datasets relevant to your research.  Once you have identified Datasets you are interested in, you can either download the GDS####.soft.gz files associated with them or click download on the area Data screen and enter the number associated with the dataset. </li>
                    </ul>
                </li>
                <li><a name="gnf">Where can I find different gene network files?</a>
                    <ul>
                        <li><a href="http://www.broadinstitute.org/gsea/msigdb/collections.jsp">The Broad</a></li>
                    </ul>
                </li>
            </ol>
            <h3><a name="lib">Library</a></h3>


    </div>
<p class="text">
 


<p class="text">
					
					
					
					
					
				
					<!-- End Content-->
					</td>
					<td width="9"><img src="/images/clear.gif" border="0" height="1" width="9"></td>
					<td bgcolor="#c6c1b8" width="1"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
					</tr>
					
					
					
					
					
					
					
					<tr>
					<td bgcolor="#c6c1b8" height="1" width="1"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
					<td colspan="3" bgcolor="#c6c1b8" width="538" height="1"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
					<td bgcolor="#c6c1b8" height="1" width="1"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
					</tr>
					</tbody>
					</table>
					<!-- END Body content table -->
		<!-- END Body content table -->
									
</td>
<td bgcolor="#827975"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
</tr>
<tr>
<td bgcolor="#827975"><img src="/images/clear.gif" border="0" height="5" width="1"></td>
<td><img src="/images/clear.gif" border="0" height="1" width="1"></td>
<td><img src="/images/clear.gif" border="0" height="1" width="1"></td>
<td bgcolor="#827975"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
</tr>
<tr>
<td bgcolor="#827975"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
<td bgcolor="#827975"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
<td bgcolor="#827975"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
<td bgcolor="#827975"><img src="/images/clear.gif" border="0" height="1" width="1"></td>
</tr>
</table>

<?php
  include("$DOCUMENT_ROOT/includes/disclaimer_footer.inc.php");
?>

