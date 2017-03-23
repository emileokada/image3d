(TeX-add-style-hook "poster"
 (lambda ()
    (TeX-add-symbols
     "don"
     "doff"
     "dsoma"
     "um"
     "dmin"
     "tabcolsep")
    (TeX-run-style-hooks
     "wrapfig"
     "psfrag"
     "pifont"
     "amsmath"
     "xspace"
     "mathptmx"
     "latex2e"
     "cuposter10"
     "cuposter"
     "noback")))

