(TeX-add-style-hook "cuposter"
 (lambda ()
    (LaTeX-add-environments
     "posterindent")
    (TeX-add-symbols
     '("epsfigure" ["argument"] 2)
     '("address" 1)
     '("homepage" 1)
     '("email" 1)
     '("enquiries" 1)
     '("subtitle" 1)
     "poster"
     "dson"
     "dsoff"
     "ItemizeColour"
     "SectionColour"
     "TitleColour"
     "SubtitleColour"
     "AuthorColour"
     "AddressColour"
     "AbstractColour"
     "CaptionColour"
     "em"
     "makeposter"
     "ps"
     "maketitle")
    (TeX-run-style-hooks
     "sectsty"
     "url"
     "multicol"
     "graphicx"
     "epsfig"
     "pstcol"
     "art10"
     "article"
     "fltfonts"
     "foil30")))

