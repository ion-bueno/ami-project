%%
%% This is file `ldvarticle.cls',
%% generated with the docstrip utility.
%%
%% The original source files were:
%%
%% ldvcommon.dtx  (with options: `article')
%% 
%% IMPORTANT NOTICE:
%% 
%% For the copyright see the source file.
%% 
%% Any modified versions of this file must be renamed
%% with new filenames distinct from ldvarticle.cls.
%% 
%% For distribution of the original source see the terms
%% for copying and modification in the file ldvcommon.dtx.
%% 
%% This generated file may be distributed as long as the
%% original source files, as listed above, are part of the
%% same distribution. (The sources need not necessarily be
%% in the same archive or directory.)
\NeedsTeXFormat{LaTeX2e}
\newcommand*\ldv@classversion{2018/06/06 Dokumentenklasse des LDV -
  Version 2.2}
\ProvidesClass{ldvarticle}[\ldv@classversion]
\newcommand*\ldv@komaclass{scrartcl}
\RequirePackage{xkeyval}
\newcommand*\ldv@choicekeyval\@empty
\newcommand*\ldv@choicekeynr\@empty
\RequirePackage{etoolbox}
\newif\ifldv@isDivSet
\DeclareOptionX<ldv>{DIV}{\ldv@isDivSettrue}
\newcommand*\ldv@fontstylenr\@empty
\define@choicekey*+{ldv}{fontstyle}[\ldv@fontstyle\ldv@fontstylenr]%
  {sans,serif}{}{%
    \ClassWarning{\@currname}{%
      The value given for the option fontstyle is not known.%
    }
  }
\newcommand*\ldv@defaultinputenc{utf8}
\DeclareOptionX<ldv>{inputenc}[\ldv@defaultinputenc]{\def\ldv@inputenc{#1}}
\edef\@classoptionslist{ngerman,english,\@classoptionslist}
\newcommand*\ldv@lang{}
\DeclareOptionX<ldv>{lang}[english]{%
  \XKV@addtolist@n\@classoptionslist{#1}%
  \renewcommand*\ldv@lang{#1}
}
\DeclareOptionX<ldv>{english}{%
  \renewcommand*\ldv@lang{english}
}
\DeclareOptionX<ldv>{ngerman}{%
  \renewcommand*\ldv@lang{ngerman}
}
\newif\ifldv@doloadhyperref
\ldv@doloadhyperreftrue
\newif\ifldv@doloadvarioref
\ldv@doloadvarioreftrue
\define@choicekey*+{ldv}{omitpackage}[\ldv@choicekeyval\ldv@choicekeynr]%
  {hyperref,varioref}{%
    \ifcase\ldv@choicekeynr\relax
      \ldv@doloadhyperreffalse
    \or
      \ldv@doloadvarioreffalse
    \fi
  }{%
    \ClassWarning{\@currname}{%
      You can only omit the packages hyperref and varioref.%
    }%
  }
\DeclareOptionX*{\PassOptionsToClass{\CurrentOption}{\ldv@komaclass}}
\ExecuteOptionsX<ldv>{%
  inputenc=\ldv@defaultinputenc,%
  fontstyle=sans%
}
\ProcessOptionsX<ldv>\relax
\ifnum\ldv@fontstylenr=0%
  \ifldv@isDivSet\else
    \PassOptionsToClass{DIV=9}{\ldv@komaclass}%
    \ClassInfo{ldvklassen}{Set DIV to 9}%
  \fi
\fi
\newlength\ldv@laxLineWidth
\newlength\ldv@bcor  %% TODO
\newcount\ldv@div
\newcommand*\ldv@roundeddiv[2]{
  \newlength\ldv@tempdima
  \setlength\ldv@tempdima{#1}
  \divide\ldv@tempdima by#2
  \ldv@div\ldv@tempdima
  \ifnum \ldv@div<4
    \ldv@div=4
  \else
    \newlength\ldv@tempdimb
    \setlength\ldv@tempdimb{#1}%
    \divide\ldv@tempdimb by\ldv@div
    \addtolength\ldv@tempdima{\ldv@tempdima}%
    \addtolength\ldv@tempdima{-\ldv@tempdimb}%
    \advance\ldv@div by\@ne
    \setlength\ldv@tempdimb{#1}%
    \divide\ldv@tempdimb by\ldv@div
    \ifdim \ldv@tempdima<\ldv@tempdimb
      \advance\ldv@div by\m@ne
    \fi
  \fi
}
\newif\ifldv@mincl  %% TODO
\ldv@minclfalse
\newcommand*\ldv@getLaxLineWidth{%
  \settowidth\ldv@laxLineWidth{\normalfont%
eeeeeeeeeeeeeeeee nnnnnnnnnn iiiiiiii sssssss rrrrrrr aaaaaaa tttttt ddddd hhhhh uuuu lll ccc ggg mmm ooowwbbffkzv%
eeeeeeeeeeeee ttttttttt aaaaaaaa oooooooo iiiiiii nnnnnnn ssssss hhhhhh rrrrrr dddd llll ccc uuu mm ww ff gg yy pp bvk}%
  \setlength\ldv@laxLineWidth{.38\ldv@laxLineWidth}%
}
\newcommand*\ldv@getDIV{%
  \newlength\ldv@hBandWidth%
  \setlength\ldv@hBandWidth{\paperwidth}%
  \addtolength\ldv@hBandWidth{-\ldv@bcor}%
  \addtolength\ldv@hBandWidth{-\ldv@laxLineWidth}%
  \if@twocolumn%
    \addtolength\ldv@hBandWidth{-\columnsep}%
    \addtolength\ldv@hBandWidth{-\ldv@laxLineWidth}%
  \fi%
  \divide\ldv@hBandWidth by3%
  \ifldv@mincl%
    \setlength\ldv@hBandWidth{.75\ldv@hBandWidth}%
  \fi%
  \ifdim \ldv@hBandWidth <5mm%
    \setlength\ldv@hBandWidth{5mm}%
  \fi%
  \ldv@roundeddiv{\paperwidth}{\ldv@hBandWidth}%
  \ClassInfo{\@currname}{Computed DIV=\the\ldv@div.}%
}
\newcommand*\ldv@autotypearea{%
  \ldv@getLaxLineWidth%
  \ldv@getDIV%
  \PassOptionsToClass{DIV=\ldv@div}{ldv@komaclass}
}
%% Das ist hier noch nicht möglich, weil die Schriftgröße noch nicht
%% eingestellt ist.
%% \ldv@autotypearea
\LoadClass{\ldv@komaclass}
\RequirePackage{silence}
\WarningFilter{inputenc}{inputenc package ignored with utf8 based engines}
\RequirePackage[\ldv@inputenc]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{babel}
\ifx\ldv@lang\@empty\else\expandafter\main@language\expandafter{\ldv@lang}\fi
\RequirePackage{array}
\RequirePackage{fancyvrb}
\fvset{xleftmargin=2em}
\newcommand\emphemph[1]{{\bfseries#1}}
\newcommand\simpleverb[1]{{\ttfamily#1}}
\newcommand*\notename{Note}
\addto\captionsngerman{%
  \renewcommand*\notename{Bemerkung}%
}
\addto\captionsgerman{%
  \renewcommand*\notename{Bemerkung}%
}
\addto\captionsenglish{%
  \renewcommand*\notename{Note}%
}
\newenvironment{note}[1][\notename]{%
  \vspace{\baselineskip}%
  \noindent\small{\usekomafont{sectioning}#1:}\hspace{.5em}%
}{}
\RequirePackage{xcolor}
\RequirePackage{graphicx}
\RequirePackage{tikz}
\newlength\graphicswidth
\setlength\graphicswidth{\columnwidth}
\addtolength\graphicswidth{-4\parindent}
\newlength\graphicswidthtwo
\setlength\graphicswidthtwo{.5\columnwidth}
\addtolength\graphicswidthtwo{-3\parindent}
\setcapindent{0pt}
\setkomafont{caption}{\small}
\setkomafont{captionlabel}{\usekomafont{sectioning}}
\definecolor{TUMBlau}       {cmyk}{1.00,0.43,0.00,0.00}
\definecolor{TUMBlau1}      {cmyk}{1.00,0.57,0.12,0.70}
\definecolor{TUMBlau2}      {cmyk}{1.00,0.54,0.04,0.19}
\definecolor{TUMBlau3}      {cmyk}{0.90,0.48,0.00,0.00}
\definecolor{TUMBlau4}      {cmyk}{0.65,0.19,0.01,0.04}
\definecolor{TUMBlau5}      {cmyk}{0.42,0.09,0.00,0.00}
\definecolor{TUMDunkelgrau} {cmyk}{0.00,0.00,0.00,0.80}
\definecolor{TUMMittelgrau} {cmyk}{0.00,0.00,0.00,0.50}
\definecolor{TUMHellgrau}   {cmyk}{0.00,0.00,0.00,0.20}
\definecolor{TUMGruen}      {cmyk}{0.35,0.00,1.00,0.20}
\definecolor{TUMOrange}     {cmyk}{0.00,0.65,0.95,0.00}
\definecolor{TUMElfenbein}  {cmyk}{0.03,0.04,0.14,0.08}
\RequirePackage{expl3}
\ExplSyntaxOn
\sys_if_engine_luatex:TF
{
  \RequirePackage{fontspec}
  \defaultfontfeatures{Scale=MatchLowercase}
  \defaultfontfeatures[TUM Neue Helvetica]{
    UprightFont = TUM Neue Helvetica 55 Regular,
    BoldFont = TUM Neue Helvetica 75 Bold,
    ItalicFont = TUM Neue Helvetica 56 Italic,
    BoldItalicFont = TUM Neue Helvetica 76 Bold Italic,
    Ligatures = TeX,
    Scale = 0.92,
  }
  \IfFontExistsTF{Times}{\setmainfont{Times}}{}
  \IfFontExistsTF{Times New Roman}{\setmainfont{Times New Roman}}{}
  \IfFontExistsTF{Arial}{\setsansfont{Arial}}{}
  \IfFontExistsTF{Helvetica}{\setsansfont{Helvetica}}{}
  \IfFontExistsTF{TUM Neue Helvetica}{\setsansfont{TUM Neue Helvetica}}{}
  \IfFontExistsTF{DejaVu Sans Mono}{\setmonofont{DejaVu Sans Mono}}{}
}
{
    \sys_if_engine_xetex:TF
    {
      \RequirePackage{fontspec}
      \defaultfontfeatures{Scale=MatchLowercase}
      \defaultfontfeatures[TUM Neue Helvetica]{
        UprightFont = TUM Neue Helvetica 55 Regular,
        BoldFont = TUM Neue Helvetica 75 Bold,
        ItalicFont = TUM Neue Helvetica 56 Italic,
        BoldItalicFont = TUM Neue Helvetica 76 Bold Italic,
        Ligatures = TeX,
        Scale = 0.92,
      }
      \IfFontExistsTF{Times}{\setmainfont{Times}}{}
      \IfFontExistsTF{Times New Roman}{\setmainfont{Times New Roman}}{}
      \IfFontExistsTF{Arial}{\setsansfont{Arial}}{}
      \IfFontExistsTF{Helvetica}{\setsansfont{Helvetica}}{}
      \IfFontExistsTF{TUM Neue Helvetica}{\setsansfont{TUM Neue Helvetica}}{}
      \IfFontExistsTF{DejaVu Sans Mono}{\setmonofont{DejaVu Sans Mono}}{}
    }
    {
        \renewcommand{\rmdefault}{ptm}
        \RequirePackage[scaled=0.92]{helvet}
    }
}
\ExplSyntaxOff
\newcommand*\ldv@setfontstyle{%
  \ifcase\ldv@fontstylenr\relax%
    \renewcommand\familydefault{\sfdefault}%
  \or%
    \renewcommand\familydefault{\rmdefault}%
  \fi%
  % The following font definitions are taken from the KOMA-Script
  % classes. Only the '\sffamily' command is left out.
  \setkomafont{disposition}{\normalcolor\bfseries}%
  \setkomafont{descriptionlabel}{\normalcolor\itshape}%
  \setkomafont{dictum}{\normalfont\normalcolor\small}%
}
\ldv@setfontstyle
\tolerance=1414
\hbadness=1414
\emergencystretch=1.5em
\hfuzz=0.3pt
\widowpenalty=10000
\vfuzz\hfuzz
\raggedbottom
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\newcommand*\definitionname{Definition}
\newcommand*\theoremname{Theorem}
\addto\captionsngerman{%
  \renewcommand*\definitionname{Definition}%
  \renewcommand*\theoremname{Satz}%
}
\addto\captionsgerman{%
  \renewcommand*\definitionname{Definition}%
  \renewcommand*\theoremname{Satz}%
}
\addto\captionsenglish{%
  \renewcommand*\definitionname{Definition}%
  \renewcommand*\theoremname{Theorem}%
}
\newtheorem{definition}{\definitionname}
\newtheorem{theorem}{\theoremname}
\newtheorem{proof}{\proofname}
\RequirePackage{natbib}
\renewcommand*\cite{\citep}
\newif\ifldv@bibstyleset
\let\ldv@latex@bibliographystyle=\bibliographystyle
\renewcommand*\bibliographystyle[1]{%
  \ldv@latex@bibliographystyle{#1}\ldv@bibstylesettrue%
}
\let\ldv@latex@bibliography=\bibliography
\renewcommand*\bibliography[1]{%
  \ifldv@bibstyleset\else\bibliographystyle{ldv}\fi%
  \ldv@latex@bibliography{#1}%
}
\newcommand\bibstyle@ldv{%
  \setcitestyle{authoryear,round,comma,aysep={,}, yysep={,},notesep={, }}%
}
\newcommand\bibstyle@ldvplain{%
  \setcitestyle{numbers,square,comma,aysep={,}, yysep={,},notesep={, }}%
  \renewcommand*\bibnumfmt[1]{##1.}%
}
\newcommand*\bbland{and}
\newcommand*\bblandsep{,}
\newcommand*\bblandsepauthor{,}
\newcommand*\bbletal{et~al.}
\newcommand*\bbleditors{editors}
\newcommand*\bbleds{eds.}
\newcommand*\bbleditor{editor}
\newcommand*\bbled{ed.}
\newcommand*\bbledby{edited by}
\newcommand*\bbledition{edition}
\newcommand*\bbledn{edn.}
\newcommand*\bblvolume{volume}
\newcommand*\bblvol{vol.}
\newcommand*\bblof{of}
\newcommand*\bblnumber{number}
\newcommand*\bblno{no.}
\newcommand*\bblin{in}
\newcommand*\bblpages{pages}
\newcommand*\bblpp{pp.}
\newcommand*\bblpage{page}
\newcommand*\bblp{p.}
\newcommand*\bbleidpp{pages}
\newcommand*\bblchapter{chapter}
\newcommand*\bblchap{chap.}
\newcommand*\bbltechreport{Technical Report}
\newcommand*\bbltechrep{Tech. Rep.}
\newcommand*\bblmthesis{Master's thesis}
\newcommand*\bblphdthesis{Ph.D. thesis}
\newcommand*\bblfirst{First}
\newcommand*\bblfirsto{1st}
\newcommand*\bblsecond{Second}
\newcommand*\bblsecondo{2nd}
\newcommand*\bblthird{Third}
\newcommand*\bblthirdo{3rd}
\newcommand*\bblfourth{Fourth}
\newcommand*\bblfourtho{4th}
\newcommand*\bblfifth{Fifth}
\newcommand*\bblfiftho{5th}
\newcommand*\bblst{st}
\newcommand*\bblnd{nd}
\newcommand*\bblrd{rd}
\newcommand*\bblth{th}
\newcommand*\bbljan{January}
\newcommand*\bblfeb{February}
\newcommand*\bblmar{March}
\newcommand*\bblapr{April}
\newcommand*\bblmay{May}
\newcommand*\bbljun{June}
\newcommand*\bbljul{July}
\newcommand*\bblaug{August}
\newcommand*\bblsep{September}
\newcommand*\bbloct{October}
\newcommand*\bblnov{November}
\newcommand*\bbldec{December}
\addto\captionsngerman{%
  \renewcommand*\bbland{und}
  \renewcommand*\bblandsep{}
  \renewcommand*\bblandsepauthor{}
  \renewcommand*\bbletal{et~al.}
  \renewcommand*\bbleditors{Herausgeber}
  \renewcommand*\bbleds{Hrsg.}
  \renewcommand*\bbleditor{Herausgeber}
  \renewcommand*\bbled{Hrsg.}
  \renewcommand*\bbledby{herausgegeben von}
  \renewcommand*\bbledition{Auf\/lage}
  \renewcommand*\bbledn{Aufl.}
  \renewcommand*\bblvolume{Band}
  \renewcommand*\bblvol{Bd.}
  \renewcommand*\bblof{von}
  \renewcommand*\bblnumber{Nummer}
  \renewcommand*\bblno{Nr.}
  \renewcommand*\bblin{in}
  \renewcommand*\bblpages{Seiten}
  \renewcommand*\bblpp{S.}
  \renewcommand*\bblpage{Seite}
  \renewcommand*\bblp{S.}
  \renewcommand*\bbleidpp{Seiten}
  \renewcommand*\bblchapter{Kapitel}
  \renewcommand*\bblchap{Kap.}
  \renewcommand*\bbltechreport{Technischer Bericht}
  \renewcommand*\bbltechrep{Techn. Ber.}
  \renewcommand*\bblmthesis{Masterarbeit}
  \renewcommand*\bblphdthesis{Dissertation}
  \renewcommand*\bblfirst{Erste}
  \renewcommand*\bblfirsto{1.}
  \renewcommand*\bblsecond{Zweite}
  \renewcommand*\bblsecondo{2.}
  \renewcommand*\bblthird{Dritte}
  \renewcommand*\bblthirdo{3.}
  \renewcommand*\bblfourth{Vierte}
  \renewcommand*\bblfourtho{4.}
  \renewcommand*\bblfifth{F\^^b{u}nfte}
  \renewcommand*\bblfiftho{5.}
  \renewcommand*\bblst{.}
  \renewcommand*\bblnd{.}
  \renewcommand*\bblrd{.}
  \renewcommand*\bblth{.}
  \renewcommand*\bbljan{Januar}
  \renewcommand*\bblfeb{Februar}
  \renewcommand*\bblmar{M\^^b{a}rz}
  \renewcommand*\bblapr{April}
  \renewcommand*\bblmay{Mai}
  \renewcommand*\bbljun{Juni}
  \renewcommand*\bbljul{Juli}
  \renewcommand*\bblaug{August}
  \renewcommand*\bblsep{September}
  \renewcommand*\bbloct{Oktober}
  \renewcommand*\bblnov{November}
  \renewcommand*\bbldec{Dezember}
}
\addto\captionsgerman{%
  \renewcommand*\bbland{und}
  \renewcommand*\bblandsep{}
  \renewcommand*\bblandsepauthor{}
  \renewcommand*\bbletal{et~al.}
  \renewcommand*\bbleditors{Herausgeber}
  \renewcommand*\bbleds{Hrsg.}
  \renewcommand*\bbleditor{Herausgeber}
  \renewcommand*\bbled{Hrsg.}
  \renewcommand*\bbledby{herausgegeben von}
  \renewcommand*\bbledition{Auf\/lage}
  \renewcommand*\bbledn{Aufl.}
  \renewcommand*\bblvolume{Band}
  \renewcommand*\bblvol{Bd.}
  \renewcommand*\bblof{von}
  \renewcommand*\bblnumber{Nummer}
  \renewcommand*\bblno{Nr.}
  \renewcommand*\bblin{in}
  \renewcommand*\bblpages{Seiten}
  \renewcommand*\bblpp{S.}
  \renewcommand*\bblpage{Seite}
  \renewcommand*\bblp{S.}
  \renewcommand*\bbleidpp{Seiten}
  \renewcommand*\bblchapter{Kapitel}
  \renewcommand*\bblchap{Kap.}
  \renewcommand*\bbltechreport{Technischer Bericht}
  \renewcommand*\bbltechrep{Techn. Ber.}
  \renewcommand*\bblmthesis{Masterarbeit}
  \renewcommand*\bblphdthesis{Dissertation}
  \renewcommand*\bblfirst{Erste}
  \renewcommand*\bblfirsto{1.}
  \renewcommand*\bblsecond{Zweite}
  \renewcommand*\bblsecondo{2.}
  \renewcommand*\bblthird{Dritte}
  \renewcommand*\bblthirdo{3.}
  \renewcommand*\bblfourth{Vierte}
  \renewcommand*\bblfourtho{4.}
  \renewcommand*\bblfifth{F\^^b{u}nfte}
  \renewcommand*\bblfiftho{5.}
  \renewcommand*\bblst{.}
  \renewcommand*\bblnd{.}
  \renewcommand*\bblrd{.}
  \renewcommand*\bblth{.}
  \renewcommand*\bbljan{Januar}
  \renewcommand*\bblfeb{Februar}
  \renewcommand*\bblmar{M\^^b{a}rz}
  \renewcommand*\bblapr{April}
  \renewcommand*\bblmay{Mai}
  \renewcommand*\bbljun{Juni}
  \renewcommand*\bbljul{Juli}
  \renewcommand*\bblaug{August}
  \renewcommand*\bblsep{September}
  \renewcommand*\bbloct{Oktober}
  \renewcommand*\bblnov{November}
  \renewcommand*\bbldec{Dezember}
}
\addto\captionsenglish{%
  \renewcommand*\bbland{and}
  \renewcommand*\bblandsep{,}
  \renewcommand*\bblandsepauthor{,}
  \renewcommand*\bbletal{et~al.}
  \renewcommand*\bbleditors{editors}
  \renewcommand*\bbleds{eds.}
  \renewcommand*\bbleditor{editor}
  \renewcommand*\bbled{ed.}
  \renewcommand*\bbledby{edited by}
  \renewcommand*\bbledition{edition}
  \renewcommand*\bbledn{edn.}
  \renewcommand*\bblvolume{volume}
  \renewcommand*\bblvol{vol.}
  \renewcommand*\bblof{of}
  \renewcommand*\bblnumber{number}
  \renewcommand*\bblno{no.}
  \renewcommand*\bblin{in}
  \renewcommand*\bblpages{pages}
  \renewcommand*\bblpp{pp.}
  \renewcommand*\bblpage{page}
  \renewcommand*\bblp{p.}
  \renewcommand*\bbleidpp{pages}
  \renewcommand*\bblchapter{chapter}
  \renewcommand*\bblchap{chap.}
  \renewcommand*\bbltechreport{Technical Report}
  \renewcommand*\bbltechrep{Tech. Rep.}
  \renewcommand*\bblmthesis{Master's thesis}
  \renewcommand*\bblphdthesis{Ph.D. thesis}
  \renewcommand*\bblfirst{First}
  \renewcommand*\bblfirsto{1st}
  \renewcommand*\bblsecond{Second}
  \renewcommand*\bblsecondo{2nd}
  \renewcommand*\bblthird{Third}
  \renewcommand*\bblthirdo{3rd}
  \renewcommand*\bblfourth{Fourth}
  \renewcommand*\bblfourtho{4th}
  \renewcommand*\bblfifth{Fifth}
  \renewcommand*\bblfiftho{5th}
  \renewcommand*\bblst{st}
  \renewcommand*\bblnd{nd}
  \renewcommand*\bblrd{rd}
  \renewcommand*\bblth{th}
  \renewcommand*\bbljan{January}
  \renewcommand*\bblfeb{February}
  \renewcommand*\bblmar{March}
  \renewcommand*\bblapr{April}
  \renewcommand*\bblmay{May}
  \renewcommand*\bbljun{June}
  \renewcommand*\bbljul{July}
  \renewcommand*\bblaug{August}
  \renewcommand*\bblsep{September}
  \renewcommand*\bbloct{October}
  \renewcommand*\bblnov{November}
  \renewcommand*\bbldec{December}
}
\ifldv@doloadhyperref%
\RequirePackage{nameref}
\fi
\ifldv@doloadvarioref%
\RequirePackage{varioref}
\fi
\ifldv@doloadhyperref%
\RequirePackage[pdfborder={0 0 0}]{hyperref}%
\expandafter\def\expandafter\UrlBreaks\expandafter{\UrlBreaks%  save the current one
  \do\a\do\b\do\c\do\d\do\e\do\f\do\g\do\h\do\i\do\j%
  \do\k\do\l\do\m\do\n\do\o\do\p\do\q\do\r\do\s\do\t%
  \do\u\do\v\do\w\do\x\do\y\do\z\do\A\do\B\do\C\do\D%
  \do\E\do\F\do\G\do\H\do\I\do\J\do\K\do\L\do\M\do\N%
  \do\O\do\P\do\Q\do\R\do\S\do\T\do\U\do\V\do\W\do\X%
  \do\Y\do\Z}%
\fi

\newcommand*\authorwithand[1]{%
  \let\tempand=\and%
  \renewcommand*\and{\leavevmode\unskip#1}%
  \let\tempthanks=\thanks%
  \renewcommand*\thanks[1]{}%
  \@author%
  \let\and=\tempand%
  \let\thanks=\tempthanks%
}
\newcommand*{\@keywords}{}
\ifldv@doloadhyperref%
\newcommand{\keywords}[1]{%
  \renewcommand*\@keywords{#1}%
  \hypersetup{pdfkeywords = {#1}}%
}%
\else%
\newcommand{\keywords}[1]{%
  \renewcommand*\@keywords{#1}%
}%
\fi%
\newcommand*\keywordsname{Key words}%
\addto\captionsngerman{%
  \renewcommand*\keywordsname{Schlagw\"orter}%
}
\addto\captionsgerman{%
  \renewcommand*\keywordsname{Schlagw\"orter}%
}
\addto\captionsenglish{%
  \renewcommand*\keywordsname{Key words}%
}
\newcommand{\makekeywords}{%
  \if@twocolumn
  \vspace{\topsep}
  \noindent{\sectfont\size@paragraph\keywordsname:} \@keywords
  \else
  \small
  \begin{center}%
    {\normalfont\sectfont\nobreak\keywordsname
      \vspace{-.5em}\vspace{\z@}}%
  \end{center}%
  \quotation\@keywords\endquotation
  \fi}
\newcommand*{\@version}{}
\newcommand{\version}[1]{\renewcommand*\@version{#1}}
\publishers{Technische Universit\"at M\"unchen}
\newcommand*\@institute{Institute for Data Processing}
\newcommand*\institute[1]{\renewcommand*\@institute{#1}}
\newcommand*{\@postaddress}{80290 M\"unchen, Germany}
\newcommand*{\postaddress}[1]{\renewcommand*{\@postaddress}{#1}}
\newcommand*{\@citationaddress}{Munich, Germany}
\newcommand*{\citationaddress}[1]{\renewcommand*{\@citationaddress}{#1}}
\newcommand*{\@publishersurl}{\url{http://www.ldv.ei.tum.de/}}
\newcommand*{\publishersurl}[1]{\renewcommand*{\@publishersurl}{#1}}
\addto\captionsenglish{%
  \institute{Institute for Data Processing}
  \postaddress{80290 M\"unchen, Germany}
  \citationaddress{Munich, Germany}
}
\addto\captionsngerman{%
  \institute{Lehrstuhl f\"ur Datenverarbeitung}
  \postaddress{80290 M\"unchen}
  \citationaddress{M\"unchen}
}
\addto\captionsgerman{%
  \institute{Lehrstuhl f\"ur Datenverarbeitung}
  \postaddress{80290 M\"unchen}
  \citationaddress{M\"unchen}
}
\newcommand*\ldv@licensetext{}
\newcommand\licensetext[1]{\renewcommand*\ldv@licensetext{#1}}
\newcommand*\license[1]{\setkeys{ldv}{license=#1}}
\newcommand*\ldv@licensetext@ccby{This work is licenced under the Creative Commons Attribution 3.0 Germany License. To view a copy of this licence, visit \url{http://creativecommons.org/licenses/by/3.0/de/} or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
\newcommand*\ldv@licensetext@ccbysa{This work is licenced under the Creative Commons Attribution-Share Alike 3.0 Germany License. To view a copy of this licence, visit \url{http://creativecommons.org/licenses/by-sa/3.0/de/} or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
\newcommand*\ldv@licensetext@ccbynd{This work is licenced under the Creative Commons Attribution-No Derivative Works 3.0 Germany License. To view a copy of this licence, visit \url{http://creativecommons.org/licenses/by-nd/3.0/de/} or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
\newcommand*\ldv@licensetext@ccbync{This work is licenced under the Creative Commons Attribution-Non-Commercial 3.0 Germany License. To view a copy of this licence, visit \url{http://creativecommons.org/licenses/by-nc/3.0/de/} or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
\newcommand*\ldv@licensetext@ccbyncsa{This work is licenced under the Creative Commons Attribution-Non-Commercial-Share Alike 3.0 Germany License. To view a copy of this licence, visit \url{http://creativecommons.org/licenses/by-nc-sa/3.0/de/} or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
\newcommand*\ldv@licensetext@ccbyncnd{This work is licenced under the Creative Commons Attribution-Non-Commercial-No Derivative Works 3.0 Germany License. To view a copy of this licence, visit \url{http://creativecommons.org/licenses/by-nc-nd/3.0/de/} or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
\addto\captionsenglish{%
  \renewcommand*\ldv@licensetext@ccby{This work is licenced under the Creative Commons Attribution 3.0 Germany License. To view a copy of this licence, visit \url{http://creativecommons.org/licenses/by/3.0/de/} or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
  \renewcommand*\ldv@licensetext@ccbysa{This work is licenced under the Creative Commons Attribution-Share Alike 3.0 Germany License. To view a copy of this licence, visit \url{http://creativecommons.org/licenses/by-sa/3.0/de/} or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
  \renewcommand*\ldv@licensetext@ccbynd{This work is licenced under the Creative Commons Attribution-No Derivative Works 3.0 Germany License. To view a copy of this licence, visit \url{http://creativecommons.org/licenses/by-nd/3.0/de/} or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
  \renewcommand*\ldv@licensetext@ccbync{This work is licenced under the Creative Commons Attribution-Non-Commercial 3.0 Germany License. To view a copy of this licence, visit \url{http://creativecommons.org/licenses/by-nc/3.0/de/} or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
  \renewcommand*\ldv@licensetext@ccbyncsa{This work is licenced under the Creative Commons Attribution-Non-Commercial-Share Alike 3.0 Germany License. To view a copy of this licence, visit \url{http://creativecommons.org/licenses/by-nc-sa/3.0/de/} or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
  \renewcommand*\ldv@licensetext@ccbyncnd{This work is licenced under the Creative Commons Attribution-Non-Commercial-No Derivative Works 3.0 Germany License. To view a copy of this licence, visit \url{http://creativecommons.org/licenses/by-nc-nd/3.0/de/} or send a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
}
\addto\captionsngerman{%
  \renewcommand*\ldv@licensetext@ccby{Dieses Werk ist unter einem Creative Commons Namensnennung 3.0 Deutschland Lizenzvertrag lizenziert. Um die Lizenz anzusehen, gehen Sie bitte zu \url{http://creativecommons.org/licenses/by/3.0/de/} oder schicken Sie einen Brief an Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
  \renewcommand*\ldv@licensetext@ccbysa{Dieses Werk ist unter einem Creative Commons Namensnennung-Weitergabe unter gleichen Bedingungen 3.0 Deutschland Lizenzvertrag lizenziert. Um die Lizenz anzusehen, gehen Sie bitte zu \url{http://creativecommons.org/licenses/by-sa/3.0/de/} oder schicken Sie einen Brief an Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
  \renewcommand*\ldv@licensetext@ccbynd{Dieses Werk ist unter einem Creative Commons Namensnennung-Keine Bearbeitung 3.0 Deutschland Lizenzvertrag lizenziert. Um die Lizenz anzusehen, gehen Sie bitte zu \url{http://creativecommons.org/licenses/by-nd/3.0/de/} oder schicken Sie einen Brief an Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
  \renewcommand*\ldv@licensetext@ccbync{Dieses Werk ist unter einem Creative Commons Namensnennung-Keine kommerzielle Nutzung 3.0 Deutschland Lizenzvertrag lizenziert. Um die Lizenz anzusehen, gehen Sie bitte zu \url{http://creativecommons.org/licenses/by-nc/3.0/de/} oder schicken Sie einen Brief an Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
  \renewcommand*\ldv@licensetext@ccbyncsa{Dieses Werk ist unter einem Creative Commons Namensnennung-Keine kommerzielle Nutzung-Weitergabe unter gleichen Bedingungen 3.0 Deutschland Lizenzvertrag lizenziert. Um die Lizenz anzusehen, gehen Sie bitte zu \url{http://creativecommons.org/licenses/by-nc-sa/3.0/de/} oder schicken Sie einen Brief an Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
  \renewcommand*\ldv@licensetext@ccbyncnd{Dieses Werk ist unter einem Creative Commons Namensnennung-Keine kommerzielle Nutzung-Keine Bearbeitung 3.0 Deutschland Lizenzvertrag lizenziert. Um die Lizenz anzusehen, gehen Sie bitte zu \url{http://creativecommons.org/licenses/by-nc-nd/3.0/de/} oder schicken Sie einen Brief an Creative Commons, 171 Second Street, Suite 300, San Francisco, California 94105, USA.}%
}
\define@choicekey*+{ldv}{license}[\ldv@choicekeyval\ldv@choicekeynr]{cc-by,cc-by-sa,cc-by-nd,cc-by-nc,cc-by-nc-sa,cc-by-nc-nd}{%
  \ifcase\ldv@choicekeynr\relax
    % Namensnennung: CC-BY
    \renewcommand*{\ldv@licensetext}{\ldv@licensetext@ccby}
  \or
    % Namensnennung und Weitergabe unter gleichen Bedingungen: CC-BY-SA
    \renewcommand*{\ldv@licensetext}{\ldv@licensetext@ccbysa}
  \or
    % Namensnennung und keine Bearbeitung: CC-BY-ND
    \renewcommand*{\ldv@licensetext}{\ldv@licensetext@ccbynd}
  \or
    % Namensnennung und nicht-kommerzielle Nutzung: CC-BY-NC
    \renewcommand*{\ldv@licensetext}{\ldv@licensetext@ccbync}
  \or
    % Namensnennung, nicht-kommerzielle Nutzung und Weitergabe unter
    % gleichen Bedingungen: CC-BY-NC-SA
    \renewcommand*{\ldv@licensetext}{\ldv@licensetext@ccbyncsa}
  \or
    % Namensnennung, nicht-kommerzielle Nutzung und keine Bearbeitung:
    % CC-BY-NC-ND
    \renewcommand*{\ldv@licensetext}{\ldv@licensetext@ccbyncnd}
  \fi
}{%
  \ClassWarning{\@currname}{%
    Value given for the option license is not known.%
  }
}
\ifldv@doloadhyperref%
\renewcommand*\title[1]{%
  \renewcommand*\@title{#1}%
  \hypersetup{%
    pdftitle = {\@title\ifx\@subtitle\@empty\else. \@subtitle.\fi}%
  }%
}
\renewcommand*\subtitle[1]{%
  \renewcommand*\@subtitle{#1}%
  \hypersetup{%
    pdftitle = {\ifx\@title\@empty\else\@title. \@subtitle.\fi}%
  }%
}
\renewcommand*\author[1]{%
  \renewcommand*\@author{#1}%
  \let\tempand=\and%
  \renewcommand*\and{, }%
  \let\tempthanks=\thanks%
  \let\thanks=\@empty%
  \hypersetup{%
    pdfauthor  = {\@author}%
  }%
  \let\and=\tempand%
  \let\thanks=\tempthanks%
}
\renewcommand*\subject[1]{%
  \renewcommand*\@subject{#1}%
  \hypersetup{%
    pdfsubject = {\@subject}
  }%
}
\fi%
\renewcommand*\subject@font{\normalfont\normalcolor\bfseries}
\RequirePackage{calc}
\newlength\ldv@ldvlogowidth
\setlength\ldv@ldvlogowidth{19mm}
\newcommand*\ldv@ldvlogoS{img/LDVLogoS_oT}
\newcommand*\ldv@ldvlogoCMYK{img/LDVLogoCMYK_oT}
\newlength\ldv@tumlogowidth
\setlength\ldv@tumlogowidth{17mm}
\newcommand*\ldv@tumlogoS{img/TUMLogo_oZ_Vollfl_sw}
\newcommand*\ldv@tumlogoCMYK{img/TUMLogo_oZ_Vollfl_CMYK}
\define@choicekey*{ldv}{frontcover}[\ldv@frontcoverdesign]
  {design1}{%
    \if@titlepage\else%
      \ClassWarning{\@currname}{%
        Option frontcover of \string\maketitle\ is only valid
        \MessageBreak
        when using titlepage=true%
      }%
    \fi%
  }%
\define@cmdkey{ldv}[ldv@]{frontcoverfile}{}
\define@key{ldv}{pagenumber}{%
  \if@titlepage%
    \setcounter{page}{#1}%
  \else%
        \ClassWarning{\@currname}{%
      Option pagenumber of \string\maketitle\ is only valid
      \MessageBreak
      when using titlepage=true%
    }%
  \fi%
}
\global\let\@maketitle\relax
\if@titlepage
  \renewcommand*\maketitle[1][]{%
    \setkeys{ldv}{#1}%
    \begin{titlepage}
      \let\footnotesize\small
      \let\footnoterule\relax
      \let\footnote\thanks
      \renewcommand*\thefootnote{\@fnsymbol\c@footnote}%
      \let\@oldmakefnmark\@makefnmark
      \renewcommand*{\@makefnmark}{\rlap\@oldmakefnmark}%
      \ifdefined\ldv@frontcoverfile%
        \setcounter{page}{-1}%
        \ldv@includefile{\ldv@frontcoverfile}%
        \if@twoside\cleardoubleemptypage\else\clearpage\fi%
        \thispagestyle{empty}
      \else%
        \ifdefined\ldv@frontcoverdesign%
          \ifstr{\ldv@frontcoverdesign}{design1}{%
            \setcounter{page}{-1}%
            \ldv@makecover@eins%
            \if@twoside\cleardoubleemptypage\else\clearpage\fi%
            \thispagestyle{empty}
          }{}%
        \fi%
      \fi%
      \ifx\@extratitle\@empty \else
        \noindent\@extratitle\next@tpage\cleardoubleemptypage
        \thispagestyle{empty}%
      \fi
      \ldv@pagetitle%
      \if@twoside\next@tpage
        \begin{minipage}[t]{\textwidth}
          \@uppertitleback
        \end{minipage}\par
        \vfill
        \begin{minipage}[b]{\textwidth}
          \@lowertitleback
        \end{minipage}
      \fi
      \ifx\@dedication\@empty \else
        \next@tpage\null\vfill
        {\centering \Large \@dedication \par}%
        \vskip \z@ \@plus3fill
        \if@twoside \next@tpage\cleardoubleemptypage \fi
      \fi
    \end{titlepage}
    \setcounter{footnote}{0}%
    \global\let\thanks\relax
    \global\let\maketitle\relax
    \global\let\@thanks\@empty
  }
\else
  \renewcommand*\maketitle[1][]{\par%
    \setkeys{ldv}{#1}%
    \begingroup
      \renewcommand*\thefootnote{\@fnsymbol\c@footnote}%
      \let\@oldmakefnmark\@makefnmark
      \renewcommand*{\@makefnmark}{\rlap\@oldmakefnmark}
      \if@twocolumn
        \ifnum \col@number=\@ne
          \ldv@headtitle
         \else
          \twocolumn[\ldv@headtitle]%
        \fi
      \else
        \newpage
        \global\@topnum\z@
        \ldv@headtitle
      \fi
      \thispagestyle{\titlepagestyle}\@thanks
    \endgroup
    \setcounter{footnote}{0}%
    \let\thanks\relax
    \let\maketitle\relax
    \global\let\@thanks\@empty
  }
\fi
\newcommand*\@titletitle{}
\newcommand*\titletitle[1]{%
  \renewcommand*\@titletitle{#1}%
}
\if@titlepage
\newcommand*\ldv@pagetitle{%
  \ldv@makepublishers%
  \setparsizes{\z@}{\z@}{\z@\@plus 1fil}\par@updaterelative%
  \ifx\@titlehead\@empty \else%
  \begin{minipage}[t]{\textwidth}%
    \@titlehead
  \end{minipage}\par
  \fi
  \null\vfill
  \begin{center}
    \ifx\@subject\@empty\else
    {\subject@font \@subject \par}%
    \vskip 3em
    \fi
    {\titlefont\huge \ifx\@titletitle\@empty \@title \else\@titletitle \fi\par}%
    \ifx\@subtitle\@empty\else%
      \vskip 1em%
      {\usekomafont{subtitle}\@subtitle\par}\fi%
    \vskip 3em
    {\lineskip 0.75em%
      \begin{tabular}[t]{c}
        \@author
      \end{tabular}\par%
    }%
    \vskip 1.5em
    {\@date%
      \ifx\@version\@empty\else, \@version\fi\par}%
    {\ifx\@license\@empty\else\if@twoside\else%
      \vskip 1.5em%
      \ldv@licensetext\par%
    \fi\fi}%
    \vfill\vfill\vfill\vfill\null
  \end{center}\par
  \@thanks
}%
\newcommand*\ldv@makepublishers{%
  \newlength\ldv@tumwidth%
  \newlength\ldv@ldvwidth%
  \newlength\ldv@publisherwidth%
  \settowidth\ldv@tumwidth{\@publishers}%
  \settowidth\ldv@ldvwidth{\@institute}%
  \ifdim\ldv@tumwidth >\ldv@ldvwidth%
    \setlength\ldv@publisherwidth{\ldv@tumwidth}%
  \else%
    \setlength\ldv@publisherwidth{\ldv@ldvwidth}%
  \fi%
  \newsavebox\ldv@publishersbox%
  \savebox\ldv@publishersbox[\textwidth]{%
    \parbox{\ldv@ldvlogowidth}{%
      \includegraphics[width=\ldv@ldvlogowidth]{\ldv@ldvlogoS}%
    }%
    \hfill%
    \parbox{\ldv@publisherwidth}{%
      \centering%
      \@institute\\%
      \@publishers%
    }%
    \hfill%
    \parbox{\ldv@tumlogowidth}{%
      \includegraphics[width=\ldv@tumlogowidth]{\ldv@tumlogoS}%
    }%
  }%
  %
  \newlength\ldv@bottommargin
  \setlength\ldv@bottommargin{1in + \hoffset + \oddsidemargin}%
  \newlength\ldv@publishersboxdepth%
  \settodepth\ldv@publishersboxdepth{\usebox\ldv@publishersbox}%
  \newlength\ldv@publishersbottom%
  \setlength\ldv@publishersbottom{%
    1in + \voffset + \topmargin + \headheight + \headsep +%
    \topskip + \ldv@publishersboxdepth%
  }%
  \newlength\ldv@publishersmove%
  \setlength\ldv@publishersmove{%
    \paperheight - \ldv@publishersbottom - \ldv@bottommargin%
  }%
  \noindent\raisebox{-\ldv@publishersmove}[0pt][0pt]{%
    \makebox[0pt][l]{\usebox\ldv@publishersbox}}%
}
\fi
\if@titlepage\else
\newcommand*\ldv@headtitle{%
  \clearpage
  \let\footnote\thanks%
  \ifx\@extratitle\@empty \else
    \noindent\@extratitle \next@tpage \if@twoside \null\next@tpage \fi
  \fi
  \noindent\includegraphics[width=\ldv@ldvlogowidth]{\ldv@ldvlogoS}%
  \hfill%
  \includegraphics[width=\ldv@tumlogowidth]{\ldv@tumlogoS}\par%
  \setparsizes{\z@}{\z@}{\z@\@plus 1fil}\par@updaterelative
  \vskip .5em
  \ifx\@titlehead\@empty \else
    \begin{minipage}[t]{\textwidth}
      \@titlehead
    \end{minipage}\par
  \fi
  \null
  \vspace\baselineskip%
  \begin{center}%
    \ifx\@subject\@empty \else%
      \vspace{-\baselineskip}{\subject@font\@subject}\par%
      \vspace\baselineskip%
    \fi%
    {\titlefont\huge\ifx\@titletitle\@empty\@title\else\@titletitle\fi\par}%
    \ifx\@subtitle\@empty\else%
      \vspace{.33\baselineskip}%
      {\usekomafont{subtitle}\@subtitle}\par%
    \fi%
    \vspace\baselineskip%
    \ifx\@author\@empty\vspace{.5em}\else%
      {\lineskip .5em%
        \begin{tabular}[t]{c}
          \@author
        \end{tabular}\par%
      }%
      \vspace{.5\baselineskip}%
    \fi%
    {\@date%
      \ifx\@version\@empty\else, \@version\fi \par}%
    {\ifx\ldv@licensetext\@empty\else\if@twoside\else%
      \vspace{.5\baselineskip}%
      \footnotesize\ldv@licensetext\par%
    \fi\fi}%
    \ifx\@dedication\@empty \else
      \vskip 2em
      {\Large \@dedication \par}
    \fi
  \end{center}%
  \par
  \vskip 2em
}
\fi
\newcommand*\@covertitle{}
\newcommand*\covertitle[1]{%
  \renewcommand*\@covertitle{#1}%
}
\if@titlepage
\newcommand\ldv@makecover@eins{%
  \newlength\ldv@coverleftcolumnwidth%
  \setlength\ldv@coverleftcolumnwidth{0.618\paperwidth %
    -\hoffset %
    -1in %
    -\oddsidemargin %
    -2mm}%
  \newlength\ldv@coverrightcolumnwidth%
  \setlength\ldv@coverrightcolumnwidth{0.382\paperwidth %
    -\hoffset %
    -1in %
    -\evensidemargin %
    -2mm %
    +\marginparsep %
    +\marginparwidth}%
  \newsavebox\ldv@covertitle%
  \savebox\ldv@covertitle{%
    \parbox{\ldv@coverleftcolumnwidth}{%
      \raggedleft\bfseries%
      {\huge\ifx\@covertitle\empty\@title\else\@covertitle\fi\medskip\par}
      \@subtitle%
    }%
  }%
  \newsavebox\ldv@coverauthor%
  \savebox\ldv@coverauthor{%
    \parbox{\ldv@coverrightcolumnwidth}{%
      \raggedright\bfseries%
      \authorwithand{\newline}%
    }%
  }%
  \newlength\ldv@margintop%
  \setlength\ldv@margintop{1in %
    +\voffset %
    +\topmargin %
    +\headheight %
    +\headsep%
  }
  \newlength\ldv@authorpadding%
  \setlength\ldv@authorpadding{\ldv@margintop %
    +\topskip %
    +\totalheightof{\usebox\ldv@covertitle} %
    +1mm %
  }%
  \begin{tikzpicture}[remember picture, overlay]
    \node [
      below left,
      align=right,
      xshift=\hoffset + 0.618\paperwidth - 2mm,
      yshift=-\ldv@margintop - \topskip,
    ] at (current page.north west) {\usebox\ldv@covertitle};
    \node [
      below right,
      align=left,
      xshift=\hoffset + 0.618\paperwidth + 2mm,
      yshift=-\ldv@authorpadding,
    ] at (current page.north west) {\usebox\ldv@coverauthor};
    \path[fill=TUMBlau5] (current page.north west) ++(\hoffset + 0.618\paperwidth - 1.5mm, 0) rectangle ++(3mm, -\paperheight);
    \node [
      below left,
      xshift=\hoffset + 0.618\paperwidth - 2mm,
      yshift=-\ldv@margintop - \textheight - \footskip,
    ] at (current page.north west) {\includegraphics[width=\ldv@ldvlogowidth]{\ldv@ldvlogoCMYK}};
    \node [
      below right,
      xshift=\hoffset + 0.618\paperwidth + 2mm,
      yshift=-\ldv@margintop - \textheight - \footskip,
    ] at (current page.north west) {\includegraphics[width=\ldv@tumlogowidth]{\ldv@tumlogoCMYK}};
  \end{tikzpicture}%
}%
\fi
\newcommand*\ldv@includefile[1]{%
  \noindent\hspace{-1in}\hspace{-\oddsidemargin}\fbox{A}%
  \raisebox{1in + \topmargin + \headheight + \headsep}[0mm][0mm]{%
    \fbox{B\includegraphics{LDVLogoS_oT}}
  }
}
\endinput
%%
%% End of file `ldvarticle.cls'.
