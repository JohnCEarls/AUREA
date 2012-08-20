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
        <h2>AUREA installation</h2>
        <p>[<a href="/AUREA">AUREA home</a>]</p>

        <div>
The AUREA application has two primary components. The <strong>workspace</strong> and the <strong>libraries</strong>.  
The AUREA <strong>libraries</strong> contain all you need to create your own scripts in Python that take advantage of the AUREA system.
The AUREA <strong>workplace</strong> contains the initialization files, settings and required data files that are required to run the GUI interface.  It requires the AUREA libraries be installed first.
        </div>
        <ul>
            <li><a class="textlink"  href="/AUREA/install.php#winstall">Windows Installation</a>
                    <ol>
                        <li><a class="textlink"  href="/AUREA/install.php#winpre">Pre-reqs</a></li>

                        <li><a class="textlink"  href="/AUREA/install.php#winlib">Libraries</a></li>
                        <li><a class="textlink"  href="/AUREA/install.php#winwork">Workspace</a></li>
                    </ol>
            </li>               
            <li><a class="textlink"  href="/AUREA/install.php#linstall">Linux Installation</a>
                    <ol>
                        <li><a class="textlink"  href="/AUREA/install.php#linpre">Pre-reqs</a></li>

                        <li><a class="textlink"  href="/AUREA/install.php#linlib">Libraries</a></li>
                        <li><a class="textlink"  href="/AUREA/install.php#linwork">Workspace</a></li>
                    </ol>
            </li>               
            <li><a class="textlink"  href="/AUREA/install.php#macinstall">OS X Installation</a>
                    <ol>
                        <li><a class="textlink"  href="/AUREA/install.php#macpre">Pre-reqs</a></li>

                        <li><a class="textlink"  href="/AUREA/install.php#maclib">Libraries</a></li>
                        <li><a class="textlink"  href="/AUREA/install.php#macwork">Workspace</a></li>
                    </ol>
            </li>               
       </ul>
       <h4>Install AUREA libraries from pre-built binary distributions.</h4>
       <h3><a name="winstall">Windows Installation</a></h3>
       <ol>
            <li><a name="winpre">Install required software</a>
                <ul>
                    <li>Python 2.6.x or 2.7.x
                        <ul>
                            <li>Available for free download from<a class="textlink"  href="http://www.python.org/getit/">python.org</a>, we recommend the 2.7.x release.</li>
                            <li>Note: at this time we do not support 3.x versions of Python</li>
                        </ul>
                    </li>
                    <li>Tcl/Tk
                        <ul>
                            <li>Note: most full python distributions will install this by default</li>
                            <li>If for some reason your distribution did not or you chose not to install it, it is available for free download from <a class="textlink"  href="http://www.activestate.com/activetcl/downloads">ActiveState</a></li>
                        </ul>
                    </li>
                </ul>
            </li>
            <li><a name="winlib">Install AUREA <strong>libraries</strong></a>
                <ul>
                    <li>Via Windows installer(recommended)
                        <ol>
                            <li><a class="textlink"  href="/AUREA/downloads.php#winbuilt">Download</a> appropriate AUREA windows installer.
                                <ul>
                                    <li>AUREA-#.#.#[AUREA version].win[architecture <em>win32 for 32bit and -amd64 for 64bit</em>]-py2.#[your python version].exe(i.e., <em>AUREA-1.6.3.win-amd64-py2.7.exe</em> for a 64 bit Windows machine running Python 2.7)</li>
                                </ul>
                            </li>
                            <li>Double click installer after downloaded.
                            </li>
                            <li>Accept default configuration. (If the installer complains that it cannot find python in the registry, double check the architecture and python version number.)
                            </li>
                        </ol>
                    </li>
                    <li>Via easy_install
                        <ol>
                             <li>Install and configure easy_install:<a class="textlink"  href="http://pypi.python.org/pypi/setuptools#windows">http://pypi.python.org/pypi/setuptools#windows</a>
                             <ul>
                                 <li>From downloaded file
                                    <ol>
                                        <li><a class="textlink"  href="/AUREA/downloads.php#winbuilt">Download</a> appropriate AUREA egg.
                                            <ul>

                                                <li>
                                                    AUREA-#.#.#[AUREA Version]-py2.#[your python version]-win[your architecture <em>32 for 32bit and -amd64 for 64bit</em>].egg (i.e., <em>AUREA-1.6.3-py2.7-win-amd64.egg</em> for a 64 bit Windows machine running Python 2.7)</li>
                                            </ul>
                                        </li>
                                         <li>
                                            Open command line(powershell or cmd)
                                        </li>
                                        <li>    
                                            Change directory to directory containing egg.(Note: if windows changed .egg to .zip you will have to rename the file back to .egg)
                                        </li>

                                        <li>
                                            Enter:  <strong>easy_install AUREA*.egg</strong>
                                        </li>
                                   </ol>             
                                </li>
                                <li>From URL
                                    <ol>
                                        <li><a class="textlink"  href="/AUREA/downloads.php#winbuilt">Copy URL for appropriate AUREA egg</a>

                                        <ul>
                                            <li>
                                            AUREA-#.#.#[AUREA Version]-py2.#[your python version]-win[your architecture <em>32 for 32bit and -amd64 for 64bit</em>].egg</li>
                                        </ul>
                                        </li>
                                        <li>
                                            Open command line(powershell or cmd)
                                        </li>

                                        <li>
                                            Enter: <strong>easy_install [URL]</strong>
                                            <ul>    
                                                <li>For example, you would enter <strong>easy_install http://price.systemsbiology.net/downloads/AUREA-1.6.3-py2.7-win-amd64.egg</strong> on a 64 bit machine running python 2.7.x</li>
                                            </ul>
                                        </li>
                                    </ol>
                                </li>
                            </ul>
                        </li>
                    </ol>
                 </li>
             </ul>
            
            </li>
            <li><a name="winwork">Install the <strong>workspace</strong></a>
                <ol>
                    <li>Download the windows workspace [<a class="textlink"  href="/AUREA/downloads.php#winwork">win-workspace.zip</a>]</li>
                    <li>Extract the workspace folder to the location you would like to work from.</li>
                </ol>
            </li>
            <li>Open the workspace folder and double click <strong>AUREAGUI.pyw</strong></li>
            
       </ol>

        <h3><a name="linstall">Linux Installation</a></h3>
        <ol>
            <li><a name="linpre">Install required software</a>
                <ul>
                    <li>Python 2.6.x or 2.7.x
                        <ul>
                            <li>Available for free download from <a class="textlink"  href="http://www.python.org/getit/">python.org</a> or through your favorite package manager.</li>

                            <li>Note: some distributions have a system python installed that you should not change (Redhat for example).  In that case you are going to have to do an alternative installation from source. see: <a class="textlink"  href="http://stackoverflow.com/questions/4149361/on-linux-suse-or-redhat-how-do-i-load-python-2-7">http://stackoverflow.com/questions/4149361/on-linux-suse-or-redhat-how-do-i-load-python-2-7</a> </li>
                            <li>Note: at this time we do not support 3.x versions of Python</li>
                        </ul>
                    </li>
                    <li>Tkinter
                        <ul>
                            <li>This is supposed to be installed with Python, but under Ubuntu at least, it is not.</li>

                            <li>see: <a class="textlink"  href="http://tkinter.unpythonic.net/wiki/How_to_install_Tkinter">http://tkinter.unpythonic.net/wiki/How_to_install_Tkinter</a></li>
                            <li>You can test if it is installed by opening a terminal, typing "python"(starting an interactive python session), then trying "import Tkinter" at the &gt;&gt;&gt; prompt </li>
                        </ul>                    </li>
                    <li>easy_install
                        <ol>
                            <li>see: <a class="textlink"  href="http://pypi.python.org/pypi/setuptools#cygwin-mac-os-x-linux-other">http://pypi.python.org/pypi/setuptools#cygwin-mac-os-x-linux-other</a></li>
                        </ol>
                    </li>
                </ul>
            </li>
            <li><a name="linlib">Install AUREA <strong>libraries</strong></a>
                <ol>
                    <li>Select appropriate .egg file for your python version and architecture. <a class="textlink"  href="AUREA/downloads.php#linbuilt">Downloads</a>
                        <ul>
                            <li>From downloaded file
                                <ol>
                                    <li><a class="textlink"  href="/AUREA/downloads.php#linbuilt">Download</a> the appropriate egg</li>
                                    <li>open a terminal and go to the folder containing the egg</li>
                                    <li>enter: <strong>sudo easy_install AUREA*.egg</strong></li>
                                </ol>
                            </li>

                            <li>From url
                                <ol>    
                                    <li>open a terminal and enter: <strong>sudo easy_install http://www.igb.uiuc.edu/labs/price/downloads/AUREA-[version]-py2.[pyversion]-linux-[arch].egg</strong></li>
                                    <li>for example, <strong>easy_install http://price.systemsbiology.net/downloads/AUREA-1.6.3-py2.7-linux-x86_64.egg</strong> for python 2.7 on a 64 bit machine.</li>
                                </ol>
                            </li>
                        </ul>
                    </li>
                </ol>
            </li>
            <li><a name="linwork">Install the <strong>workspace</strong></a>
                <ol>
                    <li>Download the windows workspace [<a class="textlink"  href="/AUREA/downloads.php#linwork">lin-workspace.zip</a>]</li>
                    <li>Extract the workspace folder to the location you would like to work from.</li>

                </ol>
            </li>
            <li>Open the workspace folder and double click <strong>AUREAGUI.py</strong></li>
            <li>If it asks, click "Run".</li>
            <li>Of course, you can also run it from the terminal by entering the workspace folder and typing <strong>./AUREAGUI.py</strong></li>
        </ol>
        <h3><a name="macinstall">OS X Installation</a></h3>
        <ol>
            <li><a name="macpre">Install required software</a>
                <ul>
                    <li>Python 2.6.x or 2.7.x
                        <ul>
                            <li>Available for free download from <a class="textlink"  href="http://www.python.org/getit/">python.org</a>.</li>
                            <li><em>Note: Snow leopard comes with 2.6 and Lion comes with 2.7.</em></li>
                            <li><em>Note: at this time we do not support 3.x versions of Python</em></li>
                        </ul>
                    </li>
                    <li>Tkinter
                        <ul>
                            <li>This should be installed.</li>
                            <li>You can test if it is installed by opening a terminal, typing <strong>python</strong>(starting an interactive python session), then trying <strong>import Tkinter</strong> at the &gt;&gt;&gt; prompt </li>
                            <li>If not, see <a href="http://www.python.org/getit/mac/tcltk/">http://www.python.org/getit/mac/tcltk/</a></li>
                        </ul>
                    </li>
                    <li>easy_install
                        <ol>
                            <li>see: <a class="textlink"  href="http://pypi.python.org/pypi/setuptools#cygwin-mac-os-x-linux-other">http://pypi.python.org/pypi/setuptools#cygwin-mac-os-x-linux-other</a></li>
                        </ol>
                    </li>
                </ul>
            </li>

            <li><a name="maclib">Install AUREA <strong>libraries</strong></a>
                <ol>
                    <li>Select appropriate .egg file for your python version(Mac eggs ship as universal binaries, so you do not have to worry about architecture). <a class="textlink"  href="AUREA/downloads.php#macbuilt">Downloads</a>
                        <ul>
                            <li>From downloaded file
                                <ol>
                                    <li>Download the appropriate egg</li>
                                    <li>open a terminal and go to the folder containing the egg</li>

                                    <li>enter: <strong>easy_install -N AUREA*.egg</strong></li>
                                </ol>
                            </li>
                            <li>From url
                                <ol>    
                                    <li>open a terminal and enter: <strong>easy_install http://price.systemsbiology.net/downloads/AUREA-[AUREA version]-py2.[python version]-macosx-10.#[OS X version]-intel.egg</strong></li>
                                    <li>for example, <strong>easy_install http://price.systemsbiology.net/downloads/AUREA-1.6.3-py2.6-macosx-10.7-intel.egg</strong> for python 2.6 on Lion.</li>

                                </ol>
                            </li>
                        </ul>
                    </li>
                </ol>
            </li>
            <li><a name="macwork">Install the <strong>workspace</strong></a>
                <ol>
                    <li>Download the windows workspace [<a class="textlink"  href="/AUREA/downloads.php#macwork">mac-workspace.zip</a>]</li>
                    <li>Extract the workspace folder to the location you would like to work from.</li>
                </ol>
            </li>
            <li>See: <a class="textlink"  href="http://stackoverflow.com/questions/1854718/how-to-auto-run-a-script">http://stackoverflow.com/questions/1854718/how-to-auto-run-a-script</a> for instructions on how to make AUREAGUI.py clickable.</li>
            <li>Of course, you can also run it from the terminal, <strong>./AUREAGUI.py</strong></li>
        </ol>


    </div>
    <p class="text">&nbsp;</p>
    <p class="text">&nbsp;</p>
					
					
					
					
					
				
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

