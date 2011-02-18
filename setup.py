#!/usr/bin/env python

"""
setup.py 

python setup.py build_ext --inplace
"""

from distutils.core import setup, Extension
import os
import os.path
import shutil

def swig_helper( module, src_dir ):
    """
    This builds the python files that use the compiled extensions 
    (dirac.py, tst.py, etc.)
    This is already being done in build_ext, but it leaves the file
    in the src directory instead of putting it into learner where it 
    belongs, so we have to do this manually.
    """
    swig_interface = os.path.join(src_dir, module +"_pywrapper.i")
    command = 'swig -c++ -python -modern ' + swig_interface
    os.system(command)
    
    shutil.copy(os.path.join(src_dir, module.lower() + ".py"),os.sep.join(['src', 'AHREA', 'learner' ] ))

modules = ["Dirac", "TSP", "TST", "KTSP", "WILCOXON"]
path_dir = ['src', 'AHREA', 'learner', 'src']
src_dir = os.sep.join(path_dir)

for mod in modules:
    swig_helper(mod,src_dir)

#define modules

dirac_module = Extension('AHREA.learner._dirac', 
    sources=map(lambda x: os.path.join(src_dir, x), ['Dirac_pywrapper.i', 'Dirac_pywrapper.cpp', 'Dirac.cpp', 'dir_Matrix.cpp','kfold.cpp' ]), 

    swig_opts=['-modern', '-c++'],
                        )
tsp_module = Extension('AHREA.learner._tsp',
    sources=map(lambda x: os.path.join(src_dir, x),[ 'TSP_pywrapper.i', 'TSP_pywrapper.cpp', 'learn_utsp_classifier.cpp', 'utils.cpp', 'matrix.cpp', 'wilcoxon.cpp', 'order.cpp', 'kfold.cpp' ])
,
    swig_opts=['-modern', '-c++'],
                    )     

tst_module = Extension('AHREA.learner._tst',
    sources = map(lambda x: os.path.join(src_dir, x),['TST_pywrapper.i', 'TST_pywrapper.cpp', 'learn_tst_classifier.cpp', 'utils.cpp', 'matrix.cpp', 'wilcoxon.cpp', 'order.cpp', 'kfold.cpp' ])
,
    swig_opts=['-modern', '-c++'],
                        )

ktsp_module = Extension('AHREA.learner._ktsp',
    sources = map(lambda x: os.path.join(src_dir, x),['KTSP_pywrapper.i', 'KTSP_pywrapper.cpp', 'Ktsp.cpp', 'kfold.cpp',  'utils.cpp', 'matrix.cpp', 'wilcoxon.cpp', 'order.cpp'])
,
    swig_opts=['-modern', '-c++'],
                    )
wilcoxon_module = Extension('AHREA.learner._wilcoxon',
    sources = map(lambda x: os.path.join(src_dir, x),['WILCOXON_pywrapper.i', 'WILCOXON_pywrapper.cpp', 'wilcoxon_test.cpp', 'utils.cpp', 'matrix.cpp', 'wilcoxon.cpp', 'order.cpp' ]),
    swig_opts=['-modern', '-c++'],
                    )

#defining the modules
GUI_mod = [ 'AHREA.GUI.'+x for x in ['AHREAApp', 'AHREAController', 'AHREAPage', 'AHREAResults']] 
heuristic_mod = ['AHREA.heuristic.'+x for x in ['LearnerQueue', 'ResourceEstimate']]
packager_mod = ['AHREA.packager.'+x for x in ['DataCleaner','DataPackager']]
parser_mod = ['AHREA.parser.' + x for x in  ['CSVParser', 'GMTParser', 'SettingsParser', 'SOFTParser', 'SynonymParser']]
learner_mod = ["AHREA.learner.dirac", "AHREA.learner.tsp","AHREA.learner.tst", "AHREA.learner.ktsp", "AHREA.learner.wilcoxon"]
#putting all of the python modules in oneList
a_modules = []
for mod_list in [GUI_mod, heuristic_mod, packager_mod, parser_mod, learner_mod]:
    for mod in mod_list:
        a_modules.append(mod)


#run setup
setup (name = 'AHREA: Adaptive Heuristic Relative Expression Analizer',
        version='1.0',
        author ='John C. Earls',
        description="""AHREA is a sofware suite that makes finding Relative Expression Learners easy.""",
        packages=['AHREA','AHREA.GUI', 'AHREA.learner', 'AHREA.packager', 'AHREA.parser','AHREA.heuristic', 'pyBabel'],
        package_dir={'AHREA': 'src/AHREA', 'pyBabel': 'src/pyBabel'},
        scripts=['scripts/AHREAGUI.py'],

        

        #ext_package='learner',
        ext_modules = [dirac_module, tsp_module, tst_module, ktsp_module, wilcoxon_module],
        py_modules = a_modules,

        )


