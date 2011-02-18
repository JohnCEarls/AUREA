#!/usr/bin/env python

"""
setup.py 

python setup.py build_ext --inplace
"""

from distutils.core import setup, Extension
import os
import os.path
import shutil

#run swig
def swig_helper( module ):
    my_path = os.path.join("learner", "src")    
    swig_interface = os.path.join(my_path , module +"_pywrapper.i")
    command = 'swig -c++ -python -modern ' + swig_interface
    print command
    os.system(command)
    shutil.copy(os.path.join(my_path, module.lower() + ".py"), "learner")

modules = ["Dirac", "TSP", "TST", "KTSP", "WILCOXON"]
for mod in modules:
    swig_helper(mod)

#define modules
src_dir = 'learner/src/'
dirac_module = Extension('_dirac', 
    sources=map(lambda x: src_dir + x, ['Dirac_pywrapper_wrap.cxx', 'Dirac_pywrapper.cpp', 'Dirac.cpp', 'Matrix.cpp','kfold.cpp' ]), 
                        )
tsp_module = Extension('_tsp',
    sources=map(lambda x: src_dir + x,[ 'TSP_pywrapper_wrap.cxx', 'TSP_pywrapper.cpp', 'learn_utsp_classifier.cpp', 'utils.cpp', 'matrix.cpp', 'wilcoxon.cpp', 'order.cpp', 'kfold.cpp' ])
                    )     

tst_module = Extension('_tst',
    sources = map(lambda x: src_dir + x,['TST_pywrapper_wrap.cxx', 'TST_pywrapper.cpp', 'learn_tst_classifier.cpp', 'utils.cpp', 'matrix.cpp', 'wilcoxon.cpp', 'order.cpp', 'kfold.cpp' ])
                        )

ktsp_module = Extension('_ktsp',
    sources = map(lambda x: src_dir + x,['KTSP_pywrapper_wrap.cxx', 'KTSP_pywrapper.cpp', 'Ktsp.cpp', 'kfold.cpp',  'utils.cpp', 'matrix.cpp', 'wilcoxon.cpp', 'order.cpp'])
                    )
wilcoxon_module = Extension('_wilcoxon',
    sources = map(lambda x: src_dir + x,['WILCOXON_pywrapper_wrap.cxx', 'WILCOXON_pywrapper.cpp', 'wilcoxon_test.cpp', 'utils.cpp', 'matrix.cpp', 'wilcoxon.cpp', 'order.cpp' ])
                    )

#run setup
GUI_modules = ["AHREA.GUI", 

setup (name = 'AHREA: Adaptive Heuristic Relative Expression Analizer',
        version='1.0',
        author ='John C. Earls',
        description="""AHREA is a sofware suite that makes finding Relative Expression Learners easy.""",
        ext_package='learner',
        ext_modules = [dirac_module, tsp_module, tst_module, ktsp_module, wilcoxon_module],
        py_modules = ["AHREA.learner.dirac", "AHREA.learner.tsp","AHREA.learner.tst", "AHREA.learner.ktsp", "AHREA.learner.wilcoxon"],

        )


